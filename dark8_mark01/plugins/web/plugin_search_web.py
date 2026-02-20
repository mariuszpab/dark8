# plugin_search_web.py
from dark8_mark01.utils.dark8_web_search import web_search

def handle_SEARCH_WEB(task: dict, context: dict) -> dict:
    query = task.get("query")
    if not query:
        return {"error": "SEARCH_WEB wymaga pola 'query'"}

    results = web_search(query)

    return {
        "status": "ok",
        "query": query,
        "results": results,
    }
