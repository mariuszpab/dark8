from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt, QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class Dark8Toast(QWidget):
    """
    Pojedyncze powiadomienie typu toast.
    """

    def __init__(self, message: str, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(300, 80)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        label = QLabel(message)
        label.setStyleSheet("color: #E5F1FF; font-size: 14px;")
        layout.addWidget(label)

        self.setStyleSheet("""
            background-color: rgba(15, 20, 30, 220);
            border: 1px solid #1F2933;
            border-radius: 8px;
        """)

        # Animacja pojawienia
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

        # Auto-zamykanie
        QTimer.singleShot(3000, self.close_with_animation)

    def show_with_animation(self, x, y):
        self.show()
        start = QRect(x, y + 40, 300, 80)
        end = QRect(x, y, 300, 80)
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()

    def close_with_animation(self):
        end = QRect(self.x(), self.y() + 40, 300, 80)
        self.anim.setStartValue(self.geometry())
        self.anim.setEndValue(end)
        self.anim.finished.connect(self.close)
        self.anim.start()
