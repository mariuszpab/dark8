# 🖤 DARK8 OS - Getting Started Guide

## ⚡ QUICK START (5 minutes)

### Step 1: Setup Environment
```bash
cd /home/mariusz/Pulpit/DARK8_MARK01
./scripts/setup_env.sh          # Linux/macOS
# OR
scripts\setup_env.bat           # Windows
```

### Step 2: Activate Environment
```bash
source venv/bin/activate        # Linux/macOS
# OR
venv\Scripts\activate.bat       # Windows
```

### Step 3: Run DARK8
```bash
python -m dark8_core
```

### Step 4: Try Commands (Polish)
```
🖤 agent> help                    # Show help
🖤 agent> status                  # System status
🖤 agent> zbuduj aplikację todo   # Build todo app
🖤 agent> szukaj Python           # Search Python
```

---

## 📺 API SERVER MODE

```bash
# Start API server
python -m dark8_core --mode api

# Visit: http://localhost:8000
# Swagger docs: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## 🐳 DOCKER MODE

```bash
# Full stack (DARK8 + Ollama + PostgreSQL + Redis)
docker-compose up

# Just DARK8
docker build -t dark8-os .
docker run -p 8000:8000 dark8-os
```

---

## 🔑 KEY FEATURES (v0.1)

### ✅ CLI Agent (Polish Language)
- Natural language command understanding
- 14+ pre-built intents (BUILD_APP, SEARCH, ANALYZE, etc)
- Memory system (conversation history, task tracking)
- Real-time feedback

### ✅ REST API
- Full RESTful interface
- NLP analysis endpoint
- Agent command execution
- Memory management
- Interactive Swagger documentation

### ✅ Code Generation
- Django scaffolds
- FastAPI templates
- React project setup
- Automatic dependency installation

### ✅ Tools & Integrations
- File operations (read, write, delete, list)
- Shell command execution (safe)
- Git integration (clone, commit, push)
- Web search (DuckDuckGo)
- HTTP client (GET, POST)
- System monitoring

### ✅ Development Ready
- PyTest testing framework
- CI/CD workflows (GitHub Actions)
- Code quality (Black, Pylint, Mypy)
- Docker containerization
- Linux installer
- Comprehensive documentation

---

## 📦 PROJECT STRUCTURE

```
DARK8_MARK01/
├── dark8_core/                # Main system package
│   ├── __main__.py           # Entry point
│   ├── config.py             # Configuration
│   ├── logger.py             # Logging
│   ├── boot.py               # Startup sequence
│   ├── nlp/                  # Polish NLP
│   ├── agent/                # Agent system
│   ├── tools/                # Tool implementations
│   ├── programmer/           # Code generation
│   ├── persistence/          # Database
│   ├── llm/                  # Ollama LLM
│   ├── browser/              # Web browser & search
│   └── ui/                   # CLI & API
│
├── docs/                      # Documentation
│   ├── INSTALLATION.md       # Install guide
│   ├── USAGE.md              # Usage examples
│   ├── DEVELOPMENT.md        # Dev guide
│   └── API.md                # API reference
│
├── tests/                     # Test suite
│   ├── test_nlp.py
│   └── test_agent.py
│
├── scripts/                   # Build scripts
│   ├── setup_env.sh          # Linux setup
│   ├── setup_env.bat         # Windows setup
│   ├── run_dark8.sh          # Run script
│   └── install_linux.sh      # System installer
│
├── README.md                 # Main readme
├── ARCHITECTURE.md           # System architecture
├── pyproject.toml            # Project config
├── requirements.txt          # Dependencies
├── Makefile                  # Build automation
├── Dockerfile                # Docker image
├── docker-compose.yml        # Dev stack
└── LICENSE                   # MIT License
```

---

## 🎯 WHAT'S READY NOW  (v0.1.0-alpha)

| Feature | Status | Notes |
|---------|--------|-------|
| CLI Agent | ✅ | Polish language support |
| REST API | ✅ | Full CRUD operations |
| NLP Engine | ✅ | 14 intents, entity recognition |
| Code Generator | ✅ | Django, FastAPI, React |
| Database | ✅ | SQLite with SQLAlchemy ORM |
| Ollama Integration | ✅ | For advanced reasoning |
| Browser | ✅ | Search & web fetch |
| Docker | ✅ | Full containerization |
| Tests | ✅ | PyTest framework ready |
| CI/CD | ✅ | GitHub Actions workflows |
| Documentation | ✅ | Complete guides |
| Linux Installer | ✅ | Automated setup |

---

## 🚀 NEXT STEPS

### Immediate (Today)
1. [ ] Setup environment: `./scripts/setup_env.sh`
2. [ ] Try CLI: `python -m dark8_core`
3. [ ] Read docs: `docs/USAGE.md`
4. [ ] Install Ollama: https://ollama.ai

### Short Term (This Week)
1. [ ] Improve NLP (BERT Polish models)
2. [ ] Add more code generation templates
3. [ ] Create system installer
4. [ ] Setup continuous integration

### Medium Term (This Month)
1. [ ] Advanced web browser
2. [ ] WebSocket real-time streaming
3. [ ] Database migrations
4. [ ] Authentication system

### Long Term (Production)
1. [ ] Multi-user support
2. [ ] Cloud deployment
3. [ ] Advanced scheduling
4. [ ] Enterprise features

---

## 🛠️ DEVELOPMENT COMMANDS

```bash
# Install with dev dependencies
make dev

