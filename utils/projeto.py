"""
Módulo para gerenciamento de projetos DevOps.
Autor: Patrick
Data: Dezembro 2025

Contém funções para criar e gerenciar estruturas de projeto.
"""

from datetime import datetime
from pathlib import Path

from .logger import configurar_logger

# Logger do módulo
logger = configurar_logger("projeto")


def gerenciar_arquivos(diretorio: str, extensao: str = None) -> list:
    """
    Lista e gerencia arquivos em um diretório.
    
    Args:
        diretorio: Caminho do diretório
        extensao: Filtrar por extensão (ex: '.py')
        
    Returns:
        Lista de arquivos encontrados
    """
    path = Path(diretorio)
    
    if not path.exists():
        logger.error(f"Diretório não encontrado: {diretorio}")
        return []
    
    arquivos = []
    for arquivo in path.rglob("*"):
        if arquivo.is_file():
            if extensao is None or arquivo.suffix == extensao:
                arquivos.append({
                    "nome": arquivo.name,
                    "caminho": str(arquivo),
                    "tamanho": arquivo.stat().st_size,
                    "modificado": datetime.fromtimestamp(
                        arquivo.stat().st_mtime
                    ).isoformat()
                })
    
    logger.info(f"Encontrados {len(arquivos)} arquivos em {diretorio}")
    return arquivos


def criar_estrutura_projeto(nome_projeto: str) -> bool:
    """
    Cria estrutura padrão de um projeto DevOps.
    
    Args:
        nome_projeto: Nome do projeto a ser criado
        
    Returns:
        True se criado com sucesso
    """
    estrutura = [
        f"{nome_projeto}/src",
        f"{nome_projeto}/tests",
        f"{nome_projeto}/docs",
        f"{nome_projeto}/scripts",
        f"{nome_projeto}/config",
        f"{nome_projeto}/.github/workflows"
    ]
    
    arquivos = {
        f"{nome_projeto}/README.md": f"# {nome_projeto}\n\nProjeto de automação DevOps.\n",
        f"{nome_projeto}/requirements.txt": "# Dependências do projeto\npytest>=7.0.0\nrequests>=2.28.0\npython-dotenv>=1.0.0\n",
        f"{nome_projeto}/.gitignore": "*.pyc\n__pycache__/\n.env\nvenv/\n*.log\n.pytest_cache/\n",
        f"{nome_projeto}/Dockerfile": """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
""",
        f"{nome_projeto}/.github/workflows/ci.yml": """name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: pytest tests/
"""
    }
    
    try:
        # Criar diretórios
        for pasta in estrutura:
            Path(pasta).mkdir(parents=True, exist_ok=True)
            logger.info(f"Criado diretório: {pasta}")
        
        # Criar arquivos
        for arquivo, conteudo in arquivos.items():
            Path(arquivo).write_text(conteudo, encoding='utf-8')
            logger.info(f"Criado arquivo: {arquivo}")
        
        logger.info(f"✓ Projeto '{nome_projeto}' criado com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"Erro ao criar projeto: {e}")
        return False