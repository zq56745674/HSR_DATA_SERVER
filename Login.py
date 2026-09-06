from PySide6.QtWidgets import QApplication, QWidget, QMessageBox
from PySide6.QtGui import QIcon
from Login_ui import Ui_Form
from dao import hsr_mapper
from config import config
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)


class MyWindow(QWidget, Ui_Form):
    """Login window for database connection."""
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Pre-fill database fields from config if available
        self.lineEdit.setText(config.DB_HOST)
        self.lineEdit_2.setText(config.DB_USER)
        self.lineEdit_3.setText(config.DB_PASSWORD)
        self.lineEdit_4.setText(config.DB_NAME)

        self.bind()
        self.db = None

    def bind(self) -> None:
        self.pushButton.clicked.connect(self.login_function)

    def login_function(self) -> None:
        """Attempt to connect to the database."""
        host = self.lineEdit.text()
        username = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        dbname = self.lineEdit_4.text()

        logger.info("Attempting database connection: host=%s, username=%s, dbname=%s",
                    host, username, dbname)

        self.db = hsr_mapper.get_database_connection(host, username, password, dbname)
        if self.db is None:
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

        # Open main window
        self.hide()
        from HSRMain import MainWindow
        self.main_window = MainWindow(self.db)
        self.main_window.show()

    def closeEvent(self, event) -> None:
        if self.db:
            hsr_mapper.close_database_connection(self.db)
            logger.info("Database connection closed")
        event.accept()


def read_qss_file(qss_file_name: str) -> str:
    """Read a QSS file and return its content."""
    with open(qss_file_name, 'r', encoding='UTF-8') as file:
        return file.read()


if __name__ == "__main__":
    config.validate()

    app = QApplication(sys.argv)
    base_dir = Path(__file__).resolve().parent

    icon_path = base_dir / 'icon' / 'HSR_HH.ico'
    app.setWindowIcon(QIcon(str(icon_path)))

    qss_file_path = base_dir / 'qss' / 'MacOS.qss'
    app.setStyleSheet(read_qss_file(str(qss_file_path)))

    window = MyWindow()
    window.show()
    app.exec()