import requests
import random
from hashlib import md5
import configparser

class BaiDuFanyi:
    def __init__(self):
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read('config/config.ini')

        appKey = config['baidufanyi']['BAIDU_APP_ID'] #你在第一步申请的APP ID
        appSecret = config['baidufanyi']['BAIDU_SECRET'] #公钥

        self.url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
        self.appid = appKey
        self.secretKey = appSecret
        self.fromLang = 'auto'
        self.toLang = 'zh'
        self.salt = random.randint(32768,65536)
        self.header = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    def BdTrans(self,text):
        sign = self.appid + text + str(self.salt) + self.secretKey
        md = md5()
        md.update(sign.encode(encoding='utf-8'))
        sign =md.hexdigest()
        data = {
            "appid": self.appid,
            "q": text,
            "from": self.fromLang,
            "to": self.toLang,
            "salt": self.salt,
            "sign": sign
        }
        response = requests.post(self.url, params= data, headers= self.header)  # 发送post请求
        text = response.json()  # 返回的为json格式用json接收数据
        print(text)
        results = text['trans_result'][0]['dst']
        return results

if __name__=='__main__':
    BaiduTranslate_test = BaiDuFanyi()
    Results = BaiduTranslate_test.BdTrans("Invalid Sign") #要翻译的词组
    print(Results)
