#!/usr/bin/env bash
set -euo pipefail

NAMESPACE=default
USERNAME=""
TOKEN=""
EMAIL=""
SECRET_NAME=dark8-ghcr-secret

usage(){
  cat <<EOF
Usage: $0 --username USER --token TOKEN [--email EMAIL] [--namespace NAME] [--secret NAME]

Creates or updates Kubernetes docker-registry secret to pull images from GHCR (ghcr.io).
This secret can be referenced in your ServiceAccount as imagePullSecrets.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --username) USERNAME="$2"; shift 2;;
    --token) TOKEN="$2"; shift 2;;
    --email) EMAIL="$2"; shift 2;;
    --namespace) NAMESPACE="$2"; shift 2;;
    --secret) SECRET_NAME="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

if [[ -z "$USERNAME" || -z "$TOKEN" ]]; then
  echo "Error: --username and --token are required" >&2
  usage
  exit 2
fi

kubectl create secret docker-registry "$SECRET_NAME" \
  --docker-server=ghcr.io \
  --docker-username="$USERNAME" \
  --docker-password="$TOKEN" \
  ${EMAIL:+--docker-email="$EMAIL"} \
  -n "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

echo "Docker registry secret '$SECRET_NAME' applied in namespace $NAMESPACE"
