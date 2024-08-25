import re
import pandas as pd
from zipfile import BadZipFile
import os
import time
import shutil
import pytesseract
import cv2
from PIL import Image

# 匹配最后登录字符串
def match_last_login(text):
    if '在线' in text:
        return '在线'
    pattern = re.compile(r"(\d+天前|\d+天)")
    pattern1 = re.compile(r"(今日内|今白内|令日内|令今日内|今日|含日内|)")
    result = pattern.search(text)
    result1 = pattern1.search(text)
    if result:
        # 如果不是“前”结尾，在后面加上“前”
        if '前' not in result.group(1):
            return result.group(1) + '前'
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

def extract_level(level):
    if level is None or level == '':
        return None
    level_str = str(level).replace('\n', '').replace('＇', '')

    # 特殊情况替换
    replacements = {
        'AC': '10',
        '92': '22',
        'o': '0',
        'c': '9',
        'C': '0',
        's': '9',
        'S': '9',
        'g': '9',
        '℃': '9'
    }

    for key, value in replacements.items():
        level_str = level_str.replace(key, value)

    # 如果大于两位数，只取前两位
    if len(level_str) > 2:
        level_str = level_str[:2]
    # 如果level_str不是数字，返回None
    if not level_str.isdigit():
        return None
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

def copy_file(uid_with_empty_level):
    # 生成当前日期yyyy-mm-dd
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    src_dir = f'D:\\ZZZPIC\\{date}\\'
    dst_dir = f'D:\\ZZZPIC\\LEVELINFO\\'
    filename_list = [f'{uid}.bmp' for uid in uid_with_empty_level]

    # 循环读取文件夹下的所有文件
    for root, _, files in os.walk(src_dir):
        for file in files:
            for filename in filename_list:
                if filename in file:
                    print(file)
                    # 复制文件到指定文件夹
                    shutil.copy(os.path.join(root, file), os.path.join(dst_dir, file))

def tesseract_ocr():
    src_dir = f'D:\\ZZZPIC\\LEVELINFO\\'
    data_list = []

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.startswith('LEVELINFO'):
                print(file)
                image = cv2.imread(os.path.join(root, file))
                temp_filename = f"{os.getpid()}.png"
                cv2.imwrite(temp_filename, image)

                custom_config = r'-l eng.num --oem 3 --psm 6'
                text = pytesseract.image_to_string(Image.open(temp_filename), config=custom_config)
                data_list.append({'Name': file, 'OCR': text.replace('\n', '')})

                os.remove(temp_filename)

    df = pd.DataFrame(data_list)
    timestamp = int(time.time())
    excel_file = f'D:/ZZZPIC/{timestamp}.xlsx'
    df.to_excel(excel_file, index=False)
    return excel_file

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
        elif 'LEVELINFO' not in name:
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

    # 提取list1中level为空的uid，复制到LEVELINFO文件夹
    uid_with_empty_level = [item['uid'] for item in list1 if 'level' not in item or item['level'] is None]
    copy_file(uid_with_empty_level)

    # OCR识别LEVELINFO文件夹中的等级
    excel_file = tesseract_ocr()
    df1 = pd.read_excel(excel_file, engine='openpyxl')
    for _, row in df1.iterrows():
        name = str(row['Name'])
        uid = extract_uid(name)
        level = extract_level(row['OCR'])
        if uid in uid_dict:
            uid_dict[uid]['level'] = level
        else:
            data_dict = {'uid': uid, 'level': level}
            list1.append(data_dict)

    return pd.DataFrame(list1)

def execute_zzz_file(file):
    df = read_file(file)
    df1 = process_data(df)
    df1.to_excel(file.replace('.csv', '_output.xlsx'), index=False)

if __name__ == "__main__":
    execute_zzz_file("D:\\ZZZPIC\\[OCR]_2024-08-25_20240825_1153.csv")