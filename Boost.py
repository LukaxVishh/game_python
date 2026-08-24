import random

import pygame

from ElementoJogo import ElementoJogo


class Boost(ElementoJogo):
    RAIO = 15
    DURACAO = 300
    TIPOS = {
        "escudo": {"cor": (80, 220, 255), "rotulo": "S"},
        "tiro_duplo": {"cor": (255, 180, 40), "rotulo": "2x"},
        "vida": {"cor": (255, 100, 140), "rotulo": "+1"},
    }
    _fonte = None

    def __init__(self, largura_tela, altura_tela, tipo=None):
        self.tipo = tipo or random.choice(tuple(self.TIPOS))
        config = self.TIPOS[self.tipo]

        super().__init__(
            x=random.randint(0, largura_tela - self.RAIO * 2),
            y=-self.RAIO * 2,
            largura=self.RAIO * 2,
            altura=self.RAIO * 2,
            cor=config["cor"],
            velocidade=3
        )
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.rotulo = config["rotulo"]
        self.quadros = 0

    @classmethod
    def fonte(cls):
        if cls._fonte is None:
            cls._fonte = pygame.font.Font(None, 23)
        return cls._fonte

    def saiu_da_tela(self):
        return self.rect.top > self.altura_tela

    def mover(self):
        self.rect.y += self.velocidade
        self.quadros += 1

    def desenhar(self, tela):
        centro = self.rect.center
        pulso = 2 + int(2 * abs(((self.quadros % 60) / 30) - 1))

        pygame.draw.circle(tela, self.cor, centro, self.RAIO)
        pygame.draw.circle(tela, (255, 255, 255), centro, self.RAIO + pulso, 2)

        texto = self.fonte().render(self.rotulo, True, (20, 20, 30))
        tela.blit(texto, texto.get_rect(center=centro))
