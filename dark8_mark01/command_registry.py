# dark8_mark01/command_registry.py

_COMMAND_HANDLERS = {}


def register_command(name, handler):
    """
    name: np. "WRITE_FILE"
    handler: funkcja (command, args, block) -> None
    """
    _COMMAND_HANDLERS[name] = handler


def get_handler(name):
    return _COMMAND_HANDLERS.get(name)


def list_commands():
    return sorted(_COMMAND_HANDLERS.keys())
