# 🏗️ DARK8 OS - Architektura Systemu

## Przegląd

DARK8 OS zbudowany jest na **6 warstwach**, od interfejsu użytkownika aż do abstrakcji kernela.

```
╔════════════════════════════════════════════════════════════════╗
║           DARK8 OS - 6-Warstwa Architektura                   ║
╚════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────┐
│ LAYER 1: USER INTERFACE                                        │
├────────────────────────────────────────────────────────────────┤
│ • CLI Agent (Polish NLP Terminal)                              │
│ • Web Browser (Electron/WebView)                               │
│ • Workspace Dashboard (React)                                  │
│ • Telemetry & Logging                                          │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│ LAYER 2: INTELLIGENCE & REASONING                              │
├────────────────────────────────────────────────────────────────┤
│ • NLP Engine (Intent + Entity Recognition)                     │
│ • Agent Core (Ollama powered)                                  │
│ • Task Planner & Decomposer                                    │
│ • Memory Context Manager                                       │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│ LAYER 3: MASTER PROGRAMMER                                     │
├────────────────────────────────────────────────────────────────┤
│ • Code Generator (Project scaffolds)                           │
│ • Code Analyzer (Quality, patterns)                            │
│ • Builder (CMake, Pip, Npm, etc)                              │
│ • Deployer (Docker, systemd, services)                         │
│ • Test Generator (Pytest, Jest fixtures)                       │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│ LAYER 4: TOOLS & CAPABILITIES                                  │
├────────────────────────────────────────────────────────────────┤
│ • File Operations (read, write, diff, merge, refactor)        │
│ • Shell Commands (sandbox execution)                           │
│ • Git Operations (clone, commit, push, PR)                     │
│ • Package Manager (pip, npm, apt, brew)                        │
│ • API Client (HTTP, WebSocket, REST)                          │
│ • Database Access (SQL, NoSQL, vector DB)                      │
│ • Web Scraping & Search                                        │
│ • System Monitor (CPU, RAM, Disk)                              │
│ • Process Manager (spawn, monitor, kill)                       │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│ LAYER 5: MEMORY & PERSISTENCE                                  │
├────────────────────────────────────────────────────────────────┤
│ • Short-term: Agent context (current session)                  │
│ • Long-term: SQLite (projects, conversations)                  │
│ • Vector DB: Chroma/Pinecone (semantic search)                │
│ • Knowledge Base: Code snippets, patterns                      │
│ • Cache: Redis (for speed)                                     │
│ • Audit Log: All operations logged                             │
└────────────────────────────────────────────────────────────────┘
                              ↓
┌────────────────────────────────────────────────────────────────┐
│ LAYER 6: SYSTEM & DISTRIBUTION                                 │
├────────────────────────────────────────────────────────────────┤
│ • Kernel Abstraction (Linux syscalls + Windows API)           │
│ • Virtual Environment Management                               │
│ • Package/Installer Generation (.deb, .msi, .tar.gz)          │
│ • Service Management (systemd, Windows services)              │
│ • Permission System (RBAC, sandboxing)                        │
│ • Versioning & Auto-update                                     │
└────────────────────────────────────────────────────────────────┘
```

---

## 📦 Struktura Modułów

### dark8_core/

