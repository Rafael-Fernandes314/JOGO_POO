import pygame
from pygame.locals import *
from typing import List

pygame.init()

class Eindein(pygame.sprite.Sprite):

    def __init__ (self, list):
        self.sprite_e:List[Eindein] = []

        self.sprite_e.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-e1"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-e2"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-e3"))
        self.sprite_e.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-e4"))

    def __init__ (self, list):
        self.sprite_d:List[Eindein] = []

        self.sprite_d.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-d1"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-d2"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-d3"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Playe/Eidein-andando-d4"))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Assets/Sprites/Player/Eidein-parado.png")
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))
        self.sprite_d = pygame.transform.scale(self.sprite, (32 * 4, 32 * 4))
        self.sprite_e = pygame.transform.scale(self.sprite, (32 * 4, 32 * 4))

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        self.vel_y = 0
        self.pulando = False
        self.gravidade = 2
        self.velocidade = 5

    def update(self):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        if self.rect.bottom >= 515:
            self.rect.bottom = 515
            self.pulando = False

    def mover(self, direcao):
        if direcao == "esquerda":
            self.rect.x -= self.velocidade
        elif direcao == "direita":
            self.rect.x += self.velocidade

    def pular(self):
        if not self.pulando:
            self.vel_y = -25
            self.pulando = True