"""Ferramenta interativa para monitorar preços de criptomoedas via CoinGecko.

O script oferece:
- Monitoramento contínuo com persistência em CSV.
- Visualização do histórico no terminal.
- Geração de gráfico comparando BTC e ETH.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from typing import Iterable

from api import buscar_precos
from config import (
    INTERVALO_ATUALIZACAO_SEGUNDOS,
    formatar_preco,
    limpar_terminal,
)
from graphics import exibir_grafico
from storage import carregar_historico, salvar_cotacao


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
