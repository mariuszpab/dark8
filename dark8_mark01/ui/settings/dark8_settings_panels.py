from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsPanelBase(QWidget):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 20px; font-weight: 600; color: #8F5BFF;")
        layout.addWidget(title_label)

        self.content_layout = layout


class SettingsThemePanel(SettingsPanelBase):
    def __init__(self):
        super().__init__("Wygląd systemu")

        label = QLabel("Motyw: DARK8 (domyślny)")
        label.setStyleSheet("color: #E5F1FF; font-size: 14px;")
        self.content_layout.addWidget(label)


class SettingsSystemPanel(SettingsPanelBase):
    def __init__(self):
        super().__init__("Ustawienia systemowe")

        label = QLabel("Opcje systemowe będą dostępne w kolejnych wersjach.")
        label.setStyleSheet("color: #E5F1FF; font-size: 14px;")
        self.content_layout.addWidget(label)


class SettingsAboutPanel(SettingsPanelBase):
    def __init__(self):
        super().__init__("Informacje o DARK8‑OS")

        info = QLabel(
            "DARK8‑OS v0.1\n"
            "Autor: Mariusz\n"
            "Silnik: Python + Qt\n"
            "Status: Wersja developerska"
        )
        info.setStyleSheet("color: #E5F1FF; font-size: 14px;")
        self.content_layout.addWidget(info)
