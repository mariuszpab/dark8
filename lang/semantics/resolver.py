from typing import List

from lang.ast.nodes import (
    BinaryOp,
    Break,
    Call,
    Continue,
    Expr,
    FunctionDef,
    If,
    Literal,
    Module,
    Return,
    VarDecl,
    VarRef,
    While,
)
from lang.semantics.scope import Scope, Symbol


class SemanticError(Exception):
    pass


class Resolver:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.errors: List[str] = []
        self.loop_depth = 0
        self.in_function = False

    def error(self, msg: str):
        self.errors.append(msg)

    def resolve_module(self, module: Module):
        # Process top-level declarations
        for node in module.body:
            self._resolve_node(node)
        if self.errors:
            raise SemanticError("\n".join(self.errors))
        return module

    def _push_scope(self):
        self.current_scope = Scope(parent=self.current_scope)

    def _pop_scope(self):
        if self.current_scope.parent is not None:
            self.current_scope = self.current_scope.parent

    def _resolve_node(self, node):
        if isinstance(node, VarDecl):
            # resolve initializer
            if node.value is not None:
                self._resolve_expr(node.value)
            # define variable in current scope
            if self.current_scope.has_in_current(node.name):
                self.error(f"Duplicate variable declaration: {node.name}")
            else:
                self.current_scope.define(Symbol(name=node.name, kind="var", node=node))

        elif isinstance(node, FunctionDef):
            # define function in current scope first (allow recursion)
            if self.current_scope.has_in_current(node.name):
                self.error(f"Duplicate function declaration: {node.name}")
            else:
                self.current_scope.define(
                    Symbol(name=node.name, kind="func", params=node.params, node=node)
                )
            # resolve body in new scope
            self._push_scope()
            # define params as variables in function scope
            for p in node.params:
                if self.current_scope.has_in_current(p):
                    self.error(f"Duplicate parameter name: {p} in function {node.name}")
                else:
                    self.current_scope.define(Symbol(name=p, kind="var", node=node))
            prev_in_function = self.in_function
            self.in_function = True
            for stmt in node.body:
                self._resolve_node(stmt)
            self.in_function = prev_in_function
            self._pop_scope()

        elif isinstance(node, If):
            self._resolve_expr(node.cond)
            # optional new scope for then/else
            self._push_scope()
            for s in node.then_body:
                self._resolve_node(s)
            self._pop_scope()
            if node.else_body:
                self._push_scope()
                for s in node.else_body:
                    self._resolve_node(s)
                self._pop_scope()

        elif isinstance(node, While):
            self._resolve_expr(node.cond)
            self.loop_depth += 1
            self._push_scope()
            for s in node.body:
                self._resolve_node(s)
            self._pop_scope()
            self.loop_depth -= 1

        elif isinstance(node, Break):
            if self.loop_depth == 0:
                self.error("'break' used outside of loop")

        elif isinstance(node, Continue):
            if self.loop_depth == 0:
                self.error("'continue' used outside of loop")

        elif isinstance(node, Return):
            if not self.in_function:
                self.error("'return' used outside of function")
            if node.value is not None:
                self._resolve_expr(node.value)

        elif isinstance(node, Expr):
            # expression-statement
            self._resolve_expr(node)

        else:
            # Unknown node type - ignore
            pass

    def _resolve_expr(self, expr: Expr):
        if expr is None:
            return
        if isinstance(expr, Literal):
            return
        if isinstance(expr, VarRef):
            sym = self.current_scope.resolve(expr.name)
            if sym is None:
                self.error(f"Use of undeclared variable: {expr.name}")
            else:
                # attach resolved symbol for downstream passes
                try:
                    expr.resolved = sym
                except Exception:
                    pass
            return
        if isinstance(expr, Call):
            # resolve args
            for a in expr.args:
                self._resolve_expr(a)
            sym = self.current_scope.resolve(expr.name)
            if sym is None:
                self.error(f"Call to undeclared function: {expr.name}")
            else:
                if sym.kind != "func":
                    self.error(f"Symbol is not callable: {expr.name}")
                else:
                    expected = len(sym.params) if sym.params else 0
                    if expected != len(expr.args):
                        self.error(
                            f"Arity mismatch in call to {expr.name}: expected {expected}, got {len(expr.args)}"
                        )
                    else:
                        # attach resolved function symbol
                        try:
                            expr.resolved = sym
                        except Exception:
                            pass
            return
        if isinstance(expr, BinaryOp):
            self._resolve_expr(expr.left)
            self._resolve_expr(expr.right)
            return
        # fallback: nothing
