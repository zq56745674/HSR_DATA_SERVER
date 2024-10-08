from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, QHBoxLayout, QWidget
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIntValidator
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from HSRMain_ui import Ui_MainWindow
from zipfile import BadZipFile
from util import baidu_translate, hsr_data_util, qianfan_chat, zzz_data_exe
from dao import hsr_mapper
import requests
import pandas as pd
import random
import time
import logging
import os

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ctrl+k ctrl+0 折叠所有代码
# ctrl+k ctrl+j 展开所有代码

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, db_connection):
        super().__init__()
        self.setupUi(self)
        self.menu.setFixedWidth(100)
        self.db = db_connection
        self.uid = ""
        self.serverName = ""
        self.interrupted = False  # 添加标志变量
        self.current_index = 0
        self.min_uid = 0
        self.max_uid = 0
        self.theme = 'light'

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
    
    def data_analysis(self):
        file = self.fileLabel_3.text()
        if file == "未选择文件":
            self.show_error_message("未选择文件")
            return
        
        self.central_layout = QHBoxLayout()
        self.widget_2.setLayout(self.central_layout)

        # 创建一个FigureCanvas来显示图表
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.central_layout.addWidget(self.canvas)
        df = pd.read_csv(file, encoding='GBK')
        # df转换为字典列表
        self.data = df.to_dict(orient='records')
        
        self.generate_table(self.data)
        self.plot_graph(self.data)
    
    def generate_table(self, data):
        # 设置表格行数和列数
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        # 设置表头
        self.tableWidget.setHorizontalHeaderLabels(data[0].keys())

        # 填充表格数据
        for row_index, row_data in enumerate(data):
            for col_index, (key, value) in enumerate(row_data.items()):
                self.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def plot_graph(self, data):
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
        # ax.set_title("Scores by Name")
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
        try:
            zzz_data_exe.execute_zzz_file(file)
            logging.info("文件处理完成")
            QMessageBox.information(self, "完成", "文件处理完成")
        except Exception as e:
            self.show_error_message(str(e), 0)

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
        result = hsr_mapper.get_max_uid(db)
        if result:
            self.set_max_uid_labels(result)
        else:
            logging.error("查询失败")

    def set_max_uid_labels(self, result):
        labels = ['cn', 'b', 'mei', 'ou', 'ya', 'gat']
        for label, value in zip(labels, result):
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

