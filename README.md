# Entregável 2 — Anotações de imagens com OpenCV

**Autora:** Mônica Amaral  
**Entrega:** 12 de outubro de 2026  
**Linguagem:** Python 3

## Objetivo

Desenvolver um visualizador de imagens anotadas utilizando **OpenCV** e leitura de arquivos **CSV**. O programa lê as coordenadas das bounding boxes fornecidas, transforma as 581 anotações em objetos, agrupa-as por imagem e desenha as caixas nas 10 fotografias originais. Os JPGs da pasta `imagens/` não são modificados.

## Organização

```text
entregavel-2-monica-amaral/
├── src/
│   ├── main.py          # Execução e visualização interativa
│   ├── modelos.py       # Classes Deteccao e ImagemAnotada
│   └── arquivos.py      # Leitura e agrupamento do CSV
├── dados/
│   ├── anotacoes.csv
│   └── mapeamento_imagens.csv
├── imagens/              # Dez imagens originais (JPG)
├── resultados/           # Dez imagens anotadas (JPG)
├── evidencias/
│   ├── terminal.png
│   └── visualizador.png
├── requirements.txt
├── .gitignore
└── README.md
```

## Dependências

- Python 3.9 ou superior (recomendado)
- Pacote `opencv-python` (instalado por `requirements.txt`)
- Módulos nativos `csv`, `pathlib`, `dataclasses` e `argparse`
- Ambiente com suporte a janelas para o modo interativo

## Como executar no Windows (PowerShell)

Abra o terminal na pasta principal deste projeto e execute:

```powershell
py -m pip install -r requirements.txt
python src/main.py
```

Caso o comando `python` não funcione, use `py src/main.py`.

## Como executar no Linux

```bash
python3 -m pip install -r requirements.txt
python3 src/main.py
```

## Teclas do visualizador

- **Espaço:** avança para a próxima imagem.
- **Q:** encerra a execução.
- **Qualquer outra tecla:** mantém a imagem atual.

Cada imagem é salva na pasta `resultados/` **antes** de aguardar a tecla. Para processar todas, pressione Espaço até o fim. O terminal informa o nome e o total de caixas desenhadas em cada imagem. O programa preserva as dimensões originais dos arquivos salvos; apenas a versão exibida em tela pode ser redimensionada. A legenda identifica a classe 0 (verde) e a classe 1 (azul).

Para gerar as dez saídas automaticamente, sem precisar abrir janelas, também existe o modo opcional:

```powershell
python src/main.py --sem-janela
```

O modo interativo (`python src/main.py`) é o exigido para testar as teclas e registrar a evidência do visualizador.

## Classes e leitura dos dados

- `Deteccao` armazena `classe_id`, `x_min`, `y_min`, `x_max` e `y_max`. O método `desenhar` valida as coordenadas da caixa e chama `cv2.rectangle`.
- `ImagemAnotada` armazena o caminho da imagem e uma lista de objetos `Deteccao`. O método `adicionar_deteccao` adiciona caixas à lista; `gerar_imagem_anotada` lê o JPG, cria uma cópia e desenha todas as detecções nessa cópia.
- `carregar_anotacoes`, em `src/arquivos.py`, lê `dados/anotacoes.csv` com `csv.DictReader`, converte os valores numéricos para inteiros e agrupa as detecções pelo nome da imagem, independentemente da ordem das linhas.
- `main`, em `src/main.py`, coordena a leitura, a ordenação alfabética dos JPGs, a gravação das imagens e a navegação interativa.

Os campos `x` e `y` do CSV representam coordenadas em pixels da imagem original, respectivamente horizontal e vertical. As classes têm apenas identificadores `0` e `1`; o material não especifica seus significados semânticos.

## Validação

Os dados fornecidos contêm **581 bounding boxes** em **10 imagens**. Para cada caixa, o programa verifica `0 ≤ x_min < x_max < largura` e `0 ≤ y_min < y_max < altura`, além de conferir a leitura do CSV, a existência das imagens e o sucesso ao salvar os resultados. Falhas geram mensagem de erro no terminal.

## Evidências de execução

A pasta `evidencias/` contém a captura do terminal (com `pwd`, `ls` e o comando de execução visíveis) e uma captura do visualizador exibindo uma imagem com caixas e a legenda.

## Documentação consultada

- [csv — documentação do Python](https://docs.python.org/3/library/csv.html)
- [OpenCV — desenho de figuras](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html)
- [OpenCV — interface e teclado](https://docs.opencv.org/4.x/d7/dfc/group__highgui.html)
