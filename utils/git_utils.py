"""
Utilitários para automação Git.
"""

import subprocess
import os
from typing import Optional, List


def verificar_repositorio() -> bool:
    """Verifica se o diretório atual é um repositório Git."""
    resultado = subprocess.run(
        "git rev-parse --is-inside-work-tree",
        shell=True,
        capture_output=True,
        text=True
    )
    return resultado.returncode == 0


def obter_branch_atual() -> Optional[str]:
    """Retorna o nome da branch atual."""
    resultado = subprocess.run(
        "git branch --show-current",
        shell=True,
        capture_output=True,
        text=True
    )
    if resultado.returncode == 0:
        return resultado.stdout.strip()
    return None


def obter_status() -> dict:
    """Obtém o status do repositório."""
    resultado = subprocess.run(
        "git status --porcelain",
        shell=True,
        capture_output=True,
        text=True
    )
    
    arquivos_modificados = []
    arquivos_novos = []
    arquivos_deletados = []
    
    for linha in resultado.stdout.strip().split('\n'):
        if linha:
            status = linha[:2]
            arquivo = linha[3:]
            
            if 'M' in status:
                arquivos_modificados.append(arquivo)
            elif '?' in status:
                arquivos_novos.append(arquivo)
            elif 'D' in status:
                arquivos_deletados.append(arquivo)
    
    return {
        "modificados": arquivos_modificados,
        "novos": arquivos_novos,
        "deletados": arquivos_deletados,
        "limpo": len(resultado.stdout.strip()) == 0
    }


def fazer_commit(mensagem: str, adicionar_todos: bool = True) -> bool:
    """Realiza um commit."""
    if adicionar_todos:
        subprocess.run("git add -A", shell=True)
    
    resultado = subprocess.run(
        f'git commit -m "{mensagem}"',
        shell=True,
        capture_output=True,
        text=True
    )
    return resultado.returncode == 0


def fazer_push(branch: Optional[str] = None) -> bool:
    """Envia alterações para o remoto."""
    comando = "git push"
    if branch:
        comando += f" origin {branch}"
    
    resultado = subprocess.run(comando, shell=True, capture_output=True)
    return resultado.returncode == 0


def fazer_pull(branch: Optional[str] = None) -> bool:
    """Puxa alterações do remoto."""
    comando = "git pull"
    if branch:
        comando += f" origin {branch}"
    
    resultado = subprocess.run(comando, shell=True, capture_output=True)
    return resultado.returncode == 0


def listar_branches() -> List[str]:
    """Lista todas as branches."""
    resultado = subprocess.run(
        "git branch -a",
        shell=True,
        capture_output=True,
        text=True
    )
    
    branches = []
    for linha in resultado.stdout.strip().split('\n'):
        branch = linha.strip().replace('* ', '')
        if branch:
            branches.append(branch)
    return branches


def obter_log(limite: int = 10) -> List[dict]:
    """Obtém o histórico de commits."""
    formato = '%H|%an|%ae|%s|%ci'
    resultado = subprocess.run(
        f'git log --format="{formato}" -n {limite}',
        shell=True,
        capture_output=True,
        text=True
    )
    
    commits = []
    for linha in resultado.stdout.strip().split('\n'):
        if linha:
            partes = linha.split('|')
            if len(partes) >= 5:
                commits.append({
                    "hash": partes[0],
                    "autor": partes[1],
                    "email": partes[2],
                    "mensagem": partes[3],
                    "data": partes[4]
                })
    return commits