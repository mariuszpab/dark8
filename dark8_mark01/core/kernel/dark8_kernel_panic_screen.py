from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt


class Dark8KernelPanicScreen(QWidget):
    """
    Minimalistyczny ekran Kernel Panic (styl C).
    """

    def __init__(self, reason: str, details: dict, restart_callback):
        super().__init__()

        self.setStyleSheet("background-color: #05070A;")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("DARK8 KERNEL PANIC")
        title.setStyleSheet("color: #FF4F4F; font-size: 48px; font-weight: 800;")
        title.setAlignment(Qt.AlignCenter)

        reason_label = QLabel(f"Critical fault detected: {reason}")
        reason_label.setStyleSheet("color: #E5E5E5; font-size: 22px;")
        reason_label.setAlignment(Qt.AlignCenter)

        detail_text = QLabel(str(details))
        detail_text.setStyleSheet("color: #888; font-size: 16px;")
        detail_text.setAlignment(Qt.AlignCenter)

        restart_btn = QPushButton("RESTART KERNEL")
        restart_btn.setFixedSize(300, 60)
        restart_btn.setStyleSheet("""
            QPushButton {
                background-color: #111827;
                color: #E5E5E5;
                border: 2px solid #8F5BFF;
                font-size: 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1A2332;
            }
        """)
        restart_btn.clicked.connect(restart_callback)

        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(reason_label)
        layout.addWidget(detail_text)
        layout.addSpacing(60)
        layout.addWidget(restart_btn)
