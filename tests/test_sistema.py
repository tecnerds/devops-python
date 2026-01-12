"""
Testes para o módulo de sistema.
"""

import sys
import pytest

from utils.sistema import (
    verificar_python_version,
    obter_informacoes_sistema,
    executar_comando,
    verificar_ferramentas_devops,
    monitorar_recursos
)


class TestVerificarPythonVersion:
    """Testes para a função verificar_python_version."""
    
    def test_versao_python_atual(self):
        """Testa verificação da versão atual do Python."""
        resultado = verificar_python_version()
        
        # Python 3.8+ deve retornar True
        if sys.version_info >= (3, 8):
            assert resultado is True
        else:
            assert resultado is False
    
    def test_retorna_booleano(self):
        """Testa que retorna um booleano."""
        resultado = verificar_python_version()
        
        assert isinstance(resultado, bool)


class TestObterInformacoesSistema:
    """Testes para a função obter_informacoes_sistema."""
    
    def test_retorna_dicionario(self):
        """Testa que retorna um dicionário."""
        info = obter_informacoes_sistema()
        
        assert isinstance(info, dict)
    
    def test_contem_chaves_esperadas(self):
        """Testa que contém as chaves esperadas."""
        info = obter_informacoes_sistema()
        
        chaves_esperadas = [
            "plataforma",
            "versao_python",
            "executavel",
            "path",
            "diretorio_atual",
            "usuario"
        ]
        
        for chave in chaves_esperadas:
            assert chave in info
    
    def test_plataforma_valida(self):
        """Testa que plataforma é válida."""
        info = obter_informacoes_sistema()
        
        plataformas_validas = ["win32", "linux", "darwin", "cygwin"]
        assert info["plataforma"] in plataformas_validas
    
    def test_versao_python_nao_vazia(self):
        """Testa que versão Python não está vazia."""
        info = obter_informacoes_sistema()
        
        assert len(info["versao_python"]) > 0


class TestExecutarComando:
    """Testes para a função executar_comando."""
    
    def test_comando_sucesso(self):
        """Testa execução de comando com sucesso."""
        resultado = executar_comando("python --version")
        
        assert resultado["sucesso"] is True
        assert "Python" in resultado["stdout"]
    
    def test_comando_invalido(self):
        """Testa execução de comando inválido."""
        resultado = executar_comando("comando_inexistente_xyz")
        
        assert resultado["sucesso"] is False
    
    def test_retorna_dicionario(self):
        """Testa que retorna um dicionário."""
        resultado = executar_comando("echo teste")
        
        assert isinstance(resultado, dict)
    
    def test_comando_echo(self):
        """Testa comando echo."""
        if sys.platform == "win32":
            resultado = executar_comando("echo teste")
        else:
            resultado = executar_comando("echo teste")
        
        assert resultado["sucesso"] is True
        assert "teste" in resultado["stdout"]
    
    def test_timeout_comando(self):
        """Testa timeout de comando."""
        # Comando que demora (ping com timeout curto)
        if sys.platform == "win32":
            resultado = executar_comando("ping -n 10 localhost", timeout=1)
        else:
            resultado = executar_comando("sleep 10", timeout=1)
        
        assert resultado["sucesso"] is False
        assert "Timeout" in resultado.get("erro", "")


class TestVerificarFerramentasDevops:
    """Testes para a função verificar_ferramentas_devops."""
    
    def test_retorna_dicionario(self):
        """Testa que retorna um dicionário."""
        resultado = verificar_ferramentas_devops()
        
        assert isinstance(resultado, dict)
    
    def test_verifica_python(self):
        """Testa que verifica Python."""
        resultado = verificar_ferramentas_devops()
        
        assert "python" in resultado
        assert resultado["python"]["instalado"] is True
    
    def test_verifica_pip(self):
        """Testa que verifica pip."""
        resultado = verificar_ferramentas_devops()
        
        assert "pip" in resultado
        assert resultado["pip"]["instalado"] is True
    
    def test_estrutura_resultado(self):
        """Testa estrutura do resultado para cada ferramenta."""
        resultado = verificar_ferramentas_devops()
        
        for ferramenta, info in resultado.items():
            assert "instalado" in info
            if info["instalado"]:
                assert "versao" in info


class TestMonitorarRecursos:
    """Testes para a função monitorar_recursos."""
    
    def test_retorna_dicionario(self):
        """Testa que retorna um dicionário."""
        resultado = monitorar_recursos()
        
        assert isinstance(resultado, dict)
    
    def test_com_psutil_instalado(self):
        """Testa quando psutil está instalado."""
        resultado = monitorar_recursos()
        
        # Se psutil não está instalado, deve retornar erro
        if "erro" not in resultado:
            assert "cpu_percent" in resultado
            assert "memoria" in resultado
            assert "disco" in resultado
    
    def test_valores_memoria(self):
        """Testa valores de memória."""
        resultado = monitorar_recursos()
        
        if "memoria" in resultado:
            mem = resultado["memoria"]
            assert mem["total"] > 0
            assert 0 <= mem["percentual"] <= 100