#!/usr/bin/env sh

export PYTHONPATH=/app
gunicorn --bind=0.0.0.0:${IMAGEN_PORT} --workers=${IMAGEN_WORKERS} app:app
