import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget

from dark8_mark01.core.dark8_core_backend import Dark8CoreBackend
from dark8_mark01.ui.dark8_ui_device_manager import DeviceManagerPanel
from dark8_mark01.ui.dark8_ui_main import Dark8MainWindow
from dark8_mark01.ui.shell.dark8_shell_sidebar import Dark8SideBar
from dark8_mark01.ui.terminal.dark8_terminal_window import Dark8TerminalWindow


class Dark8Shell(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DARK8‑OS Shell")
        self.resize(1600, 900)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar
        self.sidebar = Dark8SideBar()
        layout.addWidget(self.sidebar)

        # Główne UI
        self.main_ui = Dark8MainWindow()
        layout.addWidget(self.main_ui)

        self.setCentralWidget(container)

        # Backend
        self.backend = Dark8CoreBackend()
        self.backend.start()

        # Status backendu
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_backend_status)
        self.status_timer.start(1000)

        # PODPIĘCIE SYGNAŁÓW Z DESKTOPU
        desktop = self.main_ui.desktop_panel
        desktop.open_terminal.connect(self.open_terminal)
        desktop.open_device_manager.connect(self.open_device_manager)
        desktop.open_files.connect(self.open_files)
        desktop.open_settings.connect(self.open_settings)

        # Sidebar → terminal
        self.sidebar.menu_btn.clicked.connect(self.open_terminal)

    def update_backend_status(self):
        status = self.backend.get_status()
        self.setWindowTitle(f"DARK8‑OS Shell — Backend: {status}")

    # ====== APLIKACJE ======

    def open_terminal(self):
        self.terminal = Dark8TerminalWindow(self.backend)
        self.terminal.show()

    def open_device_manager(self):
        self.dev = DeviceManagerPanel()
        self.dev.show()

    def open_files(self):
        print("TODO: File Manager")  # placeholder

    def open_settings(self):
        print("TODO: Settings")  # placeholder


def main():
    app = QApplication(sys.argv)
    window = Dark8Shell()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
