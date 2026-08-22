import random
import math
import pygame

from ElementoJogo import ElementoJogo


class Asteroid(ElementoJogo):

    # Paleta de tons possíveis para o asteroide (cinza/marrom, várias intensidades)
    PALETA_CORES = [
        (120, 120, 120),
        (150, 140, 130),
        (100, 90, 80),
        (170, 160, 150),
        (90, 90, 95),
    ]

    # Cores usadas nos estilhaços da explosão
    CORES_EXPLOSAO = [
        (255, 180, 60),
        (255, 100, 40),
        (200, 50, 30),
        (255, 220, 120),
    ]

    def __init__(self, largura_tela, altura_tela, velocidade=50, cor=(200, 50, 50)):
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.raio = 20

        super().__init__(
            x=0,
            y=0,
            largura=self.raio * 2,
            altura=self.raio * 2,
            cor=cor,
            velocidade=velocidade
        )

        # Estado da explosão
        self.esta_explodindo = False
        self.explosao_particulas = []
        self.explosao_duracao = 25   # frames até a explosão terminar
        self.explosao_frame_atual = 0

        self.iniciar_status()

    def iniciar_status(self):
        self.rect.x = random.randint(0, self.largura_tela - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        self.velocidade = random.randint(3, 7)

        # Sorteia uma nova cor base a cada vez que o asteroide "nasce"
        self.cor = random.choice(self.PALETA_CORES)

        # Gera o contorno irregular e as crateras uma única vez aqui,
        # para não recalcular a cada frame (senão o asteroide treme)
        self._gerar_forma_irregular()
        self._gerar_crateras()

        self.esta_explodindo = False
        self.explosao_particulas = []

    def _gerar_forma_irregular(self, num_vertices=10, variacao=0.35):
        """Cria os pontos (offsets relativos ao centro) do polígono irregular."""
        self.pontos_relativos = []
        for i in range(num_vertices):
            angulo = (2 * math.pi / num_vertices) * i
            fator = random.uniform(1 - variacao, 1 + variacao)
            r = self.raio * fator
            dx = math.cos(angulo) * r
            dy = math.sin(angulo) * r
            self.pontos_relativos.append((dx, dy))

    def _gerar_crateras(self, quantidade=None):
        """Cria crateras (offset relativo, raio) espalhadas dentro do asteroide."""
        if quantidade is None:
            quantidade = random.randint(2, 4)

        self.crateras = []
        for _ in range(quantidade):
            distancia = random.uniform(0, self.raio * 0.5)
            angulo = random.uniform(0, 2 * math.pi)
            dx = math.cos(angulo) * distancia
            dy = math.sin(angulo) * distancia
            raio_cratera = random.uniform(self.raio * 0.12, self.raio * 0.28)
            self.crateras.append((dx, dy, raio_cratera))

    def explodir(self):
        """Dispara a animação de explosão. Chame isso ao invés de iniciar_status()
        no momento em que o asteroide for destruído (ex: colisão com um tiro)."""
        self.esta_explodindo = True
        self.explosao_frame_atual = 0
        self.explosao_particulas = []

        num_particulas = 14
        for _ in range(num_particulas):
            angulo = random.uniform(0, 2 * math.pi)
            velocidade = random.uniform(2, 6)
            self.explosao_particulas.append({
                "x": 0.0,
                "y": 0.0,
                "vel_x": math.cos(angulo) * velocidade,
                "vel_y": math.sin(angulo) * velocidade,
                "raio": random.uniform(3, 7),
                "cor": random.choice(self.CORES_EXPLOSAO),
            })

    def _atualizar_explosao(self):
        self.explosao_frame_atual += 1
        for p in self.explosao_particulas:
            p["x"] += p["vel_x"]
            p["y"] += p["vel_y"]
            p["raio"] = max(0.0, p["raio"] - 0.15)

        # Quando a animação termina, o asteroide "some" e reaparece no topo
        if self.explosao_frame_atual >= self.explosao_duracao:
            self.iniciar_status()

    def mover(self):
        self.rect.y += self.velocidade
        # Reinicia no topo caso passe reto pelo fundo da tela
        if self.rect.top > self.altura_tela:
            self.iniciar_status()

    def atualizar(self):
        """Use este método no lugar de mover() no game loop: ele decide
        sozinho se o asteroide deve cair normalmente ou tocar a explosão."""
        if self.esta_explodindo:
            self._atualizar_explosao()
        else:
            self.mover()

    def desenhar(self, tela):
        centro = self.rect.center

        if self.esta_explodindo:
            # Enquanto explode, o corpo do asteroide não é mais desenhado —
            # só os estilhaços se espalhando e encolhendo
            for p in self.explosao_particulas:
                if p["raio"] <= 0:
                    continue
                pos = (int(centro[0] + p["x"]), int(centro[1] + p["y"]))
                pygame.draw.circle(tela, p["cor"], pos, int(p["raio"]))
            return

        # Polígono irregular (corpo do asteroide)
        pontos_absolutos = [
            (centro[0] + dx, centro[1] + dy)
            for dx, dy in self.pontos_relativos
        ]
        pygame.draw.polygon(tela, self.cor, pontos_absolutos)

        # Crateras: tom mais escuro que a cor base, desenhadas por cima
        cor_cratera = tuple(max(0, c - 40) for c in self.cor)
        for dx, dy, raio_cratera in self.crateras:
            pos = (int(centro[0] + dx), int(centro[1] + dy))
            pygame.draw.circle(tela, cor_cratera, pos, int(raio_cratera))