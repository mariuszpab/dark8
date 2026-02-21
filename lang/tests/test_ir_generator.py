from lang.lexer import Lexer
from lang.parser import Parser
from lang.ir.generator import generate_ir


def tokens_from(src):
    return list(Lexer(src))


def test_var_decl_to_ir():
    src = 'let x = 42\n'
    toks = tokens_from(src)
    p = Parser(toks)
    mod = p.parse_module()
    ir = generate_ir(mod)
    # expect PUSH 42, STORE x
    assert ir[0] == ("PUSH", 42)
    assert ir[1] == ("STORE", 'x')


def test_binary_expr_ir():
    src = 'let y = 1 + 2 * 3\n'
    toks = tokens_from(src)
    p = Parser(toks)
    mod = p.parse_module()
    ir = generate_ir(mod)
    # expected: PUSH 1, PUSH 2, PUSH 3, MUL, ADD, STORE y
    assert ir == [
        ("PUSH", 1),
        ("PUSH", 2),
        ("PUSH", 3),
        ("MUL",),
        ("ADD",),
        ("STORE", 'y'),
    ]
