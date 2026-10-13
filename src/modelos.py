"""Modelos responsáveis pelas caixas e imagens anotadas."""

from dataclasses import dataclass, field
from pathlib import Path

import cv2

# Cores BGR usadas pelo OpenCV: verde para 0, azul para 1.
CORES = {0: (0, 255, 0), 1: (255, 0, 0)}


@dataclass
class Deteccao:
    """Bounding box em coordenadas inteiras da imagem original."""

    classe_id: int
    x_min: int
    y_min: int
    x_max: int
    y_max: int

    def desenhar(self, imagem):
        """Valida as coordenadas e desenha sua própria caixa na imagem."""
        altura, largura = imagem.shape[:2]
        if self.classe_id not in CORES:
            raise ValueError(f"Classe desconhecida: {self.classe_id}.")
        if not (0 <= self.x_min < self.x_max < largura and
                0 <= self.y_min < self.y_max < altura):
            raise ValueError(
                f"Caixa inválida para {largura}x{altura}: "
                f"({self.x_min}, {self.y_min})–({self.x_max}, {self.y_max})."
            )
        cv2.rectangle(
            imagem,
            (self.x_min, self.y_min),
            (self.x_max, self.y_max),
            CORES[self.classe_id],
            thickness=2,
        )


@dataclass
class ImagemAnotada:
    """Caminho da imagem e lista de detecções associadas a ela."""

    caminho: Path
    deteccoes: list[Deteccao] = field(default_factory=list)

    def adicionar_deteccao(self, deteccao: Deteccao):
        self.deteccoes.append(deteccao)

    def gerar_imagem_anotada(self):
        """Retorna cópia com caixas, sem alterar o arquivo JPG original."""
        imagem = cv2.imread(str(self.caminho))
        if imagem is None:
            raise OSError(f"Não foi possível ler a imagem: {self.caminho}")
        copia = imagem.copy()
        for deteccao in self.deteccoes:
            try:
                deteccao.desenhar(copia)
            except ValueError as erro:
                raise ValueError(f"{self.caminho.name}: {erro}") from erro
        return copia
