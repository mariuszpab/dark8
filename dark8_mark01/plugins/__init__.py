import importlib
import pkgutil
from typing import List, Optional, Sequence


def load_plugins(paths: Optional[Sequence[str]] = None, package_name: Optional[str] = None):
    """Load and register plugins from the `dark8_mark01.plugins` package.

    If `paths` is provided it will be used instead of the package's
    `__path__` which makes the function testable. If `package_name` is
    provided it will be used as the import base for submodules.

    The loader raises `RuntimeError` when duplicate plugin names are
    detected across multiple directories to avoid silent shadowing.
    """
    if paths is None:
        from . import __path__ as plugins_path
    else:
        plugins_path = list(paths)

    if package_name is None:
        package_name = __name__

    # Detect duplicates across individual paths to avoid silent shadowing
    name_counts: dict = {}
    for p in plugins_path:
        for _finder, name, _ispkg in pkgutil.iter_modules([p]):
            name_counts[name] = name_counts.get(name, 0) + 1

    conflicts = [n for n, c in name_counts.items() if c > 1]
    if conflicts:
        raise RuntimeError(f"Plugin name conflict detected: {conflicts}")

    seen: List[str] = []
    for finder, name, ispkg in pkgutil.iter_modules(plugins_path):
        if name in seen:
            raise RuntimeError(f"Plugin name conflict detected: {name}")
        seen.append(name)

        module_name = f"{package_name}.{name}"
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "register"):
                module.register()
                print(f"[INFO][PLUGINS] Załadowano plugin: {name}")
            else:
                print(f"[INFO][PLUGINS] Plugin {name} nie ma funkcji register() — pomijam.")
        except Exception as e:
            print(f"[ERROR][PLUGINS] Błąd ładowania {name}: {e}")


__all__ = ["load_plugins"]
