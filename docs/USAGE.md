# Usage Guide

## 🚀 Quick Start

```bash
# Activate environment
source venv/bin/activate    # Linux/macOS
# OR
venv\Scripts\activate.bat   # Windows

# Start DARK8
python -m dark8_core

# Or use the script
./scripts/run_dark8.sh      # Linux/macOS
```

---

## 💬 CLI Agent Mode (Default)

Interactive command-line agent that understands Polish.

### Examples

#### 1. Build Applications

```
🖤 agent> zbuduj aplikację todo w Django

[PLANNING] Decomposing task...
[GENERATING] Creating Django project structure...
[BUILDING] Installing dependencies...
[TESTING] Running tests...

✓ Application built: /home/user/.dark8/data/todo_app
  • models.py - Database models
  • views.py - Django views
  • urls.py - Routes
  • requirements.txt - Dependencies
```

#### 2. Search Information

```
🖤 agent> szukaj jak zrobić REST API

✓ Search results for: REST API
  1. What is REST API?
  2. Building APIs with FastAPI
  3. API Security Best Practices
  ...
```

#### 3. Analyze Code

```
🖤 agent> przeanalizuj plik main.py

[ANALYZER] Reading file...
[ANALYSIS] Checking code quality...

✓ Code analysis:
  • Structure: Good
  • Style: PEP8 compliant
  • Performance: OK
  • Security: No issues found
  • Suggestions:
    - Add docstrings to functions
    - Consider refactoring large functions
```

#### 4. Execute Commands

```
🖤 agent> uruchom: python main.py --version

[EXECUTING] Running: python main.py --version
python main.py 0.1.0

✓ Command executed successfully
```

#### 5. File Operations

```
🖤 agent> pokaż zawartość katalogu ./src

[LISTING] Directory: ./src
  ├── main.py
  ├── config.py
  ├── models.py
  ├── views.py
  └── utils.py

✓ Listed 5 files
```

---

## 🌐 API Server Mode

RESTful API for programmatic access.

### Start API Server

```bash
python -m dark8_core --mode api
# Server running on http://localhost:8000
```

### API Endpoints

#### Health Check

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

#### System Status

```bash
curl http://localhost:8000/status
# {
#   "environment": "development",
#   "cpu_percent": 15.2,
#   "memory_percent": 45.6,
#   "agent_conversations": 3,
#   "agent_tasks": 1
# }
```

#### Analyze Text (NLP)

```bash
curl -X POST http://localhost:8000/nlp/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "zbuduj aplikację todo"}'

# Response:
# {
#   "intent": "BUILD_APP",
#   "confidence": 0.95,
#   "entities": {
#     "APP_TYPE": ["aplikację todo"],
#     "FRAMEWORK": []
#   },
#   "tokens": ["zbuduj", "aplikację", "todo"]
# }
```

#### Execute Command

```bash
curl -X POST http://localhost:8000/agent/command \
  -H "Content-Type: application/json" \
  -d '{"text": "szukaj Python tutorial"}'

# Response:
# {
#   "status": "success",
#   "response": "Search results for: Python tutorial...",
#   "intent": "SEARCH",
#   "execution_time": 1.23
# }
```

#### Get Conversation History

```bash
curl http://localhost:8000/agent/memory/conversations?limit=5

# Response:
# {
#   "conversations": [
#     {"user": "...", "ai": "..."},
#     ...
#   ],
#   "total": 12
# }
```

#### Interactive API Documentation

```
http://localhost:8000/docs     # Swagger UI
http://localhost:8000/redoc    # ReDoc UI
```

---

##  Code Examples

### Python Client

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Analyze text
        response = await client.post(
            "http://localhost:8000/nlp/analyze",
            json={"text": "zbuduj aplikację"}
        )
        print(response.json())
        
        # Execute command
        response = await client.post(
            "http://localhost:8000/agent/command",
            json={"text": "szukaj Machine Learning"}
        )
        print(response.json())

