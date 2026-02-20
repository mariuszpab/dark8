# memory_context.py
# Pamięć krótkotrwała (sesyjna)

class MemoryContext:
    def __init__(self):
        self.session = {}

    def set(self, key, value):
        self.session[key] = value

    def get(self, key, default=None):
        return self.session.get(key, default)

    def delete(self, key):
        if key in self.session:
            del self.session[key]

    def list(self):
        return dict(self.session)
