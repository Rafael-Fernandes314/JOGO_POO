import pygame
from pygame.locals import *
from sys import exit

pygame.init()

class Eindein(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Assets/Sprites/Player/Eidein-parado.png")
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        self.vel_y = 0
        self.pulando = False
        self.gravidade = 2
        self.velocidade = 5

    def update(self):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        if self.rect.bottom >= 395:
            self.rect.bottom = 395
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