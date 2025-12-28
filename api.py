"""Módulo para integração com a API CoinGecko."""

import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from config import COINGECKO_URL


def buscar_precos() -> dict[str, float]:
    """Busca os preços atuais de BTC e ETH em USD via API CoinGecko.

    Realiza uma requisição HTTP para a API CoinGecko e extrai os preços
    atuais de Bitcoin e Ethereum em dólares americanos.

    Returns:
        dict[str, float]: Dicionário com os preços atuais onde:
            - "BTC": preço de Bitcoin em USD
            - "ETH": preço de Ethereum em USD

    Raises:
        SystemExit: Se houver erro de conectividade com a API ou se a resposta
            não contiver os dados esperados.
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
