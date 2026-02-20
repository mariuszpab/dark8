# 🖤 DARK8 OS - Autonomous AI Operating System

**DARK8 OS** to samodzielny, inteligentny system operacyjny zasilany sztuczną inteligencją, zdolny do budowania kompletnych aplikacji bezpośrednio z poleceń języka naturalnego w języku polskim.

![Status](https://img.shields.io/badge/Status-Alpha-orange)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Główne Cechy

- 🤖 **Agent AI oparty na Ollama** - Mistral/Neural Chat z rozumowaniem
- 🇵🇱 **Pełna obsługa języka polskiego** - NLP, intent recognition, entity extraction
- 💻 **Master Programmer** - Generuje, buduje i wdraża aplikacje
- 🌐 **Wbudowana przeglądarki** - Open-source, DuckDuckGo search
- 🐧 **Cross-platform** - Linux (Linux Mint) i Windows
- 🔧 **Tool Ecosystem** - Pełen dostęp do shell, Git, APIs, baz danych
- 💾 **Pamięć długoterminowa** - SQLite + Vector DB dla semantic search
- 📦 **Automatyczne pakowanie** - Docker, instalatory .deb, .msi

---

## 🏗️ Architektura

```
DARK8 OS (6 warstw)
├── Layer 1: User Interface (CLI, Web Browser, Dashboard)
├── Layer 2: Intelligence (NLP, Agent, Task Planner)
├── Layer 3: Master Programmer (Code Gen, Build, Deploy)
├── Layer 4: Tools & Capabilities (File, Shell, Git, Web, DB)
├── Layer 5: Memory & Persistence (SQLite, Vector DB, Cache)
└── Layer 6: System & Distribution (Kernel abstraction, Package mgmt)
```

Szczegóły: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🚀 Szybki Start

### Wymagania
- Python 3.10+
- Ollama zainstalowana (`ollama pull mistral`)
- Linux / macOS / Windows

### Instalacja

```bash
# Klonowanie
git clone <repo> DARK8_OS
cd DARK8_OS

# Przygotowanie środowiska
./scripts/setup_env.sh        # Linux/macOS
# LUB
scripts\setup_env.bat         # Windows

# Uruchomienie
./scripts/run_dark8.sh        # CLI Agent
# LUB
python -m dark8_core          # Python entry point
```

### Przykład Użycia

```bash
# Uruchamiasz DARK8 OS
$ python -m dark8_core

🖤 DARK8 OS ready
agent> zbuduj aplikację todo list w Django

[PLANNING] Rozkładam zadanie...
[BUILD] Generuję scaffold projektu...
[DEV] Tworzę modele, widoki, szablony...
[TEST] Uruchamiam testy...
[DEPLOY] Pakuję aplikację w Docker...

✓ Aplikacja gotowa: todo_app.tar.gz

agent> otwórz https://github.com w przeglądarce

[BROWSER] Otwieranie GitHub.com...

agent> analizuj kod z repozytorium UserService

[ANALYZER] Pobieram repo...
[ANALYSIS] Kod jest dobrze strukturyzowany. sugeruję refaktor w ...
```

---

## 📖 Dokumentacja

- [Installation Guide](docs/INSTALLATION.md) - Szczegółowa instalacja
- [Architecture](ARCHITECTURE.md) - Pełna architektura systemu
- [API Reference](docs/API.md) - REST API i funkcje
- [Development Guide](docs/DEVELOPMENT.md) - Rozwijanie DARK8
- [Usage Examples](docs/USAGE.md) - Zaawansowane przykłady

---

## 📁 Struktura Projektu

```
DARK8_OS/
├── dark8_core/          # System core
│   ├── agent/           # Agent loop
│   ├── nlp/             # NLP Polish
│   ├── programmer/      # Code generation
│   ├── tools/           # Tool implementations
│   ├── browser/         # Web browser
│   └── persistence/     # Database & cache
├── dark8_installer/     # System installers
├── tests/               # Test suite
├── docs/                # Documentation
└── scripts/             # Build & run scripts
```

---

## 🛠️ Development

```bash
# Instalacja dev dependencies
pip install -r requirements-dev.txt

# Uruchomienie testów
pytest tests/

# Code quality checks
pylint dark8_core/

# Static type checking
mypy dark8_core/

# Running with hot reload
python -m dark8_core --dev
```

---

## 📋 Roadmap

- [ ] v0.1 - Core Agent + NLP (Styczeń 2026)
- [ ] v0.2 - Master Programmer + Code Generation (Luty 2026)
- [ ] v0.3 - Web Browser + Search (Marzec 2026)
- [ ] v0.4 - System Installer (Kwiecień 2026)
- [ ] v1.0 - Production Ready (Maj 2026)

---

## 🤝 Contributing

Zapraszamy do współpracy! Szczegóły: [DEVELOPMENT.md](docs/DEVELOPMENT.md)

---

## 📄 License

MIT License - patrz [LICENSE](LICENSE) 

---

**Budujemy przyszłość autonomicznych systemów AI. 🚀**

---

*DARK8 OS - "Where AI becomes the programmer"*