# Run tests
make test

# Run with coverage
make test-cov

# Format code
make format

# Lint code
make lint

# Clean cache
make clean

# Run CLI
make run

# Run API
make api

# Build Docker
make docker-build

# Run Docker
make docker-run
```

---

## 📚 DOCUMENTATION MAP

| Document | Purpose |
|----------|---------|
| README.md | Overview & quick start |
| ARCHITECTURE.md | System design & flows |
| INSTALLATION.md | How to install |
| USAGE.md | How to use CLI & API |
| DEVELOPMENT.md | How to develop |
| API.md | API reference |
| CONTRIBUTING.md | Contribution guidelines |
| PROJECT_STATUS.md | Status & roadmap |

---

## ⚙️ REQUIREMENTS

- **Python:** 3.10+
- **OS:** Linux, macOS, Windows
- **RAM:** 4GB+ (8GB recommended)
- **Disk:** 2GB free

## 🔧 OPTIONAL but RECOMMENDED

- **Ollama:** For advanced LLM features
  - Install: https://ollama.ai
  - Command: `ollama pull mistral`

- **Docker:** For containerization
  - Install: https://docker.com

- **PostgreSQL:** For production (instead of SQLite)

---

## 🤔 FAQ

**Q: Do I need Ollama to run DARK8?**  
A: No, but you'll get better results with it. CLI will work without it.

**Q: Can I use this on Windows?**  
A: Yes! Use `scripts\setup_env.bat` for setup.

**Q: How do I run it as a service?**  
A: Use systemd: `sudo systemctl start dark8-os`

**Q: Can I customize the intents?**  
A: Yes! Edit `dark8_core/nlp/__init__.py` and add your intents.

**Q: Is it production-ready?**  
A: v0.1 is alpha. Production hardening coming in v1.0.

---

## 📞 GETTING HELP

- **Docs:** See `/docs` folder
- **Issues:** GitHub Issues (coming soon)
- **Discord:** Community support (coming soon)
- **Contributing:** See `CONTRIBUTING.md`

---

## 🎉 SUCCESS CHECKLIST

To verify DARK8 is working:

- [ ] Python 3.10+ installed
- [ ] Environment activated
- [ ] `python -m dark8_core` starts without error
- [ ] "🖤 agent> " prompt appears
- [ ] `help` command shows available intents
- [ ] `status` command shows system info
- [ ] `zbuduj aplikację` processes as BUILD_APP intent

---

## 📝 NOTES

- All code uses Python 3.10+ features
- Type hints throughout
- Async/await for concurrency
- Clean architecture: layers, separation of concerns
- Comprehensive documentation
- Test-driven where applicable

---

## 🎓 LEARNING RESOURCES

- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://sqlalchemy.org
- Python asyncio: https://docs.python.org/3/library/asyncio.html
- Ollama: https://ollama.ai

---

## 🖤 MISSION STATEMENT

**Build autonomous AI systems that understand natural language and can accomplish complex programming tasks.**

We're creating DARK8 OS as a platform where:
- AI understands your intent
- Agents reason about solutions
- Code is generated automatically
- Systems are deployed seamlessly
- Everything is open-source

---

**Ready to build the future? Let's go! 🚀**

---

*DARK8 OS v0.1.0-alpha*  
*"Where AI becomes the programmer"*  
*Last Updated: 2026-02-17*
