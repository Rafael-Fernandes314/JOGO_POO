import pygame
from pygame.locals import *
import random
import math
from player import *

pygame.init()

CHAO_CENARIO = 515
fonte_boss = pygame.font.Font("Assets/Fontes/PixelifySans-VariableFont_wght.ttf", 30)

class Goblin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        imagem = pygame.image.load("Assets/Sprites/Inimigos/goblin verde.png").convert_alpha()
        imagem = pygame.transform.scale(imagem, (32 * 4, 32 * 4))

        self.image_d = imagem
        self.image_e = pygame.transform.flip(imagem, True, False)
        self.image = self.image_d

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        self.velocidade = 2
        self.direcao = 1
        self.alcance = 100
        self.x_inicial = x
        self.pos_x = float(self.rect.x)

        self.vida = 2
        self.dano = 1

        self.cooldown_dano = 800
        self.ultimo_dano = 0

        self.hitbox = pygame.Rect(0, 0, 20, 128)
        self.atualizar_hitbox()

    def atualizar_hitbox(self):
        self.hitbox.center = self.rect.center

    def patrulhar(self):
        self.pos_x += self.velocidade * self.direcao
        self.rect.x = int(self.pos_x)

        if self.rect.centerx <= self.x_inicial - self.alcance:
            self.rect.centerx = self.x_inicial - self.alcance
            self.pos_x = self.rect.x
            self.direcao = 1
            self.image = self.image_d

        elif self.rect.centerx >= self.x_inicial + self.alcance:
            self.rect.centerx = self.x_inicial + self.alcance
            self.pos_x = self.rect.x
            self.direcao = -1
            self.image = self.image_e


    def inverter_direcao(self):
        self.direcao *= -1
        self.image = self.image_e if self.direcao == -1 else self.image_d

    def pode_dar_dano(self):
        agora = pygame.time.get_ticks()
        return agora - self.ultimo_dano >= self.cooldown_dano

    def encostar_no_player(self, player):
        if self.pode_dar_dano():
            player.levar_dano(self.dano)
            self.ultimo_dano = pygame.time.get_ticks()

    def levar_dano(self, qtd=1):
        self.vida -= qtd

    def morreu(self):
        return self.vida <= 0

    def update(self):
        if self.rect.bottom >= 523:
            self.rect.bottom = 523

        self.patrulhar()
        self.atualizar_hitbox()

