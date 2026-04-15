#!/bin/bash
set -e

echo "=== SmartSupport AI Startup ==="
echo "PORT: $PORT"
echo "Python version:"
python --version

# Download model if not exists
if [ ! -f "models/smartsupport_model/model.pt" ]; then
    echo "Downloading model..."
    pip install gdown
    mkdir -p models/smartsupport_model
    gdown 1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG -O models/smartsupport_model/model.pt
    echo "Model downloaded successfully"
else
    echo "Model already exists, skipping download"
fi

# Test import
echo "Testing imports..."
python -c "from app.main import app; print('✓ App imported successfully')"

# Start server
echo "Starting uvicorn on 0.0.0.0:$PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
