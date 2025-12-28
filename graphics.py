"""Módulo para visualização gráfica do histórico de cotações."""

import os
from datetime import datetime
from typing import Iterable


def exibir_grafico(historico: Iterable[tuple[datetime, str, float]]) -> None:
    """Gera e salva um gráfico de linhas comparando BTC e ETH com eixos duplos.

    Cria um gráfico visual mostrando o histórico de preços de Bitcoin e Ethereum
    em um período. Utiliza eixos Y independentes para melhor visualização das
    escalas diferentes das moedas. O gráfico é salvo como PNG no diretório atual.

    Args:
        historico (Iterable[tuple[datetime, str, float]]): Iterável contendo
            tuplas com:
            - datetime: Timestamp da cotação
            - str: Identificador da moeda ("BTC" ou "ETH")
            - float: Preço em USD

    Returns:
        None

    Note:
        - Requer matplotlib instalado. Se não estiver disponível, apenas avisa.
        - Se o histórico estiver vazio, exibe mensagem e retorna sem gerar erro.
        - O arquivo é salvo como "grafico_cotacoes.png" no diretório atual.
        - BTC é exibido em azul no eixo esquerdo.
        - ETH é exibido em laranja no eixo direito.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:  # pragma: no cover - dependência opcional
        print("matplotlib não está disponível. Instale para ver o gráfico.")
        return

    pontos = {"BTC": [], "ETH": []}
    for horario, moeda, preco in historico:
        if moeda in pontos:
            pontos[moeda].append((horario, preco))

    if not pontos["BTC"] and not pontos["ETH"]:
        print("Nenhum dados para gerar o gráfico.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    # Eixo esquerdo para BTC (azul)
    if pontos["BTC"]:
        tempos_btc, precos_btc = zip(*sorted(pontos["BTC"], key=lambda dado: dado[0]))
        line_btc = ax.plot(tempos_btc, precos_btc, marker="o", color="blue", label="BTC")
        ax.set_ylabel("BTC (USD)", color="blue")
        ax.tick_params(axis="y", labelcolor="blue")

    # Eixo direito para ETH (laranja)
    ax2 = ax.twinx()
    if pontos["ETH"]:
        tempos_eth, precos_eth = zip(*sorted(pontos["ETH"], key=lambda dado: dado[0]))
        line_eth = ax2.plot(tempos_eth, precos_eth, marker="s", color="orange", label="ETH")
        ax2.set_ylabel("ETH (USD)", color="orange")
        ax2.tick_params(axis="y", labelcolor="orange")

    ax.set_xlabel("Tempo")
    ax.set_title("Histórico de Preços - BTC x ETH")
    ax.grid(True, linestyle="--", alpha=0.5)

    # Combina as legendas dos dois eixos
    lines = []
    labels = []
    if pontos["BTC"]:
        lines.extend(line_btc)
        labels.append("BTC")
    if pontos["ETH"]:
        lines.extend(line_eth)
        labels.append("ETH")
    ax.legend(lines, labels, loc="upper left")

    fig.tight_layout()

    caminho_arquivo = os.path.abspath("grafico_cotacoes.png")
    fig.savefig(caminho_arquivo)
    plt.close(fig)

    print(f"\n✅ Gráfico salvo em: {caminho_arquivo}")
    print(f"💡 Para abrir, use: xdg-open {caminho_arquivo}\n")
