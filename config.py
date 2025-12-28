"""Configurações e constantes da aplicação Monitor de Criptomoedas."""

import os

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
)
ARQUIVO_HISTORICO = "historico_cotacoes.csv"
INTERVALO_ATUALIZACAO_SEGUNDOS = 15


def limpar_terminal() -> None:
    """Limpa o terminal em sistemas Unix e Windows."""
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def formatar_preco(valor: float) -> str:
    """Formata um preço para exibição."""
    return f"${valor:,.2f}"
