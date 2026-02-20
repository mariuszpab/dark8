import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PySide6.QtCore import QTimer

from dark8_mark01.ui.shell.dark8_shell_sidebar import Dark8SideBar
from dark8_mark01.ui.dark8_ui_main import Dark8MainWindow
from dark8_mark01.core.dark8_core_backend import Dark8CoreBackend

# Aplikacje systemowe
from dark8_mark01.ui.terminal.dark8_terminal_window import Dark8TerminalWindow
from dark8_mark01.ui.dark8_ui_device_manager import DeviceManagerPanel
from dark8_mark01.ui.file_manager.dark8_file_window import Dark8FileWindow
from dark8_mark01.ui.settings.dark8_settings_window import Dark8SettingsWindow
from dark8_mark01.ui.launcher.dark8_launcher_window import Dark8LauncherWindow
from dark8_mark01.ui.process_manager.dark8_process_manager_window import Dark8ProcessManagerWindow
from dark8_mark01.ui.system_log.dark8_system_log_window import Dark8SystemLogWindow

# Powiadomienia
from dark8_mark01.ui.notifications.dark8_notification_toast import Dark8Toast
from dark8_mark01.ui.notifications.dark8_notification_center import Dark8NotificationCenter

# System Log Bus
from dark8_mark01.ui.system_log.dark8_system_log_bus import Dark8SystemLogBus

# Kernel
from dark8_mark01.core.kernel.dark8_kernel_heartbeat import Dark8KernelHeartbeat
from dark8_mark01.core.kernel.dark8_kernel_event_dispatcher import Dark8KernelEventDispatcher
from dark8_mark01.core.kernel.dark8_kernel_system_monitor import Dark8KernelSystemMonitor
from dark8_mark01.core.kernel.dark8_kernel_panic import Dark8KernelPanic
from dark8_mark01.core.kernel.dark8_kernel_scheduler import Dark8KernelScheduler
from dark8_mark01.core.kernel.dark8_kernel_task import Dark8KernelTask

# Kernel Panic UI
from dark8_mark01.ui.kernel.dark8_kernel_panic_screen import Dark8KernelPanicScreen


