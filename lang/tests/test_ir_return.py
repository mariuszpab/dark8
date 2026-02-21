from lang.lexer import Lexer
from lang.parser import Parser
from lang.ir.generator import generate_ir


def test_function_return_ir():
    src = 'fn add(a, b) { return a + b }\n'
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    ir = generate_ir(mod)
    # expect: FUNC metadata, LABEL add, LOAD a, LOAD b, ADD, RET
    assert ir == [
        ("FUNC", 'add', ['a', 'b']),
        ("LABEL", 'add'),
        ("LOAD", 'a'),
        ("LOAD", 'b'),
        ("ADD",),
        ("RET",),
    ]
