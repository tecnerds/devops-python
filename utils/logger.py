"""
Módulo de configuração e utilitários de logging para automação DevOps.
Autor: Patrick
Data: Dezembro 2025
"""

import logging
from pathlib import Path
from datetime import datetime


def configurar_logger(
    nome: str = "devops_automation",
    nivel: int = logging.INFO,
    arquivo_log: str = "devops_automation.log",
    formato: str = "%(asctime)s - %(levelname)s - %(message)s"
) -> logging.Logger:
    """
    Configura e retorna um logger personalizado.
    
    Args:
        nome: Nome do logger
        nivel: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        arquivo_log: Nome do arquivo de log
        formato: Formato das mensagens de log
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(nome)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(nivel)
    
    # Formatter
    formatter = logging.Formatter(formato)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(arquivo_log, encoding='utf-8')
    file_handler.setLevel(nivel)
    file_handler.setFormatter(formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(nivel)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def criar_log_rotativo(
    nome: str = "devops_automation",
    diretorio_logs: str = "logs",
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Cria um logger com rotação de arquivos.
    
    Args:
        nome: Nome do logger
        diretorio_logs: Diretório para armazenar logs
        max_bytes: Tamanho máximo do arquivo antes de rotacionar
        backup_count: Número de arquivos de backup a manter
        
    Returns:
        Logger configurado com rotação
    """
    from logging.handlers import RotatingFileHandler
    
    # Criar diretório de logs se não existir
    Path(diretorio_logs).mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(nome)
    
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Handler rotativo
    arquivo_log = Path(diretorio_logs) / f"{nome}.log"
    rotating_handler = RotatingFileHandler(
        arquivo_log,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    rotating_handler.setFormatter(formatter)
    
    # Handler console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(rotating_handler)
    logger.addHandler(console_handler)
    
    return logger


def log_operacao(logger: logging.Logger, operacao: str, sucesso: bool, detalhes: str = ""):
    """
    Registra uma operação no log com formato padronizado.
    
    Args:
        logger: Logger a ser utilizado
        operacao: Nome da operação realizada
        sucesso: Se a operação foi bem-sucedida
        detalhes: Detalhes adicionais sobre a operação
    """
    status = "✓ SUCESSO" if sucesso else "✗ FALHA"
    mensagem = f"[{operacao}] {status}"
    
    if detalhes:
        mensagem += f" - {detalhes}"
    
    if sucesso:
        logger.info(mensagem)
    else:
        logger.error(mensagem)


# Logger padrão para uso direto
logger = configurar_logger()