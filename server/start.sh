#!/bin/bash

set -e  # Para o script se algum comando falhar
#whoami

# Inicia o Redis em background
redis-server --daemonize yes
sleep 2
redis-cli ping

python app.py