class ExecuteFileThread(QThread):
    progress = Signal(int)
    finished_info = Signal()
    error_occurred = Signal(str, int)
    info_view = Signal(str, str)
    progress_updated = Signal(int, str, str)

    def __init__(self, db, file, serverName, interrupted, current_index, apprType, maxLen, maxUid, minEditUid, maxEditUid, fromText, fromLang, toLang):
        super().__init__()
        self.initialize_attributes(db, file, serverName, interrupted, current_index, apprType, maxLen, maxUid, minEditUid, maxEditUid, fromText, fromLang, toLang)
        self.start_time = None

    def initialize_attributes(self, db, file, serverName, interrupted, current_index, apprType, maxLen, maxUid, minEditUid, maxEditUid, fromText, fromLang, toLang):
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

    def run(self):
        method_mapping = {
            "1": self.execute_file,
            "2": self.random_uid,
            "3": self.translate_text,
            "4": self.send_ai_text
        }
        method = method_mapping.get(self.apprType)
        if method:
            method()
    
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

    def handle_loop_limit(self, rest_time):
        logging.info(f"已达到循环次数限制，休息 {rest_time} 秒")
        self.info_view.emit(f"已达到循环次数限制，休息 {rest_time} 秒", 'infoBrowser')
        time.sleep(rest_time)

    def process_request(self, index, url, headers, table_name, uid, not_found_count=None):
        logging.info(f"i {index} url: {url}")
        self.info_view.emit(f"i {index} url: {url}", 'infoBrowser')
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            self.handle_successful_response(response, table_name, uid)
        elif response.status_code == 404 and not_found_count is not None:
            self.handle_not_found_response(response, uid, table_name, not_found_count)
        else:
            self.handle_failed_response(response, uid)

    def handle_successful_response(self, response, table_name, uid):
        data = response.json()
        detail_info = data.get("detailInfo")
        record_info = detail_info.get("recordInfo")
        assist_avatar_list = detail_info.get("assistAvatarList")
        avatar_detail_list = detail_info.get("avatarDetailList")
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
        remark, goldNum = hsr_data_util.generate_remark(assist_avatar_list, avatar_detail_list)
        exist = hsr_mapper.get_user_info_by_uid(self.db, uid, table_name)
        if exist:
            dict1 = hsr_data_util.create_dict_from_db(exist)
            dict2 = hsr_data_util.create_dict_from_response(platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, relicCount, bookCount, musicCount)
            result = hsr_data_util.print_dict_differences(dict1, dict2)
            if result:
                hsr_mapper.insert_user_info_upd_record(self.db, uid, str(result[0]), str(result[1]))
            else:
                self.info_view.emit(f"uid: {uid} 信息相同", 'infoBrowser')
            hsr_mapper.update_user_info(self.db, uid, table_name, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, goldNum)
        else:
            hsr_mapper.insert_user_info(self.db, uid, table_name, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, goldNum)

    def handle_not_found_response(self, response, uid, table_name, not_found_count):
        not_found_count += 1
        logging.info(f"请求失败，状态码：{response.status_code}，404计数：{not_found_count}")
        self.info_view.emit(f"请求失败，状态码：{response.status_code}，404计数：{not_found_count}", 'infoBrowser')
        hsr_mapper.log_request_failure(self.db, uid, response.status_code, table_name)

    def handle_failed_response(self, response, uid):
        logging.error(f"Error: {response.status_code} for uid: {uid}")
        self.info_view.emit(f"Error: {response.status_code} for uid: {uid}", 'infoBrowser')
        hsr_mapper.log_request_failure(self.db, uid, response.status_code, None, response.text)

    def handle_request_exception(self, e, uid):
        logging.error(f"请求出错：{e} for uid: {uid}")
        self.info_view.emit(f"请求出错：{e} for uid: {uid}", 'infoBrowser')
        hsr_mapper.log_request_failure(self.db, uid, 500, None, str(e))

    def update_progress(self, index, maxLen):
        progress = int((index) / maxLen * 100)
        progress_info = f"{index}/{maxLen}"
        remaining_time = self.calculate_remaining_time(index, maxLen)
        self.progress_updated.emit(progress, progress_info, remaining_time)

    def random_uid(self):
        not_found_count = 0
        self.start_time = time.time()
        endpoint = "https://api.mihomo.me/sr_info/"
        loop_limit = 70
        rest_time = 5
        counter = 0
        maxLen = int(self.maxLen)
        max_uid = self.get_max_uid() if self.maxEditUid == 0 else self.maxEditUid
        min_uid = self.get_min_uid()

        for i in range(1, maxLen):
            if self.interrupted:
                self.handle_interruption(i)
                return

            if counter >= loop_limit:
                self.handle_loop_limit(rest_time)
                counter = 0
                
            uid = str(random.randint(self.minEditUid, max_uid) + min_uid)
            url = endpoint + uid
            table_name = self.get_table_name()
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            try:
                self.process_request(i, url, headers, table_name, uid, not_found_count)
            except requests.exceptions.RequestException as e:
                self.handle_request_exception(e, uid)
            
            self.update_progress(i, maxLen) # 更新进度条
            counter += 1
            time.sleep(random.uniform(0.7, 0.8))

        self.finished_info.emit()

    def execute_file(self):
        self.start_time = time.time()  # 记录开始时间
        try:
            if self.file.endswith('.xlsx') or self.file.endswith('.xls'):
                df = pd.read_excel(self.file, engine='openpyxl')  # 读取Excel文件
            elif self.file.endswith('.csv'):
                df = pd.read_csv(self.file, encoding='GBK')  # 读取CSV文件
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
        
        endpoint = "https://api.mihomo.me/sr_info/"
        loop_limit = 70
        rest_time = 5
        counter = 0
        total_rows = len(df)
        
        for index, row in df.iterrows():
            if index < self.current_index:
                continue  # 跳过初始索引之前的行

            if self.interrupted:
                self.handle_interruption(index)
                return
            # 重置计数器，如果已经达到循环次数限制
            if counter >= loop_limit:
                self.handle_loop_limit(rest_time)
                counter = 0

            uid = str(row['uid']) # 获得uid
            url = endpoint + uid
            table_name = self.get_table_name()
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            try:
                self.process_request(index, url, headers, table_name, uid)
            except requests.exceptions.RequestException as e:
                self.handle_request_exception(e, uid)
            
            self.update_progress(index, total_rows) # 更新进度条
            counter += 1
            time.sleep(random.uniform(0.7, 0.8))
        
        self.finished_info.emit()

    def get_max_uid(self):
        max_uid_str = str(self.maxUid).lstrip('0')[1:]  # 去掉首位数字和开头的所有 '0'
        return int(max_uid_str) if max_uid_str else 0  # 转换回整数，如果字符串为空则设为 0
    
    def get_min_uid(self):
        server_min_uid = {
            'cn': 100000009,
            'b': 500000001,
            'ya': 800000002,
            'ou': 700000001,
            'mei': 600000006,
            'gat': 900000001
        }
        return server_min_uid.get(self.serverName, 100000009)

    def calculate_remaining_time(self, current_index, total_rows):
        elapsed_time = time.time() - self.start_time
        processed_rows = current_index - self.current_index + 1
        total_rows = total_rows - self.current_index
        if processed_rows == 0:
            return "计算中..."
        estimated_total_time = (elapsed_time / processed_rows) * total_rows
        remaining_time = estimated_total_time - elapsed_time
        return time.strftime("%H:%M:%S", time.gmtime(remaining_time))

    def determine_server_name(self, uid):
        if uid.startswith('1'):
            return 'cn'
        elif uid.startswith('5'):
            return 'b'
        elif uid.startswith('6'):
            return 'mei'
        elif uid.startswith('7'):
            return 'ou'
        elif uid.startswith('8'):
            return 'ya'
        elif uid.startswith('9'):
            return 'gat'
        return ""

    def get_table_name(self):
        # sr_user_info_20240715
        server_table_map = {
            'cn': 'sr_user_info_20240715', 'b': 'sr_user_info_b',
            'ya': 'sr_user_info_asia', 'ou': 'sr_user_info_europe',
            'mei': 'sr_user_info_america', 'gat': 'sr_user_info_cht'
        }
        return server_table_map.get(self.serverName, 'sr_user_info_default')
    
    def set_interrupted(self, interrupted):
        self.interrupted = interrupted
    
    def set_current_index(self, current_index):
        self.current_index = current_index