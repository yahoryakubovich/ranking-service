#!/bin/sh
set -e

WORKERS=${WORKERS:-4}
PORT=${PORT:-8000}

echo "Starting Ranking Service with Gunicorn..."
echo "Workers: $WORKERS, Port: $PORT"

exec gunicorn app.main:app \
    --workers "$WORKERS" \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind "0.0.0.0:$PORT"
