from dark8_mark01.core.dark8_core_backend import Dark8CoreBackend


class Dark8TerminalInterpreter:
    """
    Interpreter komend terminala DARK8‑OS.
    """

    def __init__(self, backend: Dark8CoreBackend):
        self.backend = backend

    def execute(self, command: str) -> str:
        cmd = command.strip().lower()

        if cmd == "":
            return ""

        if cmd == "help":
            return (
                "DARK8‑OS Terminal — dostępne komendy:\n"
                " help      — lista komend\n"
                " status    — status backendu\n"
                " ping      — test połączenia z backendem\n"
                " clear     — wyczyść ekran\n"
                " info      — informacje o systemie\n"
            )

        if cmd == "status":
            return f"Backend status: {self.backend.get_status()}"

        if cmd == "ping":
            return "pong"

        if cmd == "clear":
            return "__CLEAR__"

        if cmd == "info":
            return (
                "DARK8‑OS v0.1\n"
                "Kernel: Python‑Core (dev mode)\n"
                "Backend: Active\n"
                "UI: DARK8‑Shell\n"
            )

        return f"Nieznana komenda: {cmd}"
