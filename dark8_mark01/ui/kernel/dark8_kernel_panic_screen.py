from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt


class Dark8KernelPanicScreen(QWidget):
    """
    Minimalistyczny ekran Kernel Panic (styl DARK8).
    Pełnoekranowy, mroczny, futurystyczny.
    """

    def __init__(self, reason: str, details: dict, restart_callback):
        super().__init__()

        # pełny ekran, bez ramek, zawsze na wierzchu
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.CustomizeWindowHint
        )
        self.showFullScreen()

        # tło
        self.setStyleSheet("background-color: #05070A;")

        # layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # tytuł
        title = QLabel("DARK8 KERNEL PANIC")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #FF4F4F;
            font-size: 48px;
            font-weight: 900;
            letter-spacing: 2px;
        """)

        # powód
        reason_label = QLabel(f"Critical fault detected: {reason}")
        reason_label.setAlignment(Qt.AlignCenter)
        reason_label.setStyleSheet("""
            color: #E5E5E5;
            font-size: 22px;
            margin-top: 20px;
        """)

        # szczegóły
        detail_label = QLabel(str(details))
        detail_label.setAlignment(Qt.AlignCenter)
        detail_label.setStyleSheet("""
            color: #888;
            font-size: 16px;
            margin-top: 10px;
        """)

        # przycisk restartu
        restart_btn = QPushButton("RESTART KERNEL")
        restart_btn.setFixedSize(320, 60)
        restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #111827;
                color: #E5E5E5;
                border: 2px solid #8F5BFF;
                font-size: 20px;
                font-weight: 600;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #1A2332;
                border-color: #A97CFF;
            }
        """)
        restart_btn.clicked.connect(restart_callback)

        # dodanie elementów
        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(reason_label)
        layout.addWidget(detail_label)
        layout.addSpacing(60)
        layout.addWidget(restart_btn)
