#!/bin/bash

echo "Starting celery worker"
uv run -m celery -A src.worker.worker_app worker --loglevel=info