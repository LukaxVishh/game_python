import random

import pygame
from Asteroid import Asteroid
from Boost import Boost
from Nave import Nave
from Tela import Tela

class TelaJogo(Tela):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.pontos = 0
        self.vidas = 3
        self.contador_asteroides = 0
        self.explosoes = []
        self.asteroides = []
        self.boosts = []
        self.nave = self._nova_nave()
        self._gerar_asteroides_iniciais()

    def _nova_nave(self):
        return Nave(self.jogo.largura, self.jogo.altura, sprite=self.jogo.sprite_nave)

    @property
    def nivel(self):
        return 1 + self.pontos // 50

    def _gerar_asteroides_iniciais(self):
        for _ in range(1 + self.nivel):
            self.asteroides.append(Asteroid(self.jogo.largura, self.jogo.altura, self.nivel))

    def _adicionar_asteroid(self):
        self.contador_asteroides += 1

        intervalo = max(15, 60 - self.nivel * 8)
        chance = min(0.8, 0.3 + self.nivel * 0.1)

        if self.contador_asteroides > intervalo:
            if random.random() < chance:
                self.asteroides.append(Asteroid(self.jogo.largura, self.jogo.altura, self.nivel))
                self.contador_asteroides = 0

    def _adicionar_boost(self):
        if not self.boosts and random.random() < 0.004:
            self.boosts.append(Boost(self.jogo.largura, self.jogo.altura))

    def _coletar_boost(self, boost):
        self.jogo.audio.tocar("boost")
        if boost.tipo == "vida":
            self.vidas += 1
        else:
            self.nave.ativar_boost(boost.tipo, Boost.DURACAO)

    def _criar_explosao(self, pos):
        """Cria efeito de explosão"""
        self.explosoes.append({"pos": pos, "tamanho": 30, "tempo": 10})

    def processar_evento(self, evento):
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para_menu()
            return
        self.nave.processar_evento(evento)

    def checar_colisoes(self):
        for tiro in self.nave.tiros[:]:
            for asteroide in self.asteroides[:]:
                if tiro.colliderect(asteroide.rect):
                    if tiro in self.nave.tiros:
                        self.nave.tiros.remove(tiro)
                    self.asteroides.remove(asteroide)
                    self.pontos += 10
                    self._criar_explosao(asteroide.rect.center)
                    self.jogo.audio.tocar("explosao")
                    break

        for asteroide in self.asteroides[:]:
            if self.nave.rect.colliderect(asteroide.rect):
                self.asteroides.remove(asteroide)
                self._criar_explosao(self.nave.rect.center)

                if self.nave.boost_escudo > 0:
                    self.jogo.audio.tocar("explosao")
                    continue

                self.vidas -= 1

                if self.vidas <= 0:
                    self.jogo.audio.tocar("game_over")
                    self.jogo.ir_para_game_over(self.pontos, self.nivel)
                    return
                self.jogo.audio.tocar("dano")
                self.nave = self._nova_nave()

    def atualizar(self):
        self.jogo.fundo.fator = min(1.0 + self.nivel * 0.3, 4.0)
        self.nave.atualizar()

        if self.nave.disparou:
            self.nave.disparou = False
            self.jogo.audio.tocar("tiro")

        for asteroide in self.asteroides[:]:
            asteroide.mover()
            if asteroide.saiu_da_tela():
                self.asteroides.remove(asteroide)

        for boost in self.boosts[:]:
            boost.mover()
            if boost.saiu_da_tela():
                self.boosts.remove(boost)
            elif boost.rect.colliderect(self.nave.rect):
                self._coletar_boost(boost)
                self.boosts.remove(boost)

        self._adicionar_asteroid()
        self._adicionar_boost()

        for explosao in self.explosoes[:]:
            explosao["tempo"] -= 1
            explosao["tamanho"] -= 3
            if explosao["tempo"] <= 0:
                self.explosoes.remove(explosao)

        self.checar_colisoes()

    def desenhar(self, superficie):
        self.pintar_fundo(superficie)
        self.nave.desenhar(superficie)

        for asteroide in self.asteroides:
            asteroide.desenhar(superficie)

        for boost in self.boosts:
            boost.desenhar(superficie)

        for explosao in self.explosoes:
            pygame.draw.circle(superficie, (255, 165, 0), explosao["pos"], int(explosao["tamanho"]))
            pygame.draw.circle(superficie, (255, 255, 0), explosao["pos"], int(explosao["tamanho"] * 0.6))

        self.escrever(superficie, f"Pontos: {self.pontos}", 36, 10, self.TEXTO, x=10)
        self.escrever(superficie, f"Vidas: {self.vidas}", 36, 10, self.ALERTA, x=self.jogo.largura - 200)
        self.escrever(superficie, f"Nivel: {self.nivel}", 28, 10, (100, 200, 255))

        ativos = []
        if self.nave.boost_escudo > 0:
            ativos.append(("escudo", self.nave.boost_escudo, (80, 220, 255)))
        if self.nave.boost_tiro_duplo > 0:
            ativos.append(("tiro duplo", self.nave.boost_tiro_duplo, (255, 180, 40)))
        for i, (nome, restante, cor) in enumerate(ativos):
            texto = f"{nome}: {restante // 60 + 1}s"
            self.escrever(superficie, texto, 24, 44 + i * 24, cor, x=10)
