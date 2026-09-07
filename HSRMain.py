from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QHBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIntValidator
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from HSRMain_ui import Ui_MainWindow
from zipfile import BadZipFile
from util import baidu_translate, hsr_data_util, qianfan_chat, zzz_data_exe
from dao import hsr_mapper
from config import config
import requests
import pandas as pd
import random
import time
import logging
import os
import threading
import chardet
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# ctrl+k ctrl+0 折叠所有代码
# ctrl+k ctrl+j 展开所有代码

class MainWindow(QMainWindow, Ui_MainWindow):
    """Main application window."""
    
    # Server region constants
    SERVER_LABELS = ['cn', 'b', 'mei', 'ou', 'ya', 'gat']
    
    def __init__(self, db_connection):
        super().__init__()
        self.setupUi(self)
        self.menu.setFixedWidth(100)
        self.db = db_connection
        self.uid: str = ""
        self.serverName: str = ""
        self.interrupted: bool = False
        self.current_index: int = 0
        self.min_uid: int = 0
        self.max_uid: int = 0
        self.theme: str = 'light'

        # 设置窗口接受拖拽事件
        self.setAcceptDrops(True)
        self.get_max_uid(self.db)
        self.set_int_validator()
        self.bind()
        
    def bind(self):
        self.bind_actions([
            # 菜单栏
            (self.actionLogin, self.show_login),
            (self.actionExit, self.close),
            (self.actionAqua, lambda: self.toggle_theme('Aqua')),
            (self.actionMacOS, lambda: self.toggle_theme('MacOS')),
            (self.actionNeonButtons, lambda: self.toggle_theme('NeonButtons')),
            (self.actionUbuntu, lambda: self.toggle_theme('Ubuntu'))
        ])
        self.bind_buttons([
            # tab1按钮
            (self.fileButton, lambda: self.upload_file(1)),
            (self.fileExeButton, self.execute_file),
            (self.randomUidButton, self.random_uid),
            (self.interruptButton, self.interrupt_func),
            (self.continueButton, self.continue_func),
            (self.refreshMaxUidButton, lambda: self.get_max_uid(self.db)),
            # tab2按钮
            (self.fileButton_2, lambda: self.upload_file(2)),
            (self.fileZZZExeButton, self.execute_zzz_file),
            # tab3按钮
            (self.translateButton, self.translate_text),
            (self.sendAIButton, self.send_ai_text),
            # tab4按钮
            (self.fileButton_3, lambda: self.upload_file(3)),
            (self.dataAnalysisButton, self.data_analysis)
        ])
        self.bind_radio_buttons([
            # 单选按钮
            self.radioButton_cn,
            self.radioButton_b,
            self.radioButton_ya,
            self.radioButton_ou,
            self.radioButton_mei,
            self.radioButton_gat
        ])

    def bind_actions(self, actions):
        for action, method in actions:
            action.triggered.connect(method)

    def bind_buttons(self, buttons):
        for button, method in buttons:
            button.clicked.connect(method)

    def bind_radio_buttons(self, radio_buttons):
        for radio_button in radio_buttons:
            radio_button.clicked.connect(self.radio_button_clicked)
    
    def data_analysis(self) -> None:
        """Analyze data from uploaded CSV file."""
        file = self.fileLabel_3.text()
        if file == "未选择文件":
            self.show_error_message("未选择文件")
            return

        self.dataAnalysisButton.setEnabled(False)
        self.analysis_thread = DataAnalysisThread(file)
        self.analysis_thread.data_ready.connect(self.on_data_ready)
        self.analysis_thread.error_occurred.connect(self.on_analysis_error)
        self.analysis_thread.start()

    def on_data_ready(self, data) -> None:
        self.data = data

        # 图表画布只创建一次，后续复用
        if not hasattr(self, 'canvas'):
            self.central_layout = QHBoxLayout()
            self.widget_2.setLayout(self.central_layout)
            self.figure = Figure()
            self.canvas = FigureCanvas(self.figure)
            self.central_layout.addWidget(self.canvas)

        self.generate_table(self.data)
        self.plot_graph(self.data)
        self.dataAnalysisButton.setEnabled(True)

    def on_analysis_error(self, message) -> None:
        self.dataAnalysisButton.setEnabled(True)
        self.show_error_message(f"数据分析失败: {message}")
    
    def generate_table(self, data: list) -> None:
        """Populate table widget with data."""
        if not data:
            return
        
        # 设置表格行数和列数
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels(list(data[0].keys()))

        # 填充表格数据
        for row_index, row_data in enumerate(data):
            for col_index, (key, value) in enumerate(row_data.items()):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def plot_graph(self, data: list) -> None:
        """Plot line graph from data."""
        if not data or "DATE" not in data[0]:
            return
        
        # 清除之前的图表
        self.figure.clear()

        # 创建一个新的子图
        ax = self.figure.add_subplot(111)

        # 提取数据
        dates = [row["DATE"] for row in data]
        sorts = [row["GS"] for row in data]

        # 绘制折线图
        ax.plot(dates, sorts, marker='o')

        # 设置图表标题和标签
        ax.set_xlabel("日期")
        ax.set_ylabel("排名")

        # 刷新图表
        self.canvas.draw()
    
    def send_ai_text(self):
        text = self.fromTextEdit_2.toPlainText()
        self.start_thread(apprType="4", fromText=text)
    
    def translate_text(self):
        text = self.fromTextEdit.toPlainText()
        fromLang_str = self.fromComboBox.currentText()
        toLang_str = self.toComboBox.currentText()
        fromLang = baidu_translate.BaiDuFanyi().get_lang_code(fromLang_str)
        toLang = baidu_translate.BaiDuFanyi().get_lang_code(toLang_str)
        self.start_thread(apprType="3", fromText=text, fromLang=fromLang, toLang=toLang)

    def toggle_theme(self, theme):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qss_file_path = os.path.join(current_dir, 'qss', f'{theme}.qss')
        self.setStyleSheet(self.read_qss_file(qss_file_path))
    
    def show_login(self):
        from Login import MyWindow
        self.login_window = MyWindow()
        self.login_window.show()
        self.close()
        
    def radio_button_clicked(self):
        sender = self.sender()
        radio_name = sender.objectName()
        suffix = radio_name.split('_')[-1]
        label_name = f"label_{suffix}"
        label = getattr(self, label_name, None)
        if label:
            self.uid = label.text()
            self.serverName = suffix
            self.maxUidLabel.setText("最大uid：" + self.uid)
            self.update_min_max_uid()
        else:
            logging.info(f"未找到对应的标签: {label_name}")
    
    def interrupt_func(self):
        logging.info("中断")
        self.interrupted = True # 设置标志变量为 True
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.set_interrupted(True) # 调用线程的中断方法
        self.set_buttons_enabled(True) # 将按钮设置为不可用
    
    def continue_func(self):
        logging.info("继续")
        self.interrupted = False  # 设置标志变量为 False
        if hasattr(self, 'thread') and not self.thread.isRunning():
            self.thread.set_interrupted(False)
            self.thread.set_current_index(self.current_index)
            self.thread.start()  # 重新启动线程
        self.set_buttons_enabled(False)
    
    def execute_file(self):
        self.start_thread(apprType="1", file=self.fileLabel.text())

    def execute_zzz_file(self):
        file = self.fileLabel_2.text()
        if file == "未选择文件":
            self.show_error_message("未选择文件")
            return
        self.fileZZZExeButton.setEnabled(False)
        self.zzz_thread = ZZZThread(file)
        self.zzz_thread.finished_ok.connect(self.on_zzz_finished)
        self.zzz_thread.error_occurred.connect(self.on_zzz_error)
        self.zzz_thread.start()

    def on_zzz_finished(self):
        logging.info("文件处理完成")
        self.fileZZZExeButton.setEnabled(True)
        QMessageBox.information(self, "完成", "文件处理完成")

    def on_zzz_error(self, message):
        self.fileZZZExeButton.setEnabled(True)
        self.show_error_message(message, 0)

    def random_uid(self):
        if self.serverName == "":
            self.show_error_message("请选择服务器")
            return
        self.update_min_max_uid()
        self.start_thread(apprType="2", maxLen=self.maxLenLineEdit.text(), maxUid=self.uid)

    def start_thread(self, apprType, file=None, maxLen=None, maxUid=None, fromText=None, fromLang=None, toLang=None):
        self.interrupted = False
        self.current_index = 0
        if apprType == "1" and not file:
            self.show_error_message("未选择文件")
            return
        self.set_buttons_enabled(False)
        self.thread = ExecuteFileThread(self.db, file, self.serverName, self.interrupted, self.current_index, apprType, maxLen, maxUid, self.min_uid, self.max_uid, fromText, fromLang, toLang)
        self.thread.finished_info.connect(self.on_thread_finished)
        self.thread.error_occurred.connect(self.show_error_message)
        self.thread.info_view.connect(self.show_info_message)
        self.thread.progress_updated.connect(self.update_progress_bar)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressLabel.setText("0/0")
        self.timeLabel.setText("00:00:00")
        self.thread.start()

    def update_min_max_uid(self):
        min_edit_name = f"minUidEdit_{self.serverName}"
        max_edit_name = f"maxUidEdit_{self.serverName}"
        min_edit = getattr(self, min_edit_name, None)
        max_edit = getattr(self, max_edit_name, None)
        self.min_uid = int(min_edit.text())
        self.max_uid = int(max_edit.text())
    
    def update_progress_bar(self, value, progress_info, remaining_time):
        self.progressBar.setValue(value)
        self.progressLabel.setText(progress_info)
        self.timeLabel.setText(remaining_time)
    
    def on_thread_finished(self):
        logging.info("文件处理完成")
        self.set_buttons_enabled(True)
        QMessageBox.information(self, "完成", "文件处理完成")
    
    def read_qss_file(self, qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()
    
    def show_message(self, message, title="信息", icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStandardButtons(buttons)
        msg_box.button(buttons).setText("确定")
        msg_box.exec()

    def show_error_message(self, message, index=None):
        if index is not None:
            self.current_index = index
        self.show_message(message, title="错误", icon=QMessageBox.Critical)
        self.set_buttons_enabled(True)

    def show_info_message(self, message, textBrowser):
        if textBrowser == "infoBrowser":
            getattr(self, textBrowser).append(message)
        else:
            getattr(self, textBrowser).setText(message)

    def get_max_uid(self, db):
        if db is None:
            self.show_error_message("数据库未连接")
            return
        try:
            hsr_mapper.reconnect_database(db)
            result = hsr_mapper.get_max_uid(db)
        except Exception as e:
            logging.error(f"刷新最大UID失败: {e}")
            self.show_error_message(f"刷新最大UID失败: {e}")
            return
        if result:
            self.set_max_uid_labels(result)
            summary = ", ".join(
                f"{label}={getattr(self, f'label_{label}').text()}"
                for label in self.SERVER_LABELS
            )
            logging.info(f"刷新完成: {summary}")
            self.show_info_message(f"刷新完成: {summary}", 'infoBrowser')
            if self.serverName:
                self.uid = getattr(self, f"label_{self.serverName}").text()
                self.maxUidLabel.setText("最大uid：" + self.uid)
        else:
            logging.error("查询失败")
            self.show_error_message("查询失败：未获取到最大UID数据")

    def set_max_uid_labels(self, result) -> None:
        """Set max UID labels from query result."""
        for label, value in zip(self.SERVER_LABELS, result):
            getattr(self, f"label_{label}").setText(str(value[0]))

    def upload_file(self, tab):
        default_path = os.path.expanduser("~/Desktop")  # 使用 os.path.expanduser 获取桌面路径
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", default_path, "表格文件 (*.xlsx *.xls *.csv);;所有文件 (*)")
        file_labels = {
            1: self.fileLabel,  2: self.fileLabel_2,
            3: self.fileLabel_3
        }
        if tab in file_labels:
            file_labels[tab].setText(file_path if file_path else "未选择文件")

    def dragEnterEvent(self, event):
        # 检查拖拽的文件类型
        logging.info("dragEnterEvent")
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        # 处理拖拽的文件
        logging.info("dropEvent")
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                file_path = urls[0].toLocalFile()
                self.fileLabel.setText(file_path)
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def closeEvent(self, event):
        hsr_mapper.close_database_connection(self.db)
        hsr_mapper.get_connection_pool(config.MAX_WORKERS).close_all()
        event.accept()
    
    def set_int_validator(self):
        line_edits = [
            self.minUidEdit_cn, self.maxUidEdit_cn,
            self.minUidEdit_b, self.maxUidEdit_b,
            self.minUidEdit_ya, self.maxUidEdit_ya,
            self.minUidEdit_ou, self.maxUidEdit_ou,
            self.minUidEdit_mei, self.maxUidEdit_mei,
            self.minUidEdit_gat, self.maxUidEdit_gat,
            self.maxLenLineEdit,
        ]
        for line_edit in line_edits:
            line_edit.setValidator(QIntValidator(0, 999999999, line_edit))
    
    def set_buttons_enabled(self, enabled):
        # 按钮列表
        buttons = [
            self.fileExeButton, self.randomUidButton, self.continueButton
        ]
        # 设置按钮的启用状态
        for button in buttons:
            button.setEnabled(enabled)
        # QLineEdit 列表
        line_edits = [
            self.minUidEdit_cn, self.maxUidEdit_cn,
            self.minUidEdit_b, self.maxUidEdit_b,
            self.minUidEdit_ya, self.maxUidEdit_ya,
            self.minUidEdit_ou, self.maxUidEdit_ou,
            self.minUidEdit_mei, self.maxUidEdit_mei,
            self.minUidEdit_gat, self.maxUidEdit_gat
        ]
        # 设置 QLineEdit 的启用状态
        for line_edit in line_edits:
            line_edit.setEnabled(enabled)

class SignalThrottler:
    """Thread-safe time-based throttler for high-frequency signals."""

    def __init__(self, interval: float):
        self.interval = interval
        self._lock = threading.Lock()
        self._last = 0.0

    def ready(self) -> bool:
        """Return True if enough time has elapsed since the last emit."""
        now = time.time()
        with self._lock:
            if now - self._last >= self.interval:
                self._last = now
                return True
        return False


class RateLimiter:
    """Thread-safe rate limiter spacing out request starts."""

    def __init__(self, min_delay: float, max_delay: float, loop_limit: int, rest_time: int):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.loop_limit = loop_limit
        self.rest_time = rest_time
        self._lock = threading.Lock()
        self._next_start = 0.0
        self._count = 0

    def acquire(self) -> None:
        with self._lock:
            self._count += 1
            if self.loop_limit and self._count >= self.loop_limit:
                self._count = 0
                self._next_start = max(self._next_start, time.time()) + self.rest_time
            delay = random.uniform(self.min_delay, self.max_delay)
            now = time.time()
            self._next_start = max(self._next_start, now) + delay
            wait = self._next_start - now
        if wait > 0:
            time.sleep(wait)


class ExecuteFileThread(QThread):
    """Background thread for executing data crawling operations."""
    
    progress = Signal(int)
    finished_info = Signal()
    error_occurred = Signal(str, int)
    info_view = Signal(str, str)
    progress_updated = Signal(int, str, str)
    
    # Constant headers and server mappings
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    SERVER_PREFIX_MAP: Dict[str, str] = {
        '1': 'cn', '5': 'b', '6': 'mei', '7': 'ou', '8': 'ya', '9': 'gat'
    }

    def __init__(
        self,
        db,
        file: Optional[str],
        serverName: str,
        interrupted: bool,
        current_index: int,
        apprType: str,
        maxLen: Optional[str],
        maxUid: Optional[str],
        minEditUid: int,
        maxEditUid: int,
        fromText: Optional[str],
        fromLang: Optional[str],
        toLang: Optional[str]
    ):
        super().__init__()
        self.db = db
        self.file = file
        self.serverName = serverName
        self.interrupted = interrupted
        self.current_index = current_index
        self.apprType = apprType
        self.maxLen = maxLen
        self.maxUid = maxUid
        self.minEditUid = minEditUid
        self.maxEditUid = maxEditUid
        self.fromText = fromText
        self.fromLang = fromLang
        self.toLang = toLang
        self.start_time: Optional[float] = None
        self.endpoint = config.HSR_API_ENDPOINT
        self._local = threading.local()
        self._rate_limiter = RateLimiter(
            config.REQUEST_DELAY_MIN, config.REQUEST_DELAY_MAX,
            config.LOOP_LIMIT, config.REST_TIME_SECONDS
        )
        self._progress_throttler = SignalThrottler(config.PROGRESS_EMIT_INTERVAL)
        self._log_throttler = SignalThrottler(config.LOG_EMIT_INTERVAL)
        self._completed = current_index
        self._completed_lock = threading.Lock()
        self._dbs = set()
        self._dbs_lock = threading.Lock()

    def run(self) -> None:
        """Dispatch to the appropriate method based on apprType."""
        method_mapping = {
            "1": self.execute_file,
            "2": self.random_uid,
            "3": self.translate_text,
            "4": self.send_ai_text
        }
        method = method_mapping.get(self.apprType)
        if method:
            method()

    def _get_session(self) -> requests.Session:
        """Return a thread-local requests.Session with reused connections and retry."""
        session = getattr(self._local, 'session', None)
        if session is None:
            session = requests.Session()
            session.headers.update(self.HEADERS)
            retry_strategy = Retry(
                total=config.RETRY_TOTAL,
                backoff_factor=config.RETRY_BACKOFF_FACTOR,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=frozenset(['GET']),
                respect_retry_after_header=True,
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            self._local.session = session
        return session

    def _get_db(self):
        """Return a thread-local database connection (from the shared pool)."""
        db = getattr(self._local, 'db', None)
        if db is None:
            db = hsr_mapper.get_connection_pool(config.MAX_WORKERS).get(self.db)
            self._local.db = db
            with self._dbs_lock:
                self._dbs.add(db)
        return db

    def _after_write(self):
        """Track pending writes and commit in batches."""
        pending = getattr(self._local, 'pending', 0) + 1
        if pending >= config.COMMIT_BATCH_SIZE:
            self._get_db().commit()
            pending = 0
        self._local.pending = pending

    def _flush_and_close(self):
        """Commit pending writes and return worker connections to the pool."""
        with self._dbs_lock:
            dbs = list(self._dbs)
            self._dbs.clear()
        pool = hsr_mapper.get_connection_pool(config.MAX_WORKERS)
        for db in dbs:
            try:
                db.commit()
                pool.put(db)
            except Exception as e:
                logging.error(f"flush db failed, closing connection: {e}")
                try:
                    db.close()
                except Exception:
                    pass

    def _emit_log(self, message: str):
        """Emit a throttled log line to the info browser."""
        if self._log_throttler.ready():
            self.info_view.emit(message, 'infoBrowser')
    
    def send_ai_text(self):
        if not self.fromText:
            return
        try:
            result = qianfan_chat.QianFanChat().chat(self.fromText)
            self.info_view.emit(result, "toTextBrowser_2")
        except Exception as e:
            self.error_occurred.emit(f"send_ai_text error: {str(e)}", 0)

    def translate_text(self):
        if not self.fromText:
            return
        try:
            result = baidu_translate.BaiDuFanyi().BdTrans(self.fromText, self.fromLang, self.toLang)
            self.info_view.emit(result, "toTextBrowser")
        except Exception as e:
            self.error_occurred.emit(f"translate_text error: {str(e)}", 0)

    def handle_interruption(self, index):
        logging.info("处理文件被中断")
        self.error_occurred.emit("处理文件被中断", index)

    def process_request(self, index, url, table_name, uid):
        logging.debug(f"i {index} url: {url}")
        self._emit_log(f"i {index} url: {url}")
        response = self._get_session().get(url, timeout=5)
        if response.status_code == 200:
            self.handle_successful_response(response, table_name, uid)
        elif response.status_code == 404:
            self.handle_not_found_response(response, uid, table_name)
        elif response.status_code == 429:
            self.handle_rate_limited(response, uid)
        else:
            self.handle_failed_response(response, uid)

    def handle_successful_response(self, response, table_name, uid):
        try:
            data = response.json()
        except ValueError as e:
            logging.warning(f"响应JSON解析失败 for uid: {uid}: {e}")
            self._emit_log(f"响应JSON解析失败 for uid: {uid}")
            hsr_mapper.log_request_failure(self._get_db(), uid, response.status_code, None, response.text[:500])
            self._after_write()
            return

        detail_info = data.get("detailInfo")
        if not detail_info:
            logging.warning(f"响应缺少 detailInfo for uid: {uid}")
            self._emit_log(f"响应缺少 detailInfo for uid: {uid}")
            hsr_mapper.log_request_failure(self._get_db(), uid, response.status_code, None, response.text[:500])
            self._after_write()
            return

        development_info = data.get("developmentInfo")
        record_info = detail_info.get("recordInfo") or {}
        # assist_avatar_list = detail_info.get("assistAvatarList")
        # avatar_detail_list = detail_info.get("avatarDetailList")
        uid = int(detail_info.get("uid"))
        platform = detail_info.get("platform")
        signature = detail_info.get("signature")
        nickname = detail_info.get("nickname")
        level = detail_info.get("level")
        friendCount = detail_info.get("friendCount")
        maxRogueChallengeScore = record_info.get("maxRogueChallengeScore")
        achievementCount = record_info.get("achievementCount")
        equipmentCount = record_info.get("equipmentCount")
        avatarCount = record_info.get("avatarCount")
        bookCount = record_info.get("bookCount")
        musicCount = record_info.get("musicCount")
        relicCount = record_info.get("relicCount")
        headIcon = detail_info.get("headIcon")
        # remark, goldNum = hsr_data_util.generate_remark(assist_avatar_list, avatar_detail_list)
        remark = ''
        goldNum = ''
        eventTime, eventType = hsr_data_util.generate_development(development_info)
        db = self._get_db()
        exist = hsr_mapper.get_user_info_by_uid(db, uid, table_name)
        if exist:
            dict1 = hsr_data_util.create_dict_from_db(exist)
            dict2 = hsr_data_util.create_dict_from_response(platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, relicCount, bookCount, musicCount)
            result = hsr_data_util.print_dict_differences(dict1, dict2)
            if result:
                hsr_mapper.insert_user_info_upd_record(db, uid, str(result[0]), str(result[1]))
                self._after_write()
            else:
                self._emit_log(f"uid: {uid} 信息相同")
        hsr_mapper.upsert_user_info(db, uid, table_name, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, goldNum, eventTime, eventType)
        self._after_write()

    def handle_not_found_response(self, response, uid, table_name):
        logging.debug(f"请求失败，状态码：{response.status_code}")
        self._emit_log(f"请求失败，状态码：{response.status_code}")
        hsr_mapper.log_request_failure(self._get_db(), uid, response.status_code, table_name)
        self._after_write()

    def handle_rate_limited(self, response, uid):
        logging.warning(f"429 Too Many Requests for uid: {uid}")
        self._emit_log(f"429 Too Many Requests（请求过于频繁），稍后降低并发重试")
        hsr_mapper.log_request_failure(self._get_db(), uid, response.status_code, None, response.text)
        self._after_write()

    def handle_failed_response(self, response, uid):
        logging.error(f"Error: {response.status_code} for uid: {uid}")
        self._emit_log(f"Error: {response.status_code} for uid: {uid}")
        hsr_mapper.log_request_failure(self._get_db(), uid, response.status_code, None, response.text)
        self._after_write()

    def handle_request_exception(self, e, uid):
        logging.error(f"请求出错：{e} for uid: {uid}")
        self._emit_log(f"请求出错：{e} for uid: {uid}")
        hsr_mapper.log_request_failure(self._get_db(), uid, 500, None, str(e))
        self._after_write()

    def update_progress(self, completed, total):
        progress = int(completed / total * 100) if total else 0
        progress_info = f"{completed}/{total}"
        if completed >= total or self._progress_throttler.ready():
            remaining_time = self.calculate_remaining_time(completed, total)
            self.progress_updated.emit(progress, progress_info, remaining_time)

    def random_uid(self) -> None:
        """Generate random UIDs and crawl player data."""
        self.start_time = time.time()
        maxLen = int(self.maxLen)
        max_uid = self.get_max_uid() if self.maxEditUid == 0 else self.maxEditUid
        min_uid = self.get_min_uid()

        total = maxLen - 1
        items = [
            (i, str(random.randint(self.minEditUid, max_uid) + min_uid))
            for i in range(self.current_index + 1, maxLen)
        ]
        self._run_concurrently(items, total)

    def execute_file(self) -> None:
        """Execute data crawling from a file containing UIDs."""
        self.start_time = time.time()
        try:
            if self.file.endswith('.xlsx') or self.file.endswith('.xls'):
                df = pd.read_excel(self.file, engine='openpyxl')
            elif self.file.endswith('.csv'):
                df = pd.read_csv(self.file, encoding='GBK')
            else:
                self.error_occurred.emit("不支持的文件格式", 0)
                return
        except FileNotFoundError:
            self.error_occurred.emit("未选择文件", 0)
            return
        except ValueError as e:
            self.error_occurred.emit(str(e), 0)
            return
        except BadZipFile:
            self.error_occurred.emit("文件不是有效的Excel文件", 0)
            return

        first = df.iloc[0]
        uid = str(first['uid'])
        self.serverName = self.determine_server_name(uid)

        uids = df['uid'].astype(str).tolist()
        total = len(uids)
        items = [
            (idx, uid)
            for idx, uid in zip(df.index, uids)
            if idx >= self.current_index
        ]
        self._run_concurrently(items, total)

    def _process_uid(self, index, uid, total):
        """Process a single UID within a worker thread."""
        if self.interrupted:
            return
        self._rate_limiter.acquire()
        table_name = self.get_table_name()
        url = self.endpoint + uid
        try:
            self.process_request(index, url, table_name, uid)
        except requests.exceptions.RequestException as e:
            self.handle_request_exception(e, uid)
        finally:
            with self._completed_lock:
                self._completed += 1
                completed = self._completed
            self.update_progress(completed, total)

    def _run_concurrently(self, items, total):
        """Run the given (index, uid) tasks concurrently with a thread pool."""
        if not items:
            self.finished_info.emit()
            return

        with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
            futures = []
            for index, uid in items:
                if self.interrupted:
                    break
                futures.append(executor.submit(self._process_uid, index, uid, total))

            for future in as_completed(futures):
                if self.interrupted:
                    for f in futures:
                        f.cancel()
                    break
                try:
                    future.result()
                except Exception as e:
                    logging.error(f"任务异常: {e}")
                    self.error_occurred.emit(f"任务异常: {e}", 0)

        self._flush_and_close()

        if self.interrupted:
            self.handle_interruption(self._completed)
        else:
            self.finished_info.emit()

    def get_max_uid(self) -> int:
        """Get max UID for a server, stripping prefix and leading zeros."""
        max_uid_str = str(self.maxUid).lstrip('0')[1:]
        return int(max_uid_str) if max_uid_str else 0

    def get_min_uid(self) -> int:
        """Get minimum UID for the current server."""
        return config.SERVER_MIN_UID.get(self.serverName, config.SERVER_MIN_UID['cn'])

    def calculate_remaining_time(self, completed: int, total: int) -> str:
        """Calculate estimated remaining time."""
        if completed <= 0:
            return "计算中..."
        elapsed_time = time.time() - self.start_time
        estimated_total_time = (elapsed_time / completed) * total
        remaining_time = max(estimated_total_time - elapsed_time, 0)
        return time.strftime("%H:%M:%S", time.gmtime(remaining_time))

    def determine_server_name(self, uid: str) -> str:
        """Determine server name from UID prefix."""
        return self.SERVER_PREFIX_MAP.get(uid[:1], "")

    def get_table_name(self) -> str:
        """Get table name for the current server."""
        return config.SERVER_TABLE_MAP.get(self.serverName, 'sr_user_info_default')

    def set_interrupted(self, interrupted: bool) -> None:
        self.interrupted = interrupted

    def set_current_index(self, current_index: int) -> None:
        self.current_index = current_index
        with self._completed_lock:
            self._completed = current_index


class ZZZThread(QThread):
    """Background thread for ZZZ data processing."""

    finished_ok = Signal()
    error_occurred = Signal(str)

    def __init__(self, file: str):
        super().__init__()
        self.file = file

    def run(self) -> None:
        try:
            zzz_data_exe.execute_zzz_file(self.file)
            self.finished_ok.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))


class DataAnalysisThread(QThread):
    """Background thread for reading CSV and converting to records."""

    data_ready = Signal(object)
    error_occurred = Signal(str)

    def __init__(self, file: str):
        super().__init__()
        self.file = file

    def run(self) -> None:
        try:
            encoding = self._detect_encoding()
            df = pd.read_csv(self.file, encoding=encoding)
            self.data_ready.emit(df.to_dict(orient='records'))
        except Exception as e:
            self.error_occurred.emit(str(e))

    def _detect_encoding(self) -> str:
        """Detect file encoding with chardet, falling back to GBK."""
        try:
            with open(self.file, 'rb') as f:
                raw = f.read(65536)
            encoding = chardet.detect(raw).get('encoding')
            if encoding:
                try:
                    pd.read_csv(self.file, encoding=encoding, nrows=1)
                    return encoding
                except (UnicodeDecodeError, LookupError):
                    pass
        except Exception:
            pass
        return 'GBK'