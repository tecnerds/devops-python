"""
Configurações e fixtures compartilhadas para os testes.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def diretorio_projeto():
    """Retorna o diretório raiz do projeto."""
    return Path(__file__).parent.parent


@pytest.fixture
def temp_dir():
    """Cria um diretório temporário que é limpo após o teste."""
    temp = tempfile.mkdtemp()
    yield temp
    if os.path.exists(temp):
        shutil.rmtree(temp)