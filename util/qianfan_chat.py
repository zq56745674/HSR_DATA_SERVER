import os
import qianfan
import configparser
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QianFanChat:
    def __init__(self):
        self._load_config()
        self.chat_comp = qianfan.ChatCompletion()

    def _load_config(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')
            os.environ["QIANFAN_ACCESS_KEY"] = config['qianfan']['QIANFAN_ACCESS_KEY']
            os.environ["QIANFAN_SECRET_KEY"] = config['qianfan']['QIANFAN_SECRET_KEY']
        except Exception as e:
            logging.error(f"Error reading config file: {e}")
            raise

    def chat(self, message):
        try:
            resp = self.chat_comp.do(model="ERNIE-Speed-128K", messages=[{
                "role": "user",
                "content": message
            }])
            logging.info(f"Response: {resp['body']}")
            return resp["body"]['result']
        except Exception as e:
            logging.error(f"Error during chat: {e}")
            raise
    
def main():
    chat_test = QianFanChat()
    results = chat_test.chat("你好")  # 要翻译的词组
    print(results)

if __name__ == '__main__':
    main()