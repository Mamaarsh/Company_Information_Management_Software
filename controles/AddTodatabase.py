from pathlib import Path
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QVBoxLayout, QMessageBox, QFileDialog)
from controles.Database import Orders
import pandas as pd
import sys


class AddDataBaseGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("افزودن اطلاعات")
        self.setGeometry(100, 100, 400, 500)

        icon_path = str(Path(__file__).parent / "addition_info" / "favicon.ico")
        self.setWindowIcon(QIcon(icon_path))

        self.orders = Orders()

        self.layout = QVBoxLayout()

        self.firstname_entry = self.create_label_entry("نام:")
        self.lastname_entry = self.create_label_entry("نام خانوادگی*:")
        self.companyname_entry = self.create_label_entry("نام شرکت:")
        self.userid_entry = self.create_label_entry("کد منحصر به فرد*:")
        self.internal_entry = self.create_label_entry("شماره داخلی:")
        self.prephone_entry = self.create_label_entry("پیش شماره:")
        self.phone_entry = self.create_label_entry("شماره ثابت:")
        self.phone2_entry = self.create_label_entry("شماره ثابت دو:")
        self.mobilephone_entry = self.create_label_entry("شماره همراه:")

        self.add_button = QPushButton("افزودن اطلاعات")
        self.add_button.setFixedHeight(50)
        self.add_button.setStyleSheet("font-size: 14px; padding: 10px;")
        self.add_button.clicked.connect(self.addinfo)
        self.layout.addWidget(self.add_button)

        # ✅ دکمه برای وارد کردن اطلاعات از فایل اکسل
        self.import_excel_button = QPushButton("افزودن از فایل اکسل")
        self.import_excel_button.setFixedHeight(50)
        self.import_excel_button.setStyleSheet("font-size: 14px; padding: 10px;")
        self.import_excel_button.clicked.connect(self.import_excel)
        self.layout.addWidget(self.import_excel_button)

        self.back_button = QPushButton("بازگشت")
        self.back_button.setFixedHeight(50)
        self.back_button.setStyleSheet("font-size: 14px; padding: 10px;")
        self.back_button.clicked.connect(self.back_to_main)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def create_label_entry(self, label_text):
        label = QLabel(label_text)
        entry = QLineEdit()
        entry.setFixedHeight(30)
        entry.setMinimumWidth(250)
        self.layout.addWidget(label)
        self.layout.addWidget(entry)
        entry.installEventFilter(self)
        return entry

    def addinfo(self):
        firstname = self.firstname_entry.text()
        lastname = self.lastname_entry.text()
        userid = self.userid_entry.text()
        companyname = self.companyname_entry.text() or None
        internal = self.internal_entry.text() or None
        prephone = self.prephone_entry.text() or None
        phone = self.phone_entry.text() or None
        phone2 = self.phone2_entry.text() or None
        mobilephone = self.mobilephone_entry.text() or None

        if not lastname or not userid:
            QMessageBox.warning(self, "خطا", "لطفاً تمام فیلدهای اجباری را پر کنید.")
            return

        try:
            self.orders.cur.execute('INSERT INTO Info (userid, firstname, lastname, companyname) VALUES (%s, %s, %s, %s)',
                                     (userid, firstname, lastname, companyname))
            self.orders.cur.execute(
                'INSERT INTO Company (userid, companyname, internal, prephone, phone, phone2, mobilephone) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (userid, companyname, internal, prephone, phone, phone2, mobilephone))
            self.orders.conn.commit()
            QMessageBox.information(self, "موفقیت", "اطلاعات با موفقیت ثبت شد.")
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"مشکل در ثبت اطلاعات: {e}")

    def import_excel(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "انتخاب فایل اکسل", "", "Excel Files (*.xlsx *.xls)")
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path, header=1)
            df.columns = [str(col).strip() for col in df.columns]

            # نگاشت فارسی به انگلیسی
            mapping = {
                "نام": "firstname",
                "نام خانوادگی": "lastname",
                "نام محل تماس": "companyname",
                "داخلی": "internal",
                "پیش شماره": "prephone",
                "ثابت 1": "phone",
                "ثابت 2": "phone2",
                "همراه": "mobilephone",
                "شماره منحصر به فرد" : "userid"
            }

            df.rename(columns=mapping, inplace=True)

            # تعریف تابع تبدیل NaN به None
            def safe_get(val):
                return None if pd.isna(val) else val

            for idx, row in df.iterrows():
                userid = idx + 1
                firstname = safe_get(row.get("firstname"))
                lastname = safe_get(row.get("lastname"))
                companyname = safe_get(row.get("companyname"))
                internal = safe_get(row.get("internal"))
                prephone = safe_get(row.get("prephone"))
                phone = safe_get(row.get("phone"))
                phone2 = safe_get(row.get("phone2"))
                mobilephone = safe_get(row.get("mobilephone"))

                # فیلد اجباری بررسی شود
                if not lastname:
                    continue
                self.orders.cur.execute("SELECT COUNT(*) FROM Info WHERE userid = %s", (userid,))
                if self.orders.cur.fetchone()[0] == 0:
                    self.orders.cur.execute(
                        'INSERT INTO Info (userid, firstname, lastname, companyname) VALUES (%s ,%s, %s, %s)',
                        (userid, firstname, lastname, companyname)
                    )

                    self.orders.cur.execute(
                        'INSERT INTO Company (userid, companyname, internal, prephone, phone, phone2, mobilephone) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (userid, companyname, internal, prephone, phone, phone2, mobilephone)
                    )

            self.orders.conn.commit()
            QMessageBox.information(self, "موفقیت", "اطلاعات فایل اکسل با موفقیت ثبت شد.")

        except Exception as e:
            self.orders.conn.rollback()
            QMessageBox.critical(self, "خطا", f"خطا در وارد کردن فایل اکسل:\n{e}")

    def back_to_main(self):
        self.close()
        if self.parent:
            self.parent.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AddDataBaseGUI()
    window.show()
    sys.exit(app.exec())
