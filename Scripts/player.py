import pygame
from pygame.locals import *
from typing import List
import estado_jogo

class Eindein(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.sprite_e = []
        self.sprite_d = []
        self.sprite_agachar_e = []
        self.sprite_agachar_d = []
        self.ataque_e = []
        self.ataque_d = []

        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-parado-e.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e1.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e2.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e3.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e4.png"))

        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-parado-d.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d1.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d2.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d3.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d4.png"))

        self.sprite_agachar_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-agachado-d.png"))
        self.sprite_agachar_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-agachado-e.png"))

        self.ataque_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando1-d.png"))
        self.ataque_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando2-d.png"))
        self.ataque_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando1-d.png"))
        self.ataque_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando1-e.png"))
        self.ataque_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando2-e.png"))
        self.ataque_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando1-e.png"))

        self.image = pygame.transform.scale(self.sprite_d[0], (128, 128))
        self.rect = self.image.get_rect(topleft=(100, 535))

        self.vel_y = 0
        self.gravidade = 0.8
        self.velocidade = 3
        self.pulando = False
        self.animar = False
        self.dano = 1
        self.atacando = False
        self.atacou_esse_frame = False
        self.atual_ataque = 0
        self.ja_acertou = False
        self.em_knockback = False
        self.kb_vel_x = 0
        self.kb_vel_y = 0
        self.kb_inicio = 0
        self.kb_duracao = 180

        self.agachado = False
        self.direcao = "direita"

        self.vida_max = estado_jogo.vida_max_jogador
        self.vida = self.vida_max
        self.invencivel = False
        self.invencivel_timer = 0

        self.hitbox = pygame.Rect(0, 0, 20, 128)
        self.hitbox_ataque = pygame.Rect(0, 0, 70, 70)

        self.atual1 = 0
        self.atual2 = 0

    def update(self):
        if self.em_knockback:
            self.rect.x += self.kb_vel_x
            self.rect.y += self.kb_vel_y
            self.kb_vel_y += self.gravidade

            if pygame.time.get_ticks() - self.kb_inicio >= self.kb_duracao:
                self.em_knockback = False
                self.kb_vel_x = 0
                self.kb_vel_y = 0

        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        chao = 530 if self.agachado else 512
        if self.rect.bottom >= chao:
            self.rect.bottom = chao
            self.vel_y = 0
            self.pulando = False

        if self.invencivel:
            self.invencivel_timer += 1
            if self.invencivel_timer > 60:
                self.invencivel = False
                self.invencivel_timer = 0

        if self.atacando:
            self.atual_ataque += 0.12
            sprites = self.ataque_d if self.direcao == "direita" else self.ataque_e

            if self.atual_ataque >= len(sprites):
                self.atacando = False
                self.atual_ataque = 0
            else:
                midbottom = self.rect.midbottom

                if int(self.atual_ataque) == 1:
                    self.image = pygame.transform.scale(sprites[1], (170, 170))
                    compensacao = 25.5
                else:
                    self.image = pygame.transform.scale(sprites[0], (135, 135))
                    compensacao = 2

                self.rect = self.image.get_rect()
                self.rect.midbottom = (midbottom[0], midbottom[1] + compensacao)

            if self.direcao == "direita":
                self.hitbox_ataque.midleft = self.rect.midright
            else:
                self.hitbox_ataque.midright = self.rect.midleft
        elif self.agachado:
            self.image = pygame.transform.scale(
                self.sprite_agachar_d[0] if self.direcao == "direita" else self.sprite_agachar_e[0],
                (140, 140)
            )
        else:
            if self.animar:
                if self.direcao == "direita":
                    self.atual2 += 0.15
                    if self.atual2 >= len(self.sprite_d):
                        self.atual2 = 0
                        self.animar = False
                    self.image = pygame.transform.scale(self.sprite_d[int(self.atual2)], (128, 128))
                else:
                    self.atual1 += 0.15
                    if self.atual1 >= len(self.sprite_e):
                        self.atual1 = 0
                        self.animar = False
                    self.image = pygame.transform.scale(self.sprite_e[int(self.atual1)], (128, 128))
            else:
                self.image = pygame.transform.scale(
                    self.sprite_d[0] if self.direcao == "direita" else self.sprite_e[0],
                    (128, 128)
                )

        if self.direcao == "direita":
            self.hitbox_ataque.midleft = self.rect.midright
        else:
            self.hitbox_ataque.midright = self.rect.midleft

        midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom

        self.hitbox.height = 64 if self.agachado else 128
        self.hitbox.midbottom = self.rect.midbottom

        if self.direcao == "direita":
            self.hitbox_ataque.midleft = self.rect.midright
        else:
            self.hitbox_ataque.midright = self.rect.midleft

    def atacar(self):
        if not self.atacando and not self.em_knockback:
            self.atacando = True
            self.atual_ataque = 0
            self.ja_acertou = False

    def mover(self, direcao):
        if self.em_knockback:
            return

        self.direcao = direcao
        self.animar = True
        self.rect.x += self.velocidade if direcao == "direita" else -self.velocidade

    def pular(self):
        if not self.pulando and not self.agachado:
            self.vel_y = -15
            self.pulando = True

    def agachar(self, estado):
        self.agachado = estado

    def levar_dano(self, qtd=1, direcao_inimigo=None):
        if not self.invencivel:
            self.vida -= qtd
            if self.vida < 0:
                self.vida = 0

            self.invencivel = True
            self.invencivel_timer = 0

            self.em_knockback = True
            self.kb_inicio = pygame.time.get_ticks()

            forca_x = 8
            forca_y = -6

            if direcao_inimigo is not None:
                self.kb_vel_x = -direcao_inimigo * forca_x
            else:
                self.kb_vel_x = -forca_x if self.direcao == "direita" else forca_x

            self.kb_vel_y = forca_y

    def game_over(self):
        if self.vida == 0:
            self.gameover = True