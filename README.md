# Entregável 2 — Anotações de Imagens com OpenCV

**Nome:** Mônica Amaral

## Objetivo

O objetivo deste projeto é criar um programa em Python que leia anotações de um arquivo CSV e desenhe caixas de identificação (bounding boxes) em imagens utilizando a biblioteca OpenCV.

Foram utilizadas 10 imagens e 581 anotações disponibilizadas no material complementar da atividade.

## Bibliotecas utilizadas

- Python 3
- OpenCV (cv2)
- CSV para leitura das anotações
- Pathlib para trabalhar com os caminhos dos arquivos

## Organização do projeto

- `src/main.py`: responsável pela execução do programa e pela visualização das imagens.
- `src/modelos.py`: contém as classes utilizadas.
- `src/arquivos.py`: faz a leitura e organização das anotações.
- `dados/`: contém os arquivos CSV.
- `imagens/`: contém as imagens originais.
- `resultados/`: contém as imagens com as caixas desenhadas.
- `evidencias/`: contém as capturas de tela da execução.

## Como executar

Primeiro, instale as dependências:

```bash
python -m pip install -r requirements.txt
```

Depois, execute o programa:

```bash
python src/main.py
```

## Funcionamento

O programa lê o arquivo CSV com as coordenadas e associa as anotações às imagens correspondentes.

As caixas são desenhadas com duas cores:

- Verde: classe 0
- Azul: classe 1

Durante a visualização, é possível utilizar:

- **Espaço:** passar para a próxima imagem.
- **Q:** encerrar o programa.
- **Outras teclas:** permanecer na imagem atual.

As imagens anotadas são salvas na pasta `resultados`, sem modificar os arquivos originais.

## Classes utilizadas

**Deteccao:** armazena as coordenadas e a identificação da classe de cada caixa, além de possuir um método para desenhá-la.

**ImagemAnotada:** armazena a imagem e suas detecções, permitindo adicionar e desenhar as caixas correspondentes.

## Resultado

O programa foi testado com as 10 imagens fornecidas, gerando os arquivos anotados na pasta `resultados`.

As capturas da execução estão disponíveis na pasta `evidencias`.
