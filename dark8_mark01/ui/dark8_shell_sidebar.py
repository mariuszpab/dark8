import datetime

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QVBoxLayout, QWidget


class Dark8SideBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(70)
        self.setStyleSheet("""
            background-color: #0B0F18;
            border-right: 1px solid #1F2933;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.setSpacing(16)

        # Logo DARK8
        logo = QLabel("D8")
        logo.setAlignment(Qt.AlignHCenter)
        logo.setStyleSheet("color: #27E1C1; font-size: 22px; font-weight: 700;")
        layout.addWidget(logo)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #1F2933;")
        layout.addWidget(sep)

        # Przycisk MENU
        self.menu_btn = QPushButton("≡")
        self.menu_btn.setFixedSize(50, 50)
        self.menu_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.menu_btn, alignment=Qt.AlignHCenter)

        # Przycisk powiadomień
        self.notify_btn = QPushButton("🔔")
        self.notify_btn.setFixedSize(50, 50)
        self.notify_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.notify_btn, alignment=Qt.AlignHCenter)

        # Przycisk statusu backendu
        self.backend_btn = QPushButton("⚙")
        self.backend_btn.setFixedSize(50, 50)
        self.backend_btn.setStyleSheet(self._btn_style())
        layout.addWidget(self.backend_btn, alignment=Qt.AlignHCenter)

        layout.addStretch(1)

        # Zegar
        self.clock = QLabel()
        self.clock.setAlignment(Qt.AlignHCenter)
        self.clock.setStyleSheet("color: #E5F1FF; font-size: 12px;")
        layout.addWidget(self.clock)

        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M")
        self.clock.setText(now)

    def _btn_style(self):
        return """
            QPushButton {
                background-color: #111827;
                color: #E5F1FF;
                border: 1px solid #1F2933;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #1A2332;
            }
        """
