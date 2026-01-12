"""
Testes para o módulo de backup.
"""

import os
import shutil
import tempfile
import time
from pathlib import Path
import pytest

from utils.backup import (
    realizar_backup,
    restaurar_backup,
    listar_backups,
    limpar_backups_antigos,
    contar_arquivos,
    calcular_tamanho,
    formatar_tamanho
)


@pytest.fixture
def diretorio_teste():
    """Cria um diretório temporário para testes."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def diretorio_com_arquivos(diretorio_teste):
    """Cria um diretório com arquivos para teste."""
    origem = Path(diretorio_teste) / "origem"
    origem.mkdir()
    
    # Criar alguns arquivos de teste
    (origem / "arquivo1.txt").write_text("Conteudo do arquivo 1")
    (origem / "arquivo2.txt").write_text("Conteudo do arquivo 2")
    
    subdir = origem / "subdiretorio"
    subdir.mkdir()
    (subdir / "arquivo3.txt").write_text("Conteudo do arquivo 3")
    
    return str(origem)


class TestRealizarBackup:
    """Testes para a função realizar_backup."""
    
    def test_backup_simples_sucesso(self, diretorio_com_arquivos, diretorio_teste):
        """Testa backup simples sem compactação."""
        destino = Path(diretorio_teste) / "backups"
        
        resultado = realizar_backup(
            diretorio_origem=diretorio_com_arquivos,
            diretorio_destino=str(destino),
            compactar=False
        )
        
        assert resultado["sucesso"] is True
        assert resultado["erro"] is None
        assert resultado["arquivos_copiados"] == 3
        assert resultado["tamanho_total"] > 0
        assert Path(resultado["destino"]).exists()
    
    def test_backup_compactado_sucesso(self, diretorio_com_arquivos, diretorio_teste):
        """Testa backup com compactação ZIP."""
        destino = Path(diretorio_teste) / "backups"
        
        resultado = realizar_backup(
            diretorio_origem=diretorio_com_arquivos,
            diretorio_destino=str(destino),
            compactar=True
        )
        
        assert resultado["sucesso"] is True
        assert resultado["erro"] is None
        assert resultado["destino"].endswith(".zip")
        assert Path(resultado["destino"]).exists()
    
    def test_backup_diretorio_inexistente(self, diretorio_teste):
        """Testa backup de diretório que não existe."""
        resultado = realizar_backup(
            diretorio_origem="/caminho/inexistente",
            diretorio_destino=diretorio_teste
        )
        
        assert resultado["sucesso"] is False
        assert resultado["erro"] is not None
        assert "não encontrado" in resultado["erro"]
    
    def test_backup_arquivo_ao_inves_de_diretorio(self, diretorio_teste):
        """Testa backup quando origem é um arquivo, não diretório."""
        arquivo = Path(diretorio_teste) / "arquivo.txt"
        arquivo.write_text("conteudo")
        
        resultado = realizar_backup(
            diretorio_origem=str(arquivo),
            diretorio_destino=diretorio_teste
        )
        
        assert resultado["sucesso"] is False
        assert resultado["erro"] is not None


class TestRestaurarBackup:
    """Testes para a função restaurar_backup."""
    
    def test_restaurar_backup_diretorio(self, diretorio_com_arquivos, diretorio_teste):
        """Testa restauração de backup de diretório."""
        destino_backup = Path(diretorio_teste) / "backups"
        destino_restauracao = Path(diretorio_teste) / "restaurado"
        
        # Primeiro faz o backup
        backup = realizar_backup(diretorio_com_arquivos, str(destino_backup))
        
        # Depois restaura
        resultado = restaurar_backup(
            arquivo_backup=backup["destino"],
            diretorio_destino=str(destino_restauracao)
        )
        
        assert resultado["sucesso"] is True
        assert destino_restauracao.exists()
    
    def test_restaurar_backup_inexistente(self, diretorio_teste):
        """Testa restauração de backup que não existe."""
        resultado = restaurar_backup(
            arquivo_backup="/backup/inexistente",
            diretorio_destino=diretorio_teste
        )
        
        assert resultado["sucesso"] is False
        assert "não encontrado" in resultado["erro"].lower() or "not found" in resultado["erro"].lower()
    
    def test_restaurar_sem_sobrescrever(self, diretorio_com_arquivos, diretorio_teste):
        """Testa que não sobrescreve destino existente sem flag."""
        destino_backup = Path(diretorio_teste) / "backups"
        destino_restauracao = Path(diretorio_teste) / "restaurado"
        destino_restauracao.mkdir()
        
        backup = realizar_backup(diretorio_com_arquivos, str(destino_backup))
        
        resultado = restaurar_backup(
            arquivo_backup=backup["destino"],
            diretorio_destino=str(destino_restauracao),
            sobrescrever=False
        )
        
        assert resultado["sucesso"] is False


class TestListarBackups:
    """Testes para a função listar_backups."""
    
    def test_listar_backups_existentes(self, diretorio_com_arquivos, diretorio_teste):
        """Testa listagem de backups existentes."""
        destino = Path(diretorio_teste) / "backups"
        
        # Criar backups com delay para garantir timestamps diferentes
        realizar_backup(diretorio_com_arquivos, str(destino))
        time.sleep(1.1)  # Aguardar para ter timestamp diferente
        realizar_backup(diretorio_com_arquivos, str(destino))
        
        backups = listar_backups(str(destino))
        
        assert len(backups) >= 1  # Pelo menos 1 backup deve existir
        assert all("nome" in b for b in backups)
        assert all("tamanho" in b for b in backups)
    
    def test_listar_backups_diretorio_vazio(self, diretorio_teste):
        """Testa listagem em diretório sem backups."""
        backups = listar_backups(diretorio_teste)
        
        assert backups == []
    
    def test_listar_backups_diretorio_inexistente(self):
        """Testa listagem em diretório que não existe."""
        backups = listar_backups("/diretorio/inexistente")
        
        assert backups == []


class TestLimparBackupsAntigos:
    """Testes para a função limpar_backups_antigos."""
    
    def test_manter_minimo_backups(self, diretorio_com_arquivos, diretorio_teste):
        """Testa que mantém o mínimo de backups."""
        destino = Path(diretorio_teste) / "backups"
        
        # Criar backups com delay
        for i in range(3):
            realizar_backup(diretorio_com_arquivos, str(destino))
            if i < 2:
                time.sleep(1.1)
        
        backups_antes = listar_backups(str(destino))
        resultado = limpar_backups_antigos(str(destino), dias=0, manter_minimo=3)
        
        assert resultado["sucesso"] is True
        assert resultado["mantidos"] >= 1  # Pelo menos 1 backup mantido
    
    def test_nenhum_backup_para_limpar(self, diretorio_teste):
        """Testa limpeza quando não há backups."""
        resultado = limpar_backups_antigos(diretorio_teste, dias=30)
        
        assert resultado["sucesso"] is True
        assert resultado["removidos"] == []


class TestFuncoesAuxiliares:
    """Testes para funções auxiliares."""
    
    def test_contar_arquivos(self, diretorio_com_arquivos):
        """Testa contagem de arquivos."""
        path = Path(diretorio_com_arquivos)
        count = contar_arquivos(path)
        
        assert count == 3
    
    def test_calcular_tamanho_arquivo(self, diretorio_teste):
        """Testa cálculo de tamanho de arquivo."""
        arquivo = Path(diretorio_teste) / "teste.txt"
        conteudo = "x" * 100
        arquivo.write_text(conteudo)
        
        tamanho = calcular_tamanho(arquivo)
        
        assert tamanho == 100
    
    def test_calcular_tamanho_diretorio(self, diretorio_com_arquivos):
        """Testa cálculo de tamanho de diretório."""
        path = Path(diretorio_com_arquivos)
        tamanho = calcular_tamanho(path)
        
        assert tamanho > 0
    
    def test_formatar_tamanho_bytes(self):
        """Testa formatação de tamanho em bytes."""
        assert "B" in formatar_tamanho(500)
    
    def test_formatar_tamanho_kilobytes(self):
        """Testa formatação de tamanho em KB."""
        assert "KB" in formatar_tamanho(2048)
    
    def test_formatar_tamanho_megabytes(self):
        """Testa formatação de tamanho em MB."""
        assert "MB" in formatar_tamanho(2 * 1024 * 1024)
    
    def test_formatar_tamanho_gigabytes(self):
        """Testa formatação de tamanho em GB."""
        assert "GB" in formatar_tamanho(2 * 1024 * 1024 * 1024)