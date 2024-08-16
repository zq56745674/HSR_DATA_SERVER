import os
import qianfan
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('config/config.ini')

os.environ["QIANFAN_ACCESS_KEY"] = config['qianfan']['QIANFAN_ACCESS_KEY']
os.environ["QIANFAN_SECRET_KEY"] = config['qianfan']['QIANFAN_SECRET_KEY']

chat_comp = qianfan.ChatCompletion()

# 指定特定模型
resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
    "role": "user",
    "content": """你好"""
}])

print(resp["body"])