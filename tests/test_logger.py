"""
Testes para o módulo de logging.
"""

import os
import logging
import tempfile
import shutil
from pathlib import Path
import pytest

from utils.logger import (
    configurar_logger,
    criar_log_rotativo,
    log_operacao
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
    yield temp_dir
    # Fechar handlers antes de remover
    fechar_handlers_logger("teste_rotativo")
    # Aguardar um pouco para liberar arquivos
    import time
    time.sleep(0.1)
    # Tentar remover com tratamento de erro
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    except PermissionError:
        pass  # Ignorar se não conseguir remover


@pytest.fixture(autouse=True)
def limpar_handlers():
    """Limpa handlers após cada teste."""
    yield
    # Remove todos os handlers de todos os loggers de teste
    for name in ["teste_logger", "teste_rotativo", "teste_operacao"]:
        fechar_handlers_logger(name)


class TestConfigurarLogger:
    """Testes para a função configurar_logger."""
    
    def test_criar_logger_basico(self):
        """Testa criação de logger básico."""
        logger = configurar_logger("teste_logger")
        
        assert logger is not None
        assert logger.name == "teste_logger"
        assert logger.level == logging.INFO
    
    def test_logger_nivel_personalizado(self):
        """Testa logger com nível personalizado."""
        logger = configurar_logger("teste_logger", nivel=logging.DEBUG)
        
        assert logger.level == logging.DEBUG
    
    def test_logger_possui_handlers(self):
        """Testa que logger possui handlers configurados."""
        logger = configurar_logger("teste_logger")
        
        # Deve ter handler de arquivo e console
        assert len(logger.handlers) >= 1
    
    def test_evita_duplicacao_handlers(self):
        """Testa que não duplica handlers em chamadas repetidas."""
        logger1 = configurar_logger("teste_logger")
        num_handlers = len(logger1.handlers)
        
        logger2 = configurar_logger("teste_logger")
        
        assert logger1 is logger2
        assert len(logger2.handlers) == num_handlers


class TestCriarLogRotativo:
    """Testes para a função criar_log_rotativo."""
    
    def test_criar_logger_rotativo(self, diretorio_teste):
        """Testa criação de logger com rotação."""
        logger = criar_log_rotativo(
            nome="teste_rotativo",
            diretorio_logs=diretorio_teste
        )
        
        assert logger is not None
        assert logger.name == "teste_rotativo"
    
    def test_cria_diretorio_logs(self, diretorio_teste):
        """Testa que cria diretório de logs se não existir."""
        subdir = Path(diretorio_teste) / "logs_novos"
        
        criar_log_rotativo(
            nome="teste_rotativo",
            diretorio_logs=str(subdir)
        )
        
        assert subdir.exists()


class TestLogOperacao:
    """Testes para a função log_operacao."""
    
    def test_log_operacao_sucesso(self, caplog):
        """Testa log de operação bem-sucedida."""
        logger = logging.getLogger("teste_operacao")
        logger.setLevel(logging.INFO)
        
        with caplog.at_level(logging.INFO):
            log_operacao(logger, "TESTE", sucesso=True, detalhes="Operacao OK")
        
        assert "SUCESSO" in caplog.text
        assert "TESTE" in caplog.text
    
    def test_log_operacao_falha(self, caplog):
        """Testa log de operação com falha."""
        logger = logging.getLogger("teste_operacao")
        logger.setLevel(logging.ERROR)
        
        with caplog.at_level(logging.ERROR):
            log_operacao(logger, "TESTE", sucesso=False, detalhes="Erro encontrado")
        
        assert "FALHA" in caplog.text
    
    def test_log_operacao_sem_detalhes(self, caplog):
        """Testa log de operação sem detalhes."""
        logger = logging.getLogger("teste_operacao")
        logger.setLevel(logging.INFO)
        
        with caplog.at_level(logging.INFO):
            log_operacao(logger, "TESTE", sucesso=True)
        
        assert "TESTE" in caplog.text