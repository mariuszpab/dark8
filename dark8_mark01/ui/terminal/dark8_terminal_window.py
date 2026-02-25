from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QVBoxLayout, QWidget

from dark8_mark01.ui.terminal.dark8_terminal import Dark8TerminalInterpreter


class Dark8TerminalWindow(QWidget):
    """
    Okno terminala DARK8‑OS.
    """

    def __init__(self, backend, parent=None):
        super().__init__(parent)

        self.setWindowTitle("DARK8‑Terminal")
        self.resize(800, 500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title = QLabel("DARK8‑TERMINAL")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #8F5BFF;")
        layout.addWidget(title)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet(
            "background-color: #05060A; color: #E5F1FF; border: 1px solid #1F2933;"
        )
        layout.addWidget(self.output, 1)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Wpisz komendę...")
        self.input.setStyleSheet(
            "background-color: #0B0F18; color: #E5F1FF; border: 1px solid #1F2933; padding: 6px;"
        )
        self.input.returnPressed.connect(self.run_command)
        layout.addWidget(self.input)

        self.interpreter = Dark8TerminalInterpreter(backend)

        self.print_line("DARK8‑OS Terminal — wpisz 'help'")

    def print_line(self, text: str):
        self.output.append(text)

    def run_command(self):
        cmd = self.input.text().strip()
        self.input.clear()

        if cmd == "":
            return

        self.print_line(f"> {cmd}")

        result = self.interpreter.execute(cmd)

        if result == "__CLEAR__":
            self.output.clear()
            return

        if result:
            self.print_line(result)
