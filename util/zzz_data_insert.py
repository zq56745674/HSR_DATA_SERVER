import pandas as pd
from zipfile import BadZipFile
import pymysql
import logging
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def print_dict_differences(dict1: Dict, dict2: Dict) -> List[Dict]:
    """Compare two dictionaries and return differences."""
    result: List[Dict] = []
    before_info: Dict[str, Any] = {}
    after_info: Dict[str, Any] = {}
    for key in dict1:
        v1 = dict1[key]
        v2 = dict2[key]
        if v1 != v2:
            before_info[key] = v1
            after_info[key] = v2
    if before_info:
        result.append(before_info)
        result.append(after_info)
    else:
        logger.info('两个字典相同')
    return result


def read_file(file: str) -> pd.DataFrame:
    """Read Excel or CSV file into DataFrame."""
    try:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            return pd.read_excel(file, engine='openpyxl')
        elif file.endswith('.csv'):
            return pd.read_csv(file, encoding='GBK')
        else:
            raise Exception("文件格式不支持")
    except FileNotFoundError:
        raise FileNotFoundError("文件不存在")
    except ValueError as e:
        raise ValueError(str(e))
    except BadZipFile:
        raise BadZipFile("文件格式不正确")


def process_data(df: pd.DataFrame) -> List[Dict]:
    """Process DataFrame into list of user data dictionaries."""
    col1 = df.iloc[:, 1]
    nan_mask = col1.isna()
    if nan_mask.any():
        df = df.iloc[:nan_mask.to_numpy().argmax()]

    uids = df.iloc[:, 1].astype(int).tolist()
    last_logins = df.iloc[:, 2].tolist()
    levels = df.iloc[:, 3].tolist()

    result_list: List[Dict] = []
    for uid, last_login, level in zip(uids, last_logins, levels):
        data_dict: Dict[str, Any] = {'uid': int(uid), 'last_login': last_login}
        if not pd.isna(level):
            data_dict['level'] = int(level)
        result_list.append(data_dict)
    return result_list


def execute_zzz_file(file: str, formatted_date: str) -> None:
    """Process ZZZ data file and insert/update database records.
    
    Args:
        file: Path to data file
        formatted_date: Date in YYYY-MM-DD format
    """
    from config import config
    
    df = read_file(file)
    data_list = process_data(df)

    qry_sql = "SELECT * FROM `zzz_user_info` WHERE uid = %s"
    insert_record_sql = (
        "INSERT INTO `zzz_user_info_upd_record` "
        "(`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) "
        "VALUES (%s, NOW(), %s, %s, NOW())"
    )
    
    db = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
    
    try:
        cursor = db.cursor()
        for item in data_list:
            logger.info(f"Processing item: {item}")
            uid = item['uid']
            
            with cursor:
                cursor.execute(qry_sql, (uid,))
                exist = cursor.fetchone()
                
                if exist:
                    dict1 = {'level': exist[5], 'last_login_date': exist[6]}
                    dict2 = {'level': item['level'], 'last_login_date': item['last_login']}
                    result = print_dict_differences(dict1, dict2)
                    
                    if result:
                        update_sql = (
                            "UPDATE `zzz_user_info` SET `level` = %s, `last_login_date` = %s, "
                            "`DATA_DATE` = %s, `LAST_UPDATE_TIME` = NOW() WHERE `UID` = %s"
                        )
                        cursor.execute(update_sql, (
                            item['level'], item['last_login'], formatted_date, uid
                        ))
                        cursor.execute(insert_record_sql, (uid, str(result[0]), str(result[1])))
                else:
                    insert_sql = (
                        "INSERT INTO `zzz_user_info` "
                        "(`UID`, `level`, `last_login_date`, `DATA_DATE`, `CREATE_TIME`) "
                        "VALUES (%s, %s, %s, %s, NOW())"
                    )
                    cursor.execute(insert_sql, (
                        item['uid'], item['level'], item['last_login'], formatted_date
                    ))
                db.commit()
    except pymysql.Error as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    file = 'E:/ZZZ/7月11.xlsx'
    filename = os.path.basename(file)

    pattern = re.compile(r'(\d+)月(\d+)')
    match = pattern.search(filename)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        year = datetime.now().year
        date = datetime(year, month, day)
        formatted_date = date.strftime('%Y-%m-%d')
        execute_zzz_file(file, formatted_date)
    else:
        logger.warning("未找到日期")