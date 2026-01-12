"""
Módulo de utilitários de sistema para automação DevOps.
Autor: Patrick
Data: Dezembro 2025

Contém funções para obter informações do sistema e executar comandos.
"""

import sys
import os
import subprocess
from datetime import datetime
from pathlib import Path

from .logger import configurar_logger

# Logger do módulo
logger = configurar_logger("sistema")


def verificar_python_version() -> bool:
    """Verifica a versão do Python instalada."""
    versao = sys.version_info
    logger.info(f"Python versão: {versao.major}.{versao.minor}.{versao.micro}")
    
    if versao.major < 3 or (versao.major == 3 and versao.minor < 8):
        logger.warning("Recomendado Python 3.8 ou superior!")
        return False
    return True


def obter_informacoes_sistema() -> dict:
    """Obtém informações do sistema operacional."""
    info = {
        "plataforma": sys.platform,
        "versao_python": sys.version,
        "executavel": sys.executable,
        "path": sys.path[:3],
        "diretorio_atual": os.getcwd(),
        "usuario": os.environ.get('USERNAME', os.environ.get('USER', 'Desconhecido'))
    }
    return info


def executar_comando(comando: str, timeout: int = 60) -> dict:
    """
    Executa um comando no shell e retorna o resultado.
    
    Args:
        comando: Comando a ser executado
        timeout: Tempo máximo de execução em segundos
        
    Returns:
        Dicionário com stdout, stderr e código de retorno
    """
    logger.info(f"Executando comando: {comando}")
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "sucesso": resultado.returncode == 0,
            "stdout": resultado.stdout.strip(),
            "stderr": resultado.stderr.strip(),
            "codigo_retorno": resultado.returncode
        }
    except subprocess.TimeoutExpired:
        logger.error(f"Timeout ao executar: {comando}")
        return {"sucesso": False, "erro": "Timeout"}
    except Exception as e:
        logger.error(f"Erro ao executar comando: {e}")
        return {"sucesso": False, "erro": str(e)}


def verificar_ferramentas_devops() -> dict:
    """Verifica se as ferramentas comuns de DevOps estão instaladas."""
    ferramentas = {
        "git": "git --version",
        "docker": "docker --version",
        "python": "python --version",
        "pip": "pip --version",
        "node": "node --version",
        "npm": "npm --version"
    }
    
    resultados = {}
    for nome, comando in ferramentas.items():
        resultado = executar_comando(comando)
        if resultado.get("sucesso"):
            resultados[nome] = {
                "instalado": True,
                "versao": resultado.get("stdout", "")
            }
            logger.info(f"✓ {nome}: {resultado.get('stdout', '')}")
        else:
            resultados[nome] = {"instalado": False}
            logger.warning(f"✗ {nome}: não encontrado")
    
    return resultados


def monitorar_recursos() -> dict:
    """Monitora recursos do sistema."""
    try:
        import psutil
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memoria": {
                "total": psutil.virtual_memory().total,
                "disponivel": psutil.virtual_memory().available,
                "percentual": psutil.virtual_memory().percent
            },
            "disco": {
                "total": psutil.disk_usage('/').total,
                "usado": psutil.disk_usage('/').used,
                "percentual": psutil.disk_usage('/').percent
            }
        }
    except ImportError:
        logger.warning("psutil não instalado. Instale com: pip install psutil")
        return {"erro": "psutil não disponível"}