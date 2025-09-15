import pygame
from pygame.locals import *
from sys import exit
from player import Eindein
from enemy import Goblin

def jogar_fase_1():
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
    pygame.mixer.music.load("Assets/Sons/Música/fase_1-música.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    coração_vermelho = pygame.image.load("Assets/Sprites/UI/coração1.png")
    coração_vermelho = pygame.transform.scale(coração_vermelho, (120, 120))

    coração_preto = pygame.image.load("Assets/Sprites/UI/coração2.png")
    coração_preto = pygame.transform.scale(coração_preto, (120, 120))

    # carrega o fundo
    fundo_img = pygame.image.load("Assets/Sprites/Cenários/fundo teste.png").convert()
    fundo_img = pygame.transform.scale(fundo_img, (1020, 680))

    # sprites
    sprites = pygame.sprite.Group()
    eindein = Eindein()            # cria um jogador
    # lista de goblins
    goblins = [
        Goblin(2500, 530),
        Goblin(5000, 530),
        Goblin(7500, 530),
        Goblin(10000, 530),
        Goblin(12500, 530),
        Goblin(15000, 530),
        Goblin(17500, 530),
    ]
    sprites.add(eindein)

    relógio = pygame.time.Clock()
    scroll_x = 0  # controla a mudança da câmera
    cenario_largura = 20000 # tamanho do cenário

    # loop do jogo
    while True:
        relógio.tick(60) # 60 fps
        tela.fill(PRETO) # limpa a tela

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

        # desenha e atualiza todos os goblins
        for goblin in goblins:
            tela.blit(goblin.image, (goblin.rect.x - scroll_x, goblin.rect.y))
            goblin.update()

            # colisão entre player e goblin
            goblin_hitbox_tela = goblin.hitbox.move(-scroll_x, 0)
            if eindein.rect.colliderect(goblin_hitbox_tela):
                eindein.levar_dano()

        for goblin in goblins[:]:  # evita bug ao remover
            tela.blit(goblin.image, (goblin.rect.x - scroll_x, goblin.rect.y))
            goblin.update()

            goblin_hitbox_tela = goblin.hitbox.move(-scroll_x, 0)

        for i in range(3):
            if i < eindein.vida:
                tela.blit(coração_vermelho, (10 + i * 70, 10))
            else:
                tela.blit(coração_preto, (10 + i * 70, 10))

        if eindein.vida == 0:
            pygame.mixer.music.stop()
            return
            
        # desenha todos os sprites
        sprites.draw(tela)
        pygame.display.flip()  # atualiza a tela