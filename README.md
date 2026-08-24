# Space Shooter

Primeiro trabalho de Tópicos de Software: um jogo em Python com pygame, onde a
nave precisa destruir os asteroides que caem antes que eles a atinjam.

## Como rodar

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python Main.py
```

## Controles

| Tecla | Ação |
|---|---|
| Setas ou `WASD` | Mover a nave |
| `SPACE` | Atirar (segure para tiro contínuo) |
| `SPACE` no menu | Iniciar a partida |
| `ESC` | Sair |

## Regras

- Cada asteroide destruído vale **10 pontos**.
- A nave começa com **3 vidas**; colidir com um asteroide custa uma vida.
- A cada **50 pontos** o nível sobe: os asteroides passam a cair mais rápido e
  a aparecer com mais frequência.
- Sem vidas, o jogo vai para a tela de *game over*.

## Organização do código

| Arquivo | Responsabilidade |
|---|---|
| `ElementoJogo.py` | Classe base com `rect`, `cor`, `velocidade` e os métodos `mover()` e `desenhar()` |
| `Nave.py` | Nave do jogador: movimentação nos dois eixos, tiros e cooldown de disparo |
| `Asteroid.py` | Asteroide: sorteio de posição/velocidade e desenho como rocha irregular com crateras |
| `Main.py` | Classe `Jogo`: game loop, estados (menu / jogando / game over), colisões, explosões e HUD |

As duas subclasses sobrescrevem `mover()` e `desenhar()` da classe base — é o
ponto de **herança e polimorfismo** exigido pelo trabalho.
