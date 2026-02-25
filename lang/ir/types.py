from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Any, Dict


class OpCode(Enum):
    LOAD_CONST = auto()
    LOAD_VAR = auto()
    STORE_VAR = auto()
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    JUMP = auto()
    JUMP_IF_FALSE = auto()
    CALL = auto()
    RET = auto()
    POP = auto()
    NOP = auto()
    # comparisons
    EQ = auto()
    NEQ = auto()
    LT = auto()
    LTE = auto()
    GT = auto()
    GTE = auto()
    # logical
    AND = auto()
    OR = auto()
    NOT = auto()


@dataclass
class Instruction:
    op: OpCode
    arg1: int = 0
    arg2: int = 0


@dataclass
class IRProgram:
    code: List[Instruction]
    constants: List[Any]
    variables: List[str]
    functions: Dict[str, int]
    builtins: List[str]

    def __init__(self):
        self.code = []
        self.constants = []
        self.variables = []
        self.functions = {}
        # register known builtins so tooling can know about them
        self.builtins = ["print", "input"]

    def add_constant(self, value) -> int:
        try:
            return self.constants.index(value)
        except ValueError:
            self.constants.append(value)
            return len(self.constants) - 1

    def add_variable(self, name) -> int:
        if name in self.variables:
            return self.variables.index(name)
        self.variables.append(name)
        return len(self.variables) - 1

    def emit(self, instr: Instruction):
        self.code.append(instr)

    def is_builtin(self, name: str) -> bool:
        return name in self.builtins
