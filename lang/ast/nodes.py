from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Node:
    pass


@dataclass
class Expr(Node):
    pass


@dataclass
class Literal(Expr):
    value: object


@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr


@dataclass
class VarRef(Expr):
    name: str
    resolved: object = None


@dataclass
class Return(Node):
    value: Optional[Expr]


@dataclass
class Call(Expr):
    name: str
    args: List[Expr]
    resolved: object = None


@dataclass
class If(Node):
    cond: Expr
    then_body: List[Node]
    else_body: Optional[List[Node]] = None


@dataclass
class While(Node):
    cond: Expr
    body: List[Node]


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


@dataclass
class VarDecl(Node):
    name: str
    value: Optional[Expr]


@dataclass
class FunctionDef(Node):
    name: str
    params: List[str]
    body: List[Node]


@dataclass
class Module(Node):
    body: List[Node]
