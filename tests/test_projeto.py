"""
Testes para o módulo de projeto.
"""

import os
import shutil
import tempfile
import logging
from pathlib import Path
import pytest

from utils.projeto import (
    gerenciar_arquivos,
    criar_estrutura_projeto
)


def fechar_handlers_logger(nome: str):
    """Fecha todos os handlers de um logger."""
    logger = logging.getLogger(nome)
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


@pytest.fixture
def diretorio_teste():
    """Cria um diretório temporário para testes."""
    temp_dir = tempfile.mkdtemp()
    original_dir = os.getcwd()
    yield temp_dir
    # Restaurar diretório original
    os.chdir(original_dir)
    # Fechar handlers que podem bloquear arquivos
    fechar_handlers_logger("projeto")
    # Cleanup com tratamento de erro
    import time
    time.sleep(0.1)
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    except PermissionError:
        pass


@pytest.fixture
def diretorio_com_arquivos(diretorio_teste):
    """Cria um diretório com arquivos variados."""
    # Criar arquivos Python
    (Path(diretorio_teste) / "script1.py").write_text("# Script 1")
    (Path(diretorio_teste) / "script2.py").write_text("# Script 2")
    
    # Criar arquivos de texto
    (Path(diretorio_teste) / "readme.txt").write_text("README")
    
    # Criar subdiretório com arquivos
    subdir = Path(diretorio_teste) / "subdir"
    subdir.mkdir()
    (subdir / "script3.py").write_text("# Script 3")
    (subdir / "config.json").write_text("{}")
    
    return diretorio_teste


class TestGerenciarArquivos:
    """Testes para a função gerenciar_arquivos."""
    
    def test_listar_todos_arquivos(self, diretorio_com_arquivos):
        """Testa listagem de todos os arquivos."""
        arquivos = gerenciar_arquivos(diretorio_com_arquivos)
        
        assert len(arquivos) == 5  # 2 py + 1 txt + 1 py + 1 json
    
    def test_filtrar_por_extensao(self, diretorio_com_arquivos):
        """Testa filtragem por extensão."""
        arquivos = gerenciar_arquivos(diretorio_com_arquivos, extensao=".py")
        
        assert len(arquivos) == 3
        assert all(a["nome"].endswith(".py") for a in arquivos)
    
    def test_diretorio_inexistente(self):
        """Testa listagem em diretório inexistente."""
        arquivos = gerenciar_arquivos("/diretorio/inexistente")
        
        assert arquivos == []
    
    def test_estrutura_arquivo(self, diretorio_com_arquivos):
        """Testa estrutura do dicionário de arquivo."""
        arquivos = gerenciar_arquivos(diretorio_com_arquivos)
        
        for arquivo in arquivos:
            assert "nome" in arquivo
            assert "caminho" in arquivo
            assert "tamanho" in arquivo
            assert "modificado" in arquivo
    
    def test_tamanho_arquivo(self, diretorio_com_arquivos):
        """Testa que tamanho é calculado corretamente."""
        arquivos = gerenciar_arquivos(diretorio_com_arquivos, extensao=".py")
        
        for arquivo in arquivos:
            assert arquivo["tamanho"] > 0
    
    def test_caminho_absoluto(self, diretorio_com_arquivos):
        """Testa que caminho é absoluto."""
        arquivos = gerenciar_arquivos(diretorio_com_arquivos)
        
        for arquivo in arquivos:
            assert Path(arquivo["caminho"]).is_absolute() or os.path.exists(arquivo["caminho"])


class TestCriarEstruturaProjeto:
    """Testes para a função criar_estrutura_projeto."""
    
    def test_criar_projeto_sucesso(self, diretorio_teste):
        """Testa criação de projeto com sucesso."""
        os.chdir(diretorio_teste)
        
        resultado = criar_estrutura_projeto("meu_projeto")
        
        assert resultado is True
        assert Path("meu_projeto").exists()
    
    def test_criar_diretorios(self, diretorio_teste):
        """Testa que cria todos os diretórios."""
        os.chdir(diretorio_teste)
        criar_estrutura_projeto("meu_projeto")
        
        diretorios_esperados = [
            "meu_projeto/src",
            "meu_projeto/tests",
            "meu_projeto/docs",
            "meu_projeto/scripts",
            "meu_projeto/config",
            "meu_projeto/.github/workflows"
        ]
        
        for diretorio in diretorios_esperados:
            assert Path(diretorio).exists(), f"Diretorio {diretorio} nao foi criado"
    
    def test_criar_arquivos(self, diretorio_teste):
        """Testa que cria todos os arquivos."""
        os.chdir(diretorio_teste)
        criar_estrutura_projeto("meu_projeto")
        
        arquivos_esperados = [
            "meu_projeto/README.md",
            "meu_projeto/requirements.txt",
            "meu_projeto/.gitignore",
            "meu_projeto/Dockerfile"
        ]
        
        for arquivo in arquivos_esperados:
            assert Path(arquivo).exists(), f"Arquivo {arquivo} nao foi criado"
    
    def test_conteudo_readme(self, diretorio_teste):
        """Testa conteúdo do README."""
        os.chdir(diretorio_teste)
        criar_estrutura_projeto("meu_projeto")
        
        readme = Path("meu_projeto/README.md").read_text()
        
        assert "meu_projeto" in readme
    
    def test_conteudo_dockerfile(self, diretorio_teste):
        """Testa conteúdo do Dockerfile."""
        os.chdir(diretorio_teste)
        criar_estrutura_projeto("meu_projeto")
        
        dockerfile = Path("meu_projeto/Dockerfile").read_text()
        
        assert "FROM python" in dockerfile
        assert "WORKDIR" in dockerfile
    
    def test_criar_gitignore(self, diretorio_teste):
        """Testa conteúdo do .gitignore."""
        os.chdir(diretorio_teste)
        criar_estrutura_projeto("meu_projeto")
        
        gitignore = Path("meu_projeto/.gitignore").read_text()
        
        assert "__pycache__" in gitignore
        assert ".env" in gitignore