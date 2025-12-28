"""Testes unitários para o módulo config."""

import unittest
from unittest.mock import patch

import sys
import os

# Adiciona o diretório pai ao caminho para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import formatar_preco, limpar_terminal, INTERVALO_ATUALIZACAO_SEGUNDOS


class TestFormatarPreco(unittest.TestCase):
    """Testes para a função formatar_preco."""

    def test_formatacao_basica(self):
        """Testa formatação básica de um preço simples."""
        resultado = formatar_preco(100.0)
        self.assertEqual(resultado, "$100.00")

    def test_formatacao_com_centavos(self):
        """Testa formatação com centavos."""
        resultado = formatar_preco(1234.56)
        self.assertEqual(resultado, "$1,234.56")

    def test_formatacao_com_milhares(self):
        """Testa formatação com separador de milhares."""
        resultado = formatar_preco(45234.567)
        self.assertEqual(resultado, "$45,234.57")

    def test_formatacao_grande(self):
        """Testa formatação de preço grande (típico de BTC)."""
        resultado = formatar_preco(45234.123)
        self.assertEqual(resultado, "$45,234.12")

    def test_formatacao_pequeno(self):
        """Testa formatação de preço pequeno."""
        resultado = formatar_preco(0.5)
        self.assertEqual(resultado, "$0.50")

    def test_formatacao_zero(self):
        """Testa formatação de zero."""
        resultado = formatar_preco(0.0)
        self.assertEqual(resultado, "$0.00")

    def test_formatacao_arredonda_corretamente(self):
        """Testa se o arredondamento é feito corretamente."""
        resultado = formatar_preco(1000.996)
        self.assertEqual(resultado, "$1,001.00")

    def test_formatacao_com_multiplos_milhares(self):
        """Testa formatação com múltiplos separadores de milhares."""
        resultado = formatar_preco(1234567.89)
        self.assertEqual(resultado, "$1,234,567.89")


class TestLimparTerminal(unittest.TestCase):
    """Testes para a função limpar_terminal."""

    @patch('os.system')
    def test_limpar_terminal_unix(self, mock_system):
        """Testa se usa 'clear' em sistemas Unix/Linux."""
        with patch('os.name', 'posix'):
            limpar_terminal()
            mock_system.assert_called_once_with('clear')

    @patch('os.system')
    def test_limpar_terminal_windows(self, mock_system):
        """Testa se usa 'cls' em sistemas Windows."""
        with patch('os.name', 'nt'):
            limpar_terminal()
            mock_system.assert_called_once_with('cls')

    @patch('os.system')
    def test_limpar_terminal_sem_erro(self, mock_system):
        """Testa que a função não gera exceções."""
        try:
            limpar_terminal()
        except Exception as e:
            self.fail(f"limpar_terminal() gerou exceção: {e}")


class TestConstantes(unittest.TestCase):
    """Testes para as constantes do módulo."""

    def test_intervalo_atualizacao_positivo(self):
        """Testa se o intervalo é um valor positivo."""
        self.assertGreater(INTERVALO_ATUALIZACAO_SEGUNDOS, 0)

    def test_intervalo_atualizacao_tipo(self):
        """Testa se o intervalo é do tipo inteiro."""
        self.assertIsInstance(INTERVALO_ATUALIZACAO_SEGUNDOS, int)


if __name__ == '__main__':
    unittest.main()