asyncio.run(main())
```

### JavaScript / Node.js

```javascript
async function analyzeText(text) {
    const response = await fetch('http://localhost:8000/nlp/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });
    return await response.json();
}

async function executeCommand(text) {
    const response = await fetch('http://localhost:8000/agent/command', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text })
    });
    return await response.json();
}

// Usage
analyzeText("zbuduj aplikację todo").then(console.log);
executeCommand("szukaj Python").then(console.log);
```

### cURL

```bash
# List all conversation
curl http://localhost:8000/agent/memory/conversations

# Execute multi-step command
curl -X POST http://localhost:8000/agent/command \
  -H "Content-Type: application/json" \
  -d '{
    "text": "zbuduj REST API w Django, dodaj Bearer token auth, i wdróż na Docker",
    "context": {
      "database": "postgresql",
      "python_version": "3.10"
    }
  }'
```

---

## 🎯 Advanced Usage

### Custom Configuration

Edit `.env` file:

```env
# Debug
DARK8_DEBUG=true
DARK8_LOG_LEVEL=DEBUG

# Ollama
OLLAMA_MODEL=neural-chat
OLLAMA_TEMPERATURE=0.5

# API
API_HOST=0.0.0.0
API_PORT=8001
API_RELOAD=false

# Database
DATABASE_URL=postgresql://user:pass@localhost/dark8

# Features
CHROMA_ENABLED=true
REDIS_ENABLED=true
```

### Using Different Ollama Models

```bash
# In .env
OLLAMA_MODEL=mistral
# or
OLLAMA_MODEL=neural-chat
# or
OLLAMA_MODEL=llama2

# Pull model first
ollama pull mistral
```

### Programmatic Usage (Python)

```python
import asyncio
from dark8_core.agent import get_agent
from dark8_core.nlp import get_nlp_engine

async def main():
    # Initialize
    nlp = get_nlp_engine()
    agent = get_agent()
    
    # Understand user input
    nlp_result = nlp.understand("zbuduj aplikację todo")
    print(f"Intent: {nlp_result['intent']}")
    
    # Process through agent
    response = await agent.process_command(
        "zbuduj aplikację todo",
        nlp_result
    )
    print(f"Result: {response}")

asyncio.run(main())
```

---

## 📚 Useful Commands

### System Commands

```
🖤 agent> help          # Show help message
🖤 agent> status        # Show system status
🖤 agent> clear         # Clear screen
🖤 agent> exit          # Exit DARK8
```

### Getting Help

```
🖤 agent> jak zrobić aplikację Flask?
🖤 agent> wyjaśnij Machine Learning
🖤 agent> pokaż przykład Python async
```

### File Operations

```
🖤 agent> pokaż zawartość src/main.py
🖤 agent> utwórz plik config.py
🖤 agent> usuń stary_plik.txt
🖤 agent> lista plików w ./
```

### Git Operations

```
🖤 agent> commituj moje zmiany
🖤 agent> push do main branch
🖤 agent> sklonuj repo z github
```

---

## 🐞 Debugging

Enable debug mode in `.env`:

```env
DARK8_DEBUG=true
DARK8_LOG_LEVEL=DEBUG
```

View logs:

```bash
tail -f ~/.dark8/logs/dark8.log
```

---

## 🚀 Deployment

### Production Checklist

- [ ] Set `DARK8_ENV=production` in `.env`
- [ ] Change `SECRET_KEY` to strong random value
- [ ] Disable debug mode: `DARK8_DEBUG=false`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable Redis cache
- [ ] Set up proper logging
- [ ] Use systemd service or Docker
- [ ] Set up HTTPS/SSL

### Systemd Service

```bash
sudo cp dark8-os.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dark8-os
sudo systemctl start dark8-os
sudo systemctl status dark8-os
```

---

*Last updated: 2026-02-17*
