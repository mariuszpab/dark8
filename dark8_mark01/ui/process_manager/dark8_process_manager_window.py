from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QHBoxLayout, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, QTimer

from dark8_mark01.core.kernel.dark8_kernel_scheduler import Dark8KernelScheduler
from dark8_mark01.core.kernel.dark8_kernel_task import Dark8KernelTask


class Dark8ProcessManagerWindow(QWidget):
    """
    Process Manager DARK8 – pełna integracja z kernel schedulerem.
    STOP + NEW PROCESS.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DARK8 Process Manager")
        self.resize(800, 550)

        layout = QVBoxLayout(self)

        title = QLabel("DARK8 PROCESS MANAGER")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: 700; color: #E5E5E5;")
        layout.addWidget(title)

        # tabela procesów
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "Priority", "State"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("color: #E5E5E5; background-color: #111827;")
        layout.addWidget(self.table)

        # ===== STOP PROCESS =====
        stop_layout = QHBoxLayout()
        self.stop_input = QLineEdit()
        self.stop_input.setPlaceholderText("PID do zatrzymania")
        self.stop_input.setStyleSheet("background-color: #1F2937; color: #E5E5E5; padding: 6px;")
        stop_layout.addWidget(self.stop_input)

        stop_btn = QPushButton("STOP PROCESS")
        stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #7F1D1D;
                color: #E5E5E5;
                padding: 8px;
                border: 1px solid #B91C1C;
            }
            QPushButton:hover {
                background-color: #991B1B;
            }
        """)
        stop_btn.clicked.connect(self.stop_process)
        stop_layout.addWidget(stop_btn)

        layout.addLayout(stop_layout)

        # ===== NEW PROCESS =====
        new_layout = QHBoxLayout()
        self.new_name = QLineEdit()
        self.new_name.setPlaceholderText("Nazwa procesu")
        self.new_name.setStyleSheet("background-color: #1F2937; color: #E5E5E5; padding: 6px;")
        new_layout.addWidget(self.new_name)

        self.new_priority = QLineEdit()
        self.new_priority.setPlaceholderText("Priorytet (1-10)")
        self.new_priority.setStyleSheet("background-color: #1F2937; color: #E5E5E5; padding: 6px;")
        new_layout.addWidget(self.new_priority)

        new_btn = QPushButton("NEW PROCESS")
        new_btn.setStyleSheet("""
            QPushButton {
                background-color: #1E3A8A;
                color: #E5E5E5;
                padding: 8px;
                border: 1px solid #3B82F6;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)
        new_btn.clicked.connect(self.create_process)
        new_layout.addWidget(new_btn)

        layout.addLayout(new_layout)

        # scheduler
        self.scheduler = Dark8KernelScheduler.instance()

        # auto-refresh co 2 sekundy
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000)

        self.refresh()

    # ====== STOP PROCESS ======
    def stop_process(self):
        pid_text = self.stop_input.text().strip()
        if not pid_text.isdigit():
            QMessageBox.warning(self, "Błąd", "PID musi być liczbą.")
            return

        pid = int(pid_text)
        self.scheduler.stop_task(pid)
        self.refresh()

    # ====== NEW PROCESS ======
    def create_process(self):
        name = self.new_name.text().strip()
        priority_text = self.new_priority.text().strip()

        if not name:
            QMessageBox.warning(self, "Błąd", "Podaj nazwę procesu.")
            return

        if not priority_text.isdigit():
            QMessageBox.warning(self, "Błąd", "Priorytet musi być liczbą 1-10.")
            return

        priority = int(priority_text)
        if priority < 1 or priority > 10:
            QMessageBox.warning(self, "Błąd", "Priorytet musi być w zakresie 1-10.")
            return

        task = Dark8KernelTask(name, priority)
        self.scheduler.add_task(task)
        self.refresh()

    # ====== REFRESH TABLE ======
    def refresh(self):
        tasks = self.scheduler.tasks
        self.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(str(task.pid)))
            self.table.setItem(row, 1, QTableWidgetItem(task.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(task.priority)))
            self.table.setItem(row, 3, QTableWidgetItem(task.state.name))
