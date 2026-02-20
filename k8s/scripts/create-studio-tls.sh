#!/usr/bin/env bash
set -euo pipefail

NAMESPACE=default
CERT=""
KEY=""

usage(){
  cat <<EOF
Usage: $0 --cert /path/tls.crt --key /path/tls.key [--namespace NAME]

Creates or updates Kubernetes TLS secret `dark8-studio-tls` in the given namespace.
It uses --dry-run=client and kubectl apply to be idempotent.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cert) CERT="$2"; shift 2;;
    --key) KEY="$2"; shift 2;;
    --namespace) NAMESPACE="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

if [[ -z "$CERT" || -z "$KEY" ]]; then
  echo "Error: --cert and --key are required" >&2
  usage
  exit 2
fi

kubectl create secret tls dark8-studio-tls \
  --cert="$CERT" --key="$KEY" -n "$NAMESPACE" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "TLS secret 'dark8-studio-tls' applied in namespace $NAMESPACE"
