import pygame
from Tela import Tela

class TelaMenu(Tela):
    ITENS = ("Iniciar", "Naves", "Leaderboard", "Sair")

    def __init__(self, jogo):
        super().__init__(jogo)
        self.indice = 0

    def processar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        if evento.key in (pygame.K_UP, pygame.K_w):
            self.indice = (self.indice - 1) % len(self.ITENS)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_DOWN, pygame.K_s):
            self.indice = (self.indice + 1) % len(self.ITENS)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.jogo.audio.tocar("confirmar")
            self._confirmar()
        elif evento.key == pygame.K_ESCAPE:
            self.jogo.sair()

    def _confirmar(self):
        escolha = self.ITENS[self.indice]
        if escolha == "Iniciar":
            self.jogo.ir_para_jogo()
        elif escolha == "Naves":
            self.jogo.ir_para_naves()
        elif escolha == "Leaderboard":
            self.jogo.ir_para_leaderboard()
        else:
            self.jogo.sair()

    def desenhar(self, superficie):
        self.pintar_fundo(superficie)
        self.escrever(superficie, "SPACE SHOOTER", 72, 80, self.DESTAQUE)

        recorde = self.jogo.leaderboard.melhor_pontuacao()
        if recorde:
            self.escrever(superficie, f"Recorde: {recorde}", 26, 160, self.APAGADO)

        for i, item in enumerate(self.ITENS):
            selecionado = i == self.indice
            cor = self.DESTAQUE if selecionado else self.TEXTO
            rotulo = f"> {item} <" if selecionado else item
            self.escrever(superficie, rotulo, 44, 240 + i * 60, cor)

        self.escrever(superficie, "Setas para navegar | ENTER para confirmar", 22, 528, self.APAGADO)
        estado_som = "som: desligado (M)" if self.jogo.audio.mudo else "som: ligado (M)"
        self.escrever(superficie, estado_som, 20, 556, self.APAGADO)
