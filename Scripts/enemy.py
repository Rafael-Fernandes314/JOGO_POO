import pygame
from pygame.locals import *

pygame.init()

class Goblin(pygame.sprite.Sprite):  # define a classe do goblin
    def __init__(self, largura, altura):  # largura e altura das posições dele
        pygame.sprite.Sprite.__init__(self)

        # carrega e redimensiona as imagens do goblin
        image = pygame.image.load("Assets/Sprites/Inimigos/goblin verde.png")
        image = pygame.transform.scale(image, (32 * 4, 32 * 4))

        # cria versões virada e normal
        self.imaged = image
        self.imagee = pygame.transform.flip(image, True, False)
        self.image = self.imaged
    
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
        self.hitbox = pygame.Rect(0, 0, (20), (128))
        self.update_hitbox() # atualiza a hitbox com a posição atual dele

        if self.direcao == -1:
            self.virar()

    def update_hitbox(self):
        # alinha a hitbox no centro do sprite
        self.hitbox.center = self.rect.center

    def update(self):
        # pra o goblin ficar no chão
        if self.rect.bottom >= 523:
            self.rect.bottom = 523

        # movimento automático
        self.rect.x += self.velocidade * self.direcao
        if abs(self.rect.x - self.início_x) > self.alcance:
            self.direcao *= -1
            self.virar()

        self.update_hitbox()  # mantém a hitbox atualizada
    
    def virar(self):
        if self.direcao == -1:
            self.image = self.imagee
        else:
            self.image = self.imaged

    def levar_dano(self):
        # tira a vida do goblin
        self.vida -= 1

class Ladrão(Goblin):
    def __init__(self, largura, altura):
        super().__init__(largura, altura)

        self.image = pygame.image.load("Assets/Sprites/Inimigos/ladrão.png")
        self.image = pygame.transform.scale(self.image, (128, 128))

        self.imaged = self.image
        self.imagee = pygame.transform.flip(self.image, True, False)
        self.image = self.imaged

        self.alcance = 400
        self.vida = 3
        self.velocidade = 4

        self.hitbox = pygame.Rect(0, 0, (128), (128))

class GoblinV(Goblin):
    def __init__(self, largura, altura):
        super().__init__(largura, altura)

        self.image = pygame.image.load("Assets/Sprites/Inimigos/goblin vermelho.png")
        self.image = pygame.transform.scale(self.image, (32*4, 32*4))

        self.imaged = self.image
        self.imagee = pygame.transform.flip(self.image, True, False)
        self.image = self.imaged
        
        self.velocidade = 8
        self.alcance = 100

    def update(self):
        if self.rect.bottom >= 520:
            self.rect.bottom = 520

        # movimento automático
        self.rect.x += self.velocidade * self.direcao
        if abs(self.rect.x - self.início_x) > self.alcance:
            self.direcao *= -1  # inverte a direção do goblin
            self.virar()

class Golem(Goblin):
    def __init__(self, largura, altura):
        super().__init__(largura, altura)

        self.image = pygame.image.load("Assets/Sprites/Inimigos/golem.png")
        self.image = pygame.transform.scale(self.image, (180, 180))

        self.imaged = self.image
        self.imagee = pygame.transform.flip(self.image, True, False)
        self.image = self.imaged

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (largura, altura)
        self.início_x = largura

        self.velocidade = 1.5
        self.alcance = 100
        self.vida = 5

        self.hitbox = pygame.Rect(0, 0, 100, 120)
        self.update_hitbox()

    def update(self):
        if self.rect.bottom >= 500:
            self.rect.bottom = 500

        self.rect.x += self.velocidade * self.direcao

        if abs(self.rect.x - self.início_x) > self.alcance:
            self.direcao *= -1
            self.início_x = self.rect.x
            self.virar()

        self.update_hitbox()
