import json
import os

class Leaderboard:
    CAMINHO = os.path.join(os.path.dirname(__file__), "leaderboard.json")
    LIMITE = 10

    def __init__(self, caminho=None):
        self.caminho = caminho or self.CAMINHO
        self.registros = self._carregar()

    def _carregar(self):
        try:
            with open(self.caminho, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except (OSError, ValueError):
            return []

        if not isinstance(dados, list):
            return []

        validos = []
        for item in dados:
            if isinstance(item, dict) and "nome" in item and "pontos" in item:
                validos.append({
                    "nome": str(item["nome"])[:3].upper(),
                    "pontos": int(item["pontos"]),
                    "nivel": int(item.get("nivel", 1)),
                })
        return self._ordenar(validos)

    def _ordenar(self, registros):
        return sorted(registros, key=lambda r: r["pontos"], reverse=True)[:self.LIMITE]

    def _salvar(self):
        try:
            with open(self.caminho, "w", encoding="utf-8") as arquivo:
                json.dump(self.registros, arquivo, indent=2)
            return True
        except OSError:
            return False

    def entra_no_placar(self, pontos):
        if pontos <= 0:
            return False
        if len(self.registros) < self.LIMITE:
            return True
        return pontos > self.registros[-1]["pontos"]

    def posicao_de(self, pontos):
        for indice, registro in enumerate(self.registros):
            if pontos > registro["pontos"]:
                return indice + 1
        return len(self.registros) + 1

    def registrar(self, nome, pontos, nivel):
        self.registros = self._ordenar(
            self.registros + [{"nome": nome[:3].upper(), "pontos": int(pontos), "nivel": int(nivel)}]
        )
        self._salvar()
        return self.registros

    def melhor_pontuacao(self):
        return self.registros[0]["pontos"] if self.registros else 0
