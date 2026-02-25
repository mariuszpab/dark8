from lang.ir.generator import generate_ir_program
from lang.lexer import Lexer
from lang.parser import Parser
from lang.vm.vm_irprogram import VMProgram


def test_print_builtin_outputs():
    src = 'fn foo() { print("hello", 123); }\n' "let _ = foo();\n"
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    prog = generate_ir_program(mod)
    vm = VMProgram(prog)
    vm.run()
    assert any("hello 123" in (o or "") for o in vm.outputs)
