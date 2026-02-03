import pygame
from pygame.locals import *
from sys import exit
from player import Eindein
from enemy import Boss, AtaqueBoss, AtaqueLateralAlto, AtaqueLateralBaixo
from artefato import ItemPuzzle
from hud import desenhar_hud
import estado_jogo
import random

def fade(tela, largura, altura):
    fade = pygame.Surface((largura, altura))
    fade.fill((0, 0, 0))
    for i in range(0, 255):
        fade.set_alpha(i)
        tela.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)

def faseBoss():
    pygame.init()

    # tamanho da tela
    largura = 1020
    altura = 680

    # cor do fundo
    PRETO = (0, 0, 0)

    # cria a tela e título do jogo
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Herdeiros do Fim")

    pausado = False

    logo_pause = pygame.image.load("Assets/Sprites/UI/jogo_pausado.png").convert_alpha()
    logo_pause = pygame.transform.scale(logo_pause, (500, 250))
    rect_logo_pause = logo_pause.get_rect(center=(largura // 2, altura // 2 - 100))

    fonte_pause = pygame.font.Font("Assets/Fontes/PixelifySans-VariableFont_wght.ttf", 36)
    texto_pause = fonte_pause.render("Pressione ESC para continuar", True, (255, 255, 255))
    rect_texto_pause = texto_pause.get_rect(center=(largura // 2, altura // 2 + 120))

    pygame.mixer.init()
    pygame.mixer.music.load("Assets/Sons/Música/boss.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    pulo = pygame.mixer.Sound("Assets/Sons/Efeitos/pulo.mp3")
    pulo.set_volume(0.5)
    ataque = pygame.mixer.Sound("Assets/Sons/Efeitos/ataque.mp3")
    ataque.set_volume(0.5)

    coração_vermelho = pygame.image.load("Assets/Sprites/UI/coração1.png")
    coração_vermelho = pygame.transform.scale(coração_vermelho, (120, 120))

    coração_preto = pygame.image.load("Assets/Sprites/UI/coração2.png")
    coração_preto = pygame.transform.scale(coração_preto, (120, 120))

    # carrega o fundo
    fundo_img = pygame.image.load("Assets/Sprites/Cenários/fase9.png").convert()
    fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

    # sprites
    sprites = pygame.sprite.Group()
    eindein = Eindein()            # cria um jogador

    boss = Boss(510, 440)
    ataques_boss = pygame.sprite.Group()

    item = None

    posicoes_spawn = [
        (200, 550),
        (400, 550),
        (600, 550),
        (800, 550)
    ]

    tempo_spawn_item = 8000
    ultimo_spawn_item = pygame.time.get_ticks()

    tempo_ataque_boss = 2000
    ultimo_ataque_boss = pygame.time.get_ticks()

    sprites.add(eindein)
    sprites.add(boss)

    # lista de goblins
    sprites.add(eindein)

    relógio = pygame.time.Clock()
    scroll_x = 0  # controla a mudança da câmera
    cenario_largura = 1020 # tamanho do cenário

    fadein = True
    fade_alpha = 255
    estado_jogo.fase_atual = 10
    estado_jogo.vida_max_jogador = 5

    # loop do jogo
    while True:
        relógio.tick(60) # 60 fps
        tela.fill(PRETO)

        for i in range(cenario_largura // fundo_img.get_width() + 1):
            x = i * fundo_img.get_width() - scroll_x
            tela.blit(fundo_img, (x, 0))


        # eventos do jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pausado = not pausado
                if not pausado:
                    if event.key == K_UP:
                        eindein.pular()
                        pulo.play()

        teclas = pygame.key.get_pressed()

        if not pausado:

            agora = pygame.time.get_ticks()

            if agora - ultimo_ataque_boss >= tempo_ataque_boss:

                tipo = random.choice(["chuva", "alto", "baixo"])

                if tipo == "chuva":
                    for _ in range(random.randint(1, 3)):
                        x_random = random.randint(50, largura - 50)
                        ataques_boss.add(AtaqueBoss(x_random, 0))

                elif tipo == "alto":
                    ataques_boss.add(AtaqueLateralAlto(eindein, largura))

                elif tipo == "baixo":
                    ataques_boss.add(AtaqueLateralBaixo(eindein, largura))

                ultimo_ataque_boss = agora

            if item is None and agora - ultimo_spawn_item >= tempo_spawn_item:
                pos = random.choice(posicoes_spawn)
                item = ItemPuzzle(pos[0], pos[1])
                sprites.add(item)
                ultimo_spawn_item = agora

            if pygame.sprite.spritecollide(eindein, ataques_boss, True):
                eindein.levar_dano(1)

            if teclas[K_DOWN]:
                eindein.agachar(True)
            else:
                eindein.agachar(False)

                if teclas[K_LEFT]:
                    eindein.direcao = "esquerda"
                    eindein.animar = True

                    if scroll_x > 0 and eindein.rect.left <= 200:
                        scroll_x -= 5
                        scroll_x = max(0, scroll_x)
                    else:
                        if eindein.rect.left > 0:
                            eindein.rect.x -= eindein.velocidade

                elif teclas[K_RIGHT]:
                    eindein.mover("direita")
                    if eindein.rect.left >= 200 and scroll_x < cenario_largura - largura:
                        scroll_x += 5
                        eindein.rect.left = 200

            teclas = pygame.key.get_pressed()

            if teclas[K_m] and teclas[K_r]:
                pygame.mixer.music.stop()
                estado_jogo.fase_atual = 10
                fade(tela, largura, altura)
                from final import tela_final
                tela_final()
                return
            
            if eindein.rect.left < 0:
                eindein.rect.left = 0
            if eindein.rect.right > largura:
                eindein.rect.right = largura

            if item and eindein.rect.colliderect(item.hitbox):
                boss.levar_dano(1)
                item.kill()
                item = None

            sprites.update()
            ataques_boss.update()

            sprites.draw(tela)
            ataques_boss.draw(tela)
            boss.desenhar_barra_hp(tela)

        for i in range(eindein.vida_max):
            if i < eindein.vida:
                tela.blit(coração_vermelho, (10 + i * 70, 10))
            else:
                tela.blit(coração_preto, (10 + i * 70, 10))

        if eindein.vida == 0:
            pygame.mixer.music.stop()
            estado_jogo.fase_atual = 10
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
            overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            tela.blit(overlay, (0, 0))
            tela.blit(logo_pause, rect_logo_pause)
            tela.blit(texto_pause, rect_texto_pause)

        pygame.display.flip()  # atualiza a tela

        if boss.morreu():
            pygame.mixer.music.stop()
            fade(tela, largura, altura)
            from final import tela_final
            tela_final()
            return