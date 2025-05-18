import pygame
from pygame.locals import *
from sys import exit
from player import Eindein

pygame.init()

largura = 640
altura = 480

PRETO = (0,0,0)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Sprites")

todas_as_sprites = pygame.sprite.Group()
eindein = Eindein()
todas_as_sprites.add(eindein)

relógio = pygame.time.Clock()
        
while True:
    relógio.tick(30)
    tela.fill((PRETO))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            eindein.andar()
    
    todas_as_sprites.draw(tela)
    todas_as_sprites.update()
    pygame.display.flip()