```
dark8_core/
├── __init__.py
├── __main__.py              # Punkt wejścia
├── config.py                # Konfiguracja globalna
├── logger.py                # Unified logging
├── boot.py                  # System startup
│
├── 📁 nlp/                  # Natural Language Processing
│   ├── __init__.py
│   ├── intent_classifier.py # Intent recognition (BERT-PL)
│   ├── entity_extractor.py  # NER (Named Entity Recognition)
│   ├── parser.py            # Polish syntax parser
│   ├── tokenizer.py         # Text tokenization
│   └── models/              # Pre-trained models
│       ├── intents.joblib
│       └── vectors.npy
│
├── 📁 agent/                # Dynamic Agent
│   ├── __init__.py
│   ├── agent.py             # Main agent loop
│   ├── reasoning.py         # Reasoning engine
│   ├── function_calling.py  # Tool execution
│   ├── memory.py            # Agent context memory
│   ├── planner.py           # Task planning & decomposition
│   ├── executor.py          # Tool executor
│   └── config/
│       └── system_prompt.txt # Agent system prompt
│
├── 📁 programmer/           # Master Programmer
│   ├── __init__.py
│   ├── code_generator.py    # Generate boilerplate code
│   ├── code_analyzer.py     # Static analysis & review
│   ├── builder.py           # Build orchestration
│   ├── deployer.py          # Deployment automation
│   ├── test_generator.py    # Auto-generate tests
│   └── templates/           # Project templates
│       ├── django/
│       ├── flask/
│       ├── fastapi/
│       ├── nodejs/
│       └── rust/
│
├── 📁 tools/                # Tool Implementation
│   ├── __init__.py
│   ├── base.py              # Base tool class
│   ├── file_ops.py          # File operations
│   ├── shell_ops.py         # Shell commands
│   ├── git_ops.py           # Git operations
│   ├── web_client.py        # HTTP/API client
│   ├── system_ops.py        # System commands
│   ├── db_ops.py            # Database operations
│   ├── search_ops.py        # Search & web scraping
│   └── registry.py          # Tool registry
│
├── 📁 browser/              # Web Browser
│   ├── __init__.py
│   ├── browser.py           # Browser core
│   ├── renderer.py          # HTML/JS rendering
│   ├── search_engine.py     # DuckDuckGo integration
│   ├── automation.py        # Browser automation
│   └── cache/               # Browsing cache
│
├── 📁 persistence/          # Data Persistence
│   ├── __init__.py
│   ├── database.py          # SQLite ORM
│   ├── vector_db.py         # Vector embeddings (Chroma)
│   ├── cache.py             # Redis cache
│   ├── models.py            # SQLAlchemy models
│   └── migrations/          # DB migrations (Alembic)
│
├── 📁 ui/                   # User Interface
│   ├── __init__.py
│   ├── cli.py               # CLI interface
│   ├── api.py               # REST API (FastAPI)
│   ├── web/                 # Web dashboard
│   │   ├── index.html
│   │   ├── app.js
│   │   ├── styles.css
│   │   └── components/
│   └── formatters.py        # Output formatting
│
└── 📁 utils/                # Utilities
    ├── __init__.py
    ├── decorators.py        # Async, retry, cache decorators
    ├── validators.py        # Input validation
    ├── parsers.py           # Various parsers
    ├── crypto.py            # Encryption utilities
    ├── env.py               # Environment management
    └── helpers.py           # Helper functions
```

---

## 🔄 Agent Loop (Główny Flow)

```
┌─────────────────────┐
│  START (User Input) │
└──────────┬──────────┘
           │
           ↓
┌──────────────────────────────┐
│ 1. LISTEN                    │
│   - Czytaj polskie polecenie │
└──────────┬───────────────────┘
           │
           ↓
┌──────────────────────────────┐
│ 2. UNDERSTAND (NLP)          │
│   - Intent classification    │
│   - Entity extraction        │
│   - Context merging          │
└──────────┬───────────────────┘
           │
           ↓
┌──────────────────────────────┐
│ 3. PLAN                      │
│   - Task decomposition       │
│   - Dependency resolution    │
│   - Resource planning        │
└──────────┬───────────────────┘
           │
           ↓
┌──────────────────────────────┐
│ 4. REASON (Ollama LLM)       │
│   - Evaluate options         │
│   - Choose strategy          │
│   - Generate plan            │
└──────────┬───────────────────┘
           │
           ↓
┌──────────────────────────────┐
│ 5. ACT (Execute Tools)       │
│   - Call appropriate tools   │
│   - Monitor progress         │
│   - Handle errors            │
└──────────┬───────────────────┘
           │
           ↓
┌──────────────────────────────┐
│ 6. REFLECT (Update Memory)   │
│   - Save results             │
│   - Update context           │
│   - Learn from execution     │
└──────────┬───────────────────┘
           │
           ↓
┌──────────────────────────────┐
│ 7. RESPOND                   │
│   - Format output            │
│   - Show results to user     │
└──────────┬───────────────────┘
           │
           ↓
      [LOOP or END]
```

---

## 🧠 NLP Pipeline (Polski)

```
Input: "Zbuduj aplikację todo w Django"
  │
  ├─→ [Tokenizer] → ["Zbuduj", "aplikację", "todo", "w", "Django"]
  │
  ├─→ [Intent Classifier] → Intent: BUILD_APP
  │                         Confidence: 0.97
  │
  ├─→ [Entity Extractor] → Entities:
  │                        - APP_TYPE: "aplikacja"
  │                        - TECH_STACK: "Django"
  │
  ├─→ [Parser] → Parse Tree w pełny AST
  │
  └─→ [Context Merger] → Merged context with memory
       └─→ Output: {
             "intent": "BUILD_APP",
             "app_type": "aplikacja todo",
             "framework": "Django",
             "priority": "high",
             "context": {...}
           }
```

