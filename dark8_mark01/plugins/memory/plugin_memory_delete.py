# plugin_memory_delete.py
from dark8_mark01.memory.memory_store import MemoryStore

store = MemoryStore()

def handle_MEMORY_DELETE(task, context):
    key = task.get("key")

    if not key:
        return {"error": "MEMORY_DELETE wymaga pola 'key'"}

    store.delete(key)
    return {"status": "ok", "deleted": key}
