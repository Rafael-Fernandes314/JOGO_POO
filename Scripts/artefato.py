import pygame
from pygame.locals import *
from typing import List
import math
import random

class Artefato(pygame.sprite.Sprite):
    def __init__(self, largura, altura):
        pygame.sprite.Sprite.__init__(self)

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (largura, altura)

        self.altura_extra = -30
        self.base_y = self.rect.centery + self.altura_extra
        self.flutuar_velocidade = 2
        self.flutuar_altura = 10

        x = self.rect.width * 0.3
        y = self.rect.height * 0.3
        self.hitbox = pygame.Rect(0, 0, x, y)
        self.hitbox.center = self.rect.center

    def update(self):
        tempo = pygame.time.get_ticks() / 1000
        desvio_y = math.sin(tempo * self.flutuar_velocidade) * self.flutuar_altura
        self.rect.centery = self.base_y + desvio_y

        self.hitbox.center = self.rect.center
        
class Chave(Artefato):
    def __init__(self, largura, altura):
        self.image = pygame.image.load("Assets\Sprites\Arterfatos\chave.png")
        self.image = pygame.transform.scale(self.image, (53, 96))
        super().__init__(largura, altura)

class Orbe(Artefato):
    def __init__(self, largura, altura):
        self.image = pygame.image.load("Assets\Sprites\Arterfatos\orbe.png")
        self.image = pygame.transform.scale(self.image, (109, 108))
        super().__init__(largura, altura)
        
class Espada(Artefato):
    def __init__(self, largura, altura):
        self.image = pygame.image.load("Assets\Sprites\Arterfatos\espada.png")
        self.image = pygame.transform.scale(self.image, (111, 108))
        super().__init__(largura, altura)
        
class Escudo(Artefato):
    def __init__(self, largura, altura):
        self.image = pygame.image.load("Assets\Sprites\Arterfatos\escudo.png")
        self.image = pygame.transform.scale(self.image, (108, 108))
        super().__init__(largura, altura)

class Anel(Artefato):
    def __init__(self, largura, altura):
        self.image = pygame.image.load("Assets/Sprites/Arterfatos/anel.png")
        self.image = pygame.transform.scale(self.image, (120, 72))
        super().__init__(largura, altura)

class Emblema(Artefato):
    def __init__(self, largura, altura):
        self.image = pygame.image.load("Assets\Sprites\Arterfatos\emblema.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        super().__init__(largura, altura)

class Sangue(Artefato):
    def __init__(self, largura, altura):
        self.image = pygame.image.load("Assets\Sprites\Arterfatos\sangue.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        super().__init__(largura, altura)

class ItemPuzzle(Artefato):
    def __init__(self, largura, altura):

        self.image = pygame.image.load("Assets/Sprites/Arterfatos/item.png")
        self.image = pygame.transform.scale(self.image, (250, 250))
        super().__init__(largura, altura)

    def update(self):
        pass
