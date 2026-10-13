"""Leitura das anotações CSV e agrupamento por imagem."""

import csv
from pathlib import Path

from modelos import Deteccao, ImagemAnotada

CAMPOS_OBRIGATORIOS = {
    "imagem", "classe_id", "x_min", "y_min", "x_max", "y_max"
}


def carregar_anotacoes(caminho_csv: Path, pasta_imagens: Path):
    """Cria objetos e agrupa caixas mesmo com linhas intercaladas no CSV."""
    imagens = {}
    try:
        with caminho_csv.open("r", newline="", encoding="utf-8-sig") as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=",")
            if not leitor.fieldnames or not CAMPOS_OBRIGATORIOS.issubset(leitor.fieldnames):
                raise ValueError("CSV com cabeçalho ausente ou incompleto.")
            for numero_linha, linha in enumerate(leitor, start=2):
                try:
                    nome = linha["imagem"].strip()
                    if not nome or Path(nome).name != nome or not nome.lower().endswith(".jpg"):
                        raise ValueError("nome de imagem inválido")
                    deteccao = Deteccao(
                        classe_id=int(linha["classe_id"]),
                        x_min=int(linha["x_min"]),
                        y_min=int(linha["y_min"]),
                        x_max=int(linha["x_max"]),
                        y_max=int(linha["y_max"]),
                    )
                except (ValueError, TypeError, KeyError, AttributeError) as erro:
                    raise ValueError(f"Linha {numero_linha} do CSV inválida: {erro}") from erro

                if nome not in imagens:
                    imagens[nome] = ImagemAnotada(pasta_imagens / nome)
                imagens[nome].adicionar_deteccao(deteccao)
    except OSError as erro:
        raise OSError(f"Não foi possível abrir o CSV {caminho_csv}: {erro}") from erro
    if not imagens:
        raise ValueError("O CSV não contém anotações.")
    return imagens
