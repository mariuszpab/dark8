from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PySide6.QtCore import Qt

from dark8_mark01.ui.system_log.dark8_system_log_bus import Dark8SystemLogBus


class Dark8SystemLogWindow(QWidget):
    """
    Okno logów systemowych DARK8‑OS.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("DARK8‑System Log")
        self.resize(900, 600)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        title = QLabel("Logi systemowe")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #8F5BFF;")
        layout.addWidget(title)

        self.list = QListWidget()
        self.list.setStyleSheet(
            "background-color: #05060A; color: #E5F1FF; border: 1px solid #1F2933;"
        )
        layout.addWidget(self.list, 1)

        self.bus = Dark8SystemLogBus.instance()
        self.bus.subscribe(self.on_new_entry)

    def on_new_entry(self, entry: str):
        item = QListWidgetItem(entry)
        self.list.addItem(item)
        self.list.scrollToBottom()
