from lang.ast.nodes import FunctionDef, Literal, VarDecl
from lang.lexer import Lexer
from lang.parser import Parser


def test_parse_let():
    src = "let x = 123\n"
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    assert len(mod.body) == 1
    stmt = mod.body[0]
    assert isinstance(stmt, VarDecl)
    assert stmt.name == "x"
    assert isinstance(stmt.value, Literal)
    assert stmt.value.value == 123


def test_parse_fn():
    src = "fn add(a, b) { return a + b }\n"
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    assert len(mod.body) == 1
    fn = mod.body[0]
    assert isinstance(fn, FunctionDef)
    assert fn.name == "add"
    assert fn.params == ["a", "b"]


def test_binary_expression_precedence():
    src = "let x = 1 + 2 * 3\n"
    toks = list(Lexer(src))
    p = Parser(toks)
    mod = p.parse_module()
    stmt = mod.body[0]
    assert stmt.name == "x"
    expr = stmt.value
    # expect top-level + with left=1 and right=(2*3)
    assert hasattr(expr, "op") and expr.op == "+"
    assert expr.left.value == 1
    assert expr.right.op == "*"
    assert expr.right.left.value == 2
    assert expr.right.right.value == 3
