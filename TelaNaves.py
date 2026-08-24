import pygame
from Nave import Nave
from Tela import Tela

class TelaNaves(Tela):
    COLUNAS = 4
    CELULA = 104
    TAMANHO_PREVIA = (64, 64)

    def __init__(self, jogo):
        super().__init__(jogo)
        self.sprites = Nave.listar_sprites()
        self.indice = 0
        if self.jogo.sprite_nave in self.sprites:
            self.indice = self.sprites.index(self.jogo.sprite_nave)

    def processar_evento(self, evento):
        if evento.type != pygame.KEYDOWN or not self.sprites:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.jogo.ir_para_menu()
            return

        if evento.key in (pygame.K_LEFT, pygame.K_a):
            self.indice = (self.indice - 1) % len(self.sprites)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_RIGHT, pygame.K_d):
            self.indice = (self.indice + 1) % len(self.sprites)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_UP, pygame.K_w):
            self.indice = (self.indice - self.COLUNAS) % len(self.sprites)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_DOWN, pygame.K_s):
            self.indice = (self.indice + self.COLUNAS) % len(self.sprites)
            self.jogo.audio.tocar("navegar")
        elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
            self.jogo.sprite_nave = self.sprites[self.indice]
            self.jogo.audio.tocar("confirmar")
            self.jogo.ir_para_menu()
        elif evento.key == pygame.K_ESCAPE:
            self.jogo.audio.tocar("voltar")
            self.jogo.ir_para_menu()

    def desenhar(self, superficie):
        self.pintar_fundo(superficie)
        self.escrever(superficie, "ESCOLHA SUA NAVE", 52, 30, self.DESTAQUE)

        if not self.sprites:
            self.escrever(superficie, "Nenhuma nave encontrada em assets/naves", 26, 260, self.ALERTA)
            self.escrever(superficie, "ESC para voltar", 22, 550, self.APAGADO)
            return

        linhas = (len(self.sprites) + self.COLUNAS - 1) // self.COLUNAS
        origem_x = self.jogo.largura // 2 - (self.COLUNAS * self.CELULA) // 2
        origem_y = 92

        for i, nome in enumerate(self.sprites):
            coluna = i % self.COLUNAS
            linha = i // self.COLUNAS
            x = origem_x + coluna * self.CELULA
            y = origem_y + linha * self.CELULA
            caixa = pygame.Rect(x, y, self.CELULA - 10, self.CELULA - 10)

            if i == self.indice:
                pygame.draw.rect(superficie, self.DESTAQUE, caixa, 2)
            elif nome == self.jogo.sprite_nave:
                pygame.draw.rect(superficie, self.APAGADO, caixa, 1)

            imagem = Nave.obter_sprite(nome, self.TAMANHO_PREVIA)
            if imagem is not None:
                superficie.blit(imagem, imagem.get_rect(center=caixa.center))

        atual = self.sprites[self.indice]
        rodape = origem_y + linhas * self.CELULA + 6
        marcador = "  (em uso)" if atual == self.jogo.sprite_nave else ""
        self.escrever(superficie, atual[:-4] + marcador, 30, rodape, self.TEXTO)
        self.escrever(superficie, "Setas para navegar | ENTER para escolher | ESC para voltar", 22, 566, self.APAGADO)
