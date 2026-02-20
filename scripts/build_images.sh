#!/usr/bin/env bash
set -euo pipefail
TAG=${1:-local}
echo "Building runtime image (light deps)..."
docker build --target runtime -t dark8:runtime-${TAG} .
echo "Built runtime image: dark8:runtime-${TAG}"

echo "(Optional) Build full ML image (this can be large)"
if [ "${BUILD_ML:-0}" = "1" ]; then
  docker build --target ml -t dark8:ml-${TAG} .
  echo "Built ml image: dark8:ml-${TAG}"
else
  echo "Skipping ml image build (set BUILD_ML=1 to enable)"
fi
