import os
import sys
import time

from ..command_registry import register_command


def log_info(msg):
    print(f"[INFO][FLOW] {msg}")


def log_error(msg):
    print(f"[ERROR][FLOW] {msg}")


# ---------------------------------------------------------
# STOS WARUNKÓW IF
# ---------------------------------------------------------

_condition_stack = []


def is_block_active():
    """
    Zwraca True, jeśli wszystkie warunki IF na stosie są True.
    Jeśli którykolwiek IF jest False → blok jest nieaktywny.
    """
    return all(_condition_stack) if _condition_stack else True


# ---------------------------------------------------------
# GŁÓWNY HANDLER
# ---------------------------------------------------------


def handle(command, args, block):
    if command == "LOG":
        return log_command(args, block)

    if command == "SLEEP":
        return sleep_command(args)

    if command == "EXIT":
        return exit_command(args)

    if command == "IF_EXISTS":
        return if_exists(args)

    if command == "IF_NOT_EXISTS":
        return if_not_exists(args)

    if command == "END_IF":
        return end_if()

    log_error(f"Nieznana komenda FLOW_OPS: {command}")


# ---------------------------------------------------------
# LOG
# ---------------------------------------------------------


def log_command(args, block):
    if block and block.strip():
        msg = block.strip()
    else:
        msg = args.strip()

    if not msg:
        log_error("LOG: brak treści.")
        return

    log_info(msg)


# ---------------------------------------------------------
# SLEEP
# ---------------------------------------------------------


def sleep_command(args):
    try:
        seconds = float(args.strip())
    except Exception:
        log_error(f"SLEEP: niepoprawna liczba sekund: '{args}'")
        return

    log_info(f"Usypiam na {seconds} sekund...")
    time.sleep(seconds)
    log_info("Kontynuuję wykonanie.")


# ---------------------------------------------------------
# EXIT
# ---------------------------------------------------------


def exit_command(args):
    code = 0
    if args.strip():
        try:
            code = int(args.strip())
        except Exception:
            log_error(f"EXIT: niepoprawny kod wyjścia '{args}', używam 0.")
            code = 0

    log_info(f"EXIT z kodem {code}")
    sys.exit(code)


# ---------------------------------------------------------
# IF_EXISTS / IF_NOT_EXISTS / END_IF
# ---------------------------------------------------------


def if_exists(path):
    path = path.strip()
    if not path:
        log_error("IF_EXISTS: brak ścieżki.")
        _condition_stack.append(False)
        return

    cond = os.path.exists(path)
    _condition_stack.append(cond)
    log_info(f"IF_EXISTS {path} → {cond}")


def if_not_exists(path):
    path = path.strip()
    if not path:
        log_error("IF_NOT_EXISTS: brak ścieżki.")
        _condition_stack.append(False)
        return

    cond = not os.path.exists(path)
    _condition_stack.append(cond)
    log_info(f"IF_NOT_EXISTS {path} → {cond}")


def end_if():
    if not _condition_stack:
        log_error("END_IF bez odpowiadającego IF.")
        return

    cond = _condition_stack.pop()
    log_info(f"END_IF (zamyka blok, który był: {cond})")


# ---------------------------------------------------------
# REJESTRACJA KOMEND
# ---------------------------------------------------------


def register():
    for cmd in [
        "LOG",
        "SLEEP",
        "EXIT",
        "IF_EXISTS",
        "IF_NOT_EXISTS",
        "END_IF",
    ]:
        register_command(cmd, handle)
