#!/bin/bash

set -e  # Para o script se algum comando falhar
#whoami

# Inicia o Redis em background com persistência desabilitada
redis-server --daemonize yes --stop-writes-on-bgsave-error no
sleep 2
redis-cli ping

python app.py
