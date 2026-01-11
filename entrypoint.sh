#!/bin/sh
set -e

echo "Starting LangGraph + Qdrant API..."

# Optional: wait for Qdrant if needed
if [ -n "$QDRANT_HOST" ]; then
  echo "Waiting for Qdrant at $QDRANT_HOST..."
  while ! nc -z ${QDRANT_HOST} ${QDRANT_PORT:-6333}; do
    sleep 1
  done
  echo "Qdrant is ready"
fi

# Start FastAPI
if [ "$ENVIRONMENT" = "development" ]; then
  uvicorn main:app \
    --host 0.0.0.0 \
    --port 8001 \
    --reload
else
  uvicorn main:app \
    --host 0.0.0.0 \
    --port 8001
fi
