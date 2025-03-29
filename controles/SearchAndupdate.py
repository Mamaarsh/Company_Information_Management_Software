from pathlib import Path
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtWidgets import (QDialog, QLabel, QRadioButton, QLineEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QListWidget, QMessageBox,
                             QScrollArea, QWidget, QFrame, QApplication)
from PyQt6.QtCore import Qt
from controles.Database import Orders
from collections import defaultdict
import sys
import os


class SearchAndUpdateGUI(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("جستجوی اطلاعات")
        self.setGeometry(100, 100, 600, 800)
        self.parent = parent
        icon_path = str(Path(__file__).parent / "addition_info" / "favicon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.orders = Orders()
        self.current_results = []
        self.result_widgets = []
        self.selected_index = None
        self.search_criteria = ""
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(15)

        search_type_group = QWidget()
        search_type_layout = QVBoxLayout()

        self.search_type_label = QLabel("جستجو بر اساس:")
        self.search_type_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        search_type_layout.addWidget(self.search_type_label)

        self.search_option = "name"

        radio_group = QWidget()
        radio_layout = QHBoxLayout()

        self.name_radio = QRadioButton("نام و نام خانوادگی")
        self.name_radio.setChecked(True)
        self.name_radio.toggled.connect(lambda: self.set_search_type("name"))
        radio_layout.addWidget(self.name_radio)

        self.id_radio = QRadioButton("کد منحصر به فرد")
        self.id_radio.toggled.connect(lambda: self.set_search_type("id"))
        radio_layout.addWidget(self.id_radio)

        self.mobile_radio = QRadioButton("شماره تلفن")
        self.mobile_radio.toggled.connect(lambda: self.set_search_type("mobile"))
        radio_layout.addWidget(self.mobile_radio)

        radio_group.setLayout(radio_layout)
        search_type_layout.addWidget(radio_group)
        search_type_group.setLayout(search_type_layout)
        self.main_layout.addWidget(search_type_group)

        self.input_frame = QFrame()
        self.input_layout = QVBoxLayout()
        self.input_layout.setSpacing(10)
        self.input_frame.setLayout(self.input_layout)
        self.main_layout.addWidget(self.input_frame)

        self.create_widgets()

        button_group = QWidget()
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)

        self.search_button = QPushButton("جستجو")
        self.search_button.setFixedHeight(40)
        self.search_button.clicked.connect(self.search_order)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.edit_button = QPushButton("ویرایش")
        self.edit_button.setFixedHeight(40)
        self.edit_button.clicked.connect(self.edit_selected_order)
        self.edit_button.setEnabled(False)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        self.delete_button = QPushButton("حذف")
        self.delete_button.setFixedHeight(40)
        self.delete_button.clicked.connect(self.delete_selected_order)
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)

        self.back_button = QPushButton("بازگشت")
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.back_to_main)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #ff9800;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #e68a00;
            }
        """)

        self.button_layout.addWidget(self.search_button)
        self.button_layout.addWidget(self.edit_button)
        self.button_layout.addWidget(self.delete_button)
        self.button_layout.addWidget(self.back_button)
        button_group.setLayout(self.button_layout)
        self.main_layout.addWidget(button_group)

        self.results_area = QScrollArea()
        self.results_area.setWidgetResizable(True)
        self.results_area.setMinimumHeight(240)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout()
        self.results_layout.setSpacing(15)
        self.results_container.setLayout(self.results_layout)
        self.results_area.setWidget(self.results_container)
        self.main_layout.addWidget(self.results_area)

        self.setLayout(self.main_layout)
        self.show_name_fields()

    def create_widgets(self):
        self.name_label = QLabel("نام:")
        self.name_label.setStyleSheet("font-size: 14px;")
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText("نام (اختیاری)...")
        self.name_suggestions = QListWidget()
        self.name_suggestions.setMaximumHeight(120)

        self.lastname_label = QLabel("نام خانوادگی:")
        self.lastname_label.setStyleSheet("font-size: 14px;")
        self.lastname_entry = QLineEdit()
        self.lastname_entry.setPlaceholderText("نام خانوادگی (الزامی)...")
        self.lastname_suggestions = QListWidget()
        self.lastname_suggestions.setMaximumHeight(120)

        self.search_label = QLabel("ورودی جستجو:")
        self.search_label.setStyleSheet("font-size: 14px;")
        self.search_entry = QLineEdit()
        self.search_entry.setPlaceholderText("متن جستجو را وارد کنید...")

        self.input_layout.addWidget(self.name_label)
        self.input_layout.addWidget(self.name_entry)
        self.input_layout.addWidget(self.name_suggestions)
        self.input_layout.addWidget(self.lastname_label)
        self.input_layout.addWidget(self.lastname_entry)
        self.input_layout.addWidget(self.lastname_suggestions)
        self.input_layout.addWidget(self.search_label)
        self.input_layout.addWidget(self.search_entry)

        self.name_entry.textChanged.connect(self.update_name_suggestions)
        self.lastname_entry.textChanged.connect(self.update_lastname_suggestions)
        self.name_suggestions.itemClicked.connect(self.select_name_suggestion)
        self.lastname_suggestions.itemClicked.connect(self.select_lastname_suggestion)

        self.name_suggestions.setStyleSheet("""
            QListWidget {
                font-size: 14px;
                border: 1px solid #ddd;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
        """)
        self.lastname_suggestions.setStyleSheet(self.name_suggestions.styleSheet())

    def set_search_type(self, search_type):
        self.search_option = search_type
        self.clear_input_fields()
        self.clear_results()

        if search_type == "name":
            self.show_name_fields()
        else:
            self.show_general_search()

    def show_name_fields(self):
        self.search_label.hide()
        self.search_entry.hide()

        self.name_label.show()
        self.name_entry.show()
        self.name_suggestions.show()
        self.lastname_label.show()
        self.lastname_entry.show()
        self.lastname_suggestions.show()

    def show_general_search(self):
        self.name_label.hide()
        self.name_entry.hide()
        self.name_suggestions.hide()
        self.lastname_label.hide()
        self.lastname_entry.hide()
        self.lastname_suggestions.hide()

        self.search_label.show()
        self.search_entry.show()

    def clear_input_fields(self):
        self.name_entry.clear()
        self.lastname_entry.clear()
        self.search_entry.clear()
        self.name_suggestions.clear()
        self.lastname_suggestions.clear()

    def clear_results(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.result_widgets = []
        self.current_results = []
        self.selected_index = None
        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

    def update_name_suggestions(self):
        search_text = self.name_entry.text().strip()
        self.name_suggestions.clear()

        if search_text:
            query = "SELECT DISTINCT firstname FROM Info WHERE firstname LIKE %s LIMIT 5"
            self.orders.cur.execute(query, (search_text + "%",))
            suggestions = self.orders.cur.fetchall()

            for suggestion in suggestions:
                self.name_suggestions.addItem(suggestion[0])

    def update_lastname_suggestions(self):
        search_text = self.lastname_entry.text().strip()
        self.lastname_suggestions.clear()

        if search_text:
            query = "SELECT DISTINCT lastname FROM Info WHERE lastname LIKE %s LIMIT 5"
            self.orders.cur.execute(query, (search_text + "%",))
            suggestions = self.orders.cur.fetchall()

            for suggestion in suggestions:
                self.lastname_suggestions.addItem(suggestion[0])

    def select_name_suggestion(self, item):
        self.name_entry.setText(item.text())
        self.name_suggestions.clear()

    def select_lastname_suggestion(self, item):
        self.lastname_entry.setText(item.text())
        self.lastname_suggestions.clear()

    def phonecodecity(self, phone):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(base_dir, "addition_info", "citys.txt")

            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 2 and phone == parts[1]:
                            return parts[0]
                return "کد شهر وجود ندارد."
            return "فایل citys.txt یافت نشد."
        except Exception as e:
            return f"خطا در خواندن فایل: {str(e)}"

    def search_order(self):
        self.clear_results()
        search_type = self.search_option

        if search_type == "name":
            firstname = self.name_entry.text().strip()
            lastname = self.lastname_entry.text().strip()

            if not lastname:
                QMessageBox.warning(self, "خطا", "لطفاً حداقل نام خانوادگی را وارد کنید.")
                return

            if firstname:
                query = '''SELECT Info.firstname, Info.lastname, Company.companyname, 
                          Company.internal, Company.prephone, Company.phone, 
                          Company.phone2, Company.mobilephone, Info.userid
                          FROM Info LEFT JOIN Company ON Info.userid = Company.userid
                          WHERE Info.firstname = %s AND Info.lastname = %s'''
                self.orders.cur.execute(query, (firstname, lastname))
                self.search_criteria = f"نتایج برای: {firstname} {lastname}"
            else:
                query = '''SELECT Info.firstname, Info.lastname, Company.companyname, 
                          Company.internal, Company.prephone, Company.phone, 
                          Company.phone2, Company.mobilephone, Info.userid
                          FROM Info LEFT JOIN Company ON Info.userid = Company.userid
                          WHERE Info.lastname = %s'''
                self.orders.cur.execute(query, (lastname,))
                self.search_criteria = f"نتایج برای نام خانوادگی: {lastname}"

        elif search_type == "id":
            search_value = self.search_entry.text().strip()
            if not search_value:
                QMessageBox.warning(self, "خطا", "لطفاً کد کاربری را وارد کنید.")
                return

            query = '''SELECT Info.firstname, Info.lastname, Company.companyname, 
                      Company.internal, Company.prephone, Company.phone, 
                      Company.phone2, Company.mobilephone, Info.userid
                      FROM Info LEFT JOIN Company ON Info.userid = Company.userid
                      WHERE Info.userid = %s'''
            self.orders.cur.execute(query, (search_value,))
            self.search_criteria = f"نتایج برای کد منحصر به فرد: {search_value}"

        elif search_type == "mobile":
            search_value = self.search_entry.text().strip()
            if not search_value:
                QMessageBox.warning(self, "خطا", "لطفاً شماره تلفن را وارد کنید.")
                return

            query = '''SELECT Info.firstname, Info.lastname, Company.companyname, 
                      Company.internal, Company.prephone, Company.phone, 
                      Company.phone2, Company.mobilephone, Info.userid
                      FROM Info LEFT JOIN Company ON Info.userid = Company.userid
                      WHERE Company.phone = %s OR Company.phone2 = %s OR Company.mobilephone = %s'''
            self.orders.cur.execute(query, (search_value, search_value, search_value))
            self.search_criteria = f"نتایج برای شماره تلفن: {search_value}"

        data = self.orders.cur.fetchall()
        self.display_results(data)

    def display_results(self, data):
        if not data:
            QMessageBox.information(self, "نتیجه", "هیچ نتیجه‌ای یافت نشد.")
            return

        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #e9ecef;
                border: 1px solid #ced4da;
                border-radius: 5px;
                margin-bottom: 15px;
            }
        """)

        header_layout = QVBoxLayout()
        header_label = QLabel(f"<h3>{self.search_criteria}</h3>")
        header_label.setStyleSheet("color: #495057; padding: 10px;")
        header_layout.addWidget(header_label)
        header_frame.setLayout(header_layout)
        self.results_layout.addWidget(header_frame)

        for index, record in enumerate(data):
            record_frame = QFrame()
            record_frame.setFrameShape(QFrame.Shape.StyledPanel)
            record_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            record_frame.setProperty("record_index", index)
            record_frame.mousePressEvent = lambda e, idx=index: self.select_record(idx)

            record_frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    margin: 5px 0;
                    padding: 10px;
                }
                QFrame:hover {
                    background-color: #f1f1f1;
                }
                QFrame[selected=true] {
                    background-color: #e3f2fd;
                    border: 2px solid #2196F3;
                }
            """)

            record_layout = QVBoxLayout()
            record_layout.setSpacing(5)

            name_label = QLabel(f"<b>نام:</b> {record[0]} {record[1]}")
            name_label.setStyleSheet("color: #495057; font-size: 14px;")

            id_label = QLabel(f"<b>کد کاربری:</b> {record[8]}")
            id_label.setStyleSheet("color: #495057; font-size: 14px;")

            record_layout.addWidget(name_label)
            record_layout.addWidget(id_label)

            if record[2]:
                company_label = QLabel(f"<b>شرکت:</b> {record[2]}")
                company_label.setStyleSheet("color: #6c757d; font-size: 13px;")
                record_layout.addWidget(company_label)

            phones = []
            if record[4] and record[5]:
                city = self.phonecodecity(record[4])
                phones.append(f"<b>تلفن:</b> {city} - {record[4]}/{record[5]}")
            elif record[5]:
                phones.append(f"<b>تلفن:</b> {record[5]}")

            if record[7]:
                phones.append(f"<b>موبایل:</b> {record[7]}")

            for phone_text in phones:
                phone_label = QLabel(phone_text)
                phone_label.setStyleSheet("color: #6c757d; font-size: 13px;")
                record_layout.addWidget(phone_label)

            record_frame.setLayout(record_layout)
            self.results_layout.addWidget(record_frame)
            self.result_widgets.append(record_frame)
            self.current_results.append(record)

    def select_record(self, index):
        for i, widget in enumerate(self.result_widgets):
            widget.setProperty("selected", i == index)
            widget.style().unpolish(widget)
            widget.style().polish(widget)

        self.selected_index = index
        self.edit_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def edit_selected_order(self):
        try:
            from controles.Editinfo import EditOrderGUI

            if self.selected_index is None or not self.current_results:
                QMessageBox.warning(self, "خطا", "لطفاً ابتدا یک مورد را انتخاب کنید.")
                return

            selected_order = self.current_results[self.selected_index]

            order_data = {
                'userid': selected_order[8],
                'firstname': selected_order[0],
                'lastname': selected_order[1],
                'companyname': selected_order[2],
                'internal': selected_order[3],
                'prephone': selected_order[4],
                'phone': selected_order[5],
                'phone2': selected_order[6],
                'mobilephone': selected_order[7]
            }

            self.edit_window = EditOrderGUI(order_data, parent=self)
            self.edit_window.show()
            self.hide()

        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در باز کردن صفحه ویرایش:\n{str(e)}")

    def delete_selected_order(self):
        if self.selected_index is None or not self.current_results:
            QMessageBox.warning(self, "خطا", "لطفاً ابتدا یک مورد را انتخاب کنید.")
            return

        selected_order = self.current_results[self.selected_index]
        userid = selected_order[8]
        firstname = selected_order[0]
        lastname = selected_order[1]

        reply = QMessageBox.question(
            self, "تأیید حذف",
            f"آیا از حذف اطلاعات {firstname} {lastname} با کد {userid} اطمینان دارید؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.orders.cur.execute(
                    'DELETE FROM Company WHERE userid = %s',
                    (userid,)
                )

                self.orders.cur.execute(
                    'DELETE FROM Info WHERE userid = %s',
                    (userid,)
                )

                self.orders.conn.commit()
                QMessageBox.information(self, "حذف موفق", "اطلاعات با موفقیت حذف شد.")
                self.search_order()

            except Exception as e:
                QMessageBox.critical(self, "خطا", f"خطا در حذف اطلاعات:\n{str(e)}")
                self.orders.conn.rollback()

    def back_to_main(self):
        self.close()
        if self.parent:
            self.parent.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchAndUpdateGUI()
    window.show()
    sys.exit(app.exec())