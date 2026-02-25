from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget


class Dark8SideBar(QWidget):
    """
    Lewy pasek systemowy DARK8‑OS.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(70)
        self.setStyleSheet("background-color: #0B0F18;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignTop)

        # ===== TERMINAL =====
        self.menu_btn = QPushButton("T")
        self.menu_btn.setFixedSize(50, 50)
        self.menu_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.menu_btn)

        # ===== APP LAUNCHER =====
        self.apps_btn = QPushButton("A")
        self.apps_btn.setFixedSize(50, 50)
        self.apps_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.apps_btn)

        # ===== POWIADOMIENIA =====
        self.notify_btn = QPushButton("N")
        self.notify_btn.setFixedSize(50, 50)
        self.notify_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.notify_btn)

        # ===== PROCESS MANAGER =====
        self.proc_btn = QPushButton("P")
        self.proc_btn.setFixedSize(50, 50)
        self.proc_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.proc_btn)

        # ===== SYSTEM LOG =====
        self.log_btn = QPushButton("L")
        self.log_btn.setFixedSize(50, 50)
        self.log_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.log_btn)

        layout.addStretch()

    def _btn_style(self):
        return """
            QPushButton {
                background-color: #111827;
                color: #E5F1FF;
                border: 1px solid #1F2933;
                font-size: 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1A2332;
                border-color: #8F5BFF;
            }
        """
