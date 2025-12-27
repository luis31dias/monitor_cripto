"""Ferramenta interativa para monitorar preços de criptomoedas via CoinGecko.

O script oferece:
- Monitoramento contínuo com persistência em CSV.
- Visualização do histórico no terminal.
- Geração de gráfico comparando BTC e ETH.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Iterable
from urllib.error import URLError
from urllib.request import Request, urlopen


COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
)
ARQUIVO_HISTORICO = "historico_cotacoes.csv"

INTERVALO_ATUALIZACAO_SEGUNDOS = 15


def limpar_terminal() -> None:
    """Limpa o terminal em sistemas Unix e Windows."""

    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def buscar_precos() -> dict[str, float]:
    """Busca os preços atuais de BTC e ETH em USD.

    Returns:
        dict[str, float]: Um dicionário com as chaves "BTC" e "ETH".
    """

    request = Request(COINGECKO_URL, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except URLError as exc:  # pragma: no cover - caso de rede
        raise SystemExit(f"Erro ao acessar a API: {exc}") from exc

    try:
        return {
            "BTC": float(data["bitcoin"]["usd"]),
            "ETH": float(data["ethereum"]["usd"]),
        }
    except (KeyError, TypeError, ValueError) as exc:  # pragma: no cover - dados inesperados
        raise SystemExit("Resposta inesperada da API.") from exc


def formatar_preco(valor: float) -> str:
    """Formata um preço para exibição."""

    return f"${valor:,.2f}"


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


def exibir_menu() -> str:
    """Exibe as opções principais e retorna a escolha do usuário."""

    print("🚀 Monitor de Criptomoedas")
    print("-" * 32)
    print("[1] Iniciar Monitoramento")
    print("[2] Ver Histórico")
    print("[3] Ver Gráfico")
    print("[0] Sair")
    return input("\nSelecione uma opção: ").strip()


def iniciar_monitoramento(intervalo_segundos: int = INTERVALO_ATUALIZACAO_SEGUNDOS) -> None:
    """Executa o loop de monitoramento, salvando cotações."""

    try:
        while True:
            limpar_terminal()
            horario = datetime.now(timezone.utc).astimezone()
            precos = buscar_precos()

            print("🚀 Monitor de Criptomoedas")
            print("-" * 30)
            print(f"⏰ Atualizado em: {horario:%d/%m/%Y %H:%M:%S %Z}")
            print()
            print("Moeda  | Preço (USD)")
            print("--------------------")
            for moeda, preco in precos.items():
                print(f"{moeda:<6}| {formatar_preco(preco)}")
                salvar_cotacao(horario, moeda, preco)
            print(f"\n(Salvo no histórico. Atualizando novamente em {INTERVALO_ATUALIZACAO_SEGUNDOS}s...)")
            time.sleep(intervalo_segundos)
    except KeyboardInterrupt:
        print("\n👋 Monitor interrompido. Voltando ao menu inicial...\n")


def imprimir_historico(historico: Iterable[tuple[datetime, str, float]]) -> None:
    """Mostra o histórico de cotações formatado."""

    print("📜 Histórico de Cotações")
    print("-" * 32)
    tem_dados = False
    for horario, moeda, preco in sorted(historico, key=lambda dado: dado[0]):
        tem_dados = True
        print(f"{horario:%d/%m/%Y %H:%M:%S} | {moeda:<3} | {formatar_preco(preco)}")
    if not tem_dados:
        print("Nenhum registro encontrado.")
    print()


def exibir_grafico(historico: Iterable[tuple[datetime, str, float]]) -> None:
    """Gera um gráfico de linhas comparando BTC e ETH."""

    try:
        import matplotlib.pyplot as plt
        import matplotlib
    except ImportError:  # pragma: no cover - dependência opcional
        print("matplotlib não está disponível. Instale para ver o gráfico.")
        return

    backend = plt.get_backend() or ""
    backend_nao_interativo = backend in matplotlib.rcsetup.non_interactive_bk or backend.lower().endswith("agg")

    pontos = {"BTC": [], "ETH": []}
    for horario, moeda, preco in historico:
        if moeda in pontos:
            pontos[moeda].append((horario, preco))

    if not pontos["BTC"] and not pontos["ETH"]:
        print("Nenhum dado para gerar o gráfico.")
        return

    plt.figure(figsize=(10, 5))
    for moeda, serie in pontos.items():
        if serie:
            tempos, precos = zip(*sorted(serie, key=lambda dado: dado[0]))
            plt.plot(tempos, precos, marker="o", label=moeda)

    plt.title("Histórico de Preços - BTC x ETH")
    plt.xlabel("Tempo")
    plt.ylabel("Preço (USD)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    if backend_nao_interativo:
        caminho_arquivo = os.path.abspath("grafico_cotacoes.png")
        plt.savefig(caminho_arquivo)
        print(f"Backend '{backend}' não é interativo; gráfico salvo em: {caminho_arquivo}")
        print("Dica: configure um backend interativo disponível (ex.: MPLBACKEND=TkAgg) ou instale suporte a GUI.")
        plt.close()

        import matplotlib.image as mpimg

        try:
            imagem = mpimg.imread(caminho_arquivo)
        except OSError as exc:  # pragma: no cover - leitura opcional
            print(f"Não foi possível carregar o arquivo salvo para visualização: {exc}")
            return

        plt.figure(figsize=(10, 5))
        plt.imshow(imagem)
        plt.axis("off")
        plt.title("Pré-visualização do gráfico salvo")
        plt.tight_layout()
        plt.show()
    else:
        plt.show()


def main() -> None:
    while True:
        escolha = exibir_menu()
        if escolha == "1":
            iniciar_monitoramento()
        elif escolha == "2":
            imprimir_historico(carregar_historico())
        elif escolha == "3":
            exibir_grafico(carregar_historico())
        elif escolha == "0":
            print("Até a próxima! 👋")
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.\n")


if __name__ == "__main__":
    main()
