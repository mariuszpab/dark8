"""Simple recursive-descent parser for DARK8 (minimal features).

Supports:
- let <ident> = <literal>
- fn <ident>(params) { ... }
"""
from typing import List
from lang.lexer import Token, TokenType
from lang.ast.nodes import Module, VarDecl, FunctionDef, Literal, Expr, VarRef, BinaryOp, Return, Call


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, "", -1, -1)

    def advance(self) -> Token:
        t = self.peek()
        self.pos += 1
        return t

    def expect(self, ttype: TokenType, value: str = None) -> Token:
        t = self.peek()
        if t.type is not ttype or (value is not None and t.value != value):
            raise ParserError(f"Expected {ttype} {value}, got {t.type} '{t.value}' at {t.line}:{t.col}")
        return self.advance()

    def parse_module(self) -> Module:
        body = []
        while True:
            t = self.peek()
            if t.type == TokenType.EOF:
                break
            if t.type == TokenType.NEWLINE or t.type == TokenType.COMMENT:
                self.advance()
                continue
            if t.type == TokenType.KEYWORD and t.value == 'let':
                body.append(self.parse_let())
                continue
            if t.type == TokenType.KEYWORD and t.value == 'fn':
                body.append(self.parse_fn())
                continue
            # fallback: skip token
            self.advance()
        return Module(body=body)

    def parse_let(self) -> VarDecl:
        self.expect(TokenType.KEYWORD, 'let')
        ident = self.expect(TokenType.IDENT)
        # expect '=' operator
        self.expect(TokenType.OP, '=')
        expr = self.parse_expression()
        # optional newline or semicolon
        if self.peek().type == TokenType.OP and self.peek().value == ';':
            self.advance()
        if self.peek().type == TokenType.NEWLINE:
            self.advance()
        return VarDecl(name=ident.value, value=expr)

    def parse_fn(self) -> FunctionDef:
        self.expect(TokenType.KEYWORD, 'fn')
        name = self.expect(TokenType.IDENT).value
        # params
        self.expect(TokenType.OP, '(')
        params = []
        while self.peek().type != TokenType.OP or self.peek().value != ')':
            if self.peek().type == TokenType.IDENT:
                params.append(self.advance().value)
                if self.peek().type == TokenType.OP and self.peek().value == ',':
                    self.advance()
                    continue
                continue
            # allow empty
            break
        self.expect(TokenType.OP, ')')
        # body { ... } - parse statements inside body into a list
        self.expect(TokenType.OP, '{')
        body_nodes = []
        while True:
            t = self.peek()
            if t.type == TokenType.OP and t.value == '}':
                self.advance()
                break
            if t.type == TokenType.EOF:
                raise ParserError("Unterminated function body")
            if t.type == TokenType.NEWLINE or t.type == TokenType.COMMENT:
                self.advance()
                continue
            if t.type == TokenType.KEYWORD and t.value == 'let':
                body_nodes.append(self.parse_let())
                continue
            if t.type == TokenType.KEYWORD and t.value == 'return':
                # consume 'return' and parse the following expression
                self.advance()
                expr = self.parse_expression()
                # optional semicolon
                if self.peek().type == TokenType.OP and self.peek().value == ';':
                    self.advance()
                body_nodes.append(Return(value=expr))
                continue
            # for now parse expression statements
            expr = self.parse_expression()
            # optional semicolon
            if self.peek().type == TokenType.OP and self.peek().value == ';':
                self.advance()
            body_nodes.append(expr)
        return FunctionDef(name=name, params=params, body=body_nodes)

    def parse_expression(self) -> Expr:
        # expression parser with precedence (binops +, -, *, /) and parentheses
        return self.parse_binop()

    def parse_primary(self) -> Expr:
        t = self.peek()
        if t.type == TokenType.NUMBER:
            self.advance()
            return Literal(value=float(t.value) if '.' in t.value else int(t.value))
        if t.type == TokenType.STRING:
            self.advance()
            return Literal(value=t.value)
        if t.type == TokenType.IDENT:
            # could be a function call
            ident = self.advance()
            if self.peek().type == TokenType.OP and self.peek().value == '(':
                # parse call args
                self.advance()  # consume '('
                args = []
                while self.peek().type != TokenType.OP or self.peek().value != ')':
                    args.append(self.parse_expression())
                    if self.peek().type == TokenType.OP and self.peek().value == ',':
                        self.advance()
                        continue
                    break
                self.expect(TokenType.OP, ')')
                return Call(name=ident.value, args=args)
            return VarRef(name=ident.value)
        if t.type == TokenType.OP and t.value == '(':
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.OP, ')')
            return expr
        raise ParserError(f"Unexpected token in expression: {t.type} '{t.value}' at {t.line}:{t.col}")

    def parse_binop(self, min_prec: int = 0) -> Expr:
        left = self.parse_primary()
        prec = {"+": 10, "-": 10, "*": 20, "/": 20}
        while True:
            t = self.peek()
            if t.type != TokenType.OP or t.value not in prec:
                break
            op = t.value
            op_prec = prec[op]
            if op_prec < min_prec:
                break
            # consume operator
            self.advance()
            # parse next primary or higher-precedence binary op
            right = self.parse_binop(op_prec + 1)
            left = BinaryOp(left=left, op=op, right=right)
        return left
