import pygame
from pygame.locals import *
from sys import exit
import math

def Game_over():
    pygame.init()

    # tamanho da tela
    largura = 1020
    altura = 680

    # cor do fundo
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)

    fadein = True
    fade_alpha = 255

    # cria a tela e título do jogo
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Herdeiros do Fim - Game Over")

    morte = pygame.image.load("Assets/Sprites/UI/game-over.png")
    morte = pygame.transform.scale(morte, (610, 360))
    rect = morte.get_rect(center=(largura / 2, altura / 2.8))

    # fonte para o texto
    fonte = pygame.font.Font("Assets/Fontes/PixelifySans-VariableFont_wght.ttf", 40)
    texto = fonte.render('Pressione "Espaço" para tentar novamente', True, BRANCO)
    rect_texto = texto.get_rect(center=(largura // 2, altura // 2 + 200))

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Sons/Música/gameover.mp3")
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
                    return True

        tempo = pygame.time.get_ticks() / 1000
        offset_y = math.sin(tempo * 2) * 10
        rect_logo_animado = rect.copy()
        rect_logo_animado.centery += offset_y
        tela.blit(morte, rect_logo_animado)
        tela.blit(texto, rect_texto)

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            tela.blit(texto, rect_texto)

        if fadein:
            fadein = pygame.Surface((largura,altura))
            fadein.fill((0,0,0))
            fadein.set_alpha(fade_alpha)
            tela.blit(fadein,(0,0))
            fade_alpha -= 5
            if fade_alpha <= 0:
                fadein = False

        pygame.display.flip()