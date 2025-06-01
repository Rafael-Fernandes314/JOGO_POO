import pygame
from pygame.locals import *
from sys import exit
from player import Eindein

pygame.init()

largura = 1020
altura = 680

PRETO = (0, 0, 0)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Jogo")

fundo_img = pygame.image.load("Assets/Sprites/Cenários/fundo teste.png").convert()
fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

sprites = pygame.sprite.Group()
eindein = Eindein()
sprites.add(eindein)

relógio = pygame.time.Clock()

while True:
    relógio.tick(60)
    tela.fill(PRETO)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                eindein.pular()
            if event.key == K_a:
                eindein.mover("esquerda")
            if event.key == K_d:
                eindein.mover("direita")

    teclas = pygame.key.get_pressed()

    if teclas[K_a]:
        eindein.mover("esquerda")
        
    elif teclas[K_d]:
        eindein.mover("direita")

    tela.blit(fundo_img, (0,0))
    sprites.draw(tela)
    sprites.update()
    pygame.display.flip()