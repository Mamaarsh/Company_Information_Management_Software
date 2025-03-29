from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from controles.AddTodatabase import AddDataBaseGUI
from controles.SearchAndupdate import SearchAndUpdateGUI
import sys

class OrdersApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("سیستم مدیریت تلفن")
        self.setGeometry(100, 100, 500, 400)

        icon_path = str(Path(__file__).parent / "addition_info" / "favicon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.current_window = None

        title_label = QLabel("سیستم مدیریت تلفن", alignment=Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
        """)
        self.layout.addWidget(title_label)

        self.create_buttons()

        self.central_widget.setLayout(self.layout)

    def create_buttons(self):
        add_btn = QPushButton("افزودن اطلاعات")
        add_btn.setFixedHeight(60)
        add_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #27ae60;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
            QPushButton:pressed {
                background-color: #219653;
            }
        """)
        add_btn.clicked.connect(self.add_order)
        self.layout.addWidget(add_btn)

        search_btn = QPushButton("جستجو و حذف و ویرایش اطلاعات")
        search_btn.setFixedHeight(60)
        search_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #2980b9;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
            QPushButton:pressed {
                background-color: #2475a4;
            }
        """)
        search_btn.clicked.connect(self.search_order)
        self.layout.addWidget(search_btn)

        exit_btn = QPushButton("خروج")
        exit_btn.setFixedHeight(60)
        exit_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #c0392b;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
            QPushButton:pressed {
                background-color: #a53125;
            }
        """)
        exit_btn.clicked.connect(self.close)
        self.layout.addWidget(exit_btn)

    def open_new_window(self, window_class, title):
        if self.current_window:
            self.current_window.close()

        self.current_window = window_class(self)
        self.current_window.setWindowTitle(title)
        self.current_window.setGeometry(150, 150, 800, 600)
        self.current_window.show()

    def add_order(self):
        self.open_new_window(AddDataBaseGUI, "افزودن اطلاعات")

    def search_order(self):
        self.open_new_window(SearchAndUpdateGUI, "جستجو و حذف و ویرایش اطلاعات")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OrdersApp()
    window.show()
    sys.exit(app.exec())