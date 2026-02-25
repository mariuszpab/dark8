"""AST -> IR generator.

This module preserves the old tuple-based `generate_ir` for backward
compatibility but also exposes `generate_ir_program` which builds a
structured `IRProgram` (see `lang.ir.types`).
"""

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
from lang.ir.types import Instruction, IRProgram, OpCode


class IRGenerator:
    """Backward-compatible generator that emits simple tuple-style IR."""

    def __init__(self):
        self.instructions = []

    def gen(self, node) -> List[tuple]:
        if isinstance(node, Module):
            return self.gen_module(node)
        else:
            raise TypeError("Unsupported node for gen: %r" % type(node))

    def gen_module(self, module: Module) -> List[tuple]:
        self.instructions = []
        for n in module.body:
            self.gen_node(n)
        return self.instructions

    def gen_node(self, node):
        from lang.ir.generator import IRGenerator  # noqa: F401

        if isinstance(node, VarDecl):
            self.gen_expr(node.value)
            self.instructions.append(("STORE", node.name))
        elif isinstance(node, FunctionDef):
            self.instructions.append(("FUNC", node.name, node.params))
            self.instructions.append(("LABEL", node.name))
            for stmt in node.body:
                self.gen_node(stmt)
            if not self.instructions or self.instructions[-1] != (("RET",)):
                self.instructions.append(("RET",))
        elif isinstance(node, Expr):
            self.gen_expr(node)
            self.instructions.append(("POP",))
        elif isinstance(node, Break):
            # tuple-style: JUMP placeholder for break
            self.instructions.append(("JUMP", None))
        elif isinstance(node, Continue):
            # tuple-style: JUMP back to a caller-provided target isn't available here
            # We'll emit a special marker (JUMP, -1) and let surrounding While handle it.
            self.instructions.append(("JUMP", -1))
        elif isinstance(node, If):
            # tuple-style generator: generate cond, JUMP_IF_FALSE to else, then body, optional JUMP past else
            self.gen_expr(node.cond)
            # placeholder
            j_false_pos = len(self.instructions)
            self.instructions.append(("JUMP_IF_FALSE", None))
            # then body
            for stmt in node.then_body:
                self.gen_node(stmt)
            # jump over else
            j_end_pos = None
            if node.else_body:
                j_end_pos = len(self.instructions)
                self.instructions.append(("JUMP", None))
                # backpatch false to next instr
                self.instructions[j_false_pos] = ("JUMP_IF_FALSE", len(self.instructions))
                for stmt in node.else_body:
                    self.gen_node(stmt)
                # backpatch end
                self.instructions[j_end_pos] = ("JUMP", len(self.instructions))
            else:
                # no else: backpatch false to here
                self.instructions[j_false_pos] = ("JUMP_IF_FALSE", len(self.instructions))
        elif isinstance(node, While):
            # while: loop_start -> cond -> JUMP_IF_FALSE exit -> body -> JUMP loop_start
            loop_start = len(self.instructions)
            self.gen_expr(node.cond)
            j_false_pos = len(self.instructions)
            self.instructions.append(("JUMP_IF_FALSE", None))
            for stmt in node.body:
                self.gen_node(stmt)
            # jump back to start
            self.instructions.append(("JUMP", loop_start))
            # backpatch exit
            self.instructions[j_false_pos] = ("JUMP_IF_FALSE", len(self.instructions))
        elif isinstance(node, Return):
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
            for a in expr.args:
                self.gen_expr(a)
            self.instructions.append(("CALL", expr.name, len(expr.args)))
        else:
            raise TypeError("Unhandled expr type: %r" % type(expr))


def generate_ir(module: Module) -> List[tuple]:
    gen = IRGenerator()
    return gen.gen(module)


