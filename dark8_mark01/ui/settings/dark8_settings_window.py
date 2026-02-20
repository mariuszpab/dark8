from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QListWidget
from PySide6.QtCore import Qt

from dark8_mark01.ui.settings.dark8_settings_panels import (
    SettingsThemePanel,
    SettingsSystemPanel,
    SettingsAboutPanel,
)


class Dark8SettingsWindow(QWidget):
    """
    Okno ustawień systemowych DARK8‑OS.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("DARK8‑Settings")
        self.resize(900, 600)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Lewy panel — lista kategorii
        self.menu = QListWidget()
        self.menu.setStyleSheet(
            "background-color: #0B0F18; color: #E5F1FF; border: 1px solid #1F2933;"
        )
        self.menu.addItem("Wygląd")
        self.menu.addItem("System")
        self.menu.addItem("Informacje")
        self.menu.currentRowChanged.connect(self.change_panel)

        layout.addWidget(self.menu, 1)

        # Prawy panel — treść
        self.panel_container = QVBoxLayout()
        self.panel_container.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.panel_container, 3)

        # Domyślny panel
        self.show_panel(0)

    def create_panel(self, index):
        if index == 0:
            return SettingsThemePanel()
        if index == 1:
            return SettingsSystemPanel()
        if index == 2:
            return SettingsAboutPanel()

    def show_panel(self, index):
        # Usuń poprzedni panel
        while self.panel_container.count():
            item = self.panel_container.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Dodaj nowy panel
        panel = self.create_panel(index)
        self.panel_container.addWidget(panel)

    def change_panel(self, index):
        self.show_panel(index)
