import pygame
from pygame.locals import *
from sys import exit

pygame.init()

# tamanho da tela
largura = 1020
altura = 680

# cor do fundo
PRETO = (0, 0, 0)

# cria a tela e título do jogo
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Herdeiros do Fim - Início")

fundo_img = pygame.image.load("Assets/Sprites/Cenários/fundo teste.png").convert()
fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

logo = pygame.image.load("Assets/Sprites/UI/jogo-logo.png").convert()
logo = pygame.transform.scale(logo, (137 * 4, 110 * 4))


relógio = pygame.time.Clock()

while True:
    relógio.tick(60) # 60 fps
    tela.fill(PRETO) # limpa a tela

    # eventos do jogo
    for event in pygame.event.get():
        # sair do jogo
        if event.type == QUIT:
            pygame.quit()
            exit()

    tela.blit(fundo_img, (0,0))
    tela.blit(logo,(200,0))
    pygame.display.flip()