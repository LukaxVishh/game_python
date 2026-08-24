import array
import os

import pygame

class Audio:
    PASTA = os.path.join(os.path.dirname(__file__), "assets", "sons")
    FADE = 0.03
    LIMIAR_SILENCIO = 0.02
    EFEITOS = {
        "tiro": ("laser1.ogg", 0.26, 0.18),
        "explosao": ("tone1.ogg", 0.16, 0.16),
        "dano": ("phaserDown3.ogg", 0.38, 0.40),
        "game_over": ("lowDown.ogg", 0.42, 0.80),
        "recorde": ("powerUp2.ogg", 0.50, 0.50),
        "navegar": ("click_002.ogg", 0.35, 0.20),
        "confirmar": ("confirmation_001.ogg", 0.45, 0.35),
        "voltar": ("back_001.ogg", 0.35, 0.30),
    }

    def __init__(self):
        self.disponivel = False
        self.mudo = False
        self.sons = {}
        self.canal_tiro = None
        self._iniciar()

    def _iniciar(self):
        if pygame.mixer.get_init() is None:
            try:
                pygame.mixer.init(44100, -16, 2, 512)
            except pygame.error:
                return
        self.disponivel = True
        pygame.mixer.set_num_channels(16)
        pygame.mixer.set_reserved(1)
        self.canal_tiro = pygame.mixer.Channel(0)

        for nome, (arquivo, volume, duracao) in self.EFEITOS.items():
            som = self._carregar(arquivo, volume, duracao)
            if som is not None:
                self.sons[nome] = som

    def _carregar(self, arquivo, volume, duracao):
        try:
            som = pygame.mixer.Sound(os.path.join(self.PASTA, arquivo))
        except (pygame.error, OSError):
            return None
        som = self._ajustar(som, duracao)
        som.set_volume(volume)
        return som

    def _ajustar(self, som, duracao):
        info = pygame.mixer.get_init()
        if info is None or info[1] != -16:
            return som
        frequencia, _, canais = info

        try:
            amostras = array.array("h")
            amostras.frombytes(som.get_raw())
        except ValueError:
            return som

        inicio = self._primeiro_som(amostras, canais)
        limite = inicio + int(duracao * frequencia) * canais
        recorte = amostras[inicio:limite]
        if not recorte:
            return som

        fade = int(self.FADE * frequencia) * canais
        inicio_fade = max(0, len(recorte) - fade)
        for i in range(inicio_fade, len(recorte)):
            recorte[i] = int(recorte[i] * (len(recorte) - i) / fade)

        try:
            return pygame.mixer.Sound(buffer=recorte.tobytes())
        except pygame.error:
            return som

    def _primeiro_som(self, amostras, canais):
        pico = max(max(amostras), abs(min(amostras)))
        if pico == 0:
            return 0
        limiar = pico * self.LIMIAR_SILENCIO
        for i, valor in enumerate(amostras):
            if abs(valor) >= limiar:
                return (i // canais) * canais
        return 0

    def tocar(self, nome):
        if not self.disponivel or self.mudo:
            return
        som = self.sons.get(nome)
        if som is None:
            return
        if nome == "tiro" and self.canal_tiro is not None:
            self.canal_tiro.play(som)
        else:
            som.play()

    def alternar_mudo(self):
        self.mudo = not self.mudo
        if self.mudo and self.disponivel:
            pygame.mixer.stop()
        return self.mudo
