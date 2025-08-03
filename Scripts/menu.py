import pygame
from pygame.locals import *
from sys import exit
import math

def mostrar_menu():
    pygame.init()

    # tamanho da tela
    largura = 1020
    altura = 680

    # cor do fundo
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)

    # cria a tela e título do jogo
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Herdeiros do Fim - Início")

    fundo_img = pygame.image.load("Assets/Sprites/Cenários/menu-fundo.png").convert()
    fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

    logo = pygame.image.load("Assets/Sprites/UI/logo jogo.png")
    logo = pygame.transform.scale(logo, (610, 360))
    rect = logo.get_rect(center=(largura / 2, altura / 2.8))

    # fonte para o texto
    fonte = pygame.font.Font("Assets/Fontes/PixelifySans-VariableFont_wght.ttf", 50)
    texto = fonte.render('Pressione "Espaço" para iniciar', True, BRANCO)
    rect_texto = texto.get_rect(center=(largura // 2, altura // 2 + 200))

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Sons/Música/música-menu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    relógio = pygame.time.Clock()

    while True:
        relógio.tick(60)
        tela.fill(PRETO)

        # eventos do jogo
        for event in pygame.event.get():
            # sair do jogo
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pygame.mixer.music.stop()
                    return

        tela.blit(fundo_img, (0,0))
        tempo = pygame.time.get_ticks() / 1000
        offset_y = math.sin(tempo * 2) * 10
        rect_logo_animado = rect.copy()
        rect_logo_animado.centery += offset_y
        tela.blit(logo, rect_logo_animado)
        tela.blit(texto, rect_texto)

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            tela.blit(texto, rect_texto)

        pygame.display.flip()