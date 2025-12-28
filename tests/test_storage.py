"""Testes unitários para o módulo storage."""

import unittest
import tempfile
import os
from datetime import datetime

import sys

# Adiciona o diretório pai ao caminho para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from storage import salvar_cotacao, carregar_historico


class TestSalvarCotacao(unittest.TestCase):
    """Testes para a função salvar_cotacao."""

    def setUp(self):
        """Cria um arquivo temporário para cada teste."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        )
        self.temp_file.close()
        self.arquivo = self.temp_file.name

    def tearDown(self):
        """Remove o arquivo temporário após cada teste."""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)

    def test_salvar_cotacao_cria_arquivo(self):
        """Testa se salvar_cotacao cria o arquivo se não existir."""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)

        horario = datetime(2025, 1, 1, 12, 0, 0)
        salvar_cotacao(horario, "BTC", 50000.50, self.arquivo)

        self.assertTrue(os.path.exists(self.arquivo))

    def test_salvar_cotacao_com_cabecalho(self):
        """Testa se o cabeçalho é escrito corretamente."""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)

        horario = datetime(2025, 1, 1, 12, 0, 0)
        salvar_cotacao(horario, "BTC", 50000.50, self.arquivo)

        with open(self.arquivo, 'r') as f:
            primeira_linha = f.readline().strip()
            self.assertEqual(primeira_linha, "data_hora,moeda,preco")

    def test_salvar_cotacao_formato_correto(self):
        """Testa se os dados são salvos no formato correto."""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)

        horario = datetime(2025, 1, 1, 12, 0, 0)
        salvar_cotacao(horario, "BTC", 50000.567, self.arquivo)

        with open(self.arquivo, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Cabeçalho + 1 dado
            self.assertEqual(lines[1].strip(), "2025-01-01T12:00:00,BTC,50000.57")

    def test_salvar_multiplas_cotacoes(self):
        """Testa se múltiplas cotações são salvas corretamente."""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)

        horario1 = datetime(2025, 1, 1, 12, 0, 0)
        horario2 = datetime(2025, 1, 1, 12, 15, 0)

        salvar_cotacao(horario1, "BTC", 50000.00, self.arquivo)
        salvar_cotacao(horario2, "ETH", 3000.00, self.arquivo)

        with open(self.arquivo, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)  # Cabeçalho + 2 dados

    def test_salvar_cotacao_formata_preco(self):
        """Testa se o preço é formatado com 2 casas decimais."""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)

        horario = datetime(2025, 1, 1, 12, 0, 0)
        salvar_cotacao(horario, "BTC", 50000.1, self.arquivo)

        with open(self.arquivo, 'r') as f:
            lines = f.readlines()
            self.assertIn("50000.10", lines[1])


class TestCarregarHistorico(unittest.TestCase):
    """Testes para a função carregar_historico."""

    def setUp(self):
        """Cria um arquivo temporário para cada teste."""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False, newline=''
        )
        self.arquivo = self.temp_file.name

    def tearDown(self):
        """Remove o arquivo temporário após cada teste."""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)

    def test_carregar_arquivo_inexistente(self):
        """Testa se retorna lista vazia quando arquivo não existe."""
        os.remove(self.arquivo)
        resultado = carregar_historico(self.arquivo)
        self.assertEqual(resultado, [])

    def test_carregar_arquivo_vazio(self):
        """Testa se retorna lista vazia quando arquivo está vazio."""
        with open(self.arquivo, 'w') as f:
            f.write("")
        resultado = carregar_historico(self.arquivo)
        self.assertEqual(resultado, [])

    def test_carregar_arquivo_apenas_cabecalho(self):
        """Testa se retorna lista vazia quando há apenas cabeçalho."""
        with open(self.arquivo, 'w') as f:
            f.write("data_hora,moeda,preco\n")
        resultado = carregar_historico(self.arquivo)
        self.assertEqual(resultado, [])

    def test_carregar_uma_cotacao(self):
        """Testa carregamento de uma cotação."""
        with open(self.arquivo, 'w') as f:
            f.write("data_hora,moeda,preco\n")
            f.write("2025-01-01T12:00:00,BTC,50000.50\n")

        resultado = carregar_historico(self.arquivo)
        self.assertEqual(len(resultado), 1)

        horario, moeda, preco = resultado[0]
        self.assertEqual(horario, datetime(2025, 1, 1, 12, 0, 0))
        self.assertEqual(moeda, "BTC")
        self.assertAlmostEqual(preco, 50000.50)

    def test_carregar_multiplas_cotacoes(self):
        """Testa carregamento de múltiplas cotações."""
        with open(self.arquivo, 'w') as f:
            f.write("data_hora,moeda,preco\n")
            f.write("2025-01-01T12:00:00,BTC,50000.50\n")
            f.write("2025-01-01T12:15:00,ETH,3000.00\n")
            f.write("2025-01-01T12:30:00,BTC,50100.25\n")

        resultado = carregar_historico(self.arquivo)
        self.assertEqual(len(resultado), 3)

    def test_carregar_ignora_linhas_malformadas(self):
        """Testa se linhas malformadas são ignoradas."""
        with open(self.arquivo, 'w') as f:
            f.write("data_hora,moeda,preco\n")
            f.write("2025-01-01T12:00:00,BTC,50000.50\n")
            f.write("data_invalida,ETH,preco_invalido\n")
            f.write("2025-01-01T12:30:00,BTC,50100.25\n")

        resultado = carregar_historico(self.arquivo)
        self.assertEqual(len(resultado), 2)  # Apenas as linhas válidas

    def test_carregar_tipos_retornados(self):
        """Testa se os tipos de retorno estão corretos."""
        with open(self.arquivo, 'w') as f:
            f.write("data_hora,moeda,preco\n")
            f.write("2025-01-01T12:00:00,BTC,50000.50\n")

        resultado = carregar_historico(self.arquivo)
        horario, moeda, preco = resultado[0]

        self.assertIsInstance(horario, datetime)
        self.assertIsInstance(moeda, str)
        self.assertIsInstance(preco, float)

    def test_carregar_preserva_ordem(self):
        """Testa se a ordem das cotações é preservada."""
        with open(self.arquivo, 'w') as f:
            f.write("data_hora,moeda,preco\n")
            f.write("2025-01-01T12:00:00,BTC,50000.00\n")
            f.write("2025-01-01T12:15:00,BTC,50100.00\n")
            f.write("2025-01-01T12:30:00,BTC,50200.00\n")

        resultado = carregar_historico(self.arquivo)
        precos = [preco for _, _, preco in resultado]

        self.assertEqual(precos, [50000.00, 50100.00, 50200.00])


if __name__ == '__main__':
    unittest.main()
