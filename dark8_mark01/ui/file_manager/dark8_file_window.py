from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt

from dark8_mark01.core.vfs.dark8_vfs_manager import Dark8VFSManager


class Dark8FileWindow(QWidget):
    """
    Dwupanelowy File Manager DARK8 – pełna integracja z VFS.
    Lewy panel: drzewo katalogów
    Prawy panel: zawartość katalogu
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("DARK8 File Manager (VFS)")
        self.resize(900, 600)

        self.vfs = Dark8VFSManager.instance()
        self.current_path = "/"

        main_layout = QHBoxLayout(self)

        # ===== LEWY PANEL – DRZEWO KATALOGÓW =====
        left_layout = QVBoxLayout()
        left_label = QLabel("Katalogi")
        left_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #E5E5E5;")
        left_layout.addWidget(left_label)

        self.tree = QListWidget()
        self.tree.setStyleSheet("background-color: #111827; color: #E5E5E5;")
        self.tree.itemClicked.connect(self.on_tree_select)
        left_layout.addWidget(self.tree)

        main_layout.addLayout(left_layout, 1)

        # ===== PRAWY PANEL – ZAWARTOŚĆ KATALOGU =====
        right_layout = QVBoxLayout()
        right_label = QLabel("Zawartość")
        right_label.setStyleSheet("font-size: 18px; font-weight: 700; color: #E5E5E5;")
        right_layout.addWidget(right_label)

        self.content = QListWidget()
        self.content.setStyleSheet("background-color: #111827; color: #E5E5E5;")
        self.content.itemDoubleClicked.connect(self.on_content_double_click)
        right_layout.addWidget(self.content)

        # ===== OPERACJE =====
        op_layout = QHBoxLayout()

        self.new_dir = QLineEdit()
        self.new_dir.setPlaceholderText("Nowy katalog")
        self.new_dir.setStyleSheet("background-color: #1F2937; color: #E5E5E5; padding: 6px;")
        op_layout.addWidget(self.new_dir)

        btn_mkdir = QPushButton("mkdir")
        btn_mkdir.setStyleSheet("background-color: #1E3A8A; color: #E5E5E5; padding: 6px;")
        btn_mkdir.clicked.connect(self.create_dir)
        op_layout.addWidget(btn_mkdir)

        self.new_file = QLineEdit()
        self.new_file.setPlaceholderText("Nowy plik")
        self.new_file.setStyleSheet("background-color: #1F2937; color: #E5E5E5; padding: 6px;")
        op_layout.addWidget(self.new_file)

        btn_touch = QPushButton("touch")
        btn_touch.setStyleSheet("background-color: #1E3A8A; color: #E5E5E5; padding: 6px;")
        btn_touch.clicked.connect(self.create_file)
        op_layout.addWidget(btn_touch)

        btn_delete = QPushButton("delete")
        btn_delete.setStyleSheet("background-color: #7F1D1D; color: #E5E5E5; padding: 6px;")
        btn_delete.clicked.connect(self.delete_selected)
        op_layout.addWidget(btn_delete)

        right_layout.addLayout(op_layout)

        main_layout.addLayout(right_layout, 2)

        # Załaduj początkowe dane
        self.refresh_tree()
        self.refresh_content()

    # ===== TREE (LEWY PANEL) =====
    def refresh_tree(self):
        self.tree.clear()
        self.tree.addItem("/")  # root

        def walk(path, indent=""):
            try:
                items = self.vfs.list_dir(path)
            except:
                return

            for name in items:
                subpath = path.rstrip("/") + "/" + name
                # sprawdzamy czy to katalog
                try:
                    children = self.vfs.list_dir(subpath)
                    self.tree.addItem(indent + name + "/")
                    walk(subpath, indent + "  ")
                except:
                    pass  # plik – ignorujemy w drzewie

        walk("/")

    def on_tree_select(self, item):
        text = item.text().strip()
        if text.endswith("/"):
            name = text.rstrip("/")
            if name == "":
                self.current_path = "/"
            else:
                self.current_path = "/" + name
            self.refresh_content()

    # ===== CONTENT (PRAWY PANEL) =====
    def refresh_content(self):
        self.content.clear()
        try:
            items = self.vfs.list_dir(self.current_path)
        except:
            return

        for name in items:
            # sprawdzamy czy katalog
            subpath = self.current_path.rstrip("/") + "/" + name
            try:
                self.vfs.list_dir(subpath)
                self.content.addItem(name + "/")
            except:
                self.content.addItem(name)

    def on_content_double_click(self, item):
        name = item.text()
        if name.endswith("/"):
            # katalog
            name = name.rstrip("/")
            self.current_path = self.current_path.rstrip("/") + "/" + name
            self.refresh_content()

    # ===== OPERACJE =====
    def create_dir(self):
        name = self.new_dir.text().strip()
        if not name:
            return
        path = self.current_path.rstrip("/") + "/" + name
        try:
            self.vfs.create_dir(path)
            self.refresh_tree()
            self.refresh_content()
        except Exception as e:
            QMessageBox.warning(self, "Błąd", str(e))

    def create_file(self):
        name = self.new_file.text().strip()
        if not name:
            return
        path = self.current_path.rstrip("/") + "/" + name
        try:
            self.vfs.create_file(path)
            self.refresh_content()
        except Exception as e:
            QMessageBox.warning(self, "Błąd", str(e))

    def delete_selected(self):
        item = self.content.currentItem()
        if not item:
            return

        name = item.text().rstrip("/")
        path = self.current_path.rstrip("/") + "/" + name

        try:
            self.vfs.delete(path)
            self.refresh_tree()
            self.refresh_content()
        except Exception as e:
            QMessageBox.warning(self, "Błąd", str(e))
