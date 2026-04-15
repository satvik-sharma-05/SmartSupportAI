#!/bin/bash
set -e

echo "=== SmartSupport AI Startup ==="
echo "PORT: $PORT"
echo "Python version:"
python --version

# Start server immediately
echo "🚀 Starting uvicorn on 0.0.0.0:$PORT..."
exec uvicorn app.main_lightweight:app --host 0.0.0.0 --port $PORT --timeout-keep-alive 120
