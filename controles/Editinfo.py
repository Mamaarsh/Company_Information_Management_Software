from pathlib import Path
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QMessageBox)
from controles.Database import Orders


class EditOrderGUI(QDialog):
    def __init__(self, order_data, parent=None):
        super().__init__(parent)
        self.order_data = order_data
        self.parent = parent
        self.setWindowTitle("ویرایش اطلاعات")
        self.setGeometry(100, 100, 400, 500)

        icon_path = str(Path(__file__).parent / "addition_info" / "favicon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.orders = Orders()
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.firstname_entry = self.create_label_entry("نام:", self.order_data['firstname'])
        self.lastname_entry = self.create_label_entry("نام خانوادگی*:", self.order_data['lastname'])
        self.companyname_entry = self.create_label_entry("نام شرکت:", self.order_data['companyname'])

        self.userid_label = QLabel("کد منحصر به فرد*:")
        self.userid_entry = QLineEdit(str(self.order_data['userid']))
        self.userid_entry.setReadOnly(True)
        self.userid_entry.setFixedHeight(30)
        self.layout.addWidget(self.userid_label)
        self.layout.addWidget(self.userid_entry)

        self.internal_entry = self.create_label_entry("شماره داخلی:", self.order_data['internal'])
        self.prephone_entry = self.create_label_entry("پیش شماره:", self.order_data['prephone'])
        self.phone_entry = self.create_label_entry("شماره ثابت:", self.order_data['phone'])
        self.phone2_entry = self.create_label_entry("شماره ثابت دو:", self.order_data['phone2'])
        self.mobilephone_entry = self.create_label_entry("شماره همراه:", self.order_data['mobilephone'])

        self.save_button = QPushButton("ذخیره تغییرات")
        self.save_button.setFixedHeight(50)
        self.save_button.setStyleSheet("font-size: 14px; padding: 10px;")
        self.save_button.clicked.connect(self.update_info)
        self.layout.addWidget(self.save_button)

        self.back_button = QPushButton("بازگشت")
        self.back_button.setFixedHeight(50)
        self.back_button.setStyleSheet("font-size: 14px; padding: 10px;")
        self.back_button.clicked.connect(self.back_to_search)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def create_label_entry(self, label_text, default_value=""):
        label = QLabel(label_text)
        entry = QLineEdit(str(default_value) if default_value is not None else "")
        entry.setFixedHeight(30)
        entry.setMinimumWidth(250)
        self.layout.addWidget(label)
        self.layout.addWidget(entry)
        return entry

    def update_info(self):
        updated_data = {
            'userid': self.order_data['userid'],
            'firstname': self.firstname_entry.text(),
            'lastname': self.lastname_entry.text(),
            'companyname': self.companyname_entry.text() or None,
            'internal': self.internal_entry.text() or None,
            'prephone': self.prephone_entry.text() or None,
            'phone': self.phone_entry.text() or None,
            'phone2': self.phone2_entry.text() or None,
            'mobilephone': self.mobilephone_entry.text() or None
        }

        if not updated_data['lastname']:
            QMessageBox.warning(self, "خطا", "لطفاً فیلدهای اجباری را پر کنید.")
            return

        try:
            self.orders.cur.execute('''
                UPDATE Info 
                SET firstname = %s, lastname = %s, companyname = %s 
                WHERE userid = %s
            ''', (
                updated_data['firstname'],
                updated_data['lastname'],
                updated_data['companyname'],
                updated_data['userid']
            ))

            self.orders.cur.execute('''
                UPDATE Company 
                SET companyname = %s, internal = %s, prephone = %s, 
                    phone = %s, phone2 = %s, mobilephone = %s 
                WHERE userid = %s
            ''', (
                updated_data['companyname'],
                updated_data['internal'],
                updated_data['prephone'],
                updated_data['phone'],
                updated_data['phone2'],
                updated_data['mobilephone'],
                updated_data['userid']
            ))

            self.orders.conn.commit()
            QMessageBox.information(self, "موفقیت", "اطلاعات با موفقیت به‌روزرسانی شد.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "خطا", f"مشکل در به‌روزرسانی اطلاعات: {str(e)}")
            self.orders.conn.rollback()

    def back_to_search(self):
        self.close()
        if self.parent:
            self.parent.show()