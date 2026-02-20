#!/bin/bash
# DARK8 OS - Start Dark8 (Linux/macOS)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Run DARK8
cd "$PROJECT_ROOT"
python -m dark8_core "$@"
