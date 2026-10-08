#!/bin/bash
# One-click startup script for TrailGemma & FloraCast

set -e

echo "=========================================================="
echo "🌿 Starting TrailGemma & FloraCast (Touch Grass Edition)"
echo "=========================================================="

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# 1. Check if Ollama is running, start if not
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Starting Ollama daemon in background..."
    ollama serve > /dev/null 2>&1 &
    sleep 3
fi

# 2. Check if gemma2:2b exists in Ollama
if ! ollama list | grep -q "gemma2:2b"; then
    echo "Pulling Gemma 2 open-weight model (Google)..."
    ollama pull gemma2:2b
fi

# 3. Ensure datasets are generated
if [ ! -f "backend/datasets/frost_microclimate_train.csv" ]; then
    echo "Generating in-context environmental datasets..."
    python3 backend/generate_datasets.py
fi

# 4. Start FastAPI server
echo "Starting FastAPI Server on http://127.0.0.1:8000 ..."
echo "Press Ctrl+C to stop."
python3 -m uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
