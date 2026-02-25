from lang.ir.generator import generate_ir_program
from lang.ir.types import OpCode
from lang.lexer import Lexer
from lang.parser import Parser


def test_if_without_else():
    src = "fn main() {\n" "  if (1) {\n" "    let x = 2\n" "  }\n" "}\n"
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    prog = generate_ir_program(mod)
    # find first JUMP_IF_FALSE
    ops = [instr.op for instr in prog.code]
    assert OpCode.JUMP_IF_FALSE in ops


def test_if_with_else():
    src = (
        "fn main() {\n"
        "  if (0) {\n"
        "    let x = 1\n"
        "  } else {\n"
        "    let y = 2\n"
        "  }\n"
        "}\n"
    )
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    prog = generate_ir_program(mod)
    ops = [instr.op for instr in prog.code]
    assert OpCode.JUMP_IF_FALSE in ops
    assert OpCode.JUMP in ops


def test_while_loop():
    src = "fn main() {\n" "  while (0) {\n" "    let x = 1\n" "  }\n" "}\n"
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    prog = generate_ir_program(mod)
    ops = [instr.op for instr in prog.code]
    assert OpCode.JUMP_IF_FALSE in ops
    assert OpCode.JUMP in ops
