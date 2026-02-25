from lang.lexer import Lexer
from lang.parser import Parser
from lang.ir.generator import generate_ir_program
from lang.ir.types import IRProgram, OpCode


def test_generate_ir_program_simple():
    src = (
        'let x = 2 + 3\n'
    )
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    prog = generate_ir_program(mod)
    assert isinstance(prog, IRProgram)
    # constants should contain 2 and 3
    assert 2 in prog.constants and 3 in prog.constants
    # variables should contain x
    assert 'x' in prog.variables
    # last instruction should be STORE_VAR for x
    assert prog.code[-1].op == OpCode.STORE_VAR
    vidx = prog.variables.index('x')
    assert prog.code[-1].arg1 == vidx
