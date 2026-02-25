#!/usr/bin/env python3
"""Simple build CLI: produce IRProgram from a source file."""

import json
import sys
from pathlib import Path

from lang.ir.generator import generate_ir_program
from lang.ir.types import IRProgram
from lang.lexer import Lexer
from lang.parser import Parser
from lang.semantics.resolver import Resolver, SemanticError


def serialize_ir(prog: IRProgram) -> dict:
    return {
        "code": [
            {"op": instr.op.name, "arg1": instr.arg1, "arg2": instr.arg2} for instr in prog.code
        ],
        "constants": prog.constants,
        "variables": prog.variables,
        "functions": prog.functions,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: dark8_build.py <file.d8>")
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(2)
    src = path.read_text()
    tokens = list(Lexer(src))
    parser = Parser(tokens)
    mod = parser.parse_module()
    # semantic resolution
    resolver = Resolver()
    try:
        resolver.resolve_module(mod)
    except SemanticError as e:
        print("Semantic errors detected:\n", e)
        sys.exit(2)
    prog = generate_ir_program(mod)
    out = path.with_suffix(".ir.json")
    out.write_text(json.dumps(serialize_ir(prog), indent=2))
    print(f"Wrote IR to {out}")


if __name__ == "__main__":
    main()
