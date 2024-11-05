#!/bin/bash

# Inicia o Redis em segundo plano
service redis-server start

# Inicia o servidor web (substitua pelo seu comando)
python app.py  # Ou qualquer outro comando que inicie seu servidor
