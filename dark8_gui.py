import os
import threading
import tkinter as tk
from tkinter import scrolledtext

from dark8_mark01.dark8_uci import run_agent_auto


class Dark8ConsoleCapture:
    """
    Przechwytuje stdout z run_agent_auto i przekazuje do GUI.
    """

    def __init__(self, write_callback):
        self.write_callback = write_callback

    def write(self, text):
        text = str(text)
        if text:
            self.write_callback(text)

    def flush(self):
        pass


class Dark8GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DARK8 – Copilot")

        # Szersze okno (B1)
        self.root.geometry("700x800")
        self.root.minsize(600, 600)

        # Katalog na projekty (na przyszłość – Auto-Fix)
        self.projects_root = os.path.join(os.getcwd(), "projekty")
        os.makedirs(self.projects_root, exist_ok=True)

        self._build_layout()

        self.history = []

        self._append_system("Witaj w DARK8.")
        self._append_system("Możesz pisać po polsku, np.:")
        self._append_system("„przeanalizuj DARK8” – analiza całego projektu")
        self._append_system("„napisz funkcję sortującą listę liczb”")
        self._append_system("„stwórz projekt konsolowy w Pythonie”")

        self._update_status("Bezczynny")

    def _build_layout(self):
        main_frame = tk.Frame(self.root, bg="#101010")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Obszar rozmowy
        self.text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#181818",
            fg="#f0f0f0",
            insertbackground="#f0f0f0",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        # Pasek statusu
        self.status_label = tk.Label(
            main_frame,
            text="Status: nieznany",
            anchor="w",
            justify=tk.LEFT,
            bg="#101010",
            fg="#888888"
        )
        self.status_label.pack(fill=tk.X, padx=12, pady=(0, 4))

        # Dolny panel
        bottom_frame = tk.Frame(main_frame, bg="#101010")
        bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.entry = tk.Text(
            bottom_frame,
            height=3,
            wrap=tk.WORD,
            bg="#202020",
            fg="#f0f0f0",
            insertbackground="#f0f0f0",
            relief=tk.FLAT,
            borderwidth=4
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Shift-Return>", self._on_shift_enter)

        send_button = tk.Button(
            bottom_frame,
            text="Wyślij",
            command=self.on_send,
            bg="#3a3a3a",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=12,
            pady=6
        )
        send_button.pack(side=tk.LEFT, padx=(8, 0))

    # ====== Pomocnicze metody GUI ======

    def _append_text(self, prefix, text):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, f"{prefix}{text}")
        self.text_area.insert(tk.END, "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)

    def _append_user(self, text):
        self._append_text("TY: ", text)

    def _append_system(self, text):
        self._append_text("DARK8: ", text)

    def _update_status(self, status_text: str):
        self.status_label.config(text=f"Status: {status_text}")

    def _on_enter(self, event):
        if not (event.state & 0x0001):  # Enter bez Shift
            self.on_send()
            return "break"

    def _on_shift_enter(self, event):
        self.entry.insert(tk.INSERT, "\n")
        return "break"

    # ====== Obsługa wysyłania ======

    def on_send(self):
        cmd = self.entry.get("1.0", tk.END).strip()
        if not cmd:
            return
        self.entry.delete("1.0", tk.END)

        self._append_user(cmd)
        self.history.append(cmd)
        self._update_status("Przetwarzanie...")

        t = threading.Thread(target=self._run_command_background, args=(cmd,))
        t.daemon = True
        t.start()

    def _run_command_background(self, cmd: str):
        import sys
        old_stdout = sys.stdout
        sys.stdout = Dark8ConsoleCapture(lambda txt: self._append_system(txt.rstrip("\n")))

        try:
            run_agent_auto(cmd)
        finally:
            sys.stdout = old_stdout
            self._update_status("Bezczynny")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Dark8GUI()
    app.run()
