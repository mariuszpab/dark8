K8s secret helper scripts
=========================

This folder contains small helper scripts to create the Kubernetes secrets used by DARK8:

- `create-studio-tls.sh` — create/update TLS secret `dark8-studio-tls` (for ingress TLS)
- `create-agent-secret.sh` — create/update generic secret `dark8-agent-secret` (e.g. OLLAMA_API_KEY)
- `create-ghcr-secret.sh` — create/update docker-registry secret (for pulling GHCR images)

Usage examples
--------------

Create TLS secret for studio (namespace `default`):

```bash
k8s/scripts/create-studio-tls.sh --cert ./tls.crt --key ./tls.key --namespace default
```

Create agent secret with Ollama API key:

```bash
k8s/scripts/create-agent-secret.sh --ollama-api-key mysecret --namespace default
```

Create GHCR registry secret (so cluster can pull private images):

```bash
k8s/scripts/create-ghcr-secret.sh --username my-gh-user --token ghp_xxx --email me@example.com --namespace default
```

Notes
-----
- Scripts are idempotent (use `--dry-run=client -o yaml | kubectl apply -f -`).
- After creating the registry secret, add it to the ServiceAccount used by your deployments, e.g.:

```bash
kubectl patch serviceaccount dark8-agent-sa -p '{"imagePullSecrets":[{"name":"dark8-ghcr-secret"}]}' -n default
kubectl patch serviceaccount dark8-studio-sa -p '{"imagePullSecrets":[{"name":"dark8-ghcr-secret"}]}' -n default
```

Make the scripts executable:

```bash
chmod +x k8s/scripts/*.sh
```
