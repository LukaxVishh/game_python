import random

class Fundo:
    COR_CEU = (15, 15, 25)
    CAMADAS = (
        {"quantidade": 70, "velocidade": 0.35, "brilho": (45, 70), "tamanho": 1},
        {"quantidade": 45, "velocidade": 0.85, "brilho": (75, 105), "tamanho": 1},
        {"quantidade": 25, "velocidade": 1.7, "brilho": (110, 130), "tamanho": 2},
    )

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.fator = 1.0
        self.estrelas = [
            self._nova_estrela(camada, random.uniform(0, altura))
            for camada in self.CAMADAS
            for _ in range(camada["quantidade"])
        ]

    def _nova_estrela(self, camada, y):
        brilho = random.randint(*camada["brilho"])
        return {
            "x": random.uniform(0, self.largura),
            "y": y,
            "velocidade": camada["velocidade"] * random.uniform(0.8, 1.2),
            "cor": (int(brilho * 0.75), int(brilho * 0.85), brilho),
            "tamanho": camada["tamanho"],
        }

    def atualizar(self):
        for estrela in self.estrelas:
            estrela["y"] += estrela["velocidade"] * self.fator
            if estrela["y"] > self.altura:
                estrela["y"] = -estrela["tamanho"]
                estrela["x"] = random.uniform(0, self.largura)

    def desenhar(self, superficie):
        superficie.fill(self.COR_CEU)
        for estrela in self.estrelas:
            lado = estrela["tamanho"]
            superficie.fill(estrela["cor"], (int(estrela["x"]), int(estrela["y"]), lado, lado))
