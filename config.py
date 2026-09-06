import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load .env file from project root
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

logger = logging.getLogger(__name__)


class Config:
    """Application configuration manager."""
    
    # Baidu Qianfan (AI)
    QIANFAN_ACCESS_KEY: str = os.getenv('QIANFAN_ACCESS_KEY', '')
    QIANFAN_SECRET_KEY: str = os.getenv('QIANFAN_SECRET_KEY', '')
    
    # Baidu Translation
    BAIDU_APP_ID: str = os.getenv('BAIDU_APP_ID', '')
    BAIDU_SECRET: str = os.getenv('BAIDU_SECRET', '')
    
    # Database (optional, can be set in login UI)
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_USER: str = os.getenv('DB_USER', 'root')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_NAME: str = os.getenv('DB_NAME', 'hsr_data')
    
    # API endpoints
    HSR_API_ENDPOINT: str = 'https://api.mihomo.me/sr_info/'
    GENSHIN_API_ENDPOINT: str = 'https://enka.network/api/'
    
    # Rate limiting
    LOOP_LIMIT: int = 70
    REST_TIME_SECONDS: int = 2
    REQUEST_DELAY_MIN: float = 0.7
    REQUEST_DELAY_MAX: float = 0.8
    MAX_WORKERS: int = int(os.getenv('MAX_WORKERS', '3'))
    COMMIT_BATCH_SIZE: int = int(os.getenv('COMMIT_BATCH_SIZE', '10'))
    PROGRESS_EMIT_INTERVAL: float = 0.1
    LOG_EMIT_INTERVAL: float = 0.2
    RETRY_TOTAL: int = int(os.getenv('RETRY_TOTAL', '3'))
    RETRY_BACKOFF_FACTOR: float = float(os.getenv('RETRY_BACKOFF_FACTOR', '2.0'))
    
    # Server mappings
    SERVER_TABLE_MAP: dict = {
        'cn': 'sr_user_info',
        'b': 'sr_user_info_b',
        'ya': 'sr_user_info_asia',
        'ou': 'sr_user_info_europe',
        'mei': 'sr_user_info_america',
        'gat': 'sr_user_info_cht'
    }
    
    SERVER_MIN_UID: dict = {
        'cn': 100000009,
        'b': 500000001,
        'ya': 800000002,
        'ou': 700000001,
        'mei': 600000006,
        'gat': 900000001
    }
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        missing = []
        if not cls.QIANFAN_ACCESS_KEY:
            missing.append('QIANFAN_ACCESS_KEY')
        if not cls.QIANFAN_SECRET_KEY:
            missing.append('QIANFAN_SECRET_KEY')
        if not cls.BAIDU_APP_ID:
            missing.append('BAIDU_APP_ID')
        if not cls.BAIDU_SECRET:
            missing.append('BAIDU_SECRET')
        
        if missing:
            logger.warning(f"Missing configuration: {', '.join(missing)}")
            return False
        return True


# Singleton instance
config = Config()