import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget


class Dark8TopBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedHeight(40)
        self.setStyleSheet("""
            background-color: #0B0F18;
            border-bottom: 1px solid #1F2933;
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(20)

        # Logo
        logo = QLabel("DARK8‑OS")
        logo.setStyleSheet("color: #27E1C1; font-size: 16px; font-weight: 600;")
        layout.addWidget(logo)

        layout.addStretch(1)

        # Status backendu
        self.backend_status = QLabel("Backend: ???")
        self.backend_status.setStyleSheet("color: #E5F1FF;")
        layout.addWidget(self.backend_status)

        # Zegar
        self.clock = QLabel()
        self.clock.setStyleSheet("color: #E5F1FF; font-size: 14px;")
        layout.addWidget(self.clock)

        # Ikona menu
        self.menu_btn = QPushButton("≡")
        self.menu_btn.setFixedWidth(40)
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #111827;
                color: #E5F1FF;
                border: 1px solid #1F2933;
            }
            QPushButton:hover {
                background-color: #1A2332;
            }
        """)
        layout.addWidget(self.menu_btn)

        # Timer do aktualizacji zegara
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock.setText(now)

    def set_backend_status(self, text):
        self.backend_status.setText(f"Backend: {text}")