class Ladrão(Goblin):
    def __init__(self, x, y):
        super().__init__(x, y)

        imagem = pygame.image.load("Assets/Sprites/Inimigos/ladrão.png").convert_alpha()
        imagem = pygame.transform.scale(imagem, (128, 128))

        self.image_d = imagem
        self.image_e = pygame.transform.flip(imagem, True, False)
        self.image = self.image_d

        self.velocidade_normal = 4
        self.velocidade = self.velocidade_normal
        self.alcance = 300
        self.vida = 3
        self.sprint_ativo = False
        self.sprint_vel = 10
        self.sprint_duracao = 40
        self.sprint_contador = 0
        self.cooldown_sprint = 3000
        self.ultimo_sprint = 0

    def iniciar_sprint(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_sprint >= self.cooldown_sprint and not self.sprint_ativo:
            self.sprint_ativo = True
            self.sprint_contador = 0
            self.velocidade = self.sprint_vel
            self.ultimo_sprint = agora

    def update(self):
        if self.rect.bottom >= 523:
            self.rect.bottom = 523

        if not self.sprint_ativo:
            self.iniciar_sprint()

        if self.sprint_ativo:
            self.sprint_contador += 1
            if self.sprint_contador >= self.sprint_duracao:
                self.sprint_ativo = False
                self.velocidade = self.velocidade_normal

        self.patrulhar()
        self.atualizar_hitbox()

class GoblinV(Goblin):
    def __init__(self, x, y):
        super().__init__(x, y)

        imagem = pygame.image.load("Assets/Sprites/Inimigos/goblin vermelho.png").convert_alpha()
        imagem = pygame.transform.scale(imagem, (32 * 4, 32 * 4))
        self.image_d = imagem
        self.image_e = pygame.transform.flip(imagem, True, False)
        self.image = self.image_d

        self.velocidade = 5
        self.alcance = 120
        self.pulando = False
        self.vel_y = 0
        self.gravidade = 0.8
        self.altura_pulo = -12
        self.cooldown_pulo = 1000
        self.ultimo_pulo = 0
        self.chao = 523

    def iniciar_pulo(self):
        agora = pygame.time.get_ticks()
        if not self.pulando and agora - self.ultimo_pulo >= self.cooldown_pulo:
            self.pulando = True
            self.vel_y = self.altura_pulo
            self.ultimo_pulo = agora

            if self.direcao == -1:
                self.image = self.image_e
            else:
                self.image = self.image_d

    def update(self):
        if self.pulando:
            self.vel_y += self.gravidade
            self.rect.y += self.vel_y
            self.pos_x += self.velocidade * self.direcao
            self.rect.x = int(self.pos_x)

            if self.rect.centerx <= self.x_inicial - self.alcance:
                self.rect.centerx = self.x_inicial - self.alcance
                self.pos_x = self.rect.x
                self.direcao = 1
                self.image = self.image_d
            elif self.rect.centerx >= self.x_inicial + self.alcance:
                self.rect.centerx = self.x_inicial + self.alcance
                self.pos_x = self.rect.x
                self.direcao = -1
                self.image = self.image_e
            if self.rect.bottom >= self.chao:
                self.rect.bottom = self.chao
                self.pulando = False
                self.vel_y = 0
        else:
            self.patrulhar()
            self.iniciar_pulo()
        self.atualizar_hitbox()

class Golem(Goblin):
    CHAO = 530

    def __init__(self, x, y, grupo_projeteis, jogador):
        super().__init__(x, y)

        imagem = pygame.image.load("Assets/Sprites/Inimigos/golem.png").convert_alpha()
        imagem = pygame.transform.scale(imagem, (220, 220))
        self.image_d = imagem
        self.image_e = pygame.transform.flip(imagem, True, False)
        self.image = self.image_d

        self.jogador = jogador
        self.velocidade = 1
        self.alcance = 120
        self.vida = 2
        self.morto = False
        self.dano = 1
        self.pulando = False
        self.vel_y = 0
        self.gravidade = 0.8
        self.altura_pulo = -15
        self.cooldown_stomp = 5000
        self.ultimo_stomp = 0
        self.grupo_projeteis = grupo_projeteis
        self.explosao_ativa = False

    def levar_dano(self, dano):
        if self.morto:
            return
        self.vida -= dano
        if self.vida <= 0:
            self.morto = True

    def morreu(self):
        return self.morto

    def update(self):
        if self.morto:
            return

        agora = pygame.time.get_ticks()

        if not self.pulando and not self.explosao_ativa and agora - self.ultimo_stomp >= self.cooldown_stomp:
            self.iniciar_stomp()

        if self.pulando:
            self.vel_y += self.gravidade
            self.rect.y += self.vel_y
            if self.rect.bottom >= 425:
                self.rect.bottom = 425
                self.pulando = False
                self.vel_y = 0
                explosao = ExplosaoGolem(self.rect.centerx, self.CHAO, dano=self.dano, golem=self)
                self.grupo_projeteis.add(explosao)
                self.explosao_ativa = True

        if not self.pulando and not self.explosao_ativa:
            self.patrulhar()

        self.atualizar_hitbox()
    def iniciar_stomp(self):
        agora = pygame.time.get_ticks()
        if not self.pulando and not self.explosao_ativa and agora - self.ultimo_stomp >= self.cooldown_stomp:
            self.pulando = True
            self.vel_y = self.altura_pulo
            self.ultimo_stomp = agora

    def update(self):
        agora = pygame.time.get_ticks()

        if not self.pulando and not self.explosao_ativa and agora - self.ultimo_stomp >= self.cooldown_stomp:
            self.iniciar_stomp()

        if self.pulando:
            self.vel_y += self.gravidade
            self.rect.y += self.vel_y
            if self.rect.bottom >= 425:
                self.rect.bottom = 425
                self.pulando = False
                self.vel_y = 0
                explosao = ExplosaoGolem(self.rect.centerx, self.CHAO, dano=self.dano, golem=self)
                self.grupo_projeteis.add(explosao)
                self.explosao_ativa = True

        if not self.pulando and not self.explosao_ativa:
            self.patrulhar()
        self.atualizar_hitbox()

class ExplosaoGolem(pygame.sprite.Sprite):
    def __init__(self, x, y, dano=1, golem=None):
        super().__init__()
        self.dano = dano
        self.golem = golem
        self.image = pygame.image.load("Assets/Sprites/Ataques/explosão.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (320, 100))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.hitbox = pygame.Rect(0, 0, 200, 60)
        self.hitbox.midbottom = self.rect.midbottom
        self.tempo_inicio = pygame.time.get_ticks()
        self.duracao = 600

    def update(self):
        self.hitbox.midbottom = self.rect.midbottom
        if pygame.time.get_ticks() - self.tempo_inicio >= self.duracao:
            if self.golem:
                self.golem.explosao_ativa = False
            self.kill()

class Elfo(Goblin):
    def __init__(self, x, y, grupo_projeteis, jogador):
        super().__init__(x, y)
        imagem = pygame.image.load("Assets/Sprites/Inimigos/elfo.png").convert_alpha()
        imagem = pygame.transform.scale(imagem, (180, 180))

        self.image_d = imagem
        self.image_e = pygame.transform.flip(imagem, True, False)
        self.image = self.image_d
        self.velocidade = 3
        self.alcance = 200
        self.cooldown_dano = 500
        self.grupo_projeteis = grupo_projeteis
        self.jogador = jogador
        self.cooldown_tiro = 7000
        self.ultimo_tiro = pygame.time.get_ticks() - self.cooldown_tiro
        self.parado = False
        self.parada_duracao = 1000
        self.tempo_inicio_parada = 0
        self.alcance_tiro = 3000

    def update(self):
        if self.rect.bottom >= 480:
            self.rect.bottom = 480

        agora = pygame.time.get_ticks()
        distancia_x = self.jogador.rect.centerx - self.rect.centerx

        if self.parado:
            if agora - self.tempo_inicio_parada >= self.parada_duracao:
                self.parado = False
        else:
            self.patrulhar()
            if abs(distancia_x) <= self.alcance_tiro and agora - self.ultimo_tiro >= self.cooldown_tiro:
                self.parado = True
                self.tempo_inicio_parada = agora
                self.atirar()
                self.ultimo_tiro = agora

    def atirar(self):
        y_alvo = self.jogador.rect.centery + random.randint(-50, 50)
        direcao = 1 if self.jogador.rect.centerx > self.rect.centerx else -1

        flecha = Flecha(self.rect.centerx, y_alvo, direcao=direcao, dano=1)
        self.grupo_projeteis.add(flecha)

class Flecha(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao=1, dano=1, velocidade=5):
        super().__init__()
        self.dano = dano
        self.direcao = direcao
        self.velocidade = velocidade

        self.image = pygame.image.load("Assets/Sprites/Ataques/flecha.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (160, 160))

        if self.direcao == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=(x, y))
        hitbox_largura = 20
        hitbox_altura = 10
        self.hitbox = pygame.Rect(0, 0, hitbox_largura, hitbox_altura)
        self.hitbox.center = self.rect.center
        self.dano_aplicado = False

    def update(self):
        self.rect.x += self.velocidade * self.direcao
        self.hitbox.center = self.rect.center
        if self.rect.right < 0 or self.rect.left > 20000:
            self.kill()

class Xamã(Goblin):
    def __init__(self, x, y):
        super().__init__(x, y)

        imagem = pygame.image.load("Assets/Sprites/Inimigos/xamã.png").convert_alpha()
        imagem = pygame.transform.scale(imagem, (160, 160))
        self.image_d = imagem
        self.image_e = pygame.transform.flip(imagem, True, False)
        self.image = self.image_d
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.x_inicial = self.rect.centerx
        self.velocidade = 1.5
        self.alcance = 120
        self.vida = 2
        self.dano = 1
        self.raio_aura = 160
        self.aura_ativa = False
        self.tempo_aura = 0
        self.cooldown_aura = 4000
        self.duracao_aura = 1500
        self.ultimo_dano = 0
        self.cooldown_dano = 1000
        self.pos_x = float(self.rect.x)
        self.image_aura = pygame.image.load("Assets/Sprites/Ataques/aura.png").convert_alpha()
        self.image_aura = pygame.transform.scale(self.image_aura, (self.raio_aura*2, self.raio_aura*2))

    def ativar_aura(self):
        agora = pygame.time.get_ticks()
        if not self.aura_ativa and agora - self.tempo_aura > self.cooldown_aura:
            self.aura_ativa = True
            self.tempo_aura = agora

    def atualizar_aura(self):
        if self.aura_ativa:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_aura > self.duracao_aura:
                self.aura_ativa = False

    def aura_rect(self):
        pulsacao = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.02)
        tamanho = self.raio_aura * 2 * pulsacao
        return pygame.Rect(
            self.rect.centerx - tamanho // 2,
            self.rect.centery - tamanho // 2,
            tamanho,
            tamanho
        )

    def causar_dano(self, player, scroll_x=0):
        agora = pygame.time.get_ticks()
        if self.aura_ativa and agora - self.ultimo_dano >= self.cooldown_dano:
            pulsacao = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.02)
            tamanho = int(self.raio_aura * 2 * pulsacao * 0.7)
            aura_hitbox = pygame.Rect(int(self.rect.centerx - tamanho // 2 - scroll_x),int(self.rect.centery - tamanho // 2),tamanho,tamanho)
            if aura_hitbox.colliderect(player.rect):
                player.levar_dano(self.dano)
                self.ultimo_dano = agora

    def desenhar_aura(self, surface, scroll_x=0):
        if self.aura_ativa:
            alfa = 128 + 127 * math.sin(pygame.time.get_ticks() * 0.03)
            aura = self.image_aura.copy()
            aura.set_alpha(int(alfa))
            pos = (self.rect.centerx - self.raio_aura - scroll_x, self.rect.centery - self.raio_aura)
            surface.blit(aura, pos)

    def update(self):
        super().update()
        self.ativar_aura()
        self.atualizar_aura()