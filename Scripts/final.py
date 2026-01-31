import pygame
from pygame.locals import *
from sys import exit
import math

def fade(tela, largura, altura, fundo_img, logo, rect_logo_animado, texto, rect_texto):
    fade = pygame.Surface((largura, altura))
    fade.fill((0, 0, 0))
    for i in range(0, 255, 5):
        fade.set_alpha(i)
        tela.blit(fundo_img, (0,0))
        tela.blit(logo, rect_logo_animado)
        tela.blit(texto, rect_texto)
        tela.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(5)

def tela_final():
    
    pygame.init()

    # tamanho da tela
    largura = 1020
    altura = 680

    # cor do fundo
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)
    DOURADO = (212, 175, 55)

    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Herdeiros do Fim - Fim")

    fundo_img = pygame.image.load("Assets/Sprites/Cenários/menu final.png")
    fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

    logo = pygame.image.load("Assets/Sprites/UI/vitoria.png")
    logo = pygame.transform.scale(logo, (610, 360))
    rect = logo.get_rect(center=(largura / 2, altura / 2.8))

    fonte = pygame.font.Font("Assets/Fontes/PixelifySans-VariableFont_wght.ttf", 40)
    texto_parabens = fonte.render('Parabéns! Você realizou o seu desejo.',True,DOURADO)
    texto = fonte.render('Pressione "Espaço" para voltar ao início', True, BRANCO)
    rect_parabens = texto_parabens.get_rect(center=(largura // 2, altura // 2 + 140))
    rect_texto = texto.get_rect(center=(largura // 2, altura // 2 + 200))

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Sons/Música/menu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    iniciar = pygame.mixer.Sound("Assets/Sons/Efeitos/botão_iniciar.mp3")
    iniciar.set_volume(0.8)

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
                    iniciar.play()
                    pygame.mixer.music.stop()
                    fade(tela, largura, altura, fundo_img, logo, rect_logo_animado, texto, rect_texto)
                    import estado_jogo
                    estado_jogo.fase_atual = 0
                    return

        tela.blit(fundo_img, (0,0))
        tempo = pygame.time.get_ticks() / 1000
        offset_y = math.sin(tempo * 2) * 10
        rect_logo_animado = rect.copy()
        rect_logo_animado.centery += offset_y
        tela.blit(logo, rect_logo_animado)
        tela.blit(texto, rect_texto)

        if (pygame.time.get_ticks() // 500) % 2 == 0:
            tela.blit(texto_parabens, rect_parabens)
            tela.blit(texto, rect_texto)

        pygame.display.flip()