from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtGui import QIcon
from Login_ui import Ui_Form
import pymysql
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MyWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.bind()
        self.db = None
        
    def bind(self):
        self.pushButton.clicked.connect(self.login_function)

    def get_database_connection(self, dbhost, dbuser, dbpass, dbname):
        try:
            if dbpass == "" or dbpass == None:
                db = pymysql.connect(host=dbhost, user=dbuser, database=dbname)
            else:
                db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
            logging.info("数据库连接成功")
            return db
        except pymysql.Error as e:
            logging.error("数据库连接失败：" + str(e))
            return None
    
    def login_function(self):
        # 获取文本框的内容
        host = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        dbname = self.lineEdit_4.text()
        logging.info("host: %s, username: %s, password: %s, dbname: %s", host, username, password, dbname)
        self.db = self.get_database_connection(host, username, password, dbname)
        if self.db == None:
            # 弹窗提示
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("错误")
            msg_box.setText("连接失败")
            msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msg_box.button(QMessageBox.Ok).setText("继续")
            msg_box.button(QMessageBox.Cancel).setText("取消")
            result = msg_box.exec()

            if result == QMessageBox.Cancel:
                return
        # 进入 Ui_HSRMainWindow
        self.hide()
        from HSRMain import MainWindow  # 延迟导入
        self.main_window = MainWindow(self.db)
        self.main_window.show()
    
    def closeEvent(self, event):
        if self.db:
            self.db.close()
            logging.error("数据库连接已关闭")
        event.accept()

if __name__ == "__main__":
    app = QApplication()
    app.setWindowIcon(QIcon('icon\HSR_HH.ico')) 
    stats = MyWindow()
    stats.show()
    app.exec()