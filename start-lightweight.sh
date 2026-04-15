#!/bin/bash
set -e

echo "=== SmartSupport AI (Lightweight) Startup ==="
echo "PORT: $PORT"
echo "Python version:"
python --version
echo "Memory: 512MB (Free Tier)"
echo "Model: Rule-based classifier (no ML model download needed)"

# Start server immediately
echo "🚀 Starting uvicorn on 0.0.0.0:$PORT..."
exec uvicorn app.main_lightweight:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 120
