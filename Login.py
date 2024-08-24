from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtGui import QIcon
from Login_ui import Ui_Form
from dao import hsr_mapper
import logging
import os

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
    
    def login_function(self):
        # 获取文本框的内容
        host = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        dbname = self.lineEdit_4.text()
        logging.info("host: %s, username: %s, password: %s, dbname: %s", host, username, password, dbname)
        self.db = hsr_mapper.get_database_connection(host, username, password, dbname)
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

@staticmethod
def read_qss_file(qss_file_name):
    with open(qss_file_name, 'r',  encoding='UTF-8') as file:
        return file.read()

if __name__ == "__main__":
    app = QApplication()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(current_dir, 'icon', 'HSR_HH.ico')
    app.setWindowIcon(QIcon(icon_path))
    qss_file_path = os.path.join(current_dir, 'qss', 'MacOS.qss')
    app.setStyleSheet(read_qss_file(qss_file_path))
    stats = MyWindow()
    stats.show()
    app.exec()