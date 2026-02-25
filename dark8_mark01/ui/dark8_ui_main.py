import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget
from PySide6.QtCore import Qt

from dark8_mark01.ui.dark8_ui_theme import Dark8Theme
from dark8_mark01.ui.dark8_ui_ai_panel import AIPanel
from dark8_mark01.ui.dark8_ui_desktop import DesktopPanel


class Dark8MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DARK8‑OS UI")
        self.resize(1400, 800)

        splitter = QSplitter(Qt.Horizontal)

        self.desktop_panel = DesktopPanel()
        self.ai_panel = AIPanel()

        splitter.addWidget(self.desktop_panel)
        splitter.addWidget(self.ai_panel)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)

        container = QWidget()
        container.setLayout(None)  # QSplitter sam zarządza
        self.setCentralWidget(splitter)

        self._apply_styles()

    def _apply_styles(self):
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #05060A;
            }
            """
        )


def main():
    app = QApplication(sys.argv)
    Dark8Theme.apply(app)

    window = Dark8MainWindow()

    # TRYB B (okno) — TERAZ:
    window.show()

    # TRYB A (pełny OS fullscreen, bez ramek) — NA PÓŹNIEJ:
    # from PySide6.QtCore import Qt
    # window.setWindowFlags(Qt.FramelessWindowHint)
    # window.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
