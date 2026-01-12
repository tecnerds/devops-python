"""
Projeto: Python para Automação em DevOps - Atividade Final
Autor: Patrick
Data: Dezembro 2025

Script principal que integra os módulos e executa as operações.
"""

import sys
import json
import argparse

# Importar módulos do projeto
from utils.logger import configurar_logger
from utils.backup import realizar_backup, listar_backups, limpar_backups_antigos
from utils.sistema import (
    verificar_python_version,
    obter_informacoes_sistema,
    verificar_ferramentas_devops,
    monitorar_recursos
)
from utils.projeto import gerenciar_arquivos, criar_estrutura_projeto

# Configurar logger principal
logger = configurar_logger("main")


def main():
    """Função principal do programa."""
    parser = argparse.ArgumentParser(
        description="Ferramenta de Automação DevOps em Python"
    )
    parser.add_argument(
        '--acao', 
        choices=['info', 'ferramentas', 'criar-projeto', 'listar', 'monitorar', 'backup', 'listar-backups', 'limpar-backups'],
        default='info',
        help='Ação a ser executada'
    )
    parser.add_argument(
        '--projeto',
        type=str,
        default='meu_projeto',
        help='Nome do projeto (para criar-projeto)'
    )
    parser.add_argument(
        '--diretorio',
        type=str,
        default='.',
        help='Diretório de origem para operações'
    )
    parser.add_argument(
        '--destino',
        type=str,
        default='./backups',
        help='Diretório de destino para backups'
    )
    parser.add_argument(
        '--compactar',
        action='store_true',
        help='Compactar backup em ZIP'
    )
    parser.add_argument(
        '--dias',
        type=int,
        default=30,
        help='Dias para manter backups (para limpar-backups)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("  AUTOMAÇÃO DEVOPS COM PYTHON")
    print("=" * 60)
    
    verificar_python_version()
    
    if args.acao == 'info':
        info = obter_informacoes_sistema()
        print("\n📋 Informações do Sistema:")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        
    elif args.acao == 'ferramentas':
        print("\n🔧 Verificando ferramentas DevOps...")
        verificar_ferramentas_devops()
        
    elif args.acao == 'criar-projeto':
        print(f"\n📁 Criando projeto: {args.projeto}")
        criar_estrutura_projeto(args.projeto)
        
    elif args.acao == 'listar':
        print(f"\n📂 Listando arquivos em: {args.diretorio}")
        arquivos = gerenciar_arquivos(args.diretorio, '.py')
        for arq in arquivos[:10]:
            print(f"  - {arq['nome']} ({arq['tamanho']} bytes)")
            
    elif args.acao == 'monitorar':
        print("\n📊 Monitoramento de recursos:")
        recursos = monitorar_recursos()
        print(json.dumps(recursos, indent=2))
        
    elif args.acao == 'backup':
        print(f"\n💾 Realizando backup de: {args.diretorio}")
        resultado = realizar_backup(
            diretorio_origem=args.diretorio,
            diretorio_destino=args.destino,
            compactar=args.compactar
        )
        if resultado["sucesso"]:
            print(f"✓ Backup salvo em: {resultado['destino']}")
            print(f"  Arquivos: {resultado['arquivos_copiados']}")
            print(f"  Tamanho: {resultado['tamanho_total'] / 1024:.2f} KB")
        else:
            print(f"✗ Erro: {resultado['erro']}")
            
    elif args.acao == 'listar-backups':
        print(f"\n📋 Listando backups em: {args.destino}")
        backups = listar_backups(args.destino)
        for backup in backups:
            print(f"  - {backup['nome']} ({backup['tipo']}, {backup['tamanho'] / 1024:.2f} KB)")
            
    elif args.acao == 'limpar-backups':
        print(f"\n🧹 Limpando backups antigos (>{args.dias} dias)")
        resultado = limpar_backups_antigos(args.destino, dias=args.dias)
        if resultado["sucesso"]:
            print(f"✓ Removidos: {len(resultado['removidos'])} backups")
            print(f"  Espaço liberado: {resultado['espaco_liberado'] / 1024:.2f} KB")
        else:
            print(f"✗ Erro: {resultado['erro']}")
    
    print("\n" + "=" * 60)
    print("  Execução finalizada!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())