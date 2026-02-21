from lang.lexer import Lexer
from lang.parser import Parser
from lang.ir.generator import generate_ir
from lang.vm.vm import VM


def test_call_and_store_execution():
    src = (
        'fn add(a, b) { return a + b }\n'
        'let z = add(2, 3)\n'
    )
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    ir = generate_ir(mod)
    vm = VM(ir)
    vm.run()
    assert vm.globals.get('z') == 5
