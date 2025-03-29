import pymysql
from PyQt6.QtWidgets import QApplication, QMessageBox
import sys

class Orders:
    def __init__(self):
        try:
            self.conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='M@m@rsh!a1384_',
                charset='utf8',
                database='Orders',
                autocommit=True
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            self.show_error_message(str(e))
            sys.exit()

    def reset_cursor(self):
        self.cur.close()
        self.cur = self.conn.cursor()

    def show_error_message(self, error_text):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("خطای اتصال")
        msg_box.setText(f"مشکل در ارتباط با سرور!\nلطفاً اینترنت یا تنظیمات دیتابیس را بررسی کنید.\n\nجزئیات: {error_text}")
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = Orders()
    sys.exit(app.exec())