import pygame
from pygame.locals import *
from typing import List
from sys import exit
from gameover import Game_over

pygame.init()

class Eindein(pygame.sprite.Sprite):  # o player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # carrega a imagem dele e muda o tamanho
        self.image = pygame.image.load("Assets/Sprites/Player/Eidein-parado-e.png")
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

        # física do personagem
        self.vel_y = 0  # velocidade na vertical
        self.pulando = False # para quando pular
        self.gravidade = 2  # gravidade pra quando cair
        self.velocidade = 3 # velocidade na horizontal
        self.animar = False # pra quando for animar
        self.vida = 3   # vida
        self.atacando = False # quando for atacar
        self.invencivel = False
        self.invencivel_timer = 0
        self.gameover = False

        # listas dos sprites pra animar
        self.sprite_e:List[Eindein] = []  # Esquerda
        self.sprite_d:List[Eindein] = []  # Direita

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

        # primeiros frames
        self.atual1 = 0
        self.atual2 = 0

        # imagem atual e a posição dela
        self.image = self.sprite_e[self.atual1]
        self.image = self.sprite_d[self.atual2]
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 535)

    def update(self):
        # usa a gravidade
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        # coloca o personagem no chão
        if self.rect.bottom >= 515:
            self.rect.bottom = 515
            self.pulando = False

        if self.invencivel:
            self.invencivel_timer += 1
            if self.invencivel_timer > 60:  # 1 segundo de invencibilidade a 60 FPS
                self.invencivel = False
                self.invencivel_timer = 0

    def atacar(self):
        # ele ataca
        self.atacando = True

    def mover(self, direcao):
        # ele anima
        self.animar = True

        if direcao == "esquerda":
            self.rect.x -= self.velocidade # move o personagem no eixo x pra a esquerda
            self.atual1 = self.atual1 + 0.15 # avança a animação da esquerda
            # no fim da lista, reinicia
            if self.atual1 >= len(self.sprite_e):
                self.atual1 = 0
                self.animar = False  # para de animar
            # atualiza a imagem
            self.image = self.sprite_e[int(self.atual1)]
            self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

        elif direcao == "direita":
            self.rect.x += self.velocidade # move o personagem no eixo x pra a direita
            self.atual2 = self.atual2 + 0.15 # avança a animação da direita
            # no fim da lista, reinicia
            if self.atual2 >= len(self.sprite_d):
                self.atual2 = 0
                self.animar = False  # para de animar
            # atualiza a imagem
            self.image = self.sprite_d[int(self.atual2)]
            self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

    def pular(self):
        # permite pular se não tiver pulando
        if not self.pulando:
            self.vel_y = -30  # sobe pra cima
            self.pulando = True  # o player tá no ar

    def levar_dano(self):
        if not self.invencivel:
            self.vida -= 1
            if self.vida < 0:
                self.vida = 0
            self.invencivel = True

    def game_over(self):
        if self.vida == 0:
            self.gameover = True