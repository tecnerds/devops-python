"""
Módulo de backup para automação DevOps.
Autor: Patrick
Data: Dezembro 2025

Contém funções para realizar backup de diretórios.
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from .logger import configurar_logger, log_operacao

# Logger do módulo
logger = configurar_logger("backup")


def realizar_backup(
    diretorio_origem: str,
    diretorio_destino: str,
    compactar: bool = False,
    formato_compactacao: str = "zip"
) -> dict:
    """
    Realiza backup de um diretório de origem para um diretório de destino.
    
    Args:
        diretorio_origem: Caminho do diretório a ser copiado
        diretorio_destino: Caminho onde o backup será salvo
        compactar: Se True, cria um arquivo compactado do backup
        formato_compactacao: Formato de compactação ('zip', 'tar', 'gztar', 'bztar')
        
    Returns:
        Dicionário com informações do backup realizado
    """
    resultado = {
        "sucesso": False,
        "origem": diretorio_origem,
        "destino": None,
        "arquivos_copiados": 0,
        "tamanho_total": 0,
        "timestamp": datetime.now().isoformat(),
        "erro": None
    }
    
    try:
        # Validar diretório de origem
        origem = Path(diretorio_origem)
        if not origem.exists():
            raise FileNotFoundError(f"Diretório de origem não encontrado: {diretorio_origem}")
        
        if not origem.is_dir():
            raise NotADirectoryError(f"O caminho especificado não é um diretório: {diretorio_origem}")
        
        # Criar nome do backup com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_backup = f"{origem.name}_backup_{timestamp}"
        
        destino = Path(diretorio_destino)
        destino.mkdir(parents=True, exist_ok=True)
        
        caminho_backup = destino / nome_backup
        
        logger.info(f"Iniciando backup de '{diretorio_origem}' para '{caminho_backup}'")
        
        if compactar:
            # Criar backup compactado
            arquivo_compactado = shutil.make_archive(
                str(caminho_backup),
                formato_compactacao,
                root_dir=str(origem.parent),
                base_dir=origem.name
            )
            resultado["destino"] = arquivo_compactado
            resultado["tamanho_total"] = os.path.getsize(arquivo_compactado)
            resultado["arquivos_copiados"] = contar_arquivos(origem)
            logger.info(f"Backup compactado criado: {arquivo_compactado}")
        else:
            # Copiar diretório completo
            shutil.copytree(origem, caminho_backup)
            resultado["destino"] = str(caminho_backup)
            
            # Contar arquivos e calcular tamanho
            for arquivo in caminho_backup.rglob('*'):
                if arquivo.is_file():
                    resultado["arquivos_copiados"] += 1
                    resultado["tamanho_total"] += arquivo.stat().st_size
            
            logger.info(f"Backup criado: {caminho_backup}")
        
        resultado["sucesso"] = True
        log_operacao(
            logger, "BACKUP",
            sucesso=True,
            detalhes=f"Arquivos: {resultado['arquivos_copiados']}, "
                    f"Tamanho: {formatar_tamanho(resultado['tamanho_total'])}"
        )
        
    except FileNotFoundError as e:
        resultado["erro"] = str(e)
        log_operacao(logger, "BACKUP", sucesso=False, detalhes=str(e))
    except PermissionError as e:
        resultado["erro"] = f"Permissão negada: {e}"
        log_operacao(logger, "BACKUP", sucesso=False, detalhes=f"Permissão negada: {e}")
    except Exception as e:
        resultado["erro"] = str(e)
        log_operacao(logger, "BACKUP", sucesso=False, detalhes=str(e))
    
    return resultado


def restaurar_backup(
    arquivo_backup: str,
    diretorio_destino: str,
    sobrescrever: bool = False
) -> dict:
    """
    Restaura um backup para o diretório de destino.
    
    Args:
        arquivo_backup: Caminho do arquivo/diretório de backup
        diretorio_destino: Caminho onde restaurar o backup
        sobrescrever: Se True, sobrescreve arquivos existentes
        
    Returns:
        Dicionário com informações da restauração
    """
    resultado = {
        "sucesso": False,
        "origem": arquivo_backup,
        "destino": diretorio_destino,
        "timestamp": datetime.now().isoformat(),
        "erro": None
    }
    
    try:
        backup_path = Path(arquivo_backup)
        destino_path = Path(diretorio_destino)
        
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup não encontrado: {arquivo_backup}")
        
        # Verificar se destino existe
        if destino_path.exists() and not sobrescrever:
            raise FileExistsError(f"Destino já existe: {diretorio_destino}. Use sobrescrever=True")
        
        logger.info(f"Restaurando backup de '{arquivo_backup}' para '{diretorio_destino}'")
        
        # Verificar se é arquivo compactado
        if backup_path.suffix in ['.zip', '.tar', '.gz', '.bz2']:
            shutil.unpack_archive(str(backup_path), str(destino_path))
        else:
            # Copiar diretório
            if destino_path.exists() and sobrescrever:
                shutil.rmtree(destino_path)
            shutil.copytree(backup_path, destino_path)
        
        resultado["sucesso"] = True
        log_operacao(logger, "RESTAURAR", sucesso=True, detalhes=f"Restaurado em: {diretorio_destino}")
        
    except Exception as e:
        resultado["erro"] = str(e)
        log_operacao(logger, "RESTAURAR", sucesso=False, detalhes=str(e))
    
    return resultado


def listar_backups(diretorio: str, padrao: str = "*_backup_*") -> list:
    """
    Lista todos os backups em um diretório.
    
    Args:
        diretorio: Diretório onde procurar backups
        padrao: Padrão glob para filtrar backups
        
    Returns:
        Lista de backups encontrados com informações
    """
    backups = []
    path = Path(diretorio)
    
    if not path.exists():
        logger.warning(f"Diretório não encontrado: {diretorio}")
        return backups
    
    for item in path.glob(padrao):
        info = {
            "nome": item.name,
            "caminho": str(item),
            "tipo": "diretorio" if item.is_dir() else "arquivo",
            "tamanho": calcular_tamanho(item),
            "criado": datetime.fromtimestamp(item.stat().st_ctime).isoformat(),
            "modificado": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
        }
        backups.append(info)
    
    # Ordenar por data de modificação (mais recente primeiro)
    backups.sort(key=lambda x: x["modificado"], reverse=True)
    
    logger.info(f"Encontrados {len(backups)} backups em '{diretorio}'")
    return backups


def limpar_backups_antigos(
    diretorio: str,
    dias: int = 30,
    manter_minimo: int = 3
) -> dict:
    """
    Remove backups mais antigos que o número de dias especificado.
    
    Args:
        diretorio: Diretório onde estão os backups
        dias: Idade máxima dos backups em dias
        manter_minimo: Número mínimo de backups a manter
        
    Returns:
        Dicionário com informações da limpeza
    """
    resultado = {
        "sucesso": False,
        "removidos": [],
        "mantidos": 0,
        "espaco_liberado": 0,
        "erro": None
    }
    
    try:
        backups = listar_backups(diretorio)
        
        if len(backups) <= manter_minimo:
            resultado["sucesso"] = True
            resultado["mantidos"] = len(backups)
            logger.info(f"Mantendo todos os {len(backups)} backups (mínimo: {manter_minimo})")
            return resultado
        
        data_limite = datetime.now().timestamp() - (dias * 24 * 60 * 60)
        
        # Manter os mais recentes
        backups_para_manter = backups[:manter_minimo]
        backups_para_verificar = backups[manter_minimo:]
        
        for backup in backups_para_verificar:
            backup_path = Path(backup["caminho"])
            if backup_path.stat().st_mtime < data_limite:
                tamanho = backup["tamanho"]
                
                if backup_path.is_dir():
                    shutil.rmtree(backup_path)
                else:
                    backup_path.unlink()
                
                resultado["removidos"].append(backup["nome"])
                resultado["espaco_liberado"] += tamanho
                logger.info(f"Removido backup antigo: {backup['nome']}")
        
        resultado["sucesso"] = True
        resultado["mantidos"] = len(backups) - len(resultado["removidos"])
        
        log_operacao(
            logger, "LIMPEZA",
            sucesso=True,
            detalhes=f"Removidos: {len(resultado['removidos'])}, "
                    f"Espaço liberado: {formatar_tamanho(resultado['espaco_liberado'])}"
        )
        
    except Exception as e:
        resultado["erro"] = str(e)
        log_operacao(logger, "LIMPEZA", sucesso=False, detalhes=str(e))
    
    return resultado


# Funções auxiliares

def contar_arquivos(diretorio: Path) -> int:
    """Conta o número de arquivos em um diretório recursivamente."""
    return sum(1 for _ in diretorio.rglob('*') if _.is_file())


def calcular_tamanho(path: Path) -> int:
    """Calcula o tamanho total de um arquivo ou diretório."""
    if path.is_file():
        return path.stat().st_size
    return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())


def formatar_tamanho(bytes: int) -> str:
    """Formata tamanho em bytes para formato legível."""
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unidade}"
        bytes /= 1024
    return f"{bytes:.2f} PB"