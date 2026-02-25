"""VM for new IRProgram format (stack-based)."""
from typing import Any
from lang.ir.types import IRProgram, OpCode
from lang.runtime import builtins as runtime_builtins


class VMProgram:
    def __init__(self, prog: IRProgram):
        self.prog = prog
        self.ip = 0
        self.stack: list[Any] = []
        self.globals = {}
        self.frames = []  # frames store dicts with ret_ip, locals, fp
        self.fp = 0
        self.sp = 0
        # capture outputs of builtin calls (for testing)
        self.outputs: list[Any] = []

    def _underflow_error(self, op):
        raise RuntimeError(f"VM stack underflow at ip={self.ip-1} op={op}")

    def _pop(self, op=None):
        try:
            return self.stack.pop()
        except IndexError:
            self._underflow_error(op)

    def _pop_n(self, n: int, op=None):
        if n <= 0:
            return []
        if len(self.stack) < n:
            self._underflow_error(op)
        vals = [self.stack.pop() for _ in range(n)]
        return vals

    def run(self):
        code = self.prog.code
        while self.ip < len(code):
            instr = code[self.ip]
            self.ip += 1
            op = instr.op
            try:
                if op == OpCode.NOP:
                    continue
                if op == OpCode.LOAD_CONST:
                    self.stack.append(self.prog.constants[instr.arg1])
                elif op == OpCode.LOAD_VAR:
                    name = self.prog.variables[instr.arg1]
                    # check current frame locals first
                    if self.frames and name in self.frames[-1]["locals"]:
                        self.stack.append(self.frames[-1]["locals"][name])
                    else:
                        self.stack.append(self.globals.get(name))
                elif op == OpCode.STORE_VAR:
                    name = self.prog.variables[instr.arg1]
                    val = self.stack.pop()
                    if self.frames:
                        self.frames[-1]["locals"][name] = val
                    else:
                        # store in globals
                        self.globals[name] = val
                if op in (OpCode.ADD, OpCode.SUB, OpCode.MUL, OpCode.DIV):
                    b = self._pop(op)
                    a = self._pop(op)
                    try:
                        if op == OpCode.ADD:
                            self.stack.append(a + b)
                        elif op == OpCode.SUB:
                            self.stack.append(a - b)
                        elif op == OpCode.MUL:
                            self.stack.append(a * b)
                        elif op == OpCode.DIV:
                            self.stack.append(a / b)
                    except Exception as e:
                        raise RuntimeError(f"VM arithmetic error at ip={self.ip-1} op={op}: {e}")
                elif op == OpCode.JUMP:
                    self.ip = instr.arg1
                elif op == OpCode.JUMP_IF_FALSE:
                    cond = self._pop(op)
                    if not cond:
                        self.ip = instr.arg1
                elif op == OpCode.CALL:
                    fname = self.prog.constants[instr.arg1]
                    # builtin handlers centralised in lang.runtime.builtins
                    if fname in runtime_builtins.BUILTINS:
                        argc = instr.arg2
                        args = self._pop_n(argc, op)[::-1]
                        handler = runtime_builtins.BUILTINS[fname]
                        try:
                            val = handler(self, args)
                        except Exception as e:
                            raise RuntimeError(f"Builtin '{fname}' error at ip={self.ip-1}: {e}")
                        # push return value (could be None)
                        self.stack.append(val)
                        self.sp = len(self.stack)
                        continue
                    # resolve function offset
                    if fname not in self.prog.functions:
                        raise RuntimeError(f"Unknown function: {fname}")
                    func_info = self.prog.functions[fname]
                    func_ip = func_info["offset"]
                    params = func_info.get("params", [])
                    argc = instr.arg2
                    args = self._pop_n(argc, op)[::-1]
                    locals_map = {}
                    for i, p in enumerate(params):
                        locals_map[p] = args[i] if i < len(args) else None
                    # push frame with return ip, locals and frame pointer
                    frame = {"ret_ip": self.ip, "locals": locals_map, "fp": len(self.stack)}
                    self.frames.append(frame)
                    self.fp = frame["fp"]
                    self.sp = len(self.stack)
                    self.ip = func_ip
                elif op == OpCode.RET:
                    # if no frames, stop execution
                    if not self.frames:
                        return
                    frame = self.frames.pop()
                    ret_ip = frame["ret_ip"]
                    # if function left a value on the stack (above fp), treat it as return
                    if len(self.stack) > frame["fp"]:
                        ret_val = self._pop(op)
                    else:
                        ret_val = None
                    # restore stack to frame pointer and push return value
                    self.stack = self.stack[: frame["fp"]]
                    self.stack.append(ret_val)
                    self.ip = ret_ip
                    # restore fp/sp
                    self.fp = self.frames[-1]["fp"] if self.frames else 0
                    self.sp = len(self.stack)
                elif op == OpCode.POP:
                    self._pop(op)
                elif op == OpCode.EQ:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a == b)
                elif op == OpCode.NEQ:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a != b)
                elif op == OpCode.LT:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a < b)
                elif op == OpCode.GT:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a > b)
                elif op == OpCode.LTE:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a <= b)
                elif op == OpCode.GTE:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a >= b)
                elif op == OpCode.AND:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a and b)
                elif op == OpCode.OR:
                    b = self._pop(op)
                    a = self._pop(op)
                    self.stack.append(a or b)
                elif op == OpCode.NOT:
                    a = self._pop(op)
                    self.stack.append(not a)
                else:
                    raise RuntimeError(f"Unsupported opcode in VM: {op}")
            except Exception as e:
                raise RuntimeError(f"VM runtime error at ip={self.ip-1} op={op}: {e}")
