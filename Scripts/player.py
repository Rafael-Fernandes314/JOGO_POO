import pygame
from pygame.locals import *
from typing import List

pygame.init()

class Eindein(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Assets/Sprites/Player/Eidein-parado-e.png")
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

        self.vel_y = 0
        self.pulando = False
        self.gravidade = 2
        self.velocidade = 5
        self.animar = False

        self.sprite_e:List[Eindein] = []
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-parado-e.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e1.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e2.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e3.png"), (32 * 4, 32 * 4)))
        self.sprite_e.append(pygame.transform.scale(pygame.image.load("Assets/Sprites/Player/Eidein-andando-e4.png"), (32 * 4, 32 * 4)))
        self.atual1 = 0
        self.image = self.sprite_e[self.atual1]

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

        self.sprite_d:List[Eindein] = []
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-parado-d.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d1.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d2.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d3.png"))
        self.sprite_d.append(pygame.image.load("Assets/Sprites/Player/Eidein-andando-d4.png"))
        self.atual2 = 0
        self.image = self.sprite_d[self.atual2]
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)

    def update(self):
        self.vel_y += self.gravidade
        self.rect.y += self.vel_y

        if self.rect.bottom >= 515:
            self.rect.bottom = 515
            self.pulando = False
        if self.animar == True:
            self.atual1 = self.atual1 + 0.2
            if self.atual1 >= len(self.sprite_e):
                self.atual1 = 0
                self.animar = False
            self.image = self.sprite_e[int(self.atual1)]
            self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

            self.atual2 = self.atual2 + 0.2
            if self.atual2 >= len(self.sprite_d):
                self.atual2 = 0
                self.animar = False
            self.image = self.sprite_d[int(self.atual2)]
            self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

    def mover(self, direcao):
        self.animar = True
        if direcao == "esquerda":
            self.rect.x -= self.velocidade
            
        elif direcao == "direita":
            self.rect.x += self.velocidade
            

    def pular(self):
        if not self.pulando:
            self.vel_y = -25
            self.pulando = True