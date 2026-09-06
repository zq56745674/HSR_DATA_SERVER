import requests
import random
from hashlib import md5
import logging
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import config

logger = logging.getLogger(__name__)


class BaiDuFanyi:
    """Baidu Translation API client."""
    
    def __init__(self):
        self.appid = config.BAIDU_APP_ID
        self.secretKey = config.BAIDU_SECRET
        self.url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        self.salt = random.randint(32768, 65536)
        self.header = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        if not self.appid or not self.secretKey:
            logger.warning("Baidu translation credentials not configured")
    
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

def main():
    baidu_translate = BaiDuFanyi()
    results = baidu_translate.BdTrans("Invalid Sign")  # 要翻译的词组
    print(results)

if __name__ == '__main__':
    main()
