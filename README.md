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

**Nos menus**

| Tecla | Ação |
|---|---|
| Setas | Navegar entre as opções |
| `ENTER` | Confirmar |
| `ESC` | Voltar (ou sair, no menu principal) |
| `M` | Liga e desliga o som (funciona em qualquer tela) |

**Durante a partida**

| Tecla | Ação |
|---|---|
| Setas ou `WASD` | Mover a nave |
| `SPACE` | Atirar (segure para tiro contínuo) |
| `ESC` | Voltar ao menu |

## Regras

- Cada asteroide destruído vale **10 pontos**.
- A nave começa com **3 vidas**; colidir com um asteroide custa uma vida.
- A cada **50 pontos** o nível sobe: os asteroides passam a cair mais rápido e
  a aparecer com mais frequência.
- Sem vidas, o jogo vai para a tela de *game over*.
- As 10 melhores partidas ficam salvas no `leaderboard.json`, identificadas por
  três iniciais no estilo arcade. O arquivo é local e não vai para o repositório.
- A nave pode ser trocada no menu **Naves**, entre as 16 disponíveis.
- O campo de estrelas ao fundo acelera conforme o nível sobe.
- O jogo roda normalmente em máquinas sem placa de som: nesse caso ele
  simplesmente fica mudo, sem erro.

## Organização do código

| Arquivo | Responsabilidade |
|---|---|
| `ElementoJogo.py` | Classe base dos objetos: `rect`, `cor`, `velocidade`, `mover()` e `desenhar()` |
| `Nave.py` | Nave do jogador: sprite, movimentação nos dois eixos, tiros e cooldown de disparo |
| `Asteroid.py` | Asteroide: sorteio de posição/velocidade e desenho como rocha irregular com crateras |
| `Audio.py` | Carrega, encurta e toca os efeitos sonoros |
| `Fundo.py` | Campo de estrelas com parallax, compartilhado por todas as telas |
| `Tela.py` | Classe base das telas: `processar_evento()`, `atualizar()` e `desenhar()` |
| `TelaMenu.py` | Menu principal navegável |
| `TelaNaves.py` | Grade de seleção da nave |
| `TelaLeaderboard.py` | Placar das 10 melhores partidas |
| `TelaJogo.py` | A partida em si: asteroides, colisões, explosões e HUD |
| `TelaGameOver.py` | Fim de jogo e entrada das iniciais |
| `Leaderboard.py` | Leitura e gravação do placar em JSON |
| `Main.py` | Classe `Jogo`: game loop e troca de telas |
| `assets/naves/` | Sprites das naves |
| `assets/sons/` | Efeitos sonoros |

O projeto usa **herança e polimorfismo** em dois eixos:

- `ElementoJogo` → `Nave` e `Asteroid`, que sobrescrevem `mover()` e `desenhar()`
- `Tela` → `TelaMenu`, `TelaNaves`, `TelaLeaderboard`, `TelaJogo` e `TelaGameOver`,
  que sobrescrevem `processar_evento()`, `atualizar()` e `desenhar()`

O game loop em `Main.py` não sabe qual tela está ativa: ele chama sempre os mesmos
três métodos, e cada subclasse responde do seu jeito.

## Créditos

Todos os assets são de [Kenney](https://kenney.nl) e estão sob licença
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/) (domínio público):

- Sprites das naves (`assets/naves/`): [Simple Space](https://kenney.nl/assets/simple-space)
- Efeitos do jogo (`assets/sons/`): [Digital Audio](https://kenney.nl/assets/digital-audio)
- Efeitos de menu (`assets/sons/`): [Interface Sounds](https://kenney.nl/assets/interface-sounds)
