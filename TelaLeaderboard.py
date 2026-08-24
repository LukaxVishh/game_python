import pygame
from Tela import Tela

class TelaLeaderboard(Tela):
    def __init__(self, jogo, destaque=None):
        super().__init__(jogo)
        self.destaque = destaque

    def processar_evento(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self.jogo.audio.tocar("voltar")
                self.jogo.ir_para_menu()

    def desenhar(self, superficie):
        self.pintar_fundo(superficie)
        self.escrever(superficie, "MELHORES RUNS", 56, 50, self.DESTAQUE)

        registros = self.jogo.leaderboard.registros
        if not registros:
            self.escrever(superficie, "Nenhuma partida registrada ainda", 30, 260, self.APAGADO)
            self.escrever(superficie, "ESC para voltar", 22, 540, self.APAGADO)
            return

        margem = 180
        self.escrever(superficie, "#", 26, 140, self.APAGADO, x=margem)
        self.escrever(superficie, "NOME", 26, 140, self.APAGADO, x=margem + 60)
        self.escrever(superficie, "PONTOS", 26, 140, self.APAGADO, x=margem + 200)
        self.escrever(superficie, "NIVEL", 26, 140, self.APAGADO, x=margem + 340)

        for i, registro in enumerate(registros):
            cor = self.DESTAQUE if i == self.destaque else self.TEXTO
            y = 180 + i * 34
            self.escrever(superficie, f"{i + 1}", 30, y, cor, x=margem)
            self.escrever(superficie, registro["nome"], 30, y, cor, x=margem + 60)
            self.escrever(superficie, str(registro["pontos"]), 30, y, cor, x=margem + 200)
            self.escrever(superficie, str(registro["nivel"]), 30, y, cor, x=margem + 340)

        self.escrever(superficie, "ESC para voltar", 22, 550, self.APAGADO)
