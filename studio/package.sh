#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
echo "Building web assets (no-op: using static files in ../web)"
# Build tauri (native) - will pick up web assets if configured
cd "$ROOT/studio"
echo "Running cargo build..."
cargo build --release
echo "Studio built. For packaging use 'cargo tauri build' (requires tauri prerequisites)."
