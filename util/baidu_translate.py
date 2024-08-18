import requests
import random
from hashlib import md5
import configparser
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaiDuFanyi:
    def __init__(self):
        self._load_config()
        self.url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        self.salt = random.randint(32768, 65536)
        self.header = {'Content-Type': 'application/x-www-form-urlencoded'}

    def _load_config(self):
        config = configparser.ConfigParser()
        try:
            config.read('config/config.ini')
            self.appid = config['baidufanyi']['BAIDU_APP_ID']
            self.secretKey = config['baidufanyi']['BAIDU_SECRET']
        except Exception as e:
            logging.error(f"Error reading config file: {e}")
            raise
    
    def BdTrans(self, text, fromLang='auto', toLang='zh'):
        sign = self.appid + text + str(self.salt) + self.secretKey
        md = md5()
        md.update(sign.encode(encoding='utf-8'))
        sign = md.hexdigest()
        data = {
            "appid": self.appid,
            "q": text,
            "from": fromLang,
            "to": toLang,
            "salt": self.salt,
            "sign": sign
        }
        try:
            response = requests.post(self.url, params=data, headers=self.header)
            response.raise_for_status()
            text = response.json()
            logging.info(text)
            results = text['trans_result'][0]['dst']
            return results
        except requests.RequestException as e:
            logging.error(f"Error during translation request: {e}")
            raise

def main():
    baidu_translate = BaiDuFanyi()
    results = baidu_translate.BdTrans("Invalid Sign")  # 要翻译的词组
    print(results)

if __name__ == '__main__':
    main()
