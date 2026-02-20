# plugin_memory_get.py
from dark8_mark01.memory.memory_store import MemoryStore

store = MemoryStore()

def handle_MEMORY_GET(task, context):
    key = task.get("key")

    if not key:
        return {"error": "MEMORY_GET wymaga pola 'key'"}

    value = store.get(key)
    return {"status": "ok", "key": key, "value": value}
