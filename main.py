import tkinter as tk
from tkinter import scrolledtext

from dark8_mark01.command_registry import get_handler
from dark8_mark01.commands import register_all_commands
from dark8_mark01.nlp.nlp_engine import interpret as interpret_polish
from dark8_mark01.plugins import load_plugins
from dark8_mark01.utils.dark8_backend import ensure_backend_ready
from dark8_mark01.utils.dark8_watchdog import start_watchdog

# ---------------------------------------------------------
# 1. ŁADOWANIE DARK8 (core + pluginy)
# ---------------------------------------------------------


# Rejestracja komend core
register_all_commands()

# Załaduj wszystkie pluginy
load_plugins()


# ---------------------------------------------------------
# 2. NLP — silnik interpretacji języka naturalnego
# ---------------------------------------------------------


# ---------------------------------------------------------
# 3. Backend + Watchdog
# ---------------------------------------------------------

# Backend LLM musi być gotowy zanim UI wystartuje
ensure_backend_ready()

# Watchdog działa w tle i pilnuje backendu
start_watchdog()


# ---------------------------------------------------------
# 4. Wykonanie komendy DARK8 z przechwyceniem outputu
# ---------------------------------------------------------


def execute_dark8_command(cmd, args, block, log_callback):
    handler = get_handler(cmd)
    if handler is None:
        log_callback(f"[ERROR] Nieznana komenda: {cmd}")
        return

    import sys
    from io import StringIO

    buffer = StringIO()
    old_stdout = sys.stdout
    sys.stdout = buffer

    try:
        handler(cmd, args, block)
    except Exception as e:
        log_callback(f"[ERROR] Błąd wykonania: {e}")

    sys.stdout = old_stdout
    output = buffer.getvalue()

    if output.strip():
        log_callback(output.strip())


# ---------------------------------------------------------
# 5. UI — okno dialogowe
# ---------------------------------------------------------


def start_ui():
    root = tk.Tk()
    root.title("DARK8 — Interfejs dialogowy")

    log_box = scrolledtext.ScrolledText(root, width=80, height=25, wrap=tk.WORD)
    log_box.pack(padx=10, pady=10)

    def log(msg):
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    entry = tk.Entry(root, width=80)
    entry.pack(padx=10, pady=5)

    def on_execute():
        text = entry.get().strip()
        entry.delete(0, tk.END)

        if not text:
            return

        log(f"> {text}")

        instr = interpret_polish(text)

        execute_dark8_command(instr["command"], instr["args"], instr["block"], log)

    btn = tk.Button(root, text="Wykonaj", command=on_execute)
    btn.pack(pady=5)

    root.mainloop()


# ---------------------------------------------------------
# 6. Start
# ---------------------------------------------------------

if __name__ == "__main__":
    start_ui()
