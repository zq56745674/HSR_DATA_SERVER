import re
import pandas as pd
from zipfile import BadZipFile

# 匹配最后登录字符串
def match_last_login(str):
    if '在线' in str:
        return '在线'
    else: 
        pattern = re.compile(r"最后登录：(\d+天前)")
        pattern1 = re.compile(r"最后登录：(今日内|今白内)")
        result = pattern.search(str)
        result1 = pattern1.search(str)
        if result:
            return result.group(1)
        elif result1:
            return '今日内'
        else:
            return None
    
def extract_uid(str):
    pattern = re.compile(r"-(\d+)")
    match = pattern.search(str)
    if match:
        return int(match.group(1))
    return None

def extract_level(str):
    # 去掉换行符
    level_str = str.replace('\n', '')

    return int(level_str)

def execute_zzz_file(file):
    try:
        if file.endswith('.xlsx') or file.endswith('.xls'):
            df = pd.read_excel(file, engine='openpyxl')  # 读取Excel文件
        elif file.endswith('.csv'):
            df = pd.read_csv(file, encoding='GBK')  # 读取CSV文件
        else:
            raise Exception("文件格式不支持")
    except FileNotFoundError:
        raise FileNotFoundError("文件不存在")
    except ValueError as e:
        raise ValueError(str(e))
    except BadZipFile:
        raise BadZipFile("文件格式不正确")
    
    # 初始化列表和辅助字典
    list1 = []
    list2 = []
    uid_dict = {}

    for index, row in df.iterrows():
        columns_name = str(row['Name'])
        uid = extract_uid(columns_name)
        if '等级' not in columns_name:
            last_login = match_last_login(row['OCR'])
            data_dict = {'uid': uid, 'last_login': last_login}
            list1.append(data_dict)
            uid_dict[uid] = data_dict  # 将字典存入辅助字典
        else:
            level = extract_level(row['OCR'])
            if uid in uid_dict:
                uid_dict[uid]['level'] = level  # 更新已有字典中的level
            else:
                data_dict = {'uid': uid, 'level': level}
                list2.append(data_dict)

    # 如果需要将list2中的数据合并到list1中，可以执行以下操作
    for item in list2:
        uid = item['uid']
        if uid in uid_dict:
            uid_dict[uid]['level'] = item['level']
        else:
            list1.append(item)
    
    # 将list1转换为DataFrame
    df1 = pd.DataFrame(list1)
    # 将DataFrame写入Excel文件
    df1.to_excel(file.replace('.csv', '_output.xlsx'), index=False)
    

if __name__ == "__main__":
    execute_zzz_file("D:\\ZZZ截图\\[OCR]_2024-08-17_20240817_1801.csv")