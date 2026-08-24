import random
import pygame


class Boost:
    CORES = {"escudo": (80, 220, 255), "tiro_duplo": (255, 180, 40)}

    def __init__(self, largura_tela, tipo=None):
        self.tipo = tipo or random.choice(tuple(self.CORES))
        self.rect = pygame.Rect(0, -30, 30, 30)
        self.rect.centerx = random.randint(15, largura_tela - 15)
        self.velocidade = 3

    def mover(self):
        self.rect.y += self.velocidade

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.CORES[self.tipo], self.rect.center, 15)
        pygame.draw.circle(tela, (255, 255, 255), self.rect.center, 15, 2)
        fonte = pygame.font.Font(None, 23)
        texto = fonte.render("S" if self.tipo == "escudo" else "2x", True, (255, 255, 255))
        tela.blit(texto, texto.get_rect(center=self.rect.center))
