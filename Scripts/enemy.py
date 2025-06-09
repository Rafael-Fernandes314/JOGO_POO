import pygame
from pygame.locals import *

pygame.init()

class Goblin(pygame.sprite.Sprite):

    def __init__(self, largura, altura):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Assets/Sprites/Inimigos/goblin verde.png")
        self.image = pygame.transform.scale(self.image, (32*4, 32*4))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (largura, altura)

        self.velocidade = 2
        self.direcao = 1
        self.alcance = 100
        self.início_x = largura
        self.animar = False

        self.hitbox = pygame.Rect(0, 0, (120 * 0.6), (120 * 0.7))
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox.center = self.rect.center

    def update(self):
        if self.rect.bottom >= 530:
            self.rect.bottom = 530
        
        self.rect.x += self.velocidade * self.direcao
        if abs(self.rect.x - self.início_x) > self.alcance:
            self.direcao = self.direcao * -1

        self.update_hitbox()