import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterator


class TokenType(Enum):
    KEYWORD = auto()
    IDENT = auto()
    NUMBER = auto()
    STRING = auto()
    OP = auto()
    COMMENT = auto()
    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    col: int


class LexerError(Exception):
    pass


class Lexer:
    KEYWORDS = {
        "fn",
        "let",
        "if",
        "else",
        "return",
        "while",
        "for",
        "class",
        "import",
        "module",
        "true",
        "false",
    }

    token_specification = [
        ("NUMBER",   r"\d+(?:\.\d+)?"),
        ("IDENT",    r"[A-Za-z_][A-Za-z0-9_]*"),
        ("STRING",   r'"(?:\\.|[^"\\])*"'),
        ("OP",       r"==|!=|<=|>=|->|\+\+|--|\+|-|\*|/|%|=|<|>|\(|\)|\{|\}|\[|\]|,|:|;|\.|\\"),
        ("NEWLINE",  r"\n"),
        ("SKIP",     r"[ \t]+"),
        ("COMMENT",  r"//.*"),
    ]

    tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)
    get_token = re.compile(tok_regex).match

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.end = len(text)

    def __iter__(self) -> Iterator[Token]:
        while self.pos < self.end:
            m = self.get_token(self.text, self.pos)
            if not m:
                raise LexerError(f"Unexpected character at {self.line}:{self.col}: '{self.text[self.pos]}'")
            kind = m.lastgroup
            value = m.group(kind)
            if kind == "NUMBER":
                tok = Token(TokenType.NUMBER, value, self.line, self.col)
                yield tok
            elif kind == "IDENT":
                if value in self.KEYWORDS:
                    yield Token(TokenType.KEYWORD, value, self.line, self.col)
                else:
                    yield Token(TokenType.IDENT, value, self.line, self.col)
            elif kind == "STRING":
                # strip quotes
                sval = value[1:-1]
                yield Token(TokenType.STRING, sval, self.line, self.col)
            elif kind == "OP":
                yield Token(TokenType.OP, value, self.line, self.col)
            elif kind == "NEWLINE":
                yield Token(TokenType.NEWLINE, "\n", self.line, self.col)
                self.line += 1
                self.col = 0
            elif kind == "SKIP":
                pass
            elif kind == "COMMENT":
                yield Token(TokenType.COMMENT, value, self.line, self.col)
            self.pos = m.end()
            # update col: approximate by length of matched
            self.col += m.end() - m.start()
        yield Token(TokenType.EOF, "", self.line, self.col)
