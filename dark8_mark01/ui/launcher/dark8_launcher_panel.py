from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QLineEdit, QListWidget, QListWidgetItem, QVBoxLayout, QWidget


class Dark8LauncherPanel(QWidget):
    """
    Wysuwany panel App Launchera DARK8‑OS.
    """

    app_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedWidth(300)
        self.setStyleSheet("background-color: #0B0F18; border-right: 1px solid #1F2933;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        title = QLabel("Aplikacje")
        title.setStyleSheet("font-size: 18px; font-weight: 600; color: #8F5BFF;")
        layout.addWidget(title)

        # Wyszukiwarka
        self.search = QLineEdit()
        self.search.setPlaceholderText("Szukaj...")
        self.search.textChanged.connect(self.filter_list)
        self.search.setStyleSheet(
            "background-color: #05060A; color: #E5F1FF; border: 1px solid #1F2933; padding: 6px;"
        )
        layout.addWidget(self.search)

        # Lista aplikacji
        self.list = QListWidget()
        self.list.setStyleSheet(
            "background-color: #05060A; color: #E5F1FF; border: 1px solid #1F2933;"
        )
        self.list.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list, 1)

        # Aplikacje systemowe
        self.apps = [
            ("Terminal", "terminal"),
            ("Device Manager", "device_manager"),
            ("Pliki", "files"),
            ("Ustawienia", "settings"),
        ]

        self.populate()

    def populate(self):
        self.list.clear()
        for name, key in self.apps:
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, key)
            self.list.addItem(item)

    def filter_list(self, text):
        for i in range(self.list.count()):
            item = self.list.item(i)
            item.setHidden(text.lower() not in item.text().lower())

    def on_item_double_clicked(self, item):
        key = item.data(Qt.UserRole)
        self.app_selected.emit(key)
