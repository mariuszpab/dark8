import os

from .command_registry import get_handler
from .commands.flow_ops import is_block_active  # tylko do IF


def parse_mpx_file(path):
    if not os.path.exists(path):
        print(f"[ERROR][MPX] Plik skryptu nie istnieje: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    total = len(lines)

    while i < total:
        line = lines[i].rstrip("\n").strip()

        if not line or line.startswith("#"):
            i += 1
            continue

        parts = line.split(maxsplit=1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else ""

        block = None
        if i + 1 < total and lines[i + 1].strip().startswith("<<<END"):
            i += 2
            block_lines = []
            while i < total and lines[i].strip() != "END":
                block_lines.append(lines[i])
                i += 1
            block = "".join(block_lines)
            i += 1
        else:
            i += 1

        # IF – zawsze przepuszczamy, reszta respektuje is_block_active()
        if not is_block_active() and command not in ("IF_EXISTS", "IF_NOT_EXISTS", "END_IF"):
            continue

        handler = get_handler(command)
        if handler is None:
            print(f"[ERROR][MPX] Nieznana komenda: {command}")
            continue

        handler(command, args, block)
