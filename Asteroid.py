import math
import os
import random

import pygame

from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):
    PASTA_SPRITES = os.path.join(os.path.dirname(__file__), "assets", "asteroides")
    PALETA_CORES = [
        (120, 120, 120),
        (150, 140, 130),
        (100, 90, 80),
        (170, 160, 150),
        (90, 90, 95),
    ]
    _cache_sprites = {}
    _nomes_sprites = None

    def __init__(self, largura_tela, altura_tela, nivel=1):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.nivel = nivel
        self.raio = 20

        super().__init__(
            x=0,
            y=0,
            largura=self.raio * 2,
            altura=self.raio * 2,
            cor=random.choice(self.PALETA_CORES),
            velocidade=1
        )
        self.iniciar_status()

    @classmethod
    def listar_sprites(cls):
        if cls._nomes_sprites is None:
            if os.path.isdir(cls.PASTA_SPRITES):
                cls._nomes_sprites = sorted(
                    f for f in os.listdir(cls.PASTA_SPRITES) if f.endswith(".png")
                )
            else:
                cls._nomes_sprites = []
        return cls._nomes_sprites

    @classmethod
    def obter_sprite(cls, nome, tamanho):
        chave = (nome, tamanho)
        if chave not in cls._cache_sprites:
            try:
                caminho = os.path.join(cls.PASTA_SPRITES, nome)
                original = pygame.image.load(caminho).convert_alpha()
                cls._cache_sprites[chave] = pygame.transform.smoothscale(original, tamanho)
            except (pygame.error, OSError):
                cls._cache_sprites[chave] = None
        return cls._cache_sprites[chave]

    def iniciar_status(self):
        self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
        self.rect.y = random.randint(-150, -50)

        minima = min(3 + self.nivel, 10)
        self.velocidade = random.randint(minima, min(minima + 4, 14))
        self.vel_x = random.randint(-2, 2)

        self.cor = random.choice(self.PALETA_CORES)

        disponiveis = self.listar_sprites()
        self.sprite = random.choice(disponiveis) if disponiveis else None

        self._gerar_forma_irregular()
        self._gerar_crateras()

    def _gerar_forma_irregular(self, num_vertices=10, variacao=0.35):
        self.pontos_relativos = []
        for i in range(num_vertices):
            angulo = (2 * math.pi / num_vertices) * i
            r = self.raio * random.uniform(1 - variacao, 1 + variacao)
            self.pontos_relativos.append((math.cos(angulo) * r, math.sin(angulo) * r))

    def _gerar_crateras(self):
        self.crateras = []
        for _ in range(random.randint(2, 4)):
            distancia = random.uniform(0, self.raio * 0.5)
            angulo = random.uniform(0, 2 * math.pi)
            raio_cratera = random.uniform(self.raio * 0.12, self.raio * 0.28)
            self.crateras.append(
                (math.cos(angulo) * distancia, math.sin(angulo) * distancia, raio_cratera)
            )

    def saiu_da_tela(self):
        return self.rect.top > self.altura_tela

    def mover(self):
        self.rect.y += self.velocidade
        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x *= -1
        elif self.rect.right > self.largura_tela:
            self.rect.right = self.largura_tela
            self.vel_x *= -1

    def _desenhar_poligono(self, tela):
        centro = self.rect.center
        pontos_absolutos = [
            (centro[0] + dx, centro[1] + dy) for dx, dy in self.pontos_relativos
        ]
        pygame.draw.polygon(tela, self.cor, pontos_absolutos)

        cor_cratera = tuple(max(0, c - 40) for c in self.cor)
        for dx, dy, raio_cratera in self.crateras:
            pygame.draw.circle(
                tela,
                cor_cratera,
                (int(centro[0] + dx), int(centro[1] + dy)),
                int(raio_cratera)
            )

    def desenhar(self, tela):
        imagem = self.obter_sprite(self.sprite, self.rect.size) if self.sprite else None
        if imagem is None:
            self._desenhar_poligono(tela)
        else:
            tela.blit(imagem, self.rect)
