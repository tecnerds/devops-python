"""
Testes para o script principal main.py.
"""

import sys
import os
import subprocess
import pytest


class TestMainScript:
    """Testes para o script principal."""
    
    def _run_main(self, *args):
        """Executa o main.py com encoding UTF-8."""
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        return subprocess.run(
            [sys.executable, "main.py"] + list(args),
            capture_output=True,
            text=True,
            env=env,
            encoding="utf-8",
            errors="replace"
        )
    
    def test_executar_acao_info(self):
        """Testa execução da ação info."""
        resultado = self._run_main("--acao", "info")
        
        assert resultado.returncode == 0
        assert "AUTOMACAO DEVOPS" in resultado.stdout
    
    def test_executar_acao_ferramentas(self):
        """Testa execução da ação ferramentas."""
        resultado = self._run_main("--acao", "ferramentas")
        
        assert resultado.returncode == 0
        assert "Verificando ferramentas" in resultado.stdout
    
    def test_executar_acao_monitorar(self):
        """Testa execução da ação monitorar."""
        resultado = self._run_main("--acao", "monitorar")
        
        assert resultado.returncode == 0
        assert "Monitoramento" in resultado.stdout
    
    def test_executar_acao_listar(self):
        """Testa execução da ação listar."""
        resultado = self._run_main("--acao", "listar", "--diretorio", ".")
        
        assert resultado.returncode == 0
        assert "Listando arquivos" in resultado.stdout
    
    def test_argumento_help(self):
        """Testa argumento --help."""
        resultado = self._run_main("--help")
        
        assert resultado.returncode == 0
        assert "--acao" in resultado.stdout
    
    def test_acao_padrao_info(self):
        """Testa que ação padrão é info."""
        resultado = self._run_main()
        
        assert resultado.returncode == 0
        assert "Informacoes do Sistema" in resultado.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])