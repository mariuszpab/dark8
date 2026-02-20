# DARK8 OS - API Reference

## Base URL

```
http://localhost:8000
```

## Authentication

Currently no authentication required (will be added in v0.2).

---

## Endpoints

### Health & Status

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

#### GET /status
Get system and agent status.

**Response:**
```json
{
  "environment": "development",
  "debug": true,
  "cpu_percent": 15.2,
  "memory_percent": 45.6,
  "agent_conversations": 3,
  "agent_tasks": 1
}
```

#### GET /config
Get configuration (non-sensitive).

**Response:**
```json
{
  "environment": "development",
  "debug": true,
  "ollama_host": "http://localhost:11434",
  "ollama_model": "mistral",
  "api_host": "0.0.0.0",
  "api_port": 8000
}
```

---

### NLP Processing

#### POST /nlp/analyze
Analyze Polish text with NLP engine.

**Request:**
```json
{
  "text": "zbuduj aplikację todo w Django"
}
```

**Response:**
```json
{
  "intent": "BUILD_APP",
  "confidence": 0.95,
  "entities": {
    "APP_TYPE": ["aplikację todo"],
    "FRAMEWORK": ["Django"]
  },
  "tokens": ["zbuduj", "aplikację", "todo", "w", "Django"]
}
```

---

### Agent Execution

#### POST /agent/command
Execute command through agent.

**Request:**
```json
{
  "text": "szukaj Python tutorial",
  "context": {
    "user_id": "user_123"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "response": "Search results for: Python tutorial\n1. ...",
  "intent": "SEARCH",
  "execution_time": 1.23
}
```

---

### Memory Management

#### GET /agent/memory/conversations
Get agent conversation history.

**Query Parameters:**
- `limit` (int, default: 10) - Number of recent conversations to return

**Response:**
```json
{
  "conversations": [
    {
      "user": "zbuduj aplikację",
      "ai": "Building application...",
      "metadata": {}
    }
  ],
  "total": 5
}
```

#### GET /agent/memory/tasks
Get agent task history.

**Query Parameters:**
- `limit` (int, default: 10) - Number of recent tasks to return

**Response:**
```json
{
  "tasks": [
    {
      "id": "task_1",
      "description": "Generate project scaffold",
      "status": "completed",
      "result": "✓ Project created at /path/to/project"
    }
  ],
  "total": 3
}
```

---

## Error Handling

All endpoints return standard HTTP status codes:

- **200** - Success
- **400** - Bad Request (invalid input)
- **404** - Not Found
- **500** - Internal Server Error

Error response format:
```json
{
  "detail": "Error message description"
}
```

---

## Rate Limiting

Currently no rate limiting (will be added in v1.0).

---

## Examples

### cURL

```bash
# NLP Analysis
curl -X POST http://localhost:8000/nlp/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "zbuduj aplikację"}'

# Execute Command
curl -X POST http://localhost:8000/agent/command \
  -H "Content-Type: application/json" \
  -d '{"text": "szukaj Python"}'

# Get Conversations
curl http://localhost:8000/agent/memory/conversations?limit=5
```

### Python

```python
import httpx

client = httpx.Client(base_url="http://localhost:8000")

# Analyze
response = client.post("/nlp/analyze", json={
    "text": "zbuduj aplikację todo"
})
print(response.json())

# Execute
response = client.post("/agent/command", json={
    "text": "szukaj Python"
})
print(response.json())

# Get Status
response = client.get("/status")
print(response.json())
```

### JavaScript

```javascript
// Analyze
const response = await fetch('http://localhost:8000/nlp/analyze', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        text: 'zbuduj aplikację todo'
    })
});
const data = await response.json();
console.log(data);
```

---

## Versioning

API version is included in responses:
```
X-API-Version: 0.1.0
```

---

## WebSocket Support (Coming Soon)

Real-time streaming of agent responses via WebSocket.

---

## Rate Limiting (Coming Soon)

- Default: 100 requests per minute
- Burst: 200 requests per minute

---

## OpenAPI/Swagger

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

*Last updated: 2026-02-17*
*API Version: 0.1.0-alpha*
