import pygame
from pygame.locals import *
from sys import exit
from player import Eindein
from enemy import Ladrão
from hud import desenhar_hud
import estado_jogo

def fade(tela, largura, altura):
    fade = pygame.Surface((largura, altura))
    fade.fill((0, 0, 0))
    for i in range(0, 255):
        fade.set_alpha(i)
        tela.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)

def jogar_fase_2():
    pygame.init()

    # tamanho da tela
    largura = 1020
    altura = 680

    # cor do fundo
    PRETO = (0, 0, 0)

    # cria a tela e título do jogo
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Herdeiros do Fim")

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Sons/Música/fase2.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    pulo = pygame.mixer.Sound("Assets/Sons/Efeitos/pulo.mp3")
    pulo.set_volume(0.5)

    coração_vermelho = pygame.image.load("Assets/Sprites/UI/coração1.png")
    coração_vermelho = pygame.transform.scale(coração_vermelho, (120, 120))

    coração_preto = pygame.image.load("Assets/Sprites/UI/coração2.png")
    coração_preto = pygame.transform.scale(coração_preto, (120, 120))

    # carrega o fundo
    fundo_img = pygame.image.load("Assets/Sprites/Cenários/fase2.png").convert()
    fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

    # sprites
    sprites = pygame.sprite.Group()
    eindein = Eindein()            # cria um jogador
    # lista de goblins
    ladrões = [
        Ladrão(2500, 530),
        Ladrão(5000, 530),
        Ladrão(7500, 530),
        Ladrão(10000, 530),
        Ladrão(12500, 530),
        Ladrão(15000, 530),
        Ladrão(17500, 530),
    ]
    sprites.add(eindein)

    relógio = pygame.time.Clock()
    scroll_x = 0  # controla a mudança da câmera
    cenario_largura = 3000 # tamanho do cenário

    tela.blit(fundo_img, (0, 0))
    pygame.display.flip()

    fadein = True
    fade_alpha = 255
    estado_jogo.fase_atual = 2

    # loop do jogo
    while True:
        relógio.tick(60) # 60 fps
        tela.fill(PRETO)

        # eventos do jogo
        for event in pygame.event.get():
            # sair do jogo
            if event.type == QUIT:
                pygame.quit()
                exit()
            # eventos de tecla
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    eindein.pular()
                    pulo.play()

        # teclas que tão sendo seguradas
        teclas = pygame.key.get_pressed()

        # movimentação e rolagem da câmera
        if teclas[K_a]:
            if eindein.rect.left > 0 or scroll_x <= 0:
                eindein.mover("esquerda")

        elif teclas[K_d]:
            eindein.mover("direita")
            if eindein.rect.left >= 200 and scroll_x < cenario_largura - largura:
                scroll_x += 5
                eindein.rect.left = 200

        # desenha o cenário
        for i in range(cenario_largura // fundo_img.get_width() + 1):
            x = i * fundo_img.get_width() - scroll_x
            tela.blit(fundo_img, (x, 0))
            
        # desenha o player e o inimigo com base no fundo
        tela.blit(eindein.image, (eindein.rect.x, eindein.rect.y))
        sprites.update() # atualiza o grupo de sprites
        # desenha todos os sprites
        sprites.draw(tela)

        # desenha e atualiza todos os ladrões
        for ladrão in ladrões[:]:
            tela.blit(ladrão.image, (ladrão.rect.x - scroll_x, ladrão.rect.y))
            ladrão.update()

            ladrão_hitbox_tela = ladrão.hitbox.move(-scroll_x, 0)

            if eindein.rect.colliderect(ladrão_hitbox_tela):
                ladrão.encostar_no_player(eindein)

            if ladrão.morreu():
                ladrão.remove(ladrão)

        for i in range(3):
            if i < eindein.vida:
                tela.blit(coração_vermelho, (10 + i * 70, 10))
            else:
                tela.blit(coração_preto, (10 + i * 70, 10))

        if eindein.vida == 0:
            pygame.mixer.music.stop()
            from gameover import Game_over
            Game_over()
            return
        
        if fadein:
            fadein = pygame.Surface((largura,altura))
            fadein.fill((0,0,0))
            fadein.set_alpha(fade_alpha)
            tela.blit(fadein,(0,0))
            fade_alpha -= 5
            if fade_alpha <= 0:
                fadein = False
        
        desenhar_hud(tela, largura, altura)
        pygame.display.flip()  # atualiza a tela

        if eindein.rect.x + scroll_x >= 3000:
            pygame.mixer.music.stop()
            fade(tela,largura,altura)
            from fase3 import jogar_fase_3
            jogar_fase_3()
            return