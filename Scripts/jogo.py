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

scroll_x = 0

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

    teclas = pygame.key.get_pressed()

    if teclas[K_a]:
        eindein.mover("esquerda")
        if eindein.rect.left <= 200:
            scroll_x -= 5
            eindein.rect.left = 200 

    elif teclas[K_d]:
        eindein.mover("direita")
        if eindein.rect.left >= 200:
            scroll_x += 5
            eindein.rect.left = 200 
            
    for i in range(-1, largura // fundo_img.get_width() + 3):
        x = i * fundo_img.get_width() - (scroll_x % fundo_img.get_width())
        tela.blit(fundo_img, (x, 0))

    tela.blit(eindein.image, (eindein.rect.x, eindein.rect.y))

    sprites.update()
    pygame.display.flip()
