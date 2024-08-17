import re
import pandas as pd
from zipfile import BadZipFile

# 匹配最后登录字符串
def match_last_login(text):
    if '在线' in text:
        return '在线'
    pattern = re.compile(r"最后登录：(\d+天前)")
    pattern1 = re.compile(r"最后登录：(今日内|今白内)")
    result = pattern.search(text)
    result1 = pattern1.search(text)
    if result:
        return result.group(1)
    elif result1:
        return '今日内'
    return None
    
def extract_uid(str):
    pattern = re.compile(r"-(\d+)")
    match = pattern.search(str)
    if match:
        return int(match.group(1))
    return None

def extract_level(str):
    level_str = str.replace('\n', '')
    if 'c' in level_str:
        level_str = level_str.replace('c', '9')
    elif 'C' in level_str:
        level_str = level_str.replace('C', '0')

    return int(level_str)

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
    list1 = []
    list2 = []
    uid_dict = {}

    for _, row in df.iterrows():
        name = str(row['Name'])
        uid = extract_uid(name)
        if '问题账号' in name:
            continue
        elif '等级' not in name:
            last_login = match_last_login(row['OCR'])
            data_dict = {'uid': uid, 'last_login': last_login}
            list1.append(data_dict)
            uid_dict[uid] = data_dict
        else:
            level = extract_level(row['OCR'])
            if uid in uid_dict:
                uid_dict[uid]['level'] = level
            else:
                data_dict = {'uid': uid, 'level': level}
                list2.append(data_dict)

    for item in list2:
        uid = item['uid']
        if uid in uid_dict:
            uid_dict[uid]['level'] = item['level']
        else:
            list1.append(item)

    return pd.DataFrame(list1)

def execute_zzz_file(file):
    df = read_file(file)
    df1 = process_data(df)
    df1.to_excel(file.replace('.csv', '_output.xlsx'), index=False) 


if __name__ == "__main__":
    execute_zzz_file("D:\\ZZZPIC\\[OCR]_2024-08-17_20240817_2327.csv")