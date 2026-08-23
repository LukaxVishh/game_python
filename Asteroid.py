import random
import pygame
from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):
    def __init__(self, largura_tela, altura_tela, velocidade=None, cor=None, tamanho=1.0):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tamanho = tamanho  # Fator de tamanho (1.0 = normal, 0.5 = pequeno, etc)
        self.raio = int(20 * self.tamanho)
        
        # Varia a cor um pouco para diversidade visual
        if cor is None:
            cor = (random.randint(150, 220), random.randint(20, 80), random.randint(20, 80))
        
        # Velocidade aumenta com o tamanho
        if velocidade is None:
            velocidade = random.randint(int(3 * self.tamanho), int(7 * self.tamanho))

        super().__init__(
            x=0,
            y=0,
            largura=self.raio * 2,
            altura=self.raio * 2,
            cor=cor,
            velocidade=int(velocidade)
        )
        self.iniciar_status()
        
        # Movimento horizontal opcional
        self.vel_x = random.randint(-2, 2)

    def iniciar_status(self):
        """Inicializa posição e velocidade do asteroide"""
        self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        self.velocidade = random.randint(int(2 * self.tamanho), int(6 * self.tamanho))
        self.vel_x = random.randint(-2, 2)

    def mover(self):
        """Move o asteroide em X e Y, com possibilidade de ricochete nas laterais"""
        self.rect.y += self.velocidade
        self.rect.x += self.vel_x
        
        # Ricochete nas laterais
        if self.rect.left < 0 or self.rect.right > self.largura_tela:
            self.vel_x *= -1

    def desenhar(self, tela):
        """Desenha o asteroide como círculo com variação visual"""
        # Círculo principal
        pygame.draw.circle(tela, self.cor, self.rect.center, self.raio)
        
        # Contorno para melhor visual
        pygame.draw.circle(tela, (min(255, self.cor[0] + 50), 
                                  min(255, self.cor[1] + 50), 
                                  min(255, self.cor[2] + 50)), 
                          self.rect.center, self.raio, 2)