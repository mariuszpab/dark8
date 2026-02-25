from lang.ir.generator import generate_ir_program
from lang.lexer import Lexer
from lang.parser import Parser
from lang.vm.vm_irprogram import VMProgram


def test_call_and_store_execution():
    src = "fn add(a, b) { return a + b }\n" "let z = add(2, 3)\n"
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    prog = generate_ir_program(mod)
    vm = VMProgram(prog)
    vm.run()
    assert vm.globals.get("z") == 5
