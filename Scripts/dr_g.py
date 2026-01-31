import pygame
from pygame.locals import *
import random
import math
from enemy import Goblin
from enemy import *

pygame.init()

CHAO_CENARIO = 515
fonte_boss = pygame.font.Font("Assets/Fontes/PixelifySans-VariableFont_wght.ttf", 30)

class Dr_G(pygame.sprite.Sprite):
    def __init__(self, x, y, grupo_inimigos, grupo_projeteis):
        super().__init__()

        self.image = pygame.image.load("Assets/Sprites/Inimigos/dr_g.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 180))
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.image_e = self.image
        self.image_d = pygame.transform.flip(self.image, True, False)

        self.image = self.image_e
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.hitbox = pygame.Rect(0, 0, 60, 160)
        self.hitbox.center = self.rect.center

        self.grupo_inimigos = grupo_inimigos
        self.grupo_projeteis = grupo_projeteis
        self.vida_max = 20
        self.vida = self.vida_max
        self.hp_largura = 120
        self.hp_altura = 10
        self.direcao = -1
        self.velocidade = 1
        self.alcance = 120
        self.x_inicial = self.rect.x
        self.atacando = False
        self.tomou_dano = False
        self.ultimo_ataque = 0
        self.cooldown_ataque = 3500
        self.tempo_ultimo_dano = 0
        self.cooldown_dano = 400

    def mover(self):
        self.rect.x += self.velocidade * self.direcao

        if abs(self.rect.x - self.x_inicial) >= self.alcance:
            self.direcao *= -1

    def levar_dano(self, dano):
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_dano >= self.cooldown_dano:
            self.vida -= dano
            self.tempo_ultimo_dano = agora

            if self.vida < 0:
                self.vida = 0

    def morreu(self):
        return self.vida <= 0
    
    def desenhar_nome(self, tela, scroll_x):
        texto = fonte_boss.render("Dr. G", True, (255, 255, 255))
        rect_texto = texto.get_rect(
            center=(
                self.rect.centerx - scroll_x,
                self.rect.top - 28
            )
        )
        tela.blit(texto, rect_texto)

    def desenhar_barra_hp(self, tela, scroll_x):
        fundo = pygame.Rect(
            self.rect.centerx - self.hp_largura // 2 - scroll_x,
            self.rect.top - 10,
            self.hp_largura,
            self.hp_altura
        )
        proporcao = self.vida / self.vida_max
        largura_atual = int(self.hp_largura * proporcao)

        vida_atual = pygame.Rect(
            fundo.x,
            fundo.y,
            largura_atual,
            self.hp_altura
        )
        pygame.draw.rect(tela, (120, 0, 0), fundo)
        pygame.draw.rect(tela, (0, 200, 0), vida_atual)

    def escolher_ataque(self):
        r = random.randint(1, 100)

        if r <= 25:
            self.invocar_goblin()
        elif r <= 75:
            self.lancar_projetil()
        else:
            self.lancar_buraco_negro()

    def invocar_goblin(self):
        lado = random.choice([-1, 1])
        distancia = random.randint(120, 200)

        goblin = Goblin(self.rect.centerx + lado * distancia,self.rect.bottom)
        self.grupo_inimigos.add(goblin)

    def lancar_projetil(self):
        direcao = -1
        escolha = random.choice(["cima", "baixo"])

        if escolha == "cima":
            y = self.rect.top + 15
        else:
            y = self.rect.bottom -22

        x = self.rect.left - 40
        projetil = ProjetilDrG(x, y, direcao)
        self.grupo_projeteis.add(projetil)

    def lancar_buraco_negro(self):
        alvo_x = random.randint(2300, 2800)

        buraco = BuracoNegro(self.rect.centerx,self.rect.top - 120,alvo_x)
        self.grupo_projeteis.add(buraco)

    def encostar_no_player(self, player):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque >= 1000:
            player.levar_dano(1)
            self.ultimo_ataque = agora

    def update(self):
        self.rect.x += self.velocidade * self.direcao

        if abs(self.rect.centerx - self.x_inicial) >= self.alcance:
            self.direcao *= -1

        if self.direcao == 1:
            self.image = self.image_d
        else:
            self.image = self.image_e

        self.hitbox.center = self.rect.center

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_ataque >= self.cooldown_ataque:
            self.escolher_ataque()
            self.ultimo_ataque = agora
        
        if not pygame.mouse.get_pressed()[0]:
            self.tomou_dano = False

class ProjetilDrG(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()

        self.image = pygame.image.load("Assets/Sprites/Ataques/projetil_drg.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(x, y))

        self.hitbox = pygame.Rect(0, 0, 22, 12)
        self.hitbox.center = self.rect.center

        self.velocidade = 5 * direcao

    def update(self, *args):
        self.rect.x += self.velocidade
        self.hitbox.center = self.rect.center

        if self.rect.right < 0:
            self.kill()

class BuracoNegro(pygame.sprite.Sprite):
    def __init__(self, x, y, alvo_x):
        super().__init__()
        self.image = pygame.image.load("Assets/Sprites/Ataques/buraco_negro.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect(center=(x, y))

        self.vel_y = -15
        self.gravidade = 0.8
        self.alvo_x = alvo_x
        self.tempo_vida = pygame.time.get_ticks()
        self.delay_colisao = 400
        self.expandiu = False
        self.hitbox = pygame.Rect(0, 0, 60, 60)
        self.hitbox.center = self.rect.center
        self.estado = "voando"
        self.tempo_expandido = 0
        self.duracao_expandido = 1200
        self.pulso = 0
        self.vel_x = random.choice([-1, 1]) * random.randint(3, 6)

    def update(self, player):
        agora = pygame.time.get_ticks()
        self.hitbox.center = self.rect.center

        if self.estado == "voando":
            self.vel_y += self.gravidade
            self.rect.y += self.vel_y

            self.rect.x += self.vel_x

            if self.rect.bottom >= CHAO_CENARIO:
                self.rect.bottom = CHAO_CENARIO
                self.expandir()

        elif self.estado == "expandido":
            self.pulso += 1
            escala = 300 + int(10 * math.sin(self.pulso * 0.2))
            self.image = pygame.transform.scale(self.image, (escala, escala))
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox.center = self.rect.center
            dx = self.rect.centerx - player.rect.centerx
            dy = self.rect.centery - player.rect.centery

            distancia = math.hypot(dx, dy)
            raio = 260
            if distancia < raio and distancia != 0:
                forca = (raio - distancia) / raio

                puxao = 4 * forca

                player.rect.x += int(dx / distancia * puxao)
                player.rect.y += int(dy / distancia * puxao)
            if pygame.time.get_ticks() - self.tempo_expandido > self.duracao_expandido:
                self.kill()

    def expandir(self):
        self.estado = "expandido"
        self.tempo_expandido = pygame.time.get_ticks()

        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        self.hitbox = pygame.Rect(0, 0, 180, 180)
        self.hitbox.center = self.rect.center