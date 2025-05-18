import pygame
from pygame.locals import *
from sys import exit

pygame.init()

class Eindein(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load("main.py\Assets\Sprites\Player\Eidein-andando0.png"))
        self.sprites.append(pygame.image.load("main.py\Assets\Sprites\Player\Eidein-andando1.png"))
        self.sprites.append(pygame.image.load("main.py\Assets\Sprites\Player\Eidein-andando2.png"))
        self.sprites.append(pygame.image.load("main.py\Assets\Sprites\Player\Eidein-andando3.png"))
        self.sprites.append(pygame.image.load("main.py\Assets\Sprites\Player\Eidein-andando4.png"))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (32 * 10, 32 * 10))

        self.rect = self.image.get_rect()
        self.rect.topleft = 100, 100

        self.animar = False

    def andar(self):
            self.animar = True

    def update(self):
        if self.animar == True:
            self.atual = self.atual + 0.25
            if self.atual >= len(self.sprites):
                self.atual = 0
                self.animar = False
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (32 * 10, 32 * 10))