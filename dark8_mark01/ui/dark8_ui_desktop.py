from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PySide6.QtCore import Qt, Signal


class DesktopPanel(QWidget):
    open_files = Signal()
    open_settings = Signal()
    open_device_manager = Signal()
    open_terminal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("DARK8‑DESKTOP")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #8F5BFF;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)

        tiles = [
            ("Pliki", self.open_files),
            ("Ustawienia", self.open_settings),
            ("Device Manager", self.open_device_manager),
            ("Terminal", self.open_terminal),
        ]

        for i, (name, signal) in enumerate(tiles):
            btn = QPushButton(name)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #0B0F18;
                    color: #E5F1FF;
                    border: 1px solid #1F2933;
                    padding: 16px;
                }
                QPushButton:hover {
                    border-color: #8F5BFF;
                    background-color: #111827;
                }
            """)
            btn.clicked.connect(signal.emit)

            grid.addWidget(btn, i // 2, i % 2)

        layout.addLayout(grid)
