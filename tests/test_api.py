"""Testes unitários para o módulo api."""

import unittest
from unittest.mock import patch, MagicMock
import json

import sys
import os

# Adiciona o diretório pai ao caminho para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import buscar_precos


class TestBuscarPrecos(unittest.TestCase):
    """Testes para a função buscar_precos."""

    @patch('api.urlopen')
    def test_buscar_precos_sucesso(self, mock_urlopen):
        """Testa busca bem-sucedida de preços."""
        # Simula resposta da API
        resposta_json = {
            "bitcoin": {"usd": 45234.50},
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        resultado = buscar_precos()

        self.assertEqual(resultado["BTC"], 45234.50)
        self.assertEqual(resultado["ETH"], 2567.30)

    @patch('api.urlopen')
    def test_buscar_precos_retorna_dict(self, mock_urlopen):
        """Testa se o retorno é um dicionário."""
        resposta_json = {
            "bitcoin": {"usd": 45234.50},
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        resultado = buscar_precos()

        self.assertIsInstance(resultado, dict)
        self.assertIn("BTC", resultado)
        self.assertIn("ETH", resultado)

    @patch('api.urlopen')
    def test_buscar_precos_valores_sao_float(self, mock_urlopen):
        """Testa se os valores retornados são float."""
        resposta_json = {
            "bitcoin": {"usd": 45234.50},
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        resultado = buscar_precos()

        self.assertIsInstance(resultado["BTC"], float)
        self.assertIsInstance(resultado["ETH"], float)

    @patch('api.urlopen')
    def test_buscar_precos_valores_positivos(self, mock_urlopen):
        """Testa se os valores são positivos."""
        resposta_json = {
            "bitcoin": {"usd": 45234.50},
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        resultado = buscar_precos()

        self.assertGreater(resultado["BTC"], 0)
        self.assertGreater(resultado["ETH"], 0)

    @patch('api.urlopen')
    def test_buscar_precos_preco_pequeno(self, mock_urlopen):
        """Testa com preços muito pequenos (edge case)."""
        resposta_json = {
            "bitcoin": {"usd": 0.01},
            "ethereum": {"usd": 0.001}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        resultado = buscar_precos()

        self.assertEqual(resultado["BTC"], 0.01)
        self.assertEqual(resultado["ETH"], 0.001)

    @patch('api.urlopen')
    def test_buscar_precos_preco_grande(self, mock_urlopen):
        """Testa com preços muito grandes (edge case)."""
        resposta_json = {
            "bitcoin": {"usd": 999999.99},
            "ethereum": {"usd": 99999.99}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        resultado = buscar_precos()

        self.assertEqual(resultado["BTC"], 999999.99)
        self.assertEqual(resultado["ETH"], 99999.99)

    @patch('api.urlopen')
    def test_buscar_precos_erro_conexao(self, mock_urlopen):
        """Testa se SystemExit é lançado em erro de conexão."""
        from urllib.error import URLError

        mock_urlopen.side_effect = URLError("Erro de conexão")

        with self.assertRaises(SystemExit):
            buscar_precos()

    @patch('api.urlopen')
    def test_buscar_precos_resposta_malformada_chave_faltante(self, mock_urlopen):
        """Testa SystemExit quando falta chave na resposta."""
        # Resposta sem a chave "ethereum"
        resposta_json = {
            "bitcoin": {"usd": 45234.50}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        with self.assertRaises(SystemExit):
            buscar_precos()

    @patch('api.urlopen')
    def test_buscar_precos_resposta_malformada_valor_invalido(self, mock_urlopen):
        """Testa SystemExit quando valor não é conversível para float."""
        resposta_json = {
            "bitcoin": {"usd": "preco_invalido"},
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        with self.assertRaises(SystemExit):
            buscar_precos()

    @patch('api.urlopen')
    def test_buscar_precos_timeout(self, mock_urlopen):
        """Testa timeout na requisição."""
        from urllib.error import URLError

        mock_urlopen.side_effect = URLError("Timeout")

        with self.assertRaises(SystemExit):
            buscar_precos()

    @patch('api.urlopen')
    def test_buscar_precos_retorna_chaves_corretas(self, mock_urlopen):
        """Testa se retorna exatamente as chaves esperadas."""
        resposta_json = {
            "bitcoin": {"usd": 45234.50},
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        resultado = buscar_precos()

        self.assertEqual(set(resultado.keys()), {"BTC", "ETH"})

    @patch('api.urlopen')
    def test_buscar_precos_chama_urlopen_uma_vez(self, mock_urlopen):
        """Testa se urlopen é chamado exatamente uma vez."""
        resposta_json = {
            "bitcoin": {"usd": 45234.50},
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        buscar_precos()

        self.assertEqual(mock_urlopen.call_count, 1)

    @patch('api.urlopen')
    def test_buscar_precos_resposta_tipo_invalido(self, mock_urlopen):
        """Testa SystemExit quando estrutura da resposta tem tipo inválido."""
        resposta_json = {
            "bitcoin": {"usd": None},  # None em vez de número
            "ethereum": {"usd": 2567.30}
        }

        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(resposta_json).encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = False

        mock_urlopen.return_value = mock_response

        with self.assertRaises(SystemExit):
            buscar_precos()


if __name__ == '__main__':
    unittest.main()
