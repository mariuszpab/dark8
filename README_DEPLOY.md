## DARK8 - Deployment guide (minimal)

Kroki do lokalnego uruchomienia (zbudowanie obrazu Docker i uruchomienie compose):

1. Przygotuj środowisko (opcjonalnie):

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
```

2. Zbuduj obraz Docker (jeśli masz Docker):

```bash
docker build -t dark8:local .
```

3. Uruchom Docker Compose (jeśli masz Docker Compose):

```bash
docker compose up --build
```

4. Testy: exporter Prometheus dostępny na `http://localhost:9100/metrics`.

Uwaga: repo zawiera również katalog `k8s/` z podstawowymi manifestami Deployment/Service.
