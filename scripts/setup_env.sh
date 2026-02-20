#!/bin/bash
# DARK8 OS - Setup Environment (Linux/macOS)

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

echo "🖤 DARK8 OS - Setup Environment"
echo "================================"
echo ""

# Check Python
echo "[1/4] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION"

# Create virtual environment
echo "[2/4] Creating virtual environment..."
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    python3 -m venv "$PROJECT_ROOT/venv"
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment exists"
fi

# Activate virtual environment
echo "[3/4] Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"
echo "✓ Virtual environment activated"

# Install dependencies
echo "[4/4] Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r "$PROJECT_ROOT/requirements.txt"
echo "✓ Dependencies installed"

# Create .env if not exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo ""
    echo "Creating .env from template..."
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo "✓ .env created (edit as needed)"
fi

echo ""
echo "🖤 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Source the environment: source venv/bin/activate"
echo "  2. Install Ollama: https://ollama.ai"
echo "  3. Run: python -m dark8_core"
echo ""
