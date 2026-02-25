# DARK8 AGENT — SPECYFIKACJA MAKSYMALNA

## 1. Cel agenta

Agent DARK8 to moduł wykonujący:

- search (lokalny, DB, pluginy),
- shell exec (bezpieczny, sandboxowany),
- narzędzia (pluginy),
- analizę danych,
- interakcję z backendami LLM (opcjonalnie, np. Ollama na smartfonie),
- planowanie kroków (w przyszłości).

Agent działa jako warstwa wykonawcza dla systemu narzędziowego DARK8.

## 2. Architektura agenta

Agent
 ├── Tools
 │    ├── search
 │    ├── shell_execute
 │    ├── file tools
 │    ├── web tools
 │    └── custom plugin tools
 ├── DB (SQLite)
 ├── Execution sandbox
 ├── Logging
 └── Optional LLM backend (Ollama / remote)

## 3. API agenta

### 3.1. Metoda główna

```python
async def execute_tool(self, tool_name: str, **kwargs) -> dict:
    """
    Wykonuje narzędzie agenta.
    Zwraca słownik z kluczami:
    - success: bool
    - output: str
    - error: Optional[str]
    """
```

### 3.2. Narzędzia wbudowane

Tool	Opis
search	Przeszukiwanie lokalnych danych, DB, pluginów
shell_execute	Bezpieczne wykonanie polecenia systemowego
file_read	Czytanie plików
file_write	Zapisywanie plików
web_fetch	Pobieranie danych z internetu (httpx)
custom_*	Pluginy

## 4. Bezpieczny shell exec (zrealizowane)

Zasady bezpieczeństwa: brak shell=True, whitelist komend, blokada operatorów powłoki, timeout, limit długości outputu, logowanie błędów, brak dostępu do destrukcyjnych poleceń.

## 5. Search (specyfikacja)

Search powinien obsługiwać:

- Search w plikach lokalnych (.txt, .md, .json, .py)
- Fuzzy / case-insensitive substring match
- limit wyników
- Search w SQLite (tabela `documents`)
- Search w pamięci agenta (conversation_history, task_history)
- Search w pluginach (pluginy rejestrują źródła danych)

API:

```python
async def _tool_search(self, query: str, paths: Optional[List[str]] = None, limit: int = 10, use_db: bool = False) -> dict:
    """
    Wyszukuje dane w lokalnych źródłach.
    Zwraca słownik: {"success": bool, "results": [...], "error": Optional[str]}
    """
```

Wynik:

```json
{
  "success": true,
  "results": [
    {"source": "file", "path": "docs/intro.md", "snippet": "..."},
    {"source": "db", "table": "documents", "row_id": 12, "snippet": "..."}
  ]
}
```

## 6. Integracja z Ollama (opcjonalna)

Integracja powinna być realizowana jako plugin; endpoint i model konfigurowalne.

## 7. Logging

Każdy tool loguje: wejście, wynik, błędy, czas wykonania.

## 8. Testy

Jednostkowe: shell exec, search, file tools, web tools.
Integracyjne: agent + DB, agent + pluginy, agent + CLI.

## 9. Rozszerzalność

Pluginy narzędziowe mogą rejestrować nowe narzędzia i źródła danych.

---

Plik generowany automatycznie — dalsza implementacja `_tool_search()` i rejestracji pluginów znajduje się w `dark8_core/agent/__init__.py`.
