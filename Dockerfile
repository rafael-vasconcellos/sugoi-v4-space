FROM node:18 AS builder
RUN npm install
RUN npm run build


FROM python:3.10-slim

# Copie o código da aplicação para o container
COPY server/* /app/
# Defina o diretório de trabalho
WORKDIR /app
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN python /app/setup.py -download

# Comando para executar o script Python
CMD ["python", "app.py"]
