import pygame
from Tela import Tela

class TelaGameOver(Tela):
    LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, jogo, pontos, nivel):
        super().__init__(jogo)
        self.pontos = pontos
        self.nivel = nivel
        self.registrando = jogo.leaderboard.entra_no_placar(pontos)
        self.posicao = jogo.leaderboard.posicao_de(pontos)
        self.iniciais = [0, 0, 0]
        self.slot = 0

    def ao_entrar(self):
        if self.registrando:
            self.jogo.audio.tocar("recorde")

    def _nome(self):
        return "".join(self.LETRAS[i] for i in self.iniciais)

    def processar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        if not self.registrando:
            if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_ESCAPE):
                self.jogo.ir_para_menu()
            return

        if evento.key in (pygame.K_UP, pygame.K_w):
            self.iniciais[self.slot] = (self.iniciais[self.slot] - 1) % len(self.LETRAS)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_DOWN, pygame.K_s):
            self.iniciais[self.slot] = (self.iniciais[self.slot] + 1) % len(self.LETRAS)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_LEFT, pygame.K_a):
            self.slot = (self.slot - 1) % 3
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_RIGHT, pygame.K_d):
            self.slot = (self.slot + 1) % 3
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            self.jogo.audio.tocar("confirmar")
            self.jogo.leaderboard.registrar(self._nome(), self.pontos, self.nivel)
            self.jogo.ir_para_leaderboard(destaque=self.posicao - 1)
        elif evento.key == pygame.K_ESCAPE:
            self.jogo.ir_para_menu()

    def desenhar(self, superficie):
        self.pintar_fundo(superficie)
        self.escrever(superficie, "GAME OVER", 72, 60, self.ALERTA)
        self.escrever(superficie, f"Pontuacao: {self.pontos}", 48, 160, self.TEXTO)
        self.escrever(superficie, f"Nivel alcancado: {self.nivel}", 28, 215, self.APAGADO)

        if not self.registrando:
            self.escrever(superficie, "Sua pontuacao nao entrou no placar", 28, 320, self.APAGADO)
            self.escrever(superficie, "SPACE para voltar ao menu", 26, 500, self.APAGADO)
            return

        self.escrever(superficie, f"Novo recorde! {self.posicao}o lugar", 32, 290, self.DESTAQUE)
        self.escrever(superficie, "Digite suas iniciais", 26, 335, self.APAGADO)

        largura_slot = 60
        origem = self.jogo.largura // 2 - (3 * largura_slot) // 2
        for i, indice_letra in enumerate(self.iniciais):
            cor = self.DESTAQUE if i == self.slot else self.TEXTO
            x = origem + i * largura_slot
            self.escrever(superficie, self.LETRAS[indice_letra], 64, 380, cor, x=x + 12)
            if i == self.slot:
                pygame.draw.line(superficie, self.DESTAQUE, (x, 445), (x + 44, 445), 2)

        self.escrever(superficie, "Cima/Baixo muda a letra | Lados trocam de casa | ENTER confirma", 22, 520, self.APAGADO)
