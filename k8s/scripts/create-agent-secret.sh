#!/usr/bin/env bash
set -euo pipefail

NAMESPACE=default
OLLAMA_API_KEY=""
EXTRA_ARGS=()

usage(){
  cat <<EOF
Usage: $0 [--ollama-api-key KEY] [--from-literal KEY=VALUE ...] [--namespace NAME]

Creates or updates Kubernetes generic secret `dark8-agent-secret` with provided literals.
If --ollama-api-key is omitted, the script will try to read OLLAMA_API_KEY from environment.
Example:
  $0 --ollama-api-key abc123 --namespace production
  $0 --from-literal API_KEY=abc --from-literal OTHER=val
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ollama-api-key) OLLAMA_API_KEY="$2"; shift 2;;
    --from-literal) EXTRA_ARGS+=("--from-literal" "$2"); shift 2;;
    --namespace) NAMESPACE="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 1;;
  esac
done

if [[ -z "$OLLAMA_API_KEY" && -n "${OLLAMA_API_KEY-}" ]]; then
  : # allow empty if provided via --from-literal
fi

CMD=(kubectl create secret generic dark8-agent-secret -n "$NAMESPACE")

if [[ -n "$OLLAMA_API_KEY" ]]; then
  CMD+=(--from-literal "OLLAMA_API_KEY=$OLLAMA_API_KEY")
elif [[ -n "${OLLAMA_API_KEY-}" ]]; then
  # no-op
  :
fi

if [[ ${#EXTRA_ARGS[@]} -gt 0 ]]; then
  CMD+=("${EXTRA_ARGS[@]}")
fi

# Use dry-run and apply to be idempotent
"${CMD[@]}" --dry-run=client -o yaml | kubectl apply -f -

echo "Secret 'dark8-agent-secret' applied in namespace $NAMESPACE"
