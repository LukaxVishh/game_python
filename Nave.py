import os

import pygame
from ElementoJogo import ElementoJogo

class Nave(ElementoJogo):
    PASTA_NAVES = os.path.join(os.path.dirname(__file__), "assets", "naves")
    SPRITE_PADRAO = "ship_F.png"
    _cache_sprites = {}

    def __init__(self, largura_tela, altura_tela, velocidade=6, cor=(0, 255, 100), sprite=None):
        super().__init__(
            x=largura_tela // 2 - 20,
            y=altura_tela - 60,
            largura=40,
            altura=40,
            cor=cor,
            velocidade=velocidade
        )
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.vel_x = 0
        self.vel_y = 0
        self.tiros = []
        self.space_pressionado = False
        self.cooldown_tiro = 0
        self.disparou = False
        self.boost_escudo = 0
        self.boost_tiro_duplo = 0
        self.sprite = sprite or self.SPRITE_PADRAO

    @classmethod
    def listar_sprites(cls):
        if not os.path.isdir(cls.PASTA_NAVES):
            return []
        return sorted(f for f in os.listdir(cls.PASTA_NAVES) if f.endswith(".png"))

    @classmethod
    def obter_sprite(cls, nome, tamanho=(40, 40)):
        chave = (nome, tamanho)
        if chave not in cls._cache_sprites:
            try:
                caminho = os.path.join(cls.PASTA_NAVES, nome)
                original = pygame.image.load(caminho).convert_alpha()
                cls._cache_sprites[chave] = pygame.transform.smoothscale(original, tamanho)
            except (pygame.error, OSError):
                cls._cache_sprites[chave] = None
        return cls._cache_sprites[chave]

    def processar_evento(self, evento):
        """Controla os eventos de teclado para movimentação e disparo."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self.vel_x = -self.velocidade
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self.vel_x = self.velocidade
            elif evento.key in (pygame.K_UP, pygame.K_w):
                self.vel_y = -self.velocidade
            elif evento.key in (pygame.K_DOWN, pygame.K_s):
                self.vel_y = self.velocidade
            elif evento.key == pygame.K_SPACE:
                self.space_pressionado = True

        elif evento.type == pygame.KEYUP:
            if evento.key in (pygame.K_LEFT, pygame.K_a) and self.vel_x < 0:
                self.vel_x = 0
            elif evento.key in (pygame.K_RIGHT, pygame.K_d) and self.vel_x > 0:
                self.vel_x = 0
            elif evento.key in (pygame.K_UP, pygame.K_w) and self.vel_y < 0:
                self.vel_y = 0
            elif evento.key in (pygame.K_DOWN, pygame.K_s) and self.vel_y > 0:
                self.vel_y = 0
            elif evento.key == pygame.K_SPACE:
                self.space_pressionado = False

    def mover_lateral(self):
        """Aplica o deslocamento horizontal e trava nas bordas da tela."""
        self.rect.x += self.vel_x

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.largura_tela:
            self.rect.right = self.largura_tela

    def mover_vertical(self):
        """Aplica o deslocamento vertical e trava nas bordas da tela."""
        self.rect.y += self.vel_y

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.altura_tela:
            self.rect.bottom = self.altura_tela

    def atirar(self):
        """Cria um tiro na posição da nave"""
        largura_tiro = 4
        altura_tiro = 10
        deslocamentos = (-10, 10) if self.boost_tiro_duplo > 0 else (0,)

        for deslocamento in deslocamentos:
            self.tiros.append(pygame.Rect(
                self.rect.centerx + deslocamento - (largura_tiro // 2),
                self.rect.top - altura_tiro,
                largura_tiro,
                altura_tiro
            ))
        self.disparou = True

    def ativar_boost(self, tipo, duracao):
        if tipo == "escudo":
            self.boost_escudo = duracao
        elif tipo == "tiro_duplo":
            self.boost_tiro_duplo = duracao

    def _atualizar_boosts(self):
        self.boost_escudo = max(0, self.boost_escudo - 1)
        self.boost_tiro_duplo = max(0, self.boost_tiro_duplo - 1)

    def atualizar_tiros(self):
        """Atualiza posição de todos os tiros"""
        velocidade_tiro = 10
        for tiro in self.tiros[:]:
            tiro.y -= velocidade_tiro
            if tiro.bottom < 0:
                self.tiros.remove(tiro)

    def atualizar(self):
        """Atualiza estado da nave"""
        self.mover_lateral()
        self.mover_vertical()
        self._atualizar_boosts()

        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

        if self.space_pressionado and self.cooldown_tiro == 0:
            self.atirar()
            self.cooldown_tiro = 5

        self.atualizar_tiros()

    def _desenhar_triangulo(self, tela):
        pontos = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(tela, self.cor, pontos)
        pygame.draw.polygon(tela, (100, 255, 150), pontos, 2)

    def desenhar(self, tela):
        imagem = self.obter_sprite(self.sprite, self.rect.size)
        if imagem is None:
            self._desenhar_triangulo(tela)
        else:
            tela.blit(imagem, self.rect)

        if self.boost_escudo > 0:
            espessura = 3 if self.boost_escudo > 60 else 1 + (self.boost_escudo // 10) % 2 * 2
            pygame.draw.circle(tela, (80, 220, 255), self.rect.center, 28, espessura)

        for tiro in self.tiros:
            pygame.draw.rect(tela, (255, 255, 100), tiro)
            pygame.draw.rect(tela, (255, 255, 200), tiro, 1)
