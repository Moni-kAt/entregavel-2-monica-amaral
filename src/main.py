"""Visualizador de bounding boxes; execute: python src/main.py."""

import argparse
from pathlib import Path
import sys

import cv2

from arquivos import carregar_anotacoes
from modelos import CORES

RAIZ = Path(__file__).resolve().parent.parent
TITULO_JANELA = "Entregavel 2 - Visualizador OpenCV"


def preparar_visualizacao(imagem, nome, numero, total, quantidade):
    """Redimensiona apenas a cópia exibida e adiciona legenda na janela."""
    altura, largura = imagem.shape[:2]
    escala = min(1.0, 1100 / largura, 760 / altura)
    if escala < 1:
        imagem = cv2.resize(
            imagem, (round(largura * escala), round(altura * escala)),
            interpolation=cv2.INTER_AREA,
        )
    else:
        imagem = imagem.copy()

    altura, largura = imagem.shape[:2]
    # Faixa informativa reservada acima da imagem exibida.
    visual = cv2.copyMakeBorder(
        imagem, 76, 0, 0, 0, cv2.BORDER_CONSTANT, value=(28, 28, 28)
    )
    nome_exibicao = f"{numero}/{total}  {nome}  |  {quantidade} caixas"
    cv2.putText(visual, nome_exibicao, (12, 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.57, (255, 255, 255), 1, cv2.LINE_AA)
    for classe_id, x in ((0, 12), (1, 175)):
        cv2.rectangle(visual, (x, 42), (x + 20, 60), CORES[classe_id], -1)
        cv2.putText(visual, f"Classe {classe_id}", (x + 28, 57),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    if largura > 650:
        cv2.putText(visual, "ESPACO: proxima   Q: sair", (largura - 320, 57),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.48, (220, 220, 220), 1, cv2.LINE_AA)
    return visual


def executar(sem_janela=False):
    pasta_imagens = RAIZ / "imagens"
    pasta_resultados = RAIZ / "resultados"
    caminho_csv = RAIZ / "dados" / "anotacoes.csv"
    agrupamento = carregar_anotacoes(caminho_csv, pasta_imagens)
    if not pasta_imagens.is_dir():
        raise OSError(f"Pasta de imagens não encontrada: {pasta_imagens}")

    arquivos = sorted(p for p in pasta_imagens.iterdir() if p.suffix.lower() == ".jpg")
    nomes = {p.name for p in arquivos}
    if not arquivos:
        raise ValueError("A pasta imagens não contém arquivos JPG.")
    if nomes != set(agrupamento):
        faltando_csv = sorted(nomes - set(agrupamento))
        faltando_jpg = sorted(set(agrupamento) - nomes)
        raise ValueError(
            f"Divergência entre CSV e imagens. Sem anotações: {faltando_csv}; "
            f"sem arquivo JPG: {faltando_jpg}"
        )

    pasta_resultados.mkdir(exist_ok=True, parents=True)
    total_caixas = 0
    total_imagens = 0
    try:
        for numero, caminho in enumerate(arquivos, start=1):
            imagem_anotada = agrupamento[caminho.name]
            resultado = imagem_anotada.gerar_imagem_anotada()
            destino = pasta_resultados / caminho.name
            if not cv2.imwrite(str(destino), resultado):
                raise OSError(f"Não foi possível salvar {destino}.")
            quantidade = len(imagem_anotada.deteccoes)
            print(f"[{numero:02d}/{len(arquivos):02d}] {caminho.name}: "
                  f"{quantidade} caixas desenhadas -> resultados/{caminho.name}", flush=True)
            total_imagens += 1
            total_caixas += quantidade

            if sem_janela:
                continue
            visual = preparar_visualizacao(
                resultado, caminho.name, numero, len(arquivos), quantidade
            )
            cv2.imshow(TITULO_JANELA, visual)
            while True:
                tecla = cv2.waitKey(0) & 0xFF
                if tecla == 32:  # Barra de espaço: próxima imagem
                    break
                if tecla in (ord("q"), ord("Q")):
                    print("Visualizador encerrado pela tecla Q.", flush=True)
                    return total_imagens, total_caixas
                # Qualquer outra tecla mantém a imagem atual.
    finally:
        if not sem_janela:
            cv2.destroyAllWindows()
    print(f"Concluído: {total_imagens} imagens, {total_caixas} caixas.", flush=True)
    return total_imagens, total_caixas


def main():
    parser = argparse.ArgumentParser(description="Visualizador de anotações OpenCV")
    parser.add_argument("--sem-janela", action="store_true",
                        help="Gera todos os resultados sem abrir o visualizador.")
    argumentos = parser.parse_args()
    try:
        executar(sem_janela=argumentos.sem_janela)
    except (OSError, ValueError, cv2.error) as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        raise SystemExit(1) from erro


if __name__ == "__main__":
    main()
