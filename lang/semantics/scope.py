from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Symbol:
    name: str
    kind: str  # 'var' or 'func'
    params: Optional[List[str]] = None
    node: object = None


class Scope:
    def __init__(self, parent: Optional["Scope"] = None):
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def define(self, sym: Symbol):
        if sym.name in self.symbols:
            raise KeyError(f"Symbol already defined in this scope: {sym.name}")
        self.symbols[sym.name] = sym

    def resolve(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.resolve(name)
        return None

    def has_in_current(self, name: str) -> bool:
        return name in self.symbols
