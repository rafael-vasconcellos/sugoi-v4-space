#!/bin/bash

whoami

service redis-server start
service redis-server status

python app.py
