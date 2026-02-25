"""Simple stack VM for DARK8 IR."""

from typing import Any, Dict, List, Tuple

Instr = Tuple


class Frame:
    def __init__(self, return_pc: int, locals: Dict[str, Any]):
        self.return_pc = return_pc
        self.locals = locals


class VM:
    def __init__(self, instrs: List[Instr]):
        self.instrs = instrs
        self.pc = 0
        self.stack: List[Any] = []
        self.frames: List[Frame] = []
        self.globals: Dict[str, Any] = {}
        self.labels: Dict[str, int] = {}
        self.funcs: Dict[str, Dict] = {}
        self._scan()

    def _scan(self):
        for i, ins in enumerate(self.instrs):
            if not ins:
                continue
            op = ins[0]
            if op == "LABEL":
                self.labels[ins[1]] = i
            if op == "FUNC":
                # ('FUNC', name, params)
                self.funcs[ins[1]] = {"params": ins[2], "label": None}
        # attach label positions to funcs
        for name in list(self.funcs.keys()):
            if name in self.labels:
                self.funcs[name]["label"] = self.labels[name]
                # find end (first RET after label)
                start = self.funcs[name]["label"]
                end = None
                for j in range(start, len(self.instrs)):
                    ins = self.instrs[j]
                    if ins and ins[0] == "RET":
                        end = j
                        break
                self.funcs[name]["end"] = end

    def run(self):
        while self.pc < len(self.instrs):
            ins = self.instrs[self.pc]
            self.pc += 1
            if not ins:
                continue
            op = ins[0]
            if op == "PUSH":
                self.stack.append(ins[1])
            elif op == "POP":
                self.stack.pop()
            elif op == "STORE":
                name = ins[1]
                val = self.stack.pop()
                if self.frames:
                    self.frames[-1].locals[name] = val
                else:
                    self.globals[name] = val
            elif op == "LOAD":
                name = ins[1]
                if self.frames and name in self.frames[-1].locals:
                    self.stack.append(self.frames[-1].locals[name])
                else:
                    self.stack.append(self.globals.get(name))
            elif op == "ADD":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
            elif op == "SUB":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
            elif op == "MUL":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
            elif op == "DIV":
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a / b)
            elif op == "LABEL":
                # if this label is for a function and we're at module-level, skip the function body
                name = ins[1]
                if not self.frames and name in self.funcs:
                    end = self.funcs[name].get("end")
                    if end is not None:
                        self.pc = end + 1
                        continue
                continue
            elif op == "FUNC":
                # metadata only
                continue
            elif op == "CALL":
                # ('CALL', name, arg_count)
                _, name, argc = ins
                args = [self.stack.pop() for _ in range(argc)][::-1]
                if name not in self.funcs or self.funcs[name].get("label") is None:
                    raise RuntimeError(f"Unknown function {name}")
                label_pc = self.funcs[name]["label"]
                params = self.funcs[name]["params"]
                # bind params to args in new frame
                locals_map = {}
                for i, p in enumerate(params):
                    locals_map[p] = args[i] if i < len(args) else None
                # push frame with return pc
                self.frames.append(Frame(return_pc=self.pc, locals=locals_map))
                # jump to function body (label+1)
                self.pc = label_pc + 1
            elif op == "RET":
                # pop frame and return to caller
                if not self.frames:
                    # module-level RET -> stop
                    return
                frame = self.frames.pop()
                # return value (if any) should remain on stack
                self.pc = frame.return_pc
            else:
                raise RuntimeError(f"Unknown opcode: {op}")
