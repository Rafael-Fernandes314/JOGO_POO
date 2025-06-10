import pygame
from pygame.locals import *
from sys import exit
from player import Eindein
from enemy import Goblin

pygame.init()

# tamanho da tela
largura = 1020
altura = 680

# cor do fundo
PRETO = (0, 0, 0)

# cria a tela e título do jogo
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Herdeiros do Fim")

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
goblin = Goblin(2000, 530)     # cria um goblin
sprites.add(eindein)          # adiciona o jogador no grupo de sprites

relógio = pygame.time.Clock()
scroll_x = 0  # controla a mudança da câmera

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
        eindein.mover("esquerda")

    elif teclas[K_d]:
        eindein.mover("direita")
        if eindein.rect.left >= 200:
            scroll_x += 5
            eindein.rect.left = 200

    # repete a imagem de fundo
    for i in range(-1, largura // fundo_img.get_width() + 3):
        x = i * fundo_img.get_width() - (scroll_x % fundo_img.get_width())
        tela.blit(fundo_img, (x, 0))
        
    # desenha o player e o inimigo com base no fundo
    tela.blit(eindein.image, (eindein.rect.x, eindein.rect.y))
    tela.blit(goblin.image, (goblin.rect.x - scroll_x, goblin.rect.y))

    sprites.update() # atualiza o grupo de sprites
    goblin.update()  # atualiza o movimento do goblin

    # colisão entre player e goblin
    goblin_hitbox_tela = goblin.hitbox.move(-scroll_x, 0)
    if eindein.rect.colliderect(goblin_hitbox_tela):
        eindein.levar_dano()

    for i in range(3):
        if i < eindein.vida:
            tela.blit(coração_vermelho, (10 + i * 70, 10))
        else:
            tela.blit(coração_preto, (10 + i * 70, 10))

    if eindein.vida == 0:
        eindein.morrer()
        
    # desenha todos os sprites
    sprites.draw(tela)
    pygame.display.flip()  # atualiza a tela
