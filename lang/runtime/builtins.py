from typing import Any, List


def builtin_print(vm, args: List[Any]):
    # append to VM outputs for deterministic testing
    vm.outputs.append(" ".join(str(a) for a in args))
    return None


def builtin_input(vm, args: List[Any]):
    prompt = args[0] if args else ''
    try:
        return input(prompt)
    except Exception:
        return ''


BUILTINS = {
    'print': builtin_print,
    'input': builtin_input,
}
