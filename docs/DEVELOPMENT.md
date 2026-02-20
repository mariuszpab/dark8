# Development Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git
- Ollama (for LLM features)

### Installation

```bash
# Clone repository
git clone <repo> DARK8_OS
cd DARK8_OS

# Run setup script
./scripts/setup_env.sh          # Linux/macOS
# OR
scripts\setup_env.bat           # Windows

# Activate environment
source venv/bin/activate        # Linux/macOS
# OR
venv\Scripts\activate.bat       # Windows

# Run DARK8
python -m dark8_core
```

---

## 📁 Project Structure

```
dark8_core/
├── __init__.py
├── __main__.py          # Entry point
├── config.py            # Configuration
├── logger.py            # Logging
├── boot.py              # System startup
│
├── nlp/                 # NLP Engine
│   ├── __init__.py
│   ├── intent_classifier.py
│   ├── entity_extractor.py
│   ├── parser.py
│   └── tokenizer.py
│
├── agent/               # Agent Core
│   ├── __init__.py
│   ├── agent.py
│   ├── memory.py
│   ├── reasoning.py
│   └── executor.py
│
├── programmer/          # Code Generation
│   ├── __init__.py
│   ├── code_generator.py
│   ├── code_analyzer.py
│   ├── builder.py
│   └── templates/
│
├── tools/               # Tool Implementations
│   ├── __init__.py
│   └── [file_ops, shell_ops, git_ops, etc.]
│
├── persistence/         # Database & Storage
├── ui/                  # User Interfaces
│   ├── cli.py
│   ├── api.py
│   └── web/
│
└── utils/               # Utilities
```

---

## 🧠 Core Concepts

### 1. NLP Engine (Polish)
Process user input in Polish:
```python
from dark8_core.nlp import get_nlp_engine

nlp = get_nlp_engine()
result = nlp.understand("zbuduj aplikację todo")
# Returns: {
#   'intent': 'BUILD_APP',
#   'confidence': 0.95,
#   'entities': {...},
#   'tokens': [...]
# }
```

### 2. Agent Loop
Process commands through agent:
```python
from dark8_core.agent import get_agent

agent = get_agent()
await agent.process_command(user_input, nlp_result)
```

### 3. Master Programmer
Generate complete applications:
```python
from dark8_core.programmer import MasterProgrammer

programmer = MasterProgrammer()
result = await programmer.build_application({
    'name': 'my_app',
    'type': 'fastapi',
    'endpoints': [...]
})
```

### 4. Tools
Execute operations:
```python
from dark8_core.tools import FileOperations, ShellOperations

content = await FileOperations.read_file('file.txt')
output = await ShellOperations.execute('ls -la')
```

---

## 🔧 Adding Features

### Adding a New Intent

1. **NLPEngine** (`dark8_core/nlp/__init__.py`):
```python
INTENTS = {
    "NEW_INTENT": ["keyword1", "keyword2"],
}
```

2. **Agent** (`dark8_core/agent/__init__.py`):
```python
def _plan_tasks(self, intent, entities, user_input):
    if intent == "NEW_INTENT":
        tasks.append(Task(...))
```

3. **Tool** (create if needed):
```python
async def _tool_new_operation(self, params):
    # Implementation
```

### Adding a New Tool

1. Create in `dark8_core/tools/__init__.py`:
```python
class NewTool:
    @staticmethod
    async def operation(params):
        # Implementation
        return result
```

2. Register in `ToolRegistry`:
```python
self.tools['new_tool'] = NewTool.operation
```

3. Use in Agent:
```python
result = await self.executor.execute('new_tool', params)
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_nlp.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=dark8_core --cov-report=term-plus
```

### Add New Test
```python
# tests/test_my_feature.py
import pytest
from dark8_core.my_module import MyClass

class TestMyFeature:
    def test_something(self):
        obj = MyClass()
        assert obj.do_something() == expected
```

---

## 🐛 Debugging

### Enable Debug Mode
```bash
# Set in .env
DARK8_DEBUG=true
DARK8_LOG_LEVEL=DEBUG
```

### Add Logging
```python
from dark8_core.logger import logger

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message", exc_info=True)
```

### IPython Debugging
```bash
pip install ipdb
python -m ipdb dark8_core
```

---

## 📚 Code Style

### Python Formatting
```bash
# Format code
black dark8_core/

# Check style
pylint dark8_core/
mypy dark8_core/

# Sort imports
isort dark8_core/
```

### Pre-commit Hook
```bash
pip install pre-commit
pre-commit install
```

---

## 🚀 Deployment

### Docker
```bash
docker build -t dark8-os .
docker run -p 8000:8000 dark8-os
```

### Systemd Service
```bash
# Copy service file
sudo cp dark8-os.service /etc/systemd/system/

# Enable and start
sudo systemctl enable dark8-os
sudo systemctl start dark8-os
```

---

## 📖 Useful Resources

- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Ollama](https://ollama.ai/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests
4. Make sure tests pass
5. Submit a pull request

---

## 📞 Support

- Issues: GitHub Issues
- Documentation: See `/docs`
- Discord: (coming soon)

---

*Last updated: 2026-02-17*
