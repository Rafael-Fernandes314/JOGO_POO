import pygame
from pygame.locals import *
from typing import List
from enemy import Goblin
import estado_jogo
from sys import exit

pygame.init()

class Eindein(pygame.sprite.Sprite):  # o player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # carrega a imagem dele e muda o tamanho
        self.image = pygame.image.load("Assets/Sprites/Player/Eidein-parado-e.png")
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.sprite_agachar_e: List[pygame.Surface] = []
        self.sprite_agachar_d: List[pygame.Surface] = []

        # física do personagem
        self.vel_y = -12  # velocidade na vertical
        self.pulando = False # para quando pular
        self.gravidade = 0.8  # gravidade pra quando cair
        self.velocidade = 3 # velocidade na horizontal
        self.animar = False # pra quando for animar
        self.vida_max = estado_jogo.vida_max_jogador
        self.vida = self.vida_max
        self.atacando = False # quando for atacar
        self.ja_acertou = False
        self.invencivel = False
        self.invencivel_timer = 0
        self.gameover = False
        self.hitbox = pygame.Rect(0, 0, (20), (128))
        self.atual_ataque = 0

        # listas dos sprites pra animar
        self.sprite_e:List[Eindein] = []  # Esquerda
        self.sprite_d:List[Eindein] = []  # Direita
        self.ataque_e:List[Eindein] = []
        self.ataque_d:List[Eindein] = []

        # andar pra esquerda
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-parado-e.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e1.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e2.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e3.png"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e4.png"))

        # andar pra direita
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-parado-d.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d1.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d2.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d3.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d4.png"))

        self.sprite_agachar_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-agachado-d.png"))
        self.sprite_agachar_e.append(pygame.image.load("Assets/Sprites/Player/Eidein-agachado-e.png"))

        self.ataque_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando1-d.png"))
        self.ataque_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-atacando2-d.png"))

        self.hitbox_ataque = pygame.Rect(0, 0, 40, 40)

        self.agachado = False
        self.direcao = "direita"

        # primeiros frames
        self.atual1 = 0
        self.atual2 = 0

        # imagem atual e a posição dela
        self.image = self.sprite_e[self.atual1]
        self.image = self.sprite_d[self.atual2]
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 535)

        player = Eindein()
        player_group = pygame.sprite.Group(player)
        inimigos = pygame.sprite.Group()

    def update(self):
        # gravidade
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        # define o chão
        chao = 530 if self.agachado else 512
        if self.rect.bottom >= chao:
            self.rect.bottom = chao
            self.pulando = False
            self.vel_y = 0

        # invencibilidade
        if self.invencivel:
            self.invencivel_timer += 1
            if self.invencivel_timer > 60:
                self.invencivel = False
                self.invencivel_timer = 0

        # animação de ataque
        if self.atacando:
            self.atual_ataque += 0.2

            if self.direcao == "direita":
                if self.atual_ataque >= len(self.ataque_d):
                    self.atacando = False
                    self.atual_ataque = 0
                else:
                    self.image = pygame.transform.scale(
                        self.ataque_d[int(self.atual_ataque)], (32*4, 32*4)
                    )
            else:
                if self.atual_ataque >= len(self.ataque_e):
                    self.atacando = False
                    self.atual_ataque = 0
                else:
                    self.image = pygame.transform.scale(
                        self.ataque_e[int(self.atual_ataque)], (32*4, 32*4)
                    )

                if self.direcao == "direita":
                    self.hitbox_ataque.midleft = self.rect.midright
                else:
                    self.hitbox_ataque.midright = self.rect.midleft

            # mantém posição
            midbottom = self.rect.midbottom
            self.rect = self.image.get_rect()
            self.rect.midbottom = midbottom

            return
        
        
        if Eindein.atacando and int(Eindein.atual_ataque) == 1:
            for inimigo in Goblin:
                if Eindein.hitbox_ataque.colliderect(inimigo.rect):
                    inimigo.levar_dano(1)

        # seleção de sprite
        if self.agachado:
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
                    self.image = pygame.transform.scale(self.sprite_d[int(self.atual2)], (32*4, 32*4))
                else:
                    self.atual1 += 0.15
                    if self.atual1 >= len(self.sprite_e):
                        self.atual1 = 0
                        self.animar = False
                    self.image = pygame.transform.scale(self.sprite_e[int(self.atual1)], (32*4, 32*4))
            else:
                self.image = pygame.transform.scale(
                    self.sprite_d[0] if self.direcao == "direita" else self.sprite_e[0],
                    (32*4, 32*4)
                )

        midbottom = self.rect.midbottom
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom

        if self.agachado:
            self.hitbox.height = 64
        else:
            self.hitbox.height = 128
        self.hitbox.width = 20
        self.hitbox.midbottom = self.rect.midbottom

    def atacar(self):
            if not self.atacando:
                self.atacando = True
                self.atual_ataque = 0
                self.ja_acertou = False

    def mover(self, direcao):
        self.direcao = direcao
        self.animar = True
        if direcao == "esquerda":
            self.rect.x -= self.velocidade
        else:
            self.rect.x += self.velocidade

    def pular(self):
        if not self.pulando and not self.agachado:
            self.vel_y = -15
            self.pulando = True

    def agachar(self, estado: bool):
        self.agachado = estado
        if estado:
            self.hitbox.height = 64
        else:
            self.hitbox.height = 128

    def levar_dano(self, quantidade=1):
        if not self.invencivel:
            self.vida -= quantidade
            if self.vida < 0:
                self.vida = 0
            self.invencivel = True
            self.invencivel_timer = 0

    def game_over(self):
        if self.vida == 0:
            self.gameover = True