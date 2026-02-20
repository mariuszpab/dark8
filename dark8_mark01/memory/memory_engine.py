# memory_engine.py
# Prosty silnik pamięci dla DARK8

import os
import json

MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "system_memory.json"
)

def _load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def _save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_memory(entry: str):
    mem = _load_memory()
    mem.append({"entry": entry})
    _save_memory(mem)
    print(f"[MEMORY] Dodano wpis: {entry}")

def show_memory():
    mem = _load_memory()
    print("=== PAMIĘĆ SYSTEMU DARK8 ===")
    if not mem:
        print("(pusta)")
        return
    for i, item in enumerate(mem, start=1):
        print(f"{i}. {item['entry']}")

def clear_memory():
    _save_memory([])
    print("[MEMORY] Pamięć została wyczyszczona.")
