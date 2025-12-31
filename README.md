# Python para Automação em DevOps - Atividade Final

## 📋 Descrição

Este projeto demonstra automações comuns em DevOps usando Python, incluindo:

- ✅ Verificação de ambiente e ferramentas
- ✅ Automação de comandos Git
- ✅ Automação de operações Docker
- ✅ Criação de estrutura de projetos
- ✅ Monitoramento de recursos do sistema
- ✅ Gerenciamento de arquivos

## 🚀 Como Usar

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
# Ver informações do sistema
python main.py --acao info

# Verificar ferramentas DevOps instaladas
python main.py --acao ferramentas

# Criar estrutura de novo projeto
python main.py --acao criar-projeto --projeto meu_app

# Listar arquivos Python
python main.py --acao listar --diretorio .

# Monitorar recursos do sistema
python main.py --acao monitorar
```

## 📁 Estrutura do Projeto

```
DevOps/
├── main.py              # Script principal
├── requirements.txt     # Dependências
├── README.md           # Este arquivo
├── utils/              # Módulos utilitários
│   ├── __init__.py
│   ├── git_utils.py    # Automação Git
│   └── docker_utils.py # Automação Docker
└── tests/              # Testes unitários
    └── test_main.py
```

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=. --cov-report=html
```

## 🔧 Ferramentas Utilizadas

- **Python 3.8+**: Linguagem principal
- **subprocess**: Execução de comandos do sistema
- **pathlib**: Manipulação de arquivos e diretórios
- **argparse**: Interface de linha de comando
- **logging**: Registro de logs
- **pytest**: Framework de testes

## 📚 Referências

- [Documentação Python - sys](https://docs.python.org/3/library/sys.html)
- [Documentação Python - subprocess](https://docs.python.org/3/library/subprocess.html)
- [Documentação Python - pathlib](https://docs.python.org/3/library/pathlib.html)

## 👤 Autor

Desenvolvido como atividade final do curso **Python para Automação em DevOps**.

---

_Dezembro 2025_