class Dark8Shell(QMainWindow):
    """
    Główne środowisko DARK8‑OS.
    Zoptymalizowany pseudo‑kernel + scheduler + panic.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DARK8‑OS Shell")
        self.resize(1600, 900)

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Lewy pasek systemowy
        self.sidebar = Dark8SideBar()
        layout.addWidget(self.sidebar)

        # Główna przestrzeń robocza
        self.main_ui = Dark8MainWindow()
        layout.addWidget(self.main_ui)

        self.setCentralWidget(container)

        # Backend DARK8‑OS
        self.backend = Dark8CoreBackend()
        self.backend.start()

        # System Log Bus
        self.log_bus = Dark8SystemLogBus.instance()

        # ===== KERNEL (ZOPTYMALIZOWANY) =====
        self.dispatcher = Dark8KernelEventDispatcher.instance()

        # heartbeat co 5 sekund (mniejsze obciążenie)
        self.kernel_heartbeat = Dark8KernelHeartbeat(interval_sec=5.0)

        # system monitor
        self.kernel_monitor = Dark8KernelSystemMonitor(cpu_threshold=90, ram_threshold=95)
        self.kernel_heartbeat.subscribe(self.kernel_monitor.tick)

        # scheduler
        self.scheduler = Dark8KernelScheduler.instance()
        self.kernel_heartbeat.subscribe(self.scheduler.tick)

        # przykładowe procesy systemowe
        self.scheduler.add_task(Dark8KernelTask("system_monitor", priority=3))
        self.scheduler.add_task(Dark8KernelTask("event_dispatcher", priority=4))
        self.scheduler.add_task(Dark8KernelTask("shell_runtime", priority=5))

        # Kernel Panic
        self.kernel_panic = Dark8KernelPanic.instance()
        self.kernel_panic.callback = self.show_kernel_panic
        self.panic_screen = None

        # subskrypcja eventów kernela
        self.dispatcher.subscribe(self.on_kernel_event)

        self.kernel_heartbeat.start()
        self.log_bus.log("Kernel", "Heartbeat + monitor + scheduler + panic started")

        # Timer do odświeżania statusu backendu
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_backend_status)
        self.status_timer.start(2000)
        self.update_backend_status()

        # App Launcher
        self.launcher = Dark8LauncherWindow()
        self.launcher.app_selected.connect(self.launch_app)

        # Notification Center
        self.notification_center = Dark8NotificationCenter()

        # ===== PODPIĘCIE SYGNAŁÓW Z DESKTOPU =====
        desktop = self.main_ui.desktop_panel

        desktop.open_terminal.connect(self.open_terminal)
        desktop.open_device_manager.connect(self.open_device_manager)
        desktop.open_files.connect(self.open_files)
        desktop.open_settings.connect(self.open_settings)

        # Sidebar → terminal / launcher / powiadomienia / process manager / system log
        self.sidebar.menu_btn.clicked.connect(self.open_terminal)
        self.sidebar.apps_btn.clicked.connect(self.open_launcher)
        self.sidebar.notify_btn.clicked.connect(self.open_notification_center)
        self.sidebar.proc_btn.clicked.connect(self.open_process_manager)
        self.sidebar.log_btn.clicked.connect(self.open_system_log)

        self.log_bus.log("Shell", "DARK8 Shell uruchomiony")

    # ====== Kernel Event Handler ======
    def on_kernel_event(self, event: dict):
        etype = event["type"]
        payload = event["payload"]

        if etype == "CPU_HIGH":
            self.notify(f"Kernel: CPU HIGH {payload['cpu']}% (>{payload['threshold']}%)")

        if etype == "RAM_HIGH":
            self.notify(f"Kernel: RAM HIGH {payload['ram']}% (>{payload['threshold']}%)")

        if etype == "SYSTEM_STATUS":
            cpu = payload.get("cpu")
            ram = payload.get("ram")
            self.log_bus.log("KernelStatus", f"CPU={cpu}%, RAM={ram}%")

        if etype == "TASK_ADDED":
            self.log_bus.log("Scheduler", f"Task added: {payload}")

        if etype == "TASK_STOPPED":
            self.log_bus.log("Scheduler", f"Task stopped: {payload}")

    # ====== Kernel Panic ======
    def show_kernel_panic(self, reason, details):
        try:
            self.kernel_heartbeat.stop()
        except Exception:
            pass

        self.panic_screen = Dark8KernelPanicScreen(reason, details, self.restart_kernel)
        self.panic_screen.show()

    def restart_kernel(self):
        if self.panic_screen:
            self.panic_screen.close()
            self.panic_screen = None

        self.kernel_panic.reset()
        self.kernel_heartbeat.start()
        self.notify("Kernel restarted successfully")

    # ====== Aktualizacja statusu backendu ======
    def update_backend_status(self):
        status = self.backend.get_status()
        self.setWindowTitle(f"DARK8‑OS Shell — Backend: {status}")
        self.log_bus.log("Backend", f"Status backendu: {status}")

    # ====== APLIKACJE SYSTEMOWE ======

    def open_terminal(self):
        self.log_bus.log("Shell", "Otwieranie Terminala")
        self.terminal = Dark8TerminalWindow(self.backend)
        self.terminal.show()
        self.notify("Uruchomiono Terminal")

    def open_device_manager(self):
        self.log_bus.log("Shell", "Otwieranie Device Managera")
        self.dev = DeviceManagerPanel()
        self.dev.show()
        self.notify("Uruchomiono Device Manager")

    def open_files(self):
        self.log_bus.log("Shell", "Otwieranie File Managera")
        self.files = Dark8FileWindow()
        self.files.show()
        self.notify("Uruchomiono File Manager")

    def open_settings(self):
        self.log_bus.log("Shell", "Otwieranie Settings")
        self.settings = Dark8SettingsWindow()
        self.settings.show()
        self.notify("Uruchomiono Ustawienia")

    def open_process_manager(self):
        self.log_bus.log("Shell", "Otwieranie Process Managera")
        self.proc = Dark8ProcessManagerWindow()
        self.proc.show()
        self.notify("Uruchomiono Process Manager")

    def open_system_log(self):
        self.log_bus.log("Shell", "Otwieranie System Log")
        self.syslog = Dark8SystemLogWindow()
        self.syslog.show()
        self.notify("Uruchomiono System Log")

    # ====== APP LAUNCHER ======

    def open_launcher(self):
        self.log_bus.log("Shell", "Otwieranie App Launchera")
        self.launcher.open()

    def launch_app(self, key: str):
        self.log_bus.log("Launcher", f"Wybrano aplikację: {key}")

        if key == "terminal":
            self.open_terminal()
        elif key == "device_manager":
            self.open_device_manager()
        elif key == "files":
            self.open_files()
        elif key == "settings":
            self.open_settings()
        elif key == "process_manager":
            self.open_process_manager()
        elif key == "system_log":
            self.open_system_log()

        self.launcher.hide()

    # ====== POWIADOMIENIA ======

    def notify(self, message: str):
        self.log_bus.log("Notify", message)

        toast = Dark8Toast(message)
        screen = QApplication.primaryScreen().geometry()
        x = screen.width() - 320
        y = screen.height() - 120
        toast.show_with_animation(x, y)

        self.notification_center.add_notification(message)

    def open_notification_center(self):
        self.log_bus.log("Shell", "Otwieranie Notification Center")
        self.notification_center.open()


def main():
    app = QApplication(sys.argv)
    window = Dark8Shell()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
