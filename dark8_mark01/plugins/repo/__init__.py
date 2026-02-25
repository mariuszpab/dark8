("""Repo plugins package.

Załadowuje podmoduły z `dark8_mark01.plugins.repo` i wywołuje ich
funkcję `register()` jeżeli jest dostępna. To pozwala na centralne
rejestrowanie pluginów repozytoryjnych.
""")

import importlib
import pkgutil

from . import __path__ as _plugins_path


def register():
    """Importuj i zarejestruj wszystkie pod-pluginy w katalogu repo."""
    for finder, name, ispkg in pkgutil.iter_modules(_plugins_path):
        module_name = f"{__name__}.{name}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                module.register()
                print(f"[INFO][PLUGINS.repo] Registered sub-plugin: {name}")
            else:
                print(f"[INFO][PLUGINS.repo] Sub-module {name} has no register(); imported.")
        except Exception as e:
            print(f"[ERROR][PLUGINS.repo] Failed to load {name}: {e}")


__all__ = ["register"]
