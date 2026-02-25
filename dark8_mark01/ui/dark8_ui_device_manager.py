from PySide6.QtWidgets import QLabel, QListWidget, QPushButton, QVBoxLayout, QWidget

from dark8_mark01.devices.device_manager import get_all_devices


class DeviceManagerPanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        title = QLabel("DARK8 — Device Manager")
        title.setStyleSheet("font-size: 20px; font-weight: 600; color: #27E1C1;")
        layout.addWidget(title)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget, 1)

        refresh_btn = QPushButton("Odśwież")
        refresh_btn.clicked.connect(self.refresh_devices)
        layout.addWidget(refresh_btn)

        self.refresh_devices()

    def refresh_devices(self):
        self.list_widget.clear()

        devices = get_all_devices()

        # -----------------------------
        # USB DEVICES
        # -----------------------------
        self.list_widget.addItem("=== USB DEVICES ===")

        for dev in devices["usb"]:
            # jeśli backend zwrócił błąd
            if "error" in dev:
                self.list_widget.addItem(f"[USB ERROR] {dev['error']}")
                continue

            # normalny wpis USB
            vendor = dev.get("vendor", "N/A")
            product = dev.get("product", "N/A")
            bus = dev.get("bus", "N/A")
            address = dev.get("address", "N/A")

            self.list_widget.addItem(
                f"USB | Vendor: {vendor} | Product: {product} | Bus: {bus} | Addr: {address}"
            )

        # -----------------------------
        # WIFI NETWORKS
        # -----------------------------
        self.list_widget.addItem("")
        self.list_widget.addItem("=== Wi‑Fi NETWORKS ===")

        for net in devices["wifi"]:
            if "error" in net:
                self.list_widget.addItem(f"[Wi‑Fi ERROR] {net['error']}")
                continue

            ssid = net.get("ssid", "N/A")
            signal = net.get("signal", "N/A")

            self.list_widget.addItem(f"Wi‑Fi | SSID: {ssid} | Signal: {signal}")
