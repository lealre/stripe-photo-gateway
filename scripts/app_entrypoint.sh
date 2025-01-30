#!/bin/bash

echo "Creating database..."
uv run -m utils.init_db

if [ $? -eq 0 ]; then
    echo "Tables created successfully."
else
    echo "Error: Failed to create tables. Check logs for details."
    exit 1
fi

echo "Starting application."
uv run -m fastapi run --host 0.0.0.0 --port 8000 src/app.py
