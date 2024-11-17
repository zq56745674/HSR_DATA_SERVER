import pandas as pd
from zipfile import BadZipFile
import pymysql
import logging
import os
import re
from datetime import datetime

def print_dict_differences(dict1, dict2):
    result = []
    before_info = {}
    after_info = {}
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
        print('两个字典相同')
    return result

def read_file(file):
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

def process_data(df):
    # 初始化列表和辅助字典
    result_list = []
    for _, row in df.iterrows():
        if pd.isna(row[0]):
            break
        # 初始化字典
        data_dict = {}
        # row[0] 不为 NaN 时，转为 int
        if not pd.isna(row[0]):
            data_dict['uid'] = int(row[0])
        data_dict['last_login'] = row[1]
        if not pd.isna(row[3]):
            data_dict['level'] = int(row[3])
        result_list.append(data_dict)
    return result_list

def get_database_connection(dbhost, dbuser, dbpass, dbname):
    try:
        if not dbpass:
            db = pymysql.connect(host=dbhost, user=dbuser, database=dbname)
        else:
            db = pymysql.connect(host=dbhost, user=dbuser, password=dbpass, database=dbname)
        logging.info("数据库连接成功")
        return db
    except pymysql.Error as e:
        logging.error("数据库连接失败：" + str(e))
        return None

def execute_zzz_file(file, formatted_date):
    df = read_file(file)
    list = process_data(df)

    qry_sql = "SELECT * FROM `zzz_user_info` WHERE uid = %s"
    insert_record_sql = "INSERT INTO `sr_user_info_upd_record` (`UID`, `UPDATE_DATE`, `before_info`, `after_info`, `CREATE_TIME`) VALUES (%s, now(), %s, %s, now())"
    # 插入数据库
    db = get_database_connection('rm-uf6n58p87aw72940u3o.mysql.rds.aliyuncs.com', 'zzm', 'Zq56745674', 'my_data')
    cursor = db.cursor()
    for item in list:
        print(item)
        insert_sql = f"INSERT INTO `zzz_user_info` (`UID`, `level`, `last_login_date`, `DATA_DATE`, `CREATE_TIME`) VALUES ({item['uid']}, {item['level']}, '{item['last_login']}', '{formatted_date}', now());"
        update_sql = f"UPDATE `zzz_user_info` SET `level` = {item['level']}, `last_login_date` = '{item['last_login']}', `DATA_DATE` = '{formatted_date}', `UPDATE_TIME` = now() WHERE `UID` = {item['uid']};"
    
        cursor.execute(qry_sql, ({item['uid']}))
        exist = cursor.fetchone()
        if exist:
            dict1 = {'level': exist[5], 'last_login_date': exist[6]}
            dict2 = {'level': item['level'], 'last_login_date': item['last_login']}
            result = print_dict_differences(dict1, dict2)
            if result:
                cursor.execute(update_sql)
                cursor.execute(insert_record_sql, ({item['uid']}, str(result[0]), str(result[1])))
        else:
            cursor.execute(insert_sql)
    db.commit()
    db.close()
    
if __name__ == "__main__":
    file = 'D:/ZZZPIC/存档/7月20.xlsx'
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
        print("未找到日期")