"""Módulo para persistência e leitura de histórico de cotações."""

import csv
import os
from datetime import datetime

from config import ARQUIVO_HISTORICO


def salvar_cotacao(
    horario: datetime, moeda: str, preco: float, arquivo: str = ARQUIVO_HISTORICO
) -> None:
    """Persiste uma cotação de criptomoeda em arquivo CSV.

    Salva uma nova entrada de cotação em um arquivo CSV com timestamp,
    identificador da moeda e valor de preço. Cria o arquivo com cabeçalho
    automaticamente se não existir.

    Args:
        horario (datetime): Data e hora da cotação.
        moeda (str): Identificador da moeda (ex: "BTC", "ETH").
        preco (float): Preço da moeda em USD, será formatado com 2 casas decimais.
        arquivo (str, optional): Caminho do arquivo CSV. Padrão é ARQUIVO_HISTORICO.

    Returns:
        None
    """
    escrever_cabecalho = not os.path.exists(arquivo)
    with open(arquivo, "a", newline="", encoding="utf-8") as ponteiro:
        escritor = csv.writer(ponteiro)
        if escrever_cabecalho:
            escritor.writerow(["data_hora", "moeda", "preco"])
        escritor.writerow([horario.isoformat(), moeda, f"{preco:.2f}"])


def carregar_historico(arquivo: str = ARQUIVO_HISTORICO) -> list[tuple[datetime, str, float]]:
    """Carrega o histórico completo de cotações de um arquivo CSV.

    Lê um arquivo CSV contendo histórico de cotações e retorna uma lista
    de tuplas com data/hora, moeda e preço. Linhas com dados inválidos
    são silenciosamente ignoradas.

    Args:
        arquivo (str, optional): Caminho do arquivo CSV. Padrão é ARQUIVO_HISTORICO.

    Returns:
        list[tuple[datetime, str, float]]: Lista de tuplas contendo:
            - datetime: Data e hora da cotação
            - str: Identificador da moeda (BTC, ETH, etc)
            - float: Preço em USD

    Note:
        Se o arquivo não existe, retorna uma lista vazia.
        Linhas malformadas são puladas sem gerar exceções.
    """
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
