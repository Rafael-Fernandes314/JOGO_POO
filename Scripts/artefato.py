import pygame
from pygame.locals import *
from typing import List

class OrbeDoMar(pygame.sprite.Sprite):
    def __init__(self, largura, altura):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("Assets\Sprites\Arterfatos\Orbe_do_mar.png")
        self.image = pygame.transform.scale(self.image, (32 * 4, 32 * 4))

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (largura, altura)

    def update(self):
        if self.rect.bottom >= 500:
            self.rect.bottom = 500

        

        