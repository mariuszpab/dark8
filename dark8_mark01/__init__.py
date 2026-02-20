# dark8_mark01/plugins/__init__.py

import importlib
import pkgutil


def load_plugins():
    from . import __path__ as plugins_path

    for finder, name, ispkg in pkgutil.iter_modules(plugins_path):
        module_name = f"{__name__}.{name}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                module.register()
                print(f"[INFO][PLUGINS] Załadowano plugin: {name}")
        except Exception as e:
            print(f"[ERROR][PLUGINS] Błąd ładowania {name}: {e}")
