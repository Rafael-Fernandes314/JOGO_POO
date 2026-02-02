import pygame
from pygame.locals import *
from sys import exit
from player import Eindein
from enemy import Elfo, Flecha
from artefato import Anel
from hud import desenhar_hud
from inventario import artefatos_coletados
import estado_jogo

def fade(tela, largura, altura):
    fade = pygame.Surface((largura, altura))
    fade.fill((0, 0, 0))
    for i in range(0, 255):
        fade.set_alpha(i)
        tela.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)

def jogar_fase_6():

    pygame.init()

    # tamanho da tela
    largura = 1020
    altura = 680

    # cor do fundo
    PRETO = (0, 0, 0)

    # cria a tela e título do jogo
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Herdeiros do Fim")

    logo_pause = pygame.image.load("Assets/Sprites/UI/jogo_pausado.png").convert_alpha()
    logo_pause = pygame.transform.scale(logo_pause, (500, 250))
    rect_logo_pause = logo_pause.get_rect(center=(largura // 2, altura // 2 - 100))

    fonte_pause = pygame.font.Font("Assets/Fontes/PixelifySans-VariableFont_wght.ttf", 36)
    texto_pause = fonte_pause.render("Pressione ESC para continuar", True, (255, 255, 255))
    rect_texto_pause = texto_pause.get_rect(center=(largura // 2, altura // 2 + 120))

    pausado = False

    overlay = pygame.Surface((largura, altura))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(160)

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Sons/Música/fase3.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    pulo = pygame.mixer.Sound("Assets/Sons/Efeitos/pulo.mp3")
    pulo.set_volume(0.5)
    coletar = pygame.mixer.Sound("Assets/Sons/Efeitos/coletar_artefato.mp3")
    coletar.set_volume(0.7)

    coração_vermelho = pygame.image.load("Assets/Sprites/UI/coração1.png")
    coração_vermelho = pygame.transform.scale(coração_vermelho, (120, 120))

    coração_preto = pygame.image.load("Assets/Sprites/UI/coração2.png")
    coração_preto = pygame.transform.scale(coração_preto, (120, 120))

    # carrega o fundo
    fundo_img = pygame.image.load("Assets/Sprites/Cenários/fase6.png").convert()
    fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

    # sprites
    sprites = pygame.sprite.Group()
    grupo_projeteis = pygame.sprite.Group()
    eindein = Eindein() # cria um jogador
    # lista de goblins
    elfos = [
        Elfo(2500, 530, grupo_projeteis, eindein),
        Elfo(4000, 530, grupo_projeteis, eindein),
        Elfo(5500, 530, grupo_projeteis, eindein),
        Elfo(7000, 530, grupo_projeteis, eindein),
        Elfo(8500, 530, grupo_projeteis, eindein),
        Elfo(10000, 530, grupo_projeteis, eindein),
        Elfo(11300, 530, grupo_projeteis, eindein),
    ]
    sprites.add(eindein)
    artefato = Anel(11800, 500)
    relógio = pygame.time.Clock()
    scroll_x = 0  # controla a mudança da câmera
    cenario_largura = 12000 # tamanho do cenário

    tela.blit(fundo_img, (0, 0))
    pygame.display.flip()

    fadein = True
    fade_alpha = 255
    estado_jogo.fase_atual = 6
    estado_jogo.vida_max_jogador = 5

    # loop do jogo
    while True:
        relógio.tick(60)  # 60 fps
        tela.fill(PRETO)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pausado = not pausado

                if not pausado and event.key == K_SPACE:
                    eindein.pular()
                    pulo.play()
            if event.type == pygame.MOUSEBUTTONDOWN and not pausado:
                    eindein.atacar()

        for i in range(cenario_largura // fundo_img.get_width() + 1):
            x = i * fundo_img.get_width() - scroll_x
            tela.blit(fundo_img, (x, 0))

        teclas = pygame.key.get_pressed()

        if not pausado:
            if teclas[K_s]:
                eindein.agachar(True)
            else:
                eindein.agachar(False)

                if teclas[K_a]:
                    if eindein.rect.left > 0 or scroll_x <= 0:
                        eindein.mover("esquerda")
                elif teclas[K_d]:
                    eindein.mover("direita")
                    if eindein.rect.left >= 200 and scroll_x < cenario_largura - largura:
                        scroll_x += 5
                        eindein.rect.left = 200

            teclas = pygame.key.get_pressed()

            if teclas[K_m] and teclas[K_r]:
                pygame.mixer.music.stop()
                fade(tela, largura, altura)
                from fase7 import jogar_fase_7
                jogar_fase_7()
                return

            sprites.update()
            sprites.draw(tela)

            if artefato:
                tela.blit(artefato.image, (artefato.rect.x - scroll_x, artefato.rect.y))
                artefato.update()

                artefato_hitbox_tela = artefato.hitbox.move(-scroll_x, 0)
                if eindein.rect.colliderect(artefato_hitbox_tela):
                    coletar.play()
                    artefatos_coletados["anel"] = True
                    artefato = None

            for elfo in elfos[:]:
                elfo.scroll_x = scroll_x
                elfo.largura_tela = largura
                tela.blit(elfo.image, (elfo.rect.x - scroll_x, elfo.rect.y))
                elfo.desenhar_barra_hp(tela, scroll_x)
                elfo.update()

                elfo_hitbox_tela = elfo.hitbox.move(-scroll_x, 0)

                if eindein.atacando:
                    if eindein.hitbox_ataque.colliderect(elfo_hitbox_tela):
                        elfo.levar_dano(eindein.dano)

                if eindein.rect.colliderect(elfo_hitbox_tela):
                    elfo.encostar_no_player(eindein)

                if elfo.morreu():
                    elfos.remove(elfo)

            grupo_projeteis.update()
            for flecha in grupo_projeteis:
                tela.blit(flecha.image, (flecha.rect.x - scroll_x, flecha.rect.y))

                flecha_hitbox_tela = flecha.hitbox.move(-scroll_x, 0)
                if eindein.rect.colliderect(flecha_hitbox_tela) and not flecha.dano_aplicado:
                    eindein.levar_dano(flecha.dano)
                    flecha.dano_aplicado = True
                    flecha.kill()

        for i in range(eindein.vida_max):
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
            fade_surface = pygame.Surface((largura, altura))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            tela.blit(fade_surface, (0, 0))
            fade_alpha -= 5
            if fade_alpha <= 0:
                fadein = False

        desenhar_hud(tela, largura, altura)

        if pausado:
            tela.blit(overlay, (0, 0))
            tela.blit(logo_pause, rect_logo_pause)
            tela.blit(texto_pause, rect_texto_pause)

        pygame.display.flip()

        if not pausado and eindein.rect.x + scroll_x >= cenario_largura:
            pygame.mixer.music.stop()
            fade(tela, largura, altura)
            from fase7 import jogar_fase_7
            jogar_fase_7()
            return