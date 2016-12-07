#!/usr/bin/env sh

export PYTHONPATH=/app
gunicorn --bind=0.0.0.0:8000 app:app
