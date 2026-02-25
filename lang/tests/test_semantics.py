from lang.lexer import Lexer
from lang.parser import Parser
from lang.semantics.resolver import Resolver, SemanticError


def parse(src: str):
    tokens = list(Lexer(src))
    p = Parser(tokens)
    return p.parse_module()


def test_undeclared_variable():
    src = """
fn main() {
    let x = y + 1;
}
"""
    mod = parse(src)
    r = Resolver()
    try:
        r.resolve_module(mod)
        assert False, "Expected SemanticError for undeclared variable"
    except SemanticError as e:
        assert "undeclared variable" in str(e).lower()


def test_duplicate_var():
    src = """
let a = 1
let a = 2
"""
    mod = parse(src)
    r = Resolver()
    try:
        r.resolve_module(mod)
        assert False, "Expected SemanticError for duplicate variable"
    except SemanticError as e:
        assert "duplicate variable" in str(e).lower()


def test_function_arity():
    src = """
fn add(a,b) {
  return a + b;
}

fn main() {
  let r = add(1);
}
"""
    mod = parse(src)
    r = Resolver()
    try:
        r.resolve_module(mod)
        assert False, "Expected SemanticError for arity mismatch"
    except SemanticError as e:
        assert "arity" in str(e).lower()


def test_break_outside_loop():
    src = """
fn main() {
  break;
}
"""
    mod = parse(src)
    r = Resolver()
    try:
        r.resolve_module(mod)
        assert False, "Expected SemanticError for break outside loop"
    except SemanticError as e:
        assert "break' used" in str(e) or "break" in str(e).lower()
