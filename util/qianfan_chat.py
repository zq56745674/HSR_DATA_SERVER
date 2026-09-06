import os
import qianfan
import logging
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import config

logger = logging.getLogger(__name__)


class QianFanChat:
    """Baidu Qianfan AI chat client."""
    
    def __init__(self):
        # Set environment variables for qianfan SDK
        os.environ["QIANFAN_ACCESS_KEY"] = config.QIANFAN_ACCESS_KEY
        os.environ["QIANFAN_SECRET_KEY"] = config.QIANFAN_SECRET_KEY
        
        if not config.QIANFAN_ACCESS_KEY or not config.QIANFAN_SECRET_KEY:
            logger.warning("Qianfan credentials not configured")
        
        self.chat_comp = qianfan.ChatCompletion()

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