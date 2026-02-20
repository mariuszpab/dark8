from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication


class Dark8Theme:
    @staticmethod
    def apply(app: QApplication):
        palette = QPalette()

        palette.setColor(QPalette.Window, QColor("#000000"))
        palette.setColor(QPalette.Base, QColor("#000000"))
        palette.setColor(QPalette.AlternateBase, QColor("#0B0F18"))

        palette.setColor(QPalette.WindowText, QColor("#E5F1FF"))
        palette.setColor(QPalette.Text, QColor("#E5F1FF"))
        palette.setColor(QPalette.ButtonText, QColor("#E5F1FF"))

        # GRANATOWY AKCENT
        palette.setColor(QPalette.Highlight, QColor("#8F5BFF"))
        palette.setColor(QPalette.Link, QColor("#8F5BFF"))

        palette.setColor(QPalette.Button, QColor("#111827"))

        app.setPalette(palette)
        app.setStyle("Fusion")
