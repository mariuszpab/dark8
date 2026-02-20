# memory_store.py
# Trwała pamięć DARK8 (JSON na dysku)

import json
import os


class MemoryStore:
    def __init__(self, path="memory_store.json"):
        self.path = path
        self.data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def set(self, key, value):
        self.data[key] = value
        self._save()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            self._save()

    def list(self):
        return dict(self.data)
