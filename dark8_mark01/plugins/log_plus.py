from ..command_registry import register_command


def handle_log_plus(command, args, block):
    print("[LOG_PLUS]", args)
    if block:
        print(block)


def register():
    register_command("LOG_PLUS", handle_log_plus)
