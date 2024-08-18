from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QIntValidator
from HSRMain_ui import Ui_MainWindow
import requests
import pandas as pd
import random
import time
import logging
import pymysql
import os
from zipfile import BadZipFile
from contextlib import contextmanager
from util import baidu_translate
from util import qianfan_chat
import ZZZDataExe

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        # 菜单栏
        self.bind_actions([
            (self.actionLogin, self.show_login),
            (self.actionExit, self.close),
            (self.actionAqua, lambda: self.toggle_theme('Aqua')),
            (self.actionMacOS, lambda: self.toggle_theme('MacOS')),
            (self.actionNeonButtons, lambda: self.toggle_theme('NeonButtons')),
            (self.actionUbuntu, lambda: self.toggle_theme('Ubuntu'))
        ])
        # tab1按钮
        self.bind_buttons([
            (self.fileButton, lambda: self.upload_file(1)),
            (self.fileExeButton, self.execute_file),
            (self.randomUidButton, self.random_uid),
            (self.interruptButton, self.interrupt_func),
            (self.continueButton, self.continue_func)
        ])
        # tab2按钮
        self.bind_buttons([
            (self.fileButton_2, lambda: self.upload_file(2)),
            (self.fileZZZExeButton, self.execute_zzz_file)
        ])
        # tab3按钮
        self.bind_buttons([
            (self.translateButton, self.translate_text),
            (self.sendAIButton, self.send_ai_text)
        ])
        # 单选按钮
        self.bind_radio_buttons([
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
    
    def send_ai_text(self):
        text = self.fromTextEdit_2.toPlainText()
        self.start_thread(apprType="4", fromText=text)
    
    def translate_text(self):
        text = self.fromTextEdit.toPlainText()
        fromLang_str = self.fromComboBox.currentText()
        toLang_str = self.toComboBox.currentText()
        fromLang = self.get_lang_code(fromLang_str)
        toLang = self.get_lang_code(toLang_str)
        self.start_thread(apprType="3", fromText=text, fromLang=fromLang, toLang=toLang)
    
    def get_lang_code(self, lang_str):
        lang_dict = {
            "自动检测": "auto",
            "中文": "zh",
            "英语": "en",
            "日语": "jp",
            "韩语": "kor",
            "法语": "fra",
            "西班牙语": "spa",
            "泰语": "th",
            "阿拉伯语": "ara",
            "俄语": "ru",
            "葡萄牙语": "pt",
            "德语": "de",
            "意大利语": "it",
            "希腊语": "el",
            "荷兰语": "nl",
            "波兰语": "pl",
            "保加利亚语": "bul",
            "爱沙尼亚语": "est",
            "丹麦语": "dan",
            "芬兰语": "fin",
            "捷克语": "cs",
            "罗马尼亚语": "rom",
            "斯洛文尼亚语": "slo",
            "瑞典语": "swe",
            "匈牙利语": "hu",
            "繁体中文": "cht",
            "越南语": "vie"
        }
        return lang_dict.get(lang_str, "auto")

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
        self.interrupted = True  # 设置标志变量为 True
        if hasattr(self, 'thread') and self.thread.isRunning():
            self.thread.set_interrupted(True)  # 调用线程的中断方法
        # 将按钮设置为不可用
        self.set_buttons_enabled(True)
    
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
            ZZZDataExe.execute_zzz_file(file)
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
        qry_sql = "select uid from sr_max_uid"
        with self.get_cursor(db) as cursor:
            cursor.execute(qry_sql)
            result = cursor.fetchall()
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
        # 打开文件选择对话框，并限制文件后缀为 .xlsx, .xls 和 .csv
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", default_path, "表格文件 (*.xlsx *.xls *.csv);;所有文件 (*)")
        if tab == 1:
            self.fileLabel.setText(file_path if file_path else "未选择文件")
        elif tab == 2:
            self.fileLabel_2.setText(file_path if file_path else "未选择文件")
    
    @contextmanager
    def get_cursor(self, db):
        cursor = db.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

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
        # 从上一个页面传递过来的数据库连接
        if self.db:
            self.db.close()
            logging.info("数据库连接已关闭")
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
            self.fileExeButton,
            self.randomUidButton,
            self.continueButton
        ]
        
        # QLineEdit 列表
        line_edits = [
            self.minUidEdit_cn, self.maxUidEdit_cn,
            self.minUidEdit_b, self.maxUidEdit_b,
            self.minUidEdit_ya, self.maxUidEdit_ya,
            self.minUidEdit_ou, self.maxUidEdit_ou,
            self.minUidEdit_mei, self.maxUidEdit_mei,
            self.minUidEdit_gat, self.maxUidEdit_gat
        ]
        
        # 设置按钮的启用状态
        for button in buttons:
            button.setEnabled(enabled)
        
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
        text = self.fromText
        if not text:
            return
        try:
            aiChatUtil = qianfan_chat.QianFanChat()
            result = aiChatUtil.chat(text)
            self.info_view.emit(result, "toTextBrowser_2")
        except Exception as e:
            self.error_occurred.emit(f"send_ai_text error: {str(e)}", 0)

    def translate_text(self):
        text = self.fromText
        if not text:
            return
        try:
            translateUtil = baidu_translate.BaiDuFanyi()
            result = translateUtil.BdTrans(text, self.fromLang, self.toLang)
            self.info_view.emit(result, "toTextBrowser")
        except Exception as e:
            self.error_occurred.emit(f"translate_text error: {str(e)}", 0)
        
    def random_uid(self):
        not_found_count = 0
        self.start_time = time.time()
        endpoint = "https://api.mihomo.me/sr_info/"
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        ]
        selected_user_agent = user_agents[0]
        loop_limit = 70
        rest_time = 5
        counter = 0
        i = 0
        maxLen = int(self.maxLen)
        max_uid = max_uid = self.get_max_uid() if self.maxEditUid == 0 else self.maxEditUid
        min_uid = self.get_min_uid()

        # print(f"self.maxEditUid: {self.maxEditUid}, self.minEditUid: {self.minEditUid}, max_uid: {max_uid}, min_uid: {min_uid}")

        for i in range(1, maxLen):
            if self.interrupted:
                logging.info("处理文件被中断")
                self.error_occurred.emit("处理文件被中断", i)
                return
            
            # 重置计数器，如果已经达到循环次数限制
            if counter >= loop_limit:
                logging.info(f"已达到循环次数限制，休息 {rest_time} 秒....................................")
                self.info_view.emit(f" 已达到循环次数限制，休息 {rest_time} 秒....................................", 'infoBrowser')
                counter = 0  # 重置计数器
                time.sleep(rest_time)  # 休息rest_time秒
                
            randomNum = random.randint(self.minEditUid, max_uid) + min_uid
            uid = str(randomNum)
            url = endpoint + uid
            
            table_name = self.get_table_name()

            qry_sql = "select `UID`, `signature`, `platform`, `nickname`, `level`, `friend_count`, `max_rogue_challenge_score`, `achievement_count`, `equipment_count`, `avatar_count`, `head_icon`, `relic_count`, `book_count`, `music_count` from " + table_name + " where uid = %s"
            insert_sql = "INSERT INTO " + table_name + " (UID, signature, platform, nickname, `level`, friend_count, max_rogue_challenge_score, achievement_count, equipment_count, avatar_count, head_icon, CREATE_TIME, remark, relic_count, book_count, music_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s, %s, %s)"    
            update_sql = "UPDATE " + table_name + " SET UID=%s, signature=%s, platform=%s, nickname=%s, `level`=%s, friend_count=%s, max_rogue_challenge_score=%s, achievement_count=%s, equipment_count=%s, avatar_count=%s, head_icon=%s, remark=%s, relic_count=%s, book_count=%s, music_count=%s, LAST_UPDATE_TIME=now() WHERE UID=%s"
            insert_record_sql = "INSERT INTO `sr_user_info_upd_record` (`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) VALUES (%s, now(), %s, %s, now())"
            
            # 发送GET请求
            headers = {"User-Agent": selected_user_agent}
            try:
                logging.info(f"i {i} url: {url}")
                self.info_view.emit(f" i {i} url: {url}", 'infoBrowser')
                response = requests.get(url, headers=headers, timeout=5)  # 设置请求超时时间
                if response.status_code == 200:
                    # 将JSON数据保存到文件
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
                    relicCount = record_info.get("relicCount") # 仪器数量
                    headIcon = detail_info.get("headIcon")
                    remark = self.generate_remark(assist_avatar_list, avatar_detail_list)

                    with self.get_cursor(self.db) as cursor:
                        cursor.execute(qry_sql, (uid,))
                        exist = cursor.fetchone()
                        if exist:
                            dict1 = self.create_dict_from_db(exist)
                            dict2 = self.create_dict_from_response(platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, relicCount, bookCount, musicCount)
                            result = self.print_dict_differences(dict1, dict2)
                            if result:
                                cursor.execute(update_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, uid))
                                cursor.execute(insert_record_sql, (uid, str(result[0]), str(result[1])))
                        else:
                            cursor.execute(insert_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount))
                        self.db.commit()
                elif response.status_code == 404:
                    not_found_count += 1
                    logging.info(f"请求失败，状态码：{response.status_code}，404计数：{not_found_count}")
                    self.info_view.emit(f" 请求失败，状态码：{response.status_code}，404计数：{not_found_count}", 'infoBrowser')
                    self.log_request_failure(uid, response.status_code, table_name)
                else:
                    # 请求失败，打印错误信息
                    logging.error(f"Error: {response.status_code} for uid: {uid}")
                    self.info_view.emit(f" Error: {response.status_code} for uid: {uid}", 'infoBrowser')
                    self.log_request_failure(uid, response.status_code, None, response.text)
            except requests.exceptions.RequestException as e:
                # 请求异常，打印错误信息
                logging.error(f"请求出错：{e} for uid: {uid}")
                self.info_view.emit(f" 请求出错：{e} for uid: {uid}", 'infoBrowser')
                self.log_request_failure(uid, 500, None, str(e))
            
            # 更新进度条
            progress = int((i) / maxLen * 100)
            progress_info = f"{i}/{maxLen}"
            # 计算并发送剩余时间
            remaining_time = self.calculate_remaining_time(i, maxLen)
            self.progress_updated.emit(progress, progress_info, remaining_time)

            counter += 1
            # 随机延迟
            random_delay = random.uniform(0.7, 0.8)
            time.sleep(random_delay)

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
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        ]
        selected_user_agent = user_agents[0]
        # 设置循环次数和休息时间
        loop_limit = 70
        rest_time = 5  # 休息时间，单位为秒
        # 计数器
        counter = 0
        total_rows = len(df)
        
        for index, row in df.iterrows():
            if index < self.current_index:
                continue  # 跳过初始索引之前的行

            if self.interrupted:
                logging.info("处理文件被中断")
                self.error_occurred.emit("处理文件被中断", index)
                return
            # 重置计数器，如果已经达到循环次数限制
            if counter >= loop_limit:
                logging.info(f"已达到循环次数限制，休息 {rest_time} 秒....................................")
                self.info_view.emit(f" 已达到循环次数限制，休息 {rest_time} 秒....................................", 'infoBrowser')
                counter = 0  # 重置计数器
                time.sleep(rest_time)  # 休息10秒

            # 增加计数器
            counter += 1

            # 获得uid
            uid = str(row['uid'])  # 假设'uid'是Excel文件第一列的列名
            url = f"{endpoint}{uid}"
            table_name = self.get_table_name()
            
            qry_sql = "select `UID`, `signature`, `platform`, `nickname`, `level`, `friend_count`, `max_rogue_challenge_score`, `achievement_count`, `equipment_count`, `avatar_count`, `head_icon`, `relic_count`, `book_count`, `music_count` from " + table_name + " where uid = %s"
            insert_sql = "INSERT INTO " + table_name + " (UID, signature, platform, nickname, `level`, friend_count, max_rogue_challenge_score, achievement_count, equipment_count, avatar_count, head_icon, CREATE_TIME, remark, relic_count, book_count, music_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s, %s, %s)"    
            update_sql = "UPDATE " + table_name + " SET UID=%s, signature=%s, platform=%s, nickname=%s, `level`=%s, friend_count=%s, max_rogue_challenge_score=%s, achievement_count=%s, equipment_count=%s, avatar_count=%s, head_icon=%s, remark=%s, relic_count=%s, book_count=%s, music_count=%s, LAST_UPDATE_TIME=now() WHERE UID=%s"
            insert_record_sql = "INSERT INTO `sr_user_info_upd_record` (`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) VALUES (%s, now(), %s, %s, now())"
            fail_sql = "INSERT INTO sr_user_info_fail_record (`UID`, `FAIL_CODE`, `FAIL_DESC`, `CREATE_TIME`) VALUES (%s, %s, %s, now())"
            
            # 发送GET请求
            headers = {"User-Agent": selected_user_agent}
            try:
                logging.info(f"i {index} url: {url}")
                self.info_view.emit(f" i {index} url: {url}", 'infoBrowser')
                response = requests.get(url, headers=headers, timeout=5)  # 设置请求超时时间
                if response.status_code == 200:
                    # 将JSON数据保存到文件
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
                    relicCount = record_info.get("relicCount") # 仪器数量
                    headIcon = detail_info.get("headIcon")
                    remark = self.generate_remark(assist_avatar_list, avatar_detail_list)

                    with self.get_cursor(self.db) as cursor:
                        cursor.execute(qry_sql, (uid,))
                        exist = cursor.fetchone()
                        if exist:
                            dict1 = self.create_dict_from_db(exist)
                            dict2 = self.create_dict_from_response(platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, relicCount, bookCount, musicCount)
                            result = self.print_dict_differences(dict1, dict2)
                            if result:
                                cursor.execute(update_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount, uid))
                                cursor.execute(insert_record_sql, (uid, str(result[0]), str(result[1])))
                        else:
                            cursor.execute(insert_sql, (uid, signature, platform, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, remark, relicCount, bookCount, musicCount))
                        self.db.commit()
                    
                else:
                    # 请求失败，打印错误信息
                    logging.error(f"Error: {response.status_code} for uid: {uid}")
                    self.info_view.emit(f" Error: {response.status_code} for uid: {uid}", 'infoBrowser')
                    with self.get_cursor(self.db) as cursor:
                        cursor.execute(fail_sql, (uid, response.status_code, response.reason))
                        self.db.commit()
            except requests.exceptions.RequestException as e:
                # 请求异常，打印错误信息
                logging.error(f"请求出错：{e} for uid: {uid}")
                self.info_view.emit(f" 请求出错：{e} for uid: {uid}", 'infoBrowser')
                with self.get_cursor(self.db) as cursor:
                    cursor.execute(fail_sql, (uid, 500, str(e)))
                    self.db.commit()
            
            # 更新进度条
            progress = int((index + 1) / total_rows * 100)
            progress_info = f"{index + 1}/{total_rows}"
            # 计算并发送剩余时间
            remaining_time = self.calculate_remaining_time(index, total_rows)
            self.progress_updated.emit(progress, progress_info, remaining_time)

            # 随机延迟
            random_delay = random.uniform(0.7, 0.8)
            time.sleep(random_delay)
        
        self.finished_info.emit()

    def get_max_uid(self):
        max_uid_str = str(self.maxUid)  # 将 self.maxUid 转换为字符串
        if len(max_uid_str) > 1:
            max_uid_str = max_uid_str[1:]  # 截掉首位数字
        max_uid_str = max_uid_str.lstrip('0')  # 去掉开头的所有 '0'
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
    
    def log_request_failure(self, uid, status_code, table_name, error_desc=None):
        try:
            with self.get_cursor(self.db) as cursor:
                if error_desc:
                    fail_sql = "INSERT INTO sr_user_info_fail_record (`UID`, `FAIL_CODE`, `FAIL_DESC`, `CREATE_TIME`) VALUES (%s, %s, %s, now())"
                    cursor.execute(fail_sql, (uid, status_code, error_desc))
                else:
                    insert_sql = "INSERT INTO " + table_name + " (UID, CREATE_TIME, remark) VALUES (%s, now(), %s)"
                    cursor.execute(insert_sql, (uid, status_code))
                self.db.commit()
        except pymysql.MySQLError as e:
            print(f"数据库操作失败：{e}")
        except Exception as e:
            print(f"发生未知错误：{e}")

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
        server_table_map = {
            'cn': 'sr_user_info',
            'b': 'sr_user_info_b',
            'ya': 'sr_user_info_asia',
            'ou': 'sr_user_info_europe',
            'mei': 'sr_user_info_america',
            'gat': 'sr_user_info_cht'
        }
        return server_table_map.get(self.serverName, 'sr_user_info_default')
    
    # 打印两个字典的不同
    def print_dict_differences(self, dict1, dict2):
        result = []
        before_info = {}
        after_info = {}
        for key in dict1:
            v1 = dict1[key]
            v2 = dict2[key]
            if key == 'platform':
                v2 = str(dict2[key])
            if v1 != v2:
                before_info[key] = v1
                after_info[key] = v2
        if before_info:
            result.append(before_info)
            result.append(after_info)
        else:
            logging.info('两个字典相同')
            self.info_view.emit(' 两个字典相同', 'infoBrowser')
        return result

    def generate_remark(self, assist_avatar_list, avatar_detail_list):
        remark = ""
        avatarIdList = [8005, 8006, 1315, 1314, 1312, 1310, 1309, 1308, 1307, 1306, 1305, 1304, 1303, 1302, 1301, 1224, 1221, 1218]
        if assist_avatar_list:
            for avatar in assist_avatar_list:
                if avatar.get('avatarId') and avatar.get('avatarId') in avatarIdList:
                    remark += f"{avatar.get('avatarId')}|{avatar.get('rank') or 0}|{avatar.get('equipment').get('tid') if avatar.get('equipment') else ''}#"
        if avatar_detail_list:
            for avatar in avatar_detail_list:
                if avatar.get('avatarId') and str(avatar.get('avatarId')) not in remark and avatar.get('avatarId') in avatarIdList:
                    remark += f"{avatar.get('avatarId')}|{avatar.get('rank') or 0}|{avatar.get('equipment').get('tid') if avatar.get('equipment') else ''}#"
        return remark

    def create_dict_from_db(self, exist):
        return {
            'platform': exist[2], 'signature': exist[1], 'nickname': exist[3], 'level': exist[4],
            'friendCount': exist[5], 'maxRogueChallengeScore': exist[6], 'achievementCount': exist[7],
            'equipmentCount': exist[8], 'avatarCount': exist[9], 'headIcon': exist[10], 'relicCount': exist[11],
            'bookCount': exist[12], 'musicCount': exist[13]
        }

    def create_dict_from_response(self, platform, signature, nickname, level, friendCount, maxRogueChallengeScore, achievementCount, equipmentCount, avatarCount, headIcon, relicCount, bookCount, musicCount):
        return {
            'platform': platform, 'signature': signature, 'nickname': nickname, 'level': level,
            'friendCount': friendCount, 'maxRogueChallengeScore': maxRogueChallengeScore, 'achievementCount': achievementCount,
            'equipmentCount': equipmentCount, 'avatarCount': avatarCount, 'headIcon': headIcon, 'relicCount': relicCount, 
            'bookCount': bookCount, 'musicCount': musicCount
        }
    
    @contextmanager
    def get_cursor(self, db):
        cursor = db.cursor()
        try:
            yield cursor
        finally:
            cursor.close()
    
    def set_interrupted(self, interrupted):
        self.interrupted = interrupted
    
    def set_current_index(self, current_index):
        self.current_index = current_index