"""
Utilitários para automação Docker.
"""

import subprocess
import json
from typing import Optional, List, Dict


def listar_containers(apenas_ativos: bool = False) -> List[Dict]:
    """Lista containers Docker."""
    comando = "docker ps --format '{{json .}}'"
    if not apenas_ativos:
        comando = "docker ps -a --format '{{json .}}'"
    
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True
        )
        
        containers = []
        for linha in resultado.stdout.strip().split('\n'):
            if linha:
                containers.append(json.loads(linha))
        return containers
    except Exception as e:
        print(f"Erro ao listar containers: {e}")
        return []


def listar_imagens() -> List[Dict]:
    """Lista imagens Docker."""
    try:
        resultado = subprocess.run(
            "docker images --format '{{json .}}'",
            shell=True,
            capture_output=True,
            text=True
        )
        
        imagens = []
        for linha in resultado.stdout.strip().split('\n'):
            if linha:
                imagens.append(json.loads(linha))
        return imagens
    except Exception as e:
        print(f"Erro ao listar imagens: {e}")
        return []


def build_imagem(dockerfile_path: str, tag: str) -> bool:
    """Constrói uma imagem Docker."""
    comando = f"docker build -t {tag} -f {dockerfile_path} ."
    resultado = subprocess.run(comando, shell=True)
    return resultado.returncode == 0


def executar_container(imagem: str, nome: Optional[str] = None, 
                       portas: Optional[Dict[str, str]] = None) -> bool:
    """Executa um container Docker."""
    comando = f"docker run -d"
    
    if nome:
        comando += f" --name {nome}"
    
    if portas:
        for host, container in portas.items():
            comando += f" -p {host}:{container}"
    
    comando += f" {imagem}"
    
    resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
    
    if resultado.returncode == 0:
        print(f"Container iniciado: {resultado.stdout.strip()[:12]}")
        return True
    else:
        print(f"Erro: {resultado.stderr}")
        return False


def parar_container(container_id: str) -> bool:
    """Para um container Docker."""
    resultado = subprocess.run(
        f"docker stop {container_id}",
        shell=True,
        capture_output=True
    )
    return resultado.returncode == 0


def remover_container(container_id: str, force: bool = False) -> bool:
    """Remove um container Docker."""
    comando = f"docker rm {'-f ' if force else ''}{container_id}"
    resultado = subprocess.run(comando, shell=True, capture_output=True)
    return resultado.returncode == 0