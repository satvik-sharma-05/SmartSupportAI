#!/bin/bash
set -e

echo "=== SmartSupport AI Startup ==="
echo "PORT: $PORT"
echo "Python version:"
python --version

# Download model if not exists
if [ ! -f "models/smartsupport_model/model.pt" ]; then
    echo "Downloading model from Google Drive..."
    pip install -q gdown
    mkdir -p models/smartsupport_model
    
    # Use correct gdown syntax (no --fuzzy flag)
    gdown 1Igb0dGI6-HlyccZWe8F82c2XA5m7TyZG -O models/smartsupport_model/model.pt
    
    if [ -f "models/smartsupport_model/model.pt" ]; then
        echo "✓ Model downloaded successfully ($(du -h models/smartsupport_model/model.pt | cut -f1))"
    else
        echo "✗ Model download failed!"
        exit 1
    fi
else
    echo "✓ Model already exists ($(du -h models/smartsupport_model/model.pt | cut -f1))"
fi

# Create metadata file if missing
if [ ! -f "models/smartsupport_model/metadata.json" ]; then
    echo '{"model_name":"distilbert-base-uncased","num_categories":4,"num_priorities":3}' > models/smartsupport_model/metadata.json
    echo "✓ Created metadata.json"
fi

# Start server (no import test - let uvicorn handle it)
echo "Starting uvicorn on 0.0.0.0:$PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 120
