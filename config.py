"""Configurações e constantes da aplicação Monitor de Criptomoedas.

Este módulo centraliza todas as configurações de constantes e funções
utilitárias usadas pelos demais módulos da aplicação.
"""

import os

COINGECKO_URL = (
    "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
)
"""str: URL da API CoinGecko para obter preços de BTC e ETH."""

ARQUIVO_HISTORICO = "historico_cotacoes.csv"
"""str: Nome do arquivo CSV onde o histórico de cotações é persistido."""

INTERVALO_ATUALIZACAO_SEGUNDOS = 15
"""int: Intervalo em segundos entre atualizações de preços."""


def limpar_terminal() -> None:
    """Limpa o conteúdo do terminal/console.

    Executa o comando apropriado para limpar a tela do terminal dependendo
    do sistema operacional (Unix/Linux usa 'clear', Windows usa 'cls').

    Returns:
        None

    Note:
        Apenas limpa o terminal visual, não afeta variáveis ou estado da aplicação.
    """
    comando = "cls" if os.name == "nt" else "clear"
    os.system(comando)


def formatar_preco(valor: float) -> str:
    """Formata um valor numérico como preço em USD para exibição.

    Converte um float em string formatada com símbolo de dólar, separador
    de milhares e duas casas decimais.

    Args:
        valor (float): Preço em USD a ser formatado.

    Returns:
        str: String formatada no padrão "$X,XXX.XX".

    Example:
        >>> formatar_preco(45234.567)
        '$45,234.57'
        >>> formatar_preco(1000.5)
        '$1,000.50'
    """
    return f"${valor:,.2f}"
