from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QRect, Qt, Signal
from PySide6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QWidget

from dark8_mark01.ui.launcher.dark8_launcher_panel import Dark8LauncherPanel


class Dark8LauncherWindow(QWidget):
    """
    Wysuwane okno App Launchera DARK8‑OS.
    """

    app_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Panel aplikacji
        self.panel = Dark8LauncherPanel()
        self.panel.app_selected.connect(self.app_selected.emit)

        # Przycisk zamknięcia
        self.close_btn = QPushButton("X", self.panel)
        self.close_btn.setGeometry(250, 10, 40, 30)
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

        layout.addWidget(self.panel)

        # Start hidden on the left
        self.panel.move(-300, 0)

        self.anim = QPropertyAnimation(self.panel, b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    def open(self):
        self.show()
        self.anim.stop()
        self.anim.setStartValue(QRect(-300, 0, 300, self.height()))
        self.anim.setEndValue(QRect(0, 0, 300, self.height()))
        self.anim.start()

    def close_with_animation(self):
        self.anim.stop()
        self.anim.setStartValue(QRect(0, 0, 300, self.height()))
        self.anim.setEndValue(QRect(-300, 0, 300, self.height()))
        self.anim.finished.connect(self.hide)
        self.anim.start()

    def mousePressEvent(self, event):
        # Kliknięcie poza panelem zamyka launcher
        if event.pos().x() > 300:
            self.close_with_animation()
