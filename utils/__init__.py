"""
Módulo de utilitários para automação DevOps.
"""

from .git_utils import (
    verificar_repositorio,
    obter_branch_atual,
    obter_status,
    fazer_commit,
    fazer_push,
    fazer_pull,
    listar_branches,
    obter_log
)

from .docker_utils import (
    listar_containers,
    listar_imagens,
    build_imagem,
    executar_container,
    parar_container,
    remover_container
)

from .logger import (
    configurar_logger,
    criar_log_rotativo,
    log_operacao,
    logger
)

from .backup import (
    realizar_backup,
    restaurar_backup,
    listar_backups,
    limpar_backups_antigos,
    formatar_tamanho
)

from .sistema import (
    verificar_python_version,
    obter_informacoes_sistema,
    executar_comando,
    verificar_ferramentas_devops,
    monitorar_recursos
)

from .projeto import (
    gerenciar_arquivos,
    criar_estrutura_projeto
)

__all__ = [
    # Git
    'verificar_repositorio',
    'obter_branch_atual',
    'obter_status',
    'fazer_commit',
    'fazer_push',
    'fazer_pull',
    'listar_branches',
    'obter_log',
    # Docker
    'listar_containers',
    'listar_imagens',
    'build_imagem',
    'executar_container',
    'parar_container',
    'remover_container',
    # Logger
    'configurar_logger',
    'criar_log_rotativo',
    'log_operacao',
    'logger',
    # Backup
    'realizar_backup',
    'restaurar_backup',
    'listar_backups',
    'limpar_backups_antigos',
    'formatar_tamanho',
    # Sistema
    'verificar_python_version',
    'obter_informacoes_sistema',
    'executar_comando',
    'verificar_ferramentas_devops',
    'monitorar_recursos',
    # Projeto
    'gerenciar_arquivos',
    'criar_estrutura_projeto'
]