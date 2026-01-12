FROM python:3.11-slim

# Metadados
LABEL maintainer="Patrick"
LABEL description="DevOps Automation Tool"
LABEL version="1.0"

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY main.py .
COPY utils/ ./utils/

# Criar diretórios necessários
RUN mkdir -p /app/logs /app/backups

# Criar usuário não-root para segurança
RUN useradd -m -r devops && \
    chown -R devops:devops /app
USER devops

# Volume para persistir logs e backups
VOLUME ["/app/logs", "/app/backups"]

# Comando padrão
ENTRYPOINT ["python", "main.py"]
CMD ["--acao", "info"]