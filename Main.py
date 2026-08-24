import pygame
from Audio import Audio
from Fundo import Fundo
from Leaderboard import Leaderboard
from Nave import Nave
from TelaGameOver import TelaGameOver
from TelaJogo import TelaJogo
from TelaLeaderboard import TelaLeaderboard
from TelaMenu import TelaMenu
from TelaNaves import TelaNaves

class Jogo:
    def __init__(self, largura=800, altura=600):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.superficie = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Space Shooter")

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.rodando = True

        self.audio = Audio()
        self.fundo = Fundo(self.largura, self.altura)
        self.leaderboard = Leaderboard()
        self.sprite_nave = Nave.SPRITE_PADRAO
        self._fontes = {}

        self.tela_atual = None
        self.ir_para_menu()

    def fonte(self, tamanho):
        if tamanho not in self._fontes:
            self._fontes[tamanho] = pygame.font.Font(None, tamanho)
        return self._fontes[tamanho]

    def trocar_tela(self, tela):
        self.fundo.fator = 1.0
        self.tela_atual = tela
        self.tela_atual.ao_entrar()

    def ir_para_menu(self):
        self.trocar_tela(TelaMenu(self))

    def ir_para_jogo(self):
        self.trocar_tela(TelaJogo(self))

    def ir_para_naves(self):
        self.trocar_tela(TelaNaves(self))

    def ir_para_leaderboard(self, destaque=None):
        self.trocar_tela(TelaLeaderboard(self, destaque))

    def ir_para_game_over(self, pontos, nivel):
        self.trocar_tela(TelaGameOver(self, pontos, nivel))

    def sair(self):
        self.rodando = False

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.sair()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_m:
                self.audio.alternar_mudo()
            else:
                self.tela_atual.processar_evento(evento)

    def executar(self):
        while self.rodando:
            self.clock.tick(self.fps)
            self.processar_eventos()
            self.tela_atual.atualizar()
            self.fundo.atualizar()
            self.tela_atual.desenhar(self.superficie)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