class IRProgramGenerator:
    """Generates a structured IRProgram from AST.

    - constants are deduplicated and referenced by index
    - variables are tracked and referenced by index
    - functions map to code offsets in the resulting program
    """

    def __init__(self):
        self.prog = IRProgram()

    def gen(self, node: Module) -> IRProgram:
        for n in node.body:
            self.gen_node(n)
        return self.prog

    def gen_node(self, node):
        if isinstance(node, VarDecl):
            self.gen_expr(node.value)
            vidx = self.prog.add_variable(node.name)
            self.prog.emit(Instruction(OpCode.STORE_VAR, vidx, 0))
        elif isinstance(node, FunctionDef):
            # emit a jump to skip the function body at load time
            jpos = len(self.prog.code)
            self.prog.emit(Instruction(OpCode.JUMP, 0, 0))
            # function entry point
            func_offset = len(self.prog.code)
            # record function offset and params
            self.prog.functions[node.name] = {"offset": func_offset, "params": node.params}
            # generate body
            for stmt in node.body:
                self.gen_node(stmt)
            # ensure RET
            if not self.prog.code or self.prog.code[-1].op != OpCode.RET:
                self.prog.emit(Instruction(OpCode.RET))
            # backpatch the initial jump to after the function body
            self.prog.code[jpos].arg1 = len(self.prog.code)
        elif isinstance(node, Expr):
            self.gen_expr(node)
            self.prog.emit(Instruction(OpCode.POP))
        elif isinstance(node, Return):
            self.gen_expr(node.value)
            self.prog.emit(Instruction(OpCode.RET))
        elif isinstance(node, If):
            # cond
            self.gen_expr(node.cond)
            # placeholder for JUMP_IF_FALSE -> to else/start of after-if
            jfalse_pos = len(self.prog.code)
            self.prog.emit(Instruction(OpCode.JUMP_IF_FALSE, 0, 0))
            # then body
            for stmt in node.then_body:
                self.gen_node(stmt)
            if node.else_body:
                # placeholder for jump over else
                jend_pos = len(self.prog.code)
                self.prog.emit(Instruction(OpCode.JUMP, 0, 0))
                # backpatch JUMP_IF_FALSE to start of else
                self.prog.code[jfalse_pos].arg1 = len(self.prog.code)
                for stmt in node.else_body:
                    self.gen_node(stmt)
                # backpatch JUMP to after else
                self.prog.code[jend_pos].arg1 = len(self.prog.code)
            else:
                # no else: backpatch JUMP_IF_FALSE to here
                self.prog.code[jfalse_pos].arg1 = len(self.prog.code)
        elif isinstance(node, While):
            loop_start = len(self.prog.code)
            # condition
            self.gen_expr(node.cond)
            jfalse_pos = len(self.prog.code)
            self.prog.emit(Instruction(OpCode.JUMP_IF_FALSE, 0, 0))
            # body with break/continue handling
            break_positions = []
            for stmt in node.body:
                if isinstance(stmt, Break):
                    # emit jump to be backpatched to exit
                    pos = len(self.prog.code)
                    self.prog.emit(Instruction(OpCode.JUMP, 0, 0))
                    break_positions.append(pos)
                    continue
                if isinstance(stmt, Continue):
                    # jump back to condition (loop_start)
                    self.prog.emit(Instruction(OpCode.JUMP, loop_start, 0))
                    continue
                self.gen_node(stmt)
            # jump back to loop start
            self.prog.emit(Instruction(OpCode.JUMP, loop_start, 0))
            # backpatch exit
            self.prog.code[jfalse_pos].arg1 = len(self.prog.code)
            for p in break_positions:
                self.prog.code[p].arg1 = len(self.prog.code)
        else:
            raise TypeError(f"Unhandled node type: {type(node)}")

    def gen_expr(self, expr: Expr):
        if expr is None:
            return
        if isinstance(expr, Literal):
            cidx = self.prog.add_constant(expr.value)
            self.prog.emit(Instruction(OpCode.LOAD_CONST, cidx, 0))
        elif isinstance(expr, VarRef):
            vidx = self.prog.add_variable(expr.name)
            self.prog.emit(Instruction(OpCode.LOAD_VAR, vidx, 0))
        elif isinstance(expr, BinaryOp):
            self.gen_expr(expr.left)
            self.gen_expr(expr.right)
            op_map = {
                "+": OpCode.ADD,
                "-": OpCode.SUB,
                "*": OpCode.MUL,
                "/": OpCode.DIV,
            }
            opc = op_map.get(expr.op)
            if opc is None:
                raise ValueError(f"Unknown binary op: {expr.op}")
            self.prog.emit(Instruction(opc))
        elif isinstance(expr, Call):
            for a in expr.args:
                self.gen_expr(a)
            # function index is stored in functions table (resolve name)
            # we'll store function name index via constants as a simple approach
            fname_idx = self.prog.add_constant(expr.name)
            self.prog.emit(Instruction(OpCode.CALL, fname_idx, len(expr.args)))
        else:
            raise TypeError(f"Unhandled expr type: {type(expr)}")


def generate_ir_program(module: Module) -> IRProgram:
    gen = IRProgramGenerator()
    return gen.gen(module)
