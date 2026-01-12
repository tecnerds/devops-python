# 🚀 DevOps Automation Tool

Ferramenta de automação para tarefas DevOps desenvolvida em Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Sobre o Projeto

Este projeto oferece uma CLI (Command Line Interface) para automatizar tarefas comuns em ambientes DevOps:

| Funcionalidade       | Descrição                                                       |
| -------------------- | --------------------------------------------------------------- |
| 💾 **Backup**        | Backup de diretórios com opção de compactação ZIP               |
| 🔧 **Ferramentas**   | Verificação de ferramentas instaladas (Git, Docker, Node, etc.) |
| 📊 **Monitoramento** | Monitoramento de CPU, memória e disco                           |
| 📁 **Projetos**      | Criação de estrutura padrão de projetos DevOps                  |
| 🐳 **Docker**        | Automação de operações com containers                           |
| 🔀 **Git**           | Automação de comandos Git                                       |

---

## ⚙️ Instalação

### Pré-requisitos

- Python 3.8 ou superior

### Passos

```bash
# Clone o repositório
git clone https://github.com/tecnerds/devops-python.git
cd devops-python

# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

---

## 🎯 Como Usar

### Comandos Disponíveis

```bash
python main.py --acao <comando> [opções]
```

### Exemplos

#### 📋 Informações do Sistema

```bash
python main.py --acao info
```

#### 🔧 Verificar Ferramentas DevOps

```bash
python main.py --acao ferramentas
```

#### 💾 Realizar Backup

```bash
# Backup simples
python main.py --acao backup --diretorio ./diretorio-origem --destino ./backups

# Backup compactado (ZIP)
python main.py --acao backup --diretorio ./diretorio-origem --destino ./backups --compactar
```

#### 📋 Gerenciar Backups

```bash
# Listar backups existentes
python main.py --acao listar-backups --destino ./backups

# Limpar backups com mais de 30 dias
python main.py --acao limpar-backups --destino ./backups --dias 30
```

#### 📊 Monitorar Recursos

```bash
python main.py --acao monitorar
```

#### 📁 Criar Novo Projeto

```bash
python main.py --acao criar-projeto --projeto meu-novo-projeto
```

---

## 🎯 Como usar via docker

# Informações do sistema

```bash
docker run --rm devops-automation --acao info
```

# Verificar ferramentas

```bash
docker run --rm devops-automation --acao ferramentas
```

# Monitorar recursos

```bash
docker run --rm devops-automation --acao monitorar
```

# Realizar backup (montando volumes)

```bash
docker run --rm \
    -v /caminho/origem:/data/origem:ro \
    -v /caminho/backups:/app/backups \
    devops-automation --acao backup --diretorio /data/origem --destino /app/backups
```

# Backup compactado

```bash
docker run --rm \
 -v /caminho/origem:/data/origem:ro \
 -v /caminho/backups:/app/backups \
 devops-automation --acao backup --diretorio /data/origem --destino /app/backups --compactar
```

---

## 📂 Estrutura do Projeto

```
devops-python/
├── main.py              # Script principal (CLI)
├── requirements.txt     # Dependências do projeto
├── README.md
│
├── utils/               # Módulos utilitários
│   ├── __init__.py
│   ├── backup.py        # Funções de backup
│   ├── logger.py        # Configuração de logs
│   ├── sistema.py       # Informações do sistema
│   ├── projeto.py       # Gerenciamento de projetos
│   ├── docker_utils.py  # Operações Docker
│   └── git_utils.py     # Operações Git
│
├── tests/               # Testes automatizados
│   └── test_main.py
│
└── doc/                 # Documentação adicional
```

---

## 🧪 Testes

```bash
# Executar testes
pytest tests/ -v

# Com relatório de cobertura
pytest tests/ --cov=utils --cov-report=html
```

---

## 📦 Dependências

| Pacote   | Descrição                            |
| -------- | ------------------------------------ |
| `pytest` | Framework de testes                  |
| `psutil` | Monitoramento de recursos do sistema |

---

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

---

## 👤 Autor

**Patrick**

Desenvolvido como atividade final do curso **Python para Automação em DevOps**.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

<p align="center">
  <i>Dezembro 2025</i>
</p>
