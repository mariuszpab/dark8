from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class AIPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        title = QLabel("DARK8‑AI")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600; color: #8F5BFF;")
        layout.addWidget(title)

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setStyleSheet(
            "background-color: #05060A; border: 1px solid #1F2933; font-size: 13px;"
        )
        layout.addWidget(self.chat_view, 1)

        input_row = QHBoxLayout()
        self.input = QLineEdit()
        self.input.setPlaceholderText("Napisz polecenie dla DARK8‑OS...")
        self.input.setStyleSheet(
            "background-color: #05060A; border: 1px solid #1F2933; padding: 6px;"
        )
        send_btn = QPushButton("Wyślij")
        send_btn.setStyleSheet(
            "background-color: #8F5BFF; color: #05060A; font-weight: 600; padding: 6px 12px;"
        )

        input_row.addWidget(self.input, 1)
        input_row.addWidget(send_btn)
        layout.addLayout(input_row)
