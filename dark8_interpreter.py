import sys

from dark8_mark01.dark8_uci import run_agent_auto


def interpret(cmd: str):
    """
    Główny interpreter DARK8 w trybie LOCAL MODE.
    Obsługuje tylko agent-auto oraz proste polecenia.
    """

    cmd = cmd.strip()

    if not cmd:
        print("Brak polecenia.")
        return

    if cmd in ["exit", "quit", "wyjdz"]:
        print("Zamykanie DARK8...")
        sys.exit(0)

    if cmd.startswith("agent-auto"):
        description = cmd.replace("agent-auto", "", 1).strip()
        run_agent_auto(description)
        return

    print(f"Nieznane polecenie: {cmd}")


if __name__ == "__main__":
    print("============================================")
    print("       DARK8 MARK01 – INTERAKTYWNA KONSOLE")
    print("============================================\n")
    print("Wpisz polecenie:")

    while True:
        try:
            cmd = input("> ")
            interpret(cmd)
        except KeyboardInterrupt:
            print("\nPrzerwano. Wpisz 'exit' aby zamknąć.")
        except Exception as e:
            print(f"[ERROR] {e}")
