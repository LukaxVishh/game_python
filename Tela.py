class Tela:
    FUNDO = (15, 15, 25)
    TEXTO = (255, 255, 255)
    DESTAQUE = (0, 255, 100)
    APAGADO = (140, 140, 155)
    ALERTA = (255, 100, 100)

    def __init__(self, jogo):
        self.jogo = jogo

    def ao_entrar(self):
        pass

    def processar_evento(self, evento):
        pass

    def atualizar(self):
        pass

    def desenhar(self, superficie):
        raise NotImplementedError

    def pintar_fundo(self, superficie):
        self.jogo.fundo.desenhar(superficie)

    def escrever(self, superficie, texto, tamanho, y, cor=None, x=None):
        render = self.jogo.fonte(tamanho).render(texto, True, cor or self.TEXTO)
        if x is None:
            x = self.jogo.largura // 2 - render.get_width() // 2
        superficie.blit(render, (x, y))
        return render
