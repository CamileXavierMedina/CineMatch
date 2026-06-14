# 1. Usa uma imagem oficial leve do Python
FROM python:3.10-slim

# Força o container a usar UTF-8 e impede o Python de reter logs em cache
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# 2. Define a pasta de trabalho dentro do container
WORKDIR /app

# 3. Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o restante dos arquivos do projeto para o container
COPY . .

# 5. Informa a porta que a aplicação vai usar
EXPOSE 10000

# 6. Comando definitivo para rodar o servidor Flask
CMD ["python", "app.py"]
