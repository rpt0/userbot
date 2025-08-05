#!/bin/bash

PORT=$(python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.bind(('', 0)); print(s.getsockname()[1]); s.close()")
gunicorn --bind 0.0.0.0:$PORT app:app &

python3 -m Userbot
