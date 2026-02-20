from ..command_registry import register_command


def handle_sample(command, args, block):
    print(f"[PLUGIN][SAMPLE] command={command} args={args!r}")
    if block:
        print("[PLUGIN][SAMPLE] BLOCK:")
        print(block)


def register():
    register_command("SAMPLE", handle_sample)
