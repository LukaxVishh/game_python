import pygame
from Nave import Nave
from Asteroid import Asteroid
import random


class Jogo:
    def __init__(self, largura=800, altura=600):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Space Shooter - Melhora")

        self.clock = pygame.time.Clock()
        self.fps = 60
        self.pontos = 0
        self.vidas = 3
        self.contador_asteroides = 0
        self.explosoes = [] 
        

        self.estado = "menu" 
        

        self.nave = Nave(self.largura, self.altura)
        self.asteroides = []
        self._gerar_asteroides_iniciais()

    def _gerar_asteroides_iniciais(self):
        """Gera os asteroides iniciais baseado na pontuação"""
        quantidade = 1 + (self.pontos // 5) 
        for _ in range(quantidade):
            self.asteroides.append(Asteroid(self.largura, self.altura))

    def _adicionar_asteroid(self):
        """Adiciona um novo asteroide aleatoriamente"""
        self.contador_asteroides += 1
        if self.contador_asteroides > 60:  
            if random.random() < 0.3:
                self.asteroides.append(Asteroid(self.largura, self.altura))
                self.contador_asteroides = 0

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if self.estado == "menu":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.iniciar_jogo()
                    elif evento.key == pygame.K_ESCAPE:
                        return False
                        
            elif self.estado == "jogando":
                self.nave.processar_evento(evento)
                
            elif self.estado == "game_over":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        self.reiniciar()
                    elif evento.key == pygame.K_ESCAPE:
                        return False
        
        return True

    def iniciar_jogo(self):
        """Inicia o jogo"""
        self.estado = "jogando"
        self.pontos = 0
        self.vidas = 3
        self.nave = Nave(self.largura, self.altura)
        self.asteroides = []
        self._gerar_asteroides_iniciais()
        self.explosoes = []

    def reiniciar(self):
        """Reinicia o jogo após game over"""
        self.estado = "menu"
        self.pontos = 0
        self.vidas = 3
        self.nave = Nave(self.largura, self.altura)
        self.asteroides = []
        self.explosoes = []

    def checar_colisoes(self):

        for tiro in self.nave.tiros[:]:
            for asteroide in self.asteroides[:]:
                if tiro.colliderect(asteroide.rect):
                    if tiro in self.nave.tiros:
                        self.nave.tiros.remove(tiro)
                    self.asteroides.remove(asteroide)
                    self.pontos += 10
                    self._criar_explosao(asteroide.rect.center)
                    break


        for asteroide in self.asteroides[:]:
            if self.nave.rect.colliderect(asteroide.rect):
                self.vidas -= 1
                self.asteroides.remove(asteroide)
                self._criar_explosao(self.nave.rect.center)
                
                if self.vidas <= 0:
                    self.estado = "game_over"
                else:

                    self.nave = Nave(self.largura, self.altura)

    def _criar_explosao(self, pos):
        """Cria efeito de explosão"""
        self.explosoes.append({
            "pos": pos,
            "tamanho": 30,
            "tempo": 10
        })

    def atualizar(self):
        if self.estado != "jogando":
            return

        self.nave.atualizar()
        

        for asteroide in self.asteroides:
            asteroide.mover()
        

        self._adicionar_asteroid()
        

        for explosao in self.explosoes[:]:
            explosao["tempo"] -= 1
            explosao["tamanho"] -= 3
            if explosao["tempo"] <= 0:
                self.explosoes.remove(explosao)
        
        self.checar_colisoes()

    def desenhar_menu(self):
        """Desenha a tela de menu"""
        self.tela.fill((15, 15, 25))
        
        fonte_grande = pygame.font.Font(None, 72)
        fonte_media = pygame.font.Font(None, 36)
        fonte_pequena = pygame.font.Font(None, 24)
        
        titulo = fonte_grande.render("SPACE SHOOTER", True, (0, 255, 100))
        instrucao1 = fonte_media.render("Pressione SPACE para iniciar", True, (255, 255, 255))
        instrucao2 = fonte_pequena.render("ESC para sair", True, (200, 200, 200))
        controles = fonte_pequena.render("Setas/WASD para mover | SPACE para atirar", True, (200, 200, 200))
        
        self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 100))
        self.tela.blit(instrucao1, (self.largura // 2 - instrucao1.get_width() // 2, 250))
        self.tela.blit(controles, (self.largura // 2 - controles.get_width() // 2, 350))
        self.tela.blit(instrucao2, (self.largura // 2 - instrucao2.get_width() // 2, 500))
        
        pygame.display.flip()

    def desenhar_game_over(self):
        """Desenha a tela de game over"""
        self.tela.fill((15, 15, 25))
        
        fonte_grande = pygame.font.Font(None, 72)
        fonte_media = pygame.font.Font(None, 48)
        fonte_pequena = pygame.font.Font(None, 28)
        
        game_over_text = fonte_grande.render("GAME OVER", True, (255, 50, 50))
        pontos_text = fonte_media.render(f"Pontuação: {self.pontos}", True, (255, 255, 255))
        restart_text = fonte_pequena.render("Pressione SPACE para voltar ao menu", True, (200, 200, 200))
        
        self.tela.blit(game_over_text, (self.largura // 2 - game_over_text.get_width() // 2, 150))
        self.tela.blit(pontos_text, (self.largura // 2 - pontos_text.get_width() // 2, 300))
        self.tela.blit(restart_text, (self.largura // 2 - restart_text.get_width() // 2, 450))
        
        pygame.display.flip()

    def desenhar(self):
        if self.estado == "menu":
            self.desenhar_menu()
        elif self.estado == "jogando":
            self.desenhar_jogo()
        elif self.estado == "game_over":
            self.desenhar_game_over()

    def desenhar_jogo(self):
        """Desenha o jogo em andamento"""
        self.tela.fill((15, 15, 25))

        self.nave.desenhar(self.tela)
        

        for asteroide in self.asteroides:
            asteroide.desenhar(self.tela)


        for explosao in self.explosoes:
            pygame.draw.circle(self.tela, (255, 165, 0), explosao["pos"], int(explosao["tamanho"]))
            pygame.draw.circle(self.tela, (255, 255, 0), explosao["pos"], int(explosao["tamanho"] * 0.6))


        fonte = pygame.font.Font(None, 36)
        fonte_pequena = pygame.font.Font(None, 28)
        
        texto_pontos = fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        texto_vidas = fonte.render(f"Vidas: {self.vidas}", True, (255, 100, 100))
        nivel = fonte_pequena.render(f"Nível: {1 + self.pontos // 50}", True, (100, 200, 255))

        self.tela.blit(texto_pontos, (10, 10))
        self.tela.blit(texto_vidas, (self.largura - 200, 10))
        self.tela.blit(nivel, (self.largura // 2 - 50, 10))

        pygame.display.flip()

    def executar(self):
        rodando = True
        while rodando:
            self.clock.tick(self.fps)

            rodando = self.processar_eventos()
            self.atualizar()
            self.desenhar()

        pygame.quit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()