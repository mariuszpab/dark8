from pathlib import Path
from typing import List, Optional

from .base import SearchResult, SearchSource
from .matcher import FuzzyMatcher


class FileSearchSource(SearchSource):
    def __init__(self, paths: Optional[List[str]] = None, exts: Optional[set] = None):
        self.paths = [Path(p) for p in (paths or [])]
        self.exts = exts or {".txt", ".md", ".json", ".py"}
        self._matcher = FuzzyMatcher()

    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        results = []
        for root in self.paths or []:
            if not root.exists():
                continue
            for p in root.rglob("*"):
                if p.is_file() and p.suffix in self.exts:
                    try:
                        text = p.read_text(errors="ignore")
                    except Exception:
                        continue
                    if query.lower() in text.lower() or True:
                        snippet = next(
                            (line for line in text.splitlines() if query.lower() in line.lower()),
                            text[:200],
                        )
                        score = self._matcher.score(query, snippet)
                        results.append(
                            SearchResult(
                                source="file",
                                score=score,
                                snippet=snippet,
                                metadata={"path": str(p)},
                            )
                        )
                        if len(results) >= limit:
                            return results
        return results


class DatabaseSearchSource(SearchSource):
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        from .matcher import FuzzyMatcher

        results: List[SearchResult] = []
        if not query:
            return results

        try:
            # Use centralized DB helper to run the query
            from dark8_core.agent.tools.db import db_execute

            q = f"%{query}%"
            sql = "SELECT id, content FROM documents WHERE content LIKE ? LIMIT ?"
            res = await db_execute({"action": "query", "db_path": self.db_path, "sql": sql, "params": (q, limit)})
            rows = res.get("rows", []) if res.get("success") else []
            matcher = FuzzyMatcher()
            for row in rows:
                # row is dict from _serialize_rows
                row_id = row.get("id")
                content = row.get("content", "")

                snippet = None
                for line in str(content).splitlines():
                    if query.lower() in line.lower():
                        snippet = line.strip()
                        break
                if snippet is None:
                    snippet = (str(content)[:200] + "...") if len(str(content)) > 200 else str(content)

                score = matcher.score(query, content)
                results.append(
                    SearchResult(source="db", score=score, snippet=snippet, metadata={"row_id": row_id})
                )
                if len(results) >= limit:
                    break
        except Exception:
            # Don't raise in search, just return what we have
            pass

        return results


class MemorySearchSource(SearchSource):
    def __init__(self, memory):
        self.memory = memory
        self._matcher = FuzzyMatcher()

    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        results = []
        for turn in getattr(self.memory, "conversation_history", []):
            text = f"{turn.get('user','')} {turn.get('ai','')}"
            if True:
                s = self._matcher.score(query, text)
                if s > 0:
                    results.append(
                        SearchResult(source="memory", score=s, snippet=text[:200], metadata={})
                    )
                if len(results) >= limit:
                    break
        return results


class PluginSearchSource(SearchSource):
    def __init__(self, func):
        self.func = func

    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        # plugin function may be async or sync
        res = self.func(query=query, limit=limit)
        if hasattr(res, "__await__"):
            res = await res
        return res or []
