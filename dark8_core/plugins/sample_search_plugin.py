"""Sample plugin that registers a simple search source."""

from typing import List

from dark8_core.search import SearchResult


def simple_plugin_search(query: str, limit: int = 10) -> List[SearchResult]:
    # Return a trivial result for demonstration
    if not query:
        return []
    return [SearchResult(source="plugin", score=1.0, snippet=f"plugin found: {query}", metadata={})]


def register(agent):
    """Register this plugin's search source with the agent."""
    from dark8_core.search import PluginSearchSource

    src = PluginSearchSource(simple_plugin_search)
    agent.register_search_source("sample_plugin", src)
