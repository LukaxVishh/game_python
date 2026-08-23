import pygame
from ElementoJogo import ElementoJogo

class Nave(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=6, cor=(0, 255, 100)):
      
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
        tiro = pygame.Rect(
            self.rect.centerx - (largura_tiro // 2),
            self.rect.top - altura_tiro,
            largura_tiro,
            altura_tiro
        )
        self.tiros.append(tiro)

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
        

        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1
        

        if self.space_pressionado and self.cooldown_tiro == 0:
            self.atirar()
            self.cooldown_tiro = 5  
        
        self.atualizar_tiros()

    def desenhar(self, tela):

        pontos = [
            (self.rect.centerx, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom)
        ]
        pygame.draw.polygon(tela, self.cor, pontos)
        

        pygame.draw.polygon(tela, (100, 255, 150), pontos, 2)


        for tiro in self.tiros:
            pygame.draw.rect(tela, (255, 255, 100), tiro)  
            pygame.draw.rect(tela, (255, 255, 200), tiro, 1)  