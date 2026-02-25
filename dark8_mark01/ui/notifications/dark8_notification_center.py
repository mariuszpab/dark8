from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class Dark8NotificationCenter(QWidget):
    """
    Wysuwany panel powiadomień.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.resize(350, screen.height())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        # Przycisk zamknięcia
        self.close_btn = QPushButton("X")
        self.close_btn.setFixedSize(40, 30)
        self.close_btn.clicked.connect(self.close_with_animation)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A2332;
                color: #E5F1FF;
                border: 1px solid #8F5BFF;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #8F5BFF;
                color: black;
            }
        """)
        layout.addWidget(self.close_btn, alignment=Qt.AlignRight)

        title = QLabel("Powiadomienia")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #8F5BFF;")
        layout.addWidget(title)

        self.list = QListWidget()
        self.list.setStyleSheet(
            "background-color: #05060A; color: #E5F1FF; border: 1px solid #1F2933;"
        )
        layout.addWidget(self.list, 1)

        # Animacja
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def add_notification(self, message: str):
        item = QListWidgetItem(message)
        self.list.addItem(item)

    def open(self):
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.width(), 0, 350, screen.height())

        self.show()
        self.anim.stop()
        self.anim.setStartValue(QRect(screen.width(), 0, 350, screen.height()))
        self.anim.setEndValue(QRect(screen.width() - 350, 0, 350, screen.height()))
        self.anim.start()

    def close_with_animation(self):
        screen = QApplication.primaryScreen().geometry()
        self.anim.stop()
        self.anim.setStartValue(QRect(screen.width() - 350, 0, 350, screen.height()))
        self.anim.setEndValue(QRect(screen.width(), 0, 350, screen.height()))
        self.anim.finished.connect(self.hide)
        self.anim.start()

    def mousePressEvent(self, event):
        # Kliknięcie poza panelem zamyka
        if event.pos().x() < 0:
            self.close_with_animation()
