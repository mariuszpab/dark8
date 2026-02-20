# plugin_memory_set.py
from dark8_mark01.memory.memory_store import MemoryStore

store = MemoryStore()

def handle_MEMORY_SET(task, context):
    key = task.get("key")
    value = task.get("value")

    if not key:
        return {"error": "MEMORY_SET wymaga pola 'key'"}

    store.set(key, value)
    return {"status": "ok", "key": key, "value": value}