---

## 🤖 Agent with Ollama

```
Agent Flow:
  1. NLP Engine converts Polish → Structured intent
  2. Planner breaks down task
  3. Ollama LLM reasons about approach
  4. Function calling selects tools
  5. Tools execute (file ops, shell, git, etc)
  6. Results fed back to LLM for next step
  7. Loop until goal achieved

Ollama Integration:
  - Model: mistral-7b or neural-chat-7b
  - Context window: 8K tokens
  - Temperature: 0.3 (deterministic)
  - Tools: via function_calling with JSON schema
```

---

## 💻 Master Programmer Workflow

```
User: "Zbuduj REST API w FastAPI"

  1. CODE_GENERATION
     └─→ Load fastapi/advanced template
     └─→ Generate project structure
     └─→ Create models.py, routes.py, main.py
     └─→ Add authentication, logging

  2. ANALYSIS
     └─→ Run pylint, mypy
     └─→ Check code style (PEP8)
     └─→ Security scan

  3. BUILD
     └─→ Install dependencies (pip)
     └─→ Create virtual env
     └─→ Run setup.py

  4. TEST
     └─→ Generate pytest fixtures
     └─→ Run tests
     └─→ Coverage report

  5. DEPLOY
     └─→ Create Dockerfile
     └─→ Build container
     └─→ Generate systemd unit file
     └─→ Package as .tar.gz / Docker image

  Result: Production-ready API ready to deploy
```

---

## 🔐 Security Model

- **Sandboxing**: Shell commands run w subprocess z limited permissions
- **Code Review**: AI analyzes generated code before execution
- **Input Validation**: All user inputs sanitized
- **Audit Logging**: All operations logged with timestamps
- **Permission System**: RBAC for sensitive operations
- **Secret Management**: Via environment variables & encrypted vault

---

## 📊 Database Schema

```sql
-- Projects
CREATE TABLE projects (
  id INTEGER PRIMARY KEY,
  name TEXT,
  path TEXT,
  created_at TIMESTAMP,
  metadata JSON
);

-- Conversations
CREATE TABLE conversations (
  id INTEGER PRIMARY KEY,
  timestamp TIMESTAMP,
  user_input TEXT,
  ai_response TEXT,
  intent TEXT,
  context JSON
);

-- Knowledge Base
CREATE TABLE knowledge_base (
  id INTEGER PRIMARY KEY,
  type TEXT,  -- 'code_snippet', 'pattern', 'template'
  content TEXT,
  embedding BLOB,  -- Vector embedding
  tags TEXT,
  created_at TIMESTAMP
);

-- Audit Log
CREATE TABLE audit_log (
  id INTEGER PRIMARY KEY,
  timestamp TIMESTAMP,
  action TEXT,
  parameters JSON,
  result TEXT,
  status TEXT  -- 'success', 'error'
);
```

---

## 🚀 Deployment Architecture

```
┌──────────────────┐
│  DARK8 OS Core   │  (Python process)
├──────────────────┤
│ ├─ Agent          │
│ ├─ NLP            │
│ ├─ Programmer     │
│ ├─ Tools          │
│ └─ Persistence    │
└──────┬───────────┘
       │
       ├─→ [Ollama Backend] (localhost:11434)
       ├─→ [SQLite DB] (local file)
       ├─→ [Vector DB] (Chroma local)
       ├─→ [Redis Cache] (optional)
       └─→ [Web Server] (FastAPI on :8000)

Systemd Service:
  dark8-os.service → runs dark8_core as daemon
  dark8-web.service → runs FastAPI server

Docker:
  FROM python:3.10
  → Install DARK8 OS
  → Mount /var/dark8 (data volume)
  → Expose :8000
  → CMD: python -m dark8_core
```

---

## 📈 Scaling & Performance

- **Async/Await**: IO-bound operations are async
- **Worker Pool**: Parallel task execution
- **Caching**: Redis for frequently accessed data
- **Lazy Loading**: Models loaded on demand
- **Database Indexing**: Optimized queries
- **Vector DB**: Fast semantic search with HNSW index

---

*Dokument Version: 0.1 | Last Updated: 2026-02-17*
