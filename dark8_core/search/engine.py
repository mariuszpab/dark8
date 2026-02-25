import time
from typing import Dict, List, Tuple

from .base import SearchResult, SearchSource
from .ranking import RankingEngine

try:
    from dark8_core.search.sources import DatabaseSearchSource
except Exception:
    DatabaseSearchSource = None

try:
    from dark8_core.agent.tools.db import search_fts
except Exception:
    search_fts = None


class SearchEngine:
    def __init__(self):
        self.sources: Dict[str, SearchSource] = {}
        self._ranker = RankingEngine()
        # simple in-memory cache: key -> (timestamp, results_dict)
        self._cache: Dict[Tuple[str, int, bool], Tuple[float, Dict]] = {}
        self.cache_ttl_seconds = 30

    def register_source(self, name: str, source: SearchSource) -> None:
        self.sources[name] = source

    def unregister_source(self, name: str) -> None:
        if name in self.sources:
            del self.sources[name]

    async def search(
        self, query: str, limit: int = 10, fuzzy: bool = True, extra_sources: list | None = None
    ) -> Dict:
        """Run search across registered sources, aggregate and rank results.

        extra_sources: optional list of SearchSource instances to include for this call only.
        """
        # Validate query
        if not query or not isinstance(query, str):
            return {"success": False, "results": [], "error": "invalid query"}
        # cache key is based on query + limit + fuzzy - sources are assumed stable for TTL
        cache_key = (query or "", int(limit), bool(fuzzy))
        now = time.time()
        cached = self._cache.get(cache_key)
        if cached:
            ts, val = cached
            if now - ts <= self.cache_ttl_seconds:
                return val

        results: List[SearchResult] = []
        # First, attempt FTS5 search on any registered DatabaseSearchSource
        fts_results: List[SearchResult] = []
        if search_fts is not None and DatabaseSearchSource is not None:
            for name, src in self.sources.items():
                try:
                    if isinstance(src, DatabaseSearchSource) and getattr(src, "db_path", None):
                        fts_rows = search_fts(src.db_path, query, limit=limit)
                        # search_fts is sync, might return list of dicts
                        if hasattr(fts_rows, "__await__"):
                            fts_rows = await fts_rows
                        for r in fts_rows:
                            # prefer FTS results with high score
                            res = SearchResult(
                                source="db_fts",
                                score=float(r.get("score", 1.0) or 1.0),
                                snippet=r.get("snippet", ""),
                                metadata={"row_id": r.get("id")},
                            )
                            fts_results.append(res)
                except Exception:
                    continue

        if fts_results:
            ranked = self._ranker.rank(fts_results)
            trimmed = ranked[:limit]
            out = {"success": True, "results": [r.__dict__ for r in trimmed]}
            try:
                self._cache[cache_key] = (now, out)
            except Exception:
                pass
            return out
        # iterate registered sources first
        for name, src in self.sources.items():
            try:
                src_results = await src.search(query, limit=limit)
                results.extend(src_results)
            except Exception:
                # individual source failures should not break overall search
                continue

        # then iterate any extra ephemeral sources provided
        if extra_sources:
            for src in extra_sources:
                try:
                    src_results = await src.search(query, limit=limit)
                    results.extend(src_results)
                except Exception:
                    continue

        # Rank aggregated results
        ranked = self._ranker.rank(results)

        # Trim to limit
        trimmed = ranked[:limit]

        out = {"success": True, "results": [r.__dict__ for r in trimmed]}
        # store in cache
        try:
            self._cache[cache_key] = (now, out)
        except Exception:
            pass

        return out
