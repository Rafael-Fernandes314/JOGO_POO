import pygame
from inventario import artefatos_coletados

chave = pygame.image.load("Assets\Sprites\Arterfatos\chave.png")
chave = pygame.transform.scale(chave, (30, 64))

orbe = pygame.image.load("Assets\Sprites\Arterfatos\orbe.png")
orbe = pygame.transform.scale(orbe, (64, 64))

espada = pygame.image.load("Assets\Sprites\Arterfatos\espada.png")
espada = pygame.transform.scale(espada, (64, 64))

escudo = pygame.image.load("Assets\Sprites\Arterfatos\escudo.png")
escudo = pygame.transform.scale(escudo, (64, 64))

anel = pygame.image.load("Assets/Sprites/Arterfatos/anel.png")
anel = pygame.transform.scale(anel, (64, 64))

def desenhar_hud(tela, largura, altura):
    pos_x = largura - 80
    pos_y = altura - 640

    # ordem de exibição
    if artefatos_coletados["chave"]:
        tela.blit(chave, (pos_x, pos_y))
        pos_x -= 80

    if artefatos_coletados["orbe"]:
        tela.blit(orbe, (pos_x, pos_y))
        pos_x -= 80

    if artefatos_coletados["espada"]:
        tela.blit(espada, (pos_x, pos_y))
        pos_x -= 80

    if artefatos_coletados["escudo"]:
        tela.blit(escudo, (pos_x, pos_y))
        pos_x -= 80

    if artefatos_coletados["anel"]:
        tela.blit(anel, (pos_x, pos_y))
        pos_x -= 80