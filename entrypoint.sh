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

gunicorn src.app.main:app --workers 16 --worker-class uvicorn.workers.UvicornWorker --bind "0.0.0.0:8000"