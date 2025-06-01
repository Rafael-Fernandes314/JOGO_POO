import pygame
from pygame.locals import *
from typing import List

pygame.init()

class Eindein(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.vel_y = 0
        self.pulando = False
        self.gravidade = 2
        self.velocidade = 5

        self.sprite_e:List[Eindein] = []
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-parado-e.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e1.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e2.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e3.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e4.png"), (32 * 4, 32 * 4)))
        self.atual = 0
        self.image = self.sprite_e[self.atual]

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        self.sprite_d:List[Eindein] = []
        self.sprite_d.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-parado-d.png"), (32 * 4, 32 * 4)))
        self.sprite_d.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d1.png"), (32 * 4, 32 * 4)))
        self.sprite_d.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d2.png"), (32 * 4, 32 * 4)))
        self.sprite_d.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d3.png"), (32 * 4, 32 * 4)))
        self.sprite_d.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d4.png"), (32 * 4, 32 * 4)))
        self.atual = 0
        self.image = self.sprite_e[self.atual]

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

    def update(self):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        if self.rect.bottom >= 515:
            self.rect.bottom = 515
            self.pulando = False

        self.atual = self.atual + 1
        if self.atual >= len(self.sprite_e and self.sprite_d):
            self.atual = 0
        self.image = self.sprite_d[self.atual]
        self.image = self.sprite_e[self.atual]

    def mover(self, direcao):
        if direcao == "esquerda":
            self.rect.x -= self.velocidade
        elif direcao == "direita":
            self.rect.x += self.velocidade

    def pular(self):
        if not self.pulando:
            self.vel_y = -25
            self.pulando = True