# DARK8 AGENT — SPECYFIKACJA ROZSZERZONEGO SEARCH (WERSJA MAX)
## 1. Cel modułu search

Rozszerzony search ma zapewnić agentowi:

    szybkie i inteligentne wyszukiwanie informacji,
    przeszukiwanie wielu źródeł danych,
    fuzzy matching,
    ranking wyników,
    integrację z pluginami,
    opcjonalne indeksowanie (embeddingi),
    cache wyników.

Search jest fundamentem reasoning, planowania i integracji z LLM.

## 2. Architektura search

SearchEngine
 ├── FileSearchSource
 ├── DatabaseSearchSource
 ├── MemorySearchSource
 ├── PluginSearchSources (dynamiczne)
 ├── FuzzyMatcher
 ├── Indexer (opcjonalnie: Chroma / FAISS / mini-index)
 └── RankingEngine

## 3. API search
### 3.1. Główna metoda

```python
async def _tool_search(self, query: str, limit: int = 10, fuzzy: bool = True) -> dict:
    """
    Wyszukuje dane w wielu źródłach:
    - pliki
    - SQLite
    - pamięć agenta
    - pluginy
    - indeks (opcjonalnie)
    """
```

### 3.2. Wynik

```json
{
  "success": true,
  "results": [
    {
      "source": "file",
      "path": "docs/intro.md",
      "score": 0.92,
      "snippet": "..."
    },
    {
      "source": "db",
      "table": "documents",
      "row_id": 12,
      "score": 0.88,
      "snippet": "..."
    }
  ]
}
```

## 4. Źródła danych (search sources)

Każde źródło implementuje:

```python
class SearchSource:
    async def search(self, query: str, limit: int) -> list[SearchResult]:
        ...
```

### 4.1. FileSearchSource

    przeszukuje .txt, .md, .json, .py
    fuzzy matching
    snippet extraction
    ranking

### 4.2. DatabaseSearchSource

    tabela documents
    tabela history
    tabela notes
    LIKE + fuzzy

### 4.3. MemorySearchSource

    cache
    ostatnie wyniki
    kontekst agenta

### 4.4. PluginSearchSources

Plugin może zarejestrować własne źródło:

```python
def register(agent):
    agent.register_search_source("my_source", my_search_function)
```

## 5. Fuzzy matching
### 5.1. Algorytm

    rapidfuzz (jeśli dostępny)
    fallback: Levenshtein
    scoring 0–1

### 5.2. Zasady

    fuzzy domyślnie włączone
    threshold: 0.6
    sortowanie po score

## 6. Indexing (opcjonalnie)
### 6.1. Warianty

    ChromaDB

        embeddingi
        szybkie wyszukiwanie semantyczne

    FAISS

        szybkie wyszukiwanie wektorowe

    Mini-index (własny)

        tokenizacja
        TF-IDF
        ranking

### 6.2. API

```python
class Indexer:
    def index_document(self, doc_id: str, text: str): ...
    def search(self, query: str, limit: int): ...
```

## 7. Ranking wyników

Ranking łączy:

    fuzzy score,
    długość dopasowania,
    pozycję dopasowania,
    źródło (priorytety),
    świeżość danych (DB/history).

## 8. Cache
### 8.1. Cache krótkoterminowy

    klucz: query
    wartość: lista wyników
    TTL: 30 sekund

### 8.2. Cache długoterminowy (SQLite)

    tabela search_cache
    kolumny: query, results_json, timestamp

## 9. Testy
### 9.1. Testy jednostkowe

    fuzzy matching
    ranking
    file search
    db search
    plugin search
    indexing (jeśli włączony)

### 9.2. Testy integracyjne

    agent + search + DB
    agent + plugin search sources
    agent + indexing

## 10. Kolejność implementacji (wersja maksymalna)
Etap 1 — Fuzzy matching

    rapidfuzz / Levenshtein
    testy fuzzy

Etap 2 — Plugin search sources

    rejestracja
    testy plugin search

Etap 3 — Ranking

    scoring
    sortowanie
    testy ranking

Etap 4 — Indexing

    mini-index lub Chroma
    testy indexing

Etap 5 — Cache

    memory cache
    db cache
    testy cache

## 11. Minimalny kod startowy (szkielet)

Jeśli chcesz, mogę przygotować gotowy szkielet klas:

    SearchEngine
    SearchSource
    FileSearchSource
    DatabaseSearchSource
    PluginSearchSource
    FuzzyMatcher
    RankingEngine
    Indexer

🎯 Podsumowanie

Masz teraz pełną, maksymalną specyfikację rozszerzonego search, gotową do implementacji w DARK8.

Jeśli chcesz, mogę przygotować:

    gotowy szkielet kodu,
    gotowe testy,
    albo od razu zacząć implementację fuzzy search.
