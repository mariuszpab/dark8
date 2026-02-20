from ..command_registry import register_command, list_commands


def handle_command_list(command, args, block):
    """
    COMMAND_LIST
    Wypisuje wszystkie zarejestrowane komendy (core + pluginy).
    """
    cmds = list_commands()
    print("[COMMAND_LIST] Dostępne komendy:")
    for c in cmds:
        print(" -", c)
    print(f"[COMMAND_LIST] Razem: {len(cmds)} komend.")


def register():
    register_command("COMMAND_LIST", handle_command_list)
    print("[INFO][PLUGINS] Plugin COMMAND_LIST zarejestrowany")
