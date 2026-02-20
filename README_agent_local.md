# DARK8 Agent Local

Quickstart

1. Create a virtualenv and install requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r agent_local/requirements.txt
```

2. Run the FastAPI app:

```bash
uvicorn agent_local.main:app --host 0.0.0.0 --port 8000
```

3. Open the minimal UI by visiting `http://localhost:8000/index.html` or the Monaco editor at `http://localhost:8000/monaco.html` and ensure the API is reachable at `http://localhost:8000`.

Docker

Build and run local container:

```bash
docker build -t dark8-agent:local -f agent_local/Dockerfile .
docker run --rm -p 8000:8000 dark8-agent:local
```

Systemd

Install template service (replace USER with your username):

```bash
sudo cp deploy/dark8-agent.service /etc/systemd/system/dark8-agent@USER.service
sudo systemctl daemon-reload
sudo systemctl enable --now dark8-agent@USER
```


Config

Edit `config/ollama.yaml` to point to your smartphone running Ollama (host/port/model).
