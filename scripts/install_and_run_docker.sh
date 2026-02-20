#!/usr/bin/env bash
set -euo pipefail
echo "This script installs Docker (docker.io + compose plugin), builds the dark8 image and runs docker compose. Run with sudo if required."

if [ "$EUID" -ne 0 ]; then
  echo "It is recommended to run this script as root or with sudo. Continuing may fail without privileges." >&2
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y docker.io docker-compose-plugin
systemctl enable --now docker

echo "Building Docker image dark8:local"
docker build -t dark8:local . | tee phase4_docker_build_log.txt

echo "Starting docker compose"
docker compose up --build -d 2>&1 | tee phase4_docker_compose_log.txt

echo "Waiting for services to start..."
sleep 5

echo "Checking exporter metrics at http://127.0.0.1:9100/metrics"
curl -sS http://127.0.0.1:9100/metrics || true

echo "Done. Logs: phase4_docker_build_log.txt, phase4_docker_compose_log.txt"
