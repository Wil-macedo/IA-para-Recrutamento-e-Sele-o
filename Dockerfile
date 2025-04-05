# Imagem base oficial do Python
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para dentro do container
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]