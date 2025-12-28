"""Módulo para persistência e leitura de histórico de cotações."""

import csv
import os
from datetime import datetime

from config import ARQUIVO_HISTORICO


def salvar_cotacao(
    horario: datetime, moeda: str, preco: float, arquivo: str = ARQUIVO_HISTORICO
) -> None:
    """Persiste uma cotação em CSV (data, moeda, preço)."""
    escrever_cabecalho = not os.path.exists(arquivo)
    with open(arquivo, "a", newline="", encoding="utf-8") as ponteiro:
        escritor = csv.writer(ponteiro)
        if escrever_cabecalho:
            escritor.writerow(["data_hora", "moeda", "preco"])
        escritor.writerow([horario.isoformat(), moeda, f"{preco:.2f}"])


def carregar_historico(arquivo: str = ARQUIVO_HISTORICO) -> list[tuple[datetime, str, float]]:
    """Carrega o histórico de cotações do arquivo informado."""
    if not os.path.exists(arquivo):
        return []

    historico: list[tuple[datetime, str, float]] = []
    with open(arquivo, newline="", encoding="utf-8") as ponteiro:
        leitor = csv.DictReader(ponteiro)
        for linha in leitor:
            try:
                horario = datetime.fromisoformat(linha["data_hora"])
                moeda = linha["moeda"]
                preco = float(linha["preco"])
            except (TypeError, ValueError, KeyError):
                continue
            historico.append((horario, moeda, preco))
    return historico
