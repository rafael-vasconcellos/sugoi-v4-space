# um estágio de dockerfile com múltiplos estágios não "herdam o sistema de arquivos" do estágio 
# anterior "by default", é necessário copiar os arquivos manualmente.

# o ambiente temporário onde a construção da imagem é executado é isolado do sistema host, salvo
# algumas exceções como em comandos como "COPY" e "ADD"


FROM node:18 AS builder

# Defina o diretório de trabalho
WORKDIR /app
# Copie os arquivos do projeto para o container
COPY . /app

RUN npm install
RUN npm run build


FROM python:3.10-slim
WORKDIR /app

# Copie o build gerado pelo Node.js para o novo estágio
COPY --from=builder /app/server ./

RUN pip install --no-cache-dir -r requirements.txt
RUN python setup.py -download

EXPOSE 7860

# Comando para executar o servidor Python
CMD ["python", "app.py"]
