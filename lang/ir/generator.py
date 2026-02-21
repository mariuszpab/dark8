"""Simple AST -> IR generator for DARK8.

Generates a list of tuple instructions, e.g.
- ("PUSH", value)
- ("STORE", name)
- ("LOAD", name)
- ("ADD",)
- ("SUB",)
- ("MUL",)
- ("DIV",)
- ("LABEL", name)
- ("RET",)
"""
from typing import List, Tuple, Any
from lang.ast.nodes import Module, VarDecl, FunctionDef, Literal, BinaryOp, VarRef, Expr, Return, Call

Instr = Tuple[str, Any]


class IRGenerator:
    def __init__(self):
        self.instructions: List[Instr] = []

    def gen(self, node) -> List[Instr]:
        if isinstance(node, Module):
            return self.gen_module(node)
        else:
            raise TypeError("Unsupported node for gen: %r" % type(node))

    def gen_module(self, module: Module) -> List[Instr]:
        self.instructions = []
        for n in module.body:
            self.gen_node(n)
        return self.instructions

    def gen_node(self, node):
        if isinstance(node, VarDecl):
            self.gen_expr(node.value)
            # store top of stack into variable
            self.instructions.append(("STORE", node.name))
        elif isinstance(node, FunctionDef):
            # emit function metadata and label, then generate body
            self.instructions.append(("FUNC", node.name, node.params))
            self.instructions.append(("LABEL", node.name))
            for stmt in node.body:
                self.gen_node(stmt)
            # only append RET if function body didn't already emit a RET
            if not self.instructions or self.instructions[-1] != ("RET",):
                self.instructions.append(("RET",))
        elif isinstance(node, Expr):
            # expression statement
            self.gen_expr(node)
            self.instructions.append(("POP",))
        elif isinstance(node, Return):
            # generate return value and emit RET (value stays on stack)
            self.gen_expr(node.value)
            self.instructions.append(("RET",))
        else:
            raise TypeError("Unhandled node type: %r" % type(node))

    def gen_expr(self, expr: Expr):
        if expr is None:
            return
        if isinstance(expr, Literal):
            self.instructions.append(("PUSH", expr.value))
        elif isinstance(expr, VarRef):
            self.instructions.append(("LOAD", expr.name))
        elif isinstance(expr, BinaryOp):
            # left then right, then operator
            self.gen_expr(expr.left)
            self.gen_expr(expr.right)
            op_map = {
                "+": "ADD",
                "-": "SUB",
                "*": "MUL",
                "/": "DIV",
            }
            opcode = op_map.get(expr.op)
            if opcode is None:
                raise ValueError(f"Unknown binary op: {expr.op}")
            self.instructions.append((opcode,))
        elif isinstance(expr, Call):
            # generate args left-to-right then emit CALL
            for a in expr.args:
                self.gen_expr(a)
            self.instructions.append(("CALL", expr.name, len(expr.args)))
        else:
            raise TypeError("Unhandled expr type: %r" % type(expr))


def generate_ir(module: Module) -> List[Instr]:
    gen = IRGenerator()
    return gen.gen(module)
