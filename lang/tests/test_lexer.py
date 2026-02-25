from lang.lexer import Lexer, TokenType


def test_basic_tokens():
    code = "let x = 42\nfn add(a, b) { return a + b } // end"
    lex = Lexer(code)
    toks = list(lex)
    # expect sequence: KEYWORD(let), IDENT(x), OP('='), NUMBER(42), NEWLINE, KEYWORD(fn), IDENT(add)
    types = [t.type for t in toks if t.type != TokenType.COMMENT]
    assert types[0] == TokenType.KEYWORD
    assert types[1] == TokenType.IDENT
    assert any(t.type == TokenType.NUMBER for t in toks)
    assert types[-1] == TokenType.EOF


def test_string_token():
    code = 'let s = "hello\\nworld"'
    lex = Lexer(code)
    toks = list(lex)
    strings = [t for t in toks if t.type == TokenType.STRING]
    assert len(strings) == 1
    assert strings[0].value == "hello\\nworld"
