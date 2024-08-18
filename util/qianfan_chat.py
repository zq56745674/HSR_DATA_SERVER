import os
import qianfan
import configparser
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QianFanChat:
    def __init__(self):
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read('config/config.ini')

        os.environ["QIANFAN_ACCESS_KEY"] = config['qianfan']['QIANFAN_ACCESS_KEY']
        os.environ["QIANFAN_SECRET_KEY"] = config['qianfan']['QIANFAN_SECRET_KEY']

        self.chat_comp = qianfan.ChatCompletion()

    def chat(self, message):
        # 指定特定模型
        resp = self.chat_comp.do(model="ERNIE-Speed-128K", messages=[{
            "role": "user",
            "content": message
        }])
        logging.info(resp["body"])
        return resp["body"]['result']
    
if __name__=='__main__':
    chat_test = QianFanChat()
    Results = chat_test.chat("你好") #要翻译的词组
    print(Results)