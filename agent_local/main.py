from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import subprocess
import yaml
import requests
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from fastapi.responses import StreamingResponse

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "ollama.yaml"

app = FastAPI(title="DARK8 Agent Local")

# Serve minimal web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
WEB_DIR = BASE_DIR / "web"
if WEB_DIR.exists():
    # Serve UI under /static to avoid overshadowing API routes
    app.mount("/static", StaticFiles(directory=str(WEB_DIR), html=True), name="web_static")


@app.get("/")
def root_index():
    # simple redirect to the Monaco editor
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/static/monaco.html")


def load_ollama_config():
    if not CONFIG_PATH.exists():
        return None
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


class ChatRequest(BaseModel):
    prompt: str
    model: str | None = None


@app.get("/fs/read")
def fs_read(path: str):
    safe_path = (BASE_DIR / path).resolve()
    if not str(safe_path).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not safe_path.exists():
        raise HTTPException(status_code=404, detail="Not found")
    if safe_path.is_dir():
        return {"type": "dir", "path": str(safe_path)}
    return {"type": "file", "content": safe_path.read_text(encoding='utf-8')}


@app.post("/fs/write")
def fs_write(path: str, content: str = Body(...)):
    safe_path = (BASE_DIR / path).resolve()
    if not str(safe_path).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=400, detail="Invalid path")
    safe_path.parent.mkdir(parents=True, exist_ok=True)
    # content may arrive as JSON string or raw
    if isinstance(content, (dict, list)):
        import json

        content = json.dumps(content, indent=2, ensure_ascii=False)
    safe_path.write_text(str(content), encoding='utf-8')
    return {"ok": True, "path": str(safe_path)}


@app.get("/fs/list")
def fs_list(path: str = "."):
    safe_path = (BASE_DIR / path).resolve()
    if not str(safe_path).startswith(str(BASE_DIR)):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not safe_path.exists() or not safe_path.is_dir():
        raise HTTPException(status_code=404, detail="Not found or not a directory")
    items = []
    for p in safe_path.iterdir():
        items.append({"name": p.name, "is_dir": p.is_dir()})
    return {"path": str(safe_path), "items": items}


@app.post("/system/exec")
def system_exec(cmd: str):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Command timeout")


@app.post("/build/run")
def build_run(cmd: str):
    # simple wrapper for build commands (make, python -m build, etc.)
    return system_exec(cmd)


@app.post("/vm/start")
def vm_start(name: str):
    # placeholder: expect qemu-system command configured elsewhere
    return {"ok": False, "msg": "Not implemented: start vm %s" % name}


@app.post("/vm/stop")
def vm_stop(name: str):
    return {"ok": False, "msg": "Not implemented: stop vm %s" % name}


@app.post("/agent/chat")
def agent_chat(req: ChatRequest):
    cfg = load_ollama_config()
    if not cfg:
        raise HTTPException(status_code=500, detail="OLLAMA config not found")
    host = cfg.get("host")
    port = cfg.get("port")
    endpoint = cfg.get("endpoint", "/v1/chat/completions")
    url = f"http://{host}:{port}{endpoint}"
    payload = {"model": req.model or cfg.get("model"), "prompt": req.prompt}
    # Session with retry
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[502, 503, 504])
    session.mount("http://", HTTPAdapter(max_retries=retries))
    try:
        r = session.post(url, json=payload, timeout=30)
        r.raise_for_status()
        try:
            return r.json()
        except ValueError:
            return {"text": r.text}
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post("/agent/chat_stream")
def agent_chat_stream(req: ChatRequest):
    cfg = load_ollama_config()
    if not cfg:
        raise HTTPException(status_code=500, detail="OLLAMA config not found")
    host = cfg.get("host")
    port = cfg.get("port")
    endpoint = cfg.get("endpoint", "/v1/chat/completions")
    url = f"http://{host}:{port}{endpoint}"
    payload = {"model": req.model or cfg.get("model"), "prompt": req.prompt}
    try:
        r = requests.post(url, json=payload, stream=True, timeout=60)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=str(e))

    def iter_stream():
        try:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
        finally:
            r.close()

    return StreamingResponse(iter_stream(), media_type='text/plain')
