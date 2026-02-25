from typing import List

from .base import SearchResult


class RankingEngine:
    def __init__(self):
        pass

    def rank(self, results: List[SearchResult]) -> List[SearchResult]:
        # simple rank by score descending
        return sorted(results, key=lambda r: r.score, reverse=True)
