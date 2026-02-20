# Installation Guide

## System Requirements

- **OS**: Linux (Ubuntu 20.04+, Debian 11+, Linux Mint 20+), macOS 11+, Windows 10/11
- **Python**: 3.10+
- **RAM**: 4GB minimum (8GB recommended for LLM)
- **Disk**: 2GB free space (more for LLM models)

## Option 1: Automatic Installation (Recommended)

### Linux / macOS

```bash
# Clone repository
git clone <repo> DARK8_OS
cd DARK8_OS

# Run setup script (makes venv and installs dependencies)
./scripts/setup_env.sh

# Activate environment
source venv/bin/activate

# Install Ollama (optional, for LLM features)
# https://ollama.ai/download
```

### Windows

```cmd
# Clone repository
git clone <repo> DARK8_OS
cd DARK8_OS

# Run setup script
scripts\setup_env.bat

# Activate environment
venv\Scripts\activate.bat

# Install Ollama (optional)
# https://ollama.ai/download
```

## Option 2: Manual Installation

### 1. Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate.bat
```

### 2. Install Dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit .env with your settings
nano .env   # Linux/macOS
notepad .env   # Windows
```

### 4. Install Ollama (Optional but Recommended)

```bash
# For Linux arm64:
curl https://ollama.ai/install.sh | sh

# For other platforms:
# https://ollama.ai/download

# Pull a model
ollama pull mistral
# or
ollama pull neural-chat
```

## Option 3: Docker Installation

```bash
# Build Docker image
docker build -t dark8-os .

# Run container
docker run -it -p 8000:8000 dark8-os

# With persistent data
docker run -it -p 8000:8000 -v ~/.dark8:/root/.dark8 dark8-os
```

## Option 4: Linux Package Installation (Coming Soon)

```bash
# Ubuntu/Debian
sudo apt install dark8-os

# Fedora/RHEL
sudo dnf install dark8-os

# Arch
yay -S dark8-os
```

---

## Verification

### Check Installation

```bash
# Verify Python
python --version   # Should be 3.10+

# Verify DARK8
python -m dark8_core --help

# Check Ollama (if installed)
ollama list
```

### First Run

```bash
# Start DARK8 in CLI mode
python -m dark8_core

# Or with explicit mode
python -m dark8_core --mode cli

# Try a command (in Polish)
🖤 agent> help
🖤 agent> status
🖤 agent> zbuduj aplikację todo w FastAPI
```

---

## Troubleshooting

### Python Version Error

```
Error: Python 3.10 or higher required
```

**Solution**: Install Python 3.10+
- Ubuntu: `sudo apt install python3.10`
- macOS: `brew install python@3.10`
- Windows: https://python.org

### Missing Dependencies

```
ModuleNotFoundError: No module named 'dark8_core'
```

**Solution**: Ensure you're in the virtual environment
```bash
source venv/bin/activate   # Linux/macOS
# OR
venv\Scripts\activate.bat  # Windows
```

### Ollama Connection Error

```
Error: Ollama not available
```

**Solution**: Install and start Ollama
```bash
# Install from https://ollama.ai
# Start Ollama (pulls model automatically)
ollama pull mistral
ollama serve
```

### Port Already in Use (API mode)

```
OSError: [Errno 48] Address already in use
```

**Solution**: Change port in .env
```env
API_PORT=8001  # Instead of 8000
```

---

## Next Steps

1. Read [Usage Guide](USAGE.md)
2. Explore [Development Guide](docs/DEVELOPMENT.md)
3. Check [Architecture](../ARCHITECTURE.md)
4. Try examples in the repository

---

## Uninstallation

### Linux/macOS
```bash
rm -rf DARK8_OS
```

### Windows
```cmd
rmdir /s /q DARK8_OS
```

### Docker
```bash
docker rmi dark8-os
```

---

*Last updated: 2026-02-17*
