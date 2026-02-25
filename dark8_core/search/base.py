from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SearchResult:
    source: str
    score: float
    snippet: str
    metadata: Dict[str, Any]


class SearchSource:
    async def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """Search the source for query. Return list of SearchResult."""
        raise NotImplementedError()
