# plugin_memory_list.py
from dark8_mark01.memory.memory_store import MemoryStore

store = MemoryStore()

def handle_MEMORY_LIST(task, context):
    return {"status": "ok", "memory": store.list()}
