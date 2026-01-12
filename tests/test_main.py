"""
Testes unitários para o projeto de automação DevOps.
"""

import pytest
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import (
    verificar_python_version,
    obter_informacoes_sistema,
    executar_comando,
    gerenciar_arquivos
)


class TestPythonVersion:
    """Testes para verificação de versão do Python."""
    
    def test_verificar_python_version_retorna_bool(self):
        resultado = verificar_python_version()
        assert isinstance(resultado, bool)
    
    def test_versao_atual_compativel(self):
        # Python 3.8+ é requerido
        assert sys.version_info >= (3, 8)


class TestInformacoesSistema:
    """Testes para obtenção de informações do sistema."""
    
    def test_obter_informacoes_retorna_dict(self):
        info = obter_informacoes_sistema()
        assert isinstance(info, dict)
    
    def test_informacoes_contem_campos_obrigatorios(self):
        info = obter_informacoes_sistema()
        campos = ['plataforma', 'versao_python', 'executavel', 'diretorio_atual']
        for campo in campos:
            assert campo in info


class TestExecutarComando:
    """Testes para execução de comandos."""
    
    def test_comando_simples_retorna_dict(self):
        resultado = executar_comando("echo teste")
        assert isinstance(resultado, dict)
    
    def test_comando_sucesso(self):
        resultado = executar_comando("echo hello")
        assert resultado.get('sucesso') == True
    
    def test_comando_invalido(self):
        resultado = executar_comando("comando_que_nao_existe_xyz")
        assert resultado.get('sucesso') == False


class TestGerenciarArquivos:
    """Testes para gerenciamento de arquivos."""
    
    def test_diretorio_inexistente(self):
        resultado = gerenciar_arquivos("/caminho/que/nao/existe")
        assert resultado == []
    
    def test_diretorio_atual(self):
        resultado = gerenciar_arquivos(".")
        assert isinstance(resultado, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])