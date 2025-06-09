import pygame
from pygame.locals import *

pygame.init()

class Goblin(pygame.sprite.Sprite):  # define a classe do goblin
    def __init__(self, largura, altura):  # largura e altura das posições dele
        pygame.sprite.Sprite.__init__(self)

        # carrega e redimensiona as imagens do goblin
        self.image = pygame.image.load("Assets/Sprites/Inimigos/goblin verde.png")
        self.image = pygame.transform.scale(self.image, (32*4, 32*4))

        # define a posição do goblin com base no canto inferior esquerdo
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (largura, altura)

        # atributos de movimento e comportamento
        self.velocidade = 2 # velocidade de movimento
        self.direcao = 1    # direção do movimento
        self.alcance = 100  # distância máxima que ele pode andar
        self.início_x = largura # ponto de início pra o alcance
        self.animar = False # permite a animação
        self.vida = 2   # vida do goblin

        # hitbox usada pra colisão
        self.hitbox = pygame.Rect(0, 0, (120 * 0.6), (120 * 0.7))
        self.update_hitbox() # atualiza a hitbox com a posição atual dele

    def update_hitbox(self):
        # alinha a hitbox no centro do sprite
        self.hitbox.center = self.rect.center

    def update(self):
        # pra o goblin ficar no chão
        if self.rect.bottom >= 530:
            self.rect.bottom = 530

        # movimento automático
        self.rect.x += self.velocidade * self.direcao
        if abs(self.rect.x - self.início_x) > self.alcance:
            self.direcao = self.direcao * -1  # inverte a direção do goblin

        self.update_hitbox()  # mantém a hitbox atualizada

    def levar_dano(self):
        # tira a vida do goblin
        self.vida -= 1