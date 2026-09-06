import re
import pandas as pd
import numpy as np
from zipfile import BadZipFile
import os
import time
import shutil
from PIL import Image
from collections import Counter
import chardet
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional, Tuple, Union, Any

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)


# 匹配最后登录字符串
def match_last_login(text: Any) -> str:
    """Normalize last login string."""
    if pd.isna(text):
        text = ''
    else:
        text = str(text)
    if '在线' in text:
        return '在线'
    pattern = re.compile(r"(\d+天前|\d+天)")
    pattern1 = re.compile(r"(今日内|今白内|令日内|令今日内|今日|含日内|今|令|含|日内|内|日)")
    pattern2 = re.compile(r"(年)")
    result = pattern.search(text)
    result1 = pattern1.search(text)
    result2 = pattern2.search(text)
    if result:
        # 如果不是“前”结尾，在后面加上“前”
        if '前' not in result.group(1):
            return result.group(1) + '前'
        return result.group(1)
    elif result1:
        return '今日内'
    elif result2:
        return '1年以上'
    return 'None'
    
def extract_uid(filename, last_login=None, server=None):
    pattern = None
    if 'UID不存在' in filename or 'LEVELINFO' in filename or 'UID不存在' in last_login:
        pattern = re.compile(r'-(\d+)(?:\.jpg|\.bmp)$')
    else:
        if server == 1:
            # pattern = re.compile(r'-(\d{8})-')
            pattern = re.compile(r'-(\d{8})')
        else:
            pattern = re.compile(r'-(\d{10})-')
    match = pattern.search(filename)
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
        '95': '22',
        '99': '39',
        '72': '12',
        'o': '0',
        'c': '9',
        'C': '0',
        's': '9',
        'S': '9',
        'g': '9',
        '℃': '9',
        '69': '60'
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
            # 先尝试手动检测编码（需要安装 chardet）
            with open(file, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result['encoding'] if result['encoding'] else 'utf-8'
            return pd.read_csv(file, encoding=encoding)
        else:
            raise Exception("文件格式不支持")
    except FileNotFoundError:
        raise FileNotFoundError("文件不存在")
    except ValueError as e:
        raise ValueError(str(e))
    except BadZipFile:
        raise BadZipFile("文件格式不正确")

def copy_file(uid_with_empty_level, server=None):
    # 生成当前日期yyyy-mm-dd
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    src_dir = None
    if server == 1:
        src_dir = f'E:\\ZZZPIC\\{date}\\'
        # src_dir = f'E:\\ZZZPIC\\2024-11-20\\'
    elif server == 13:
        src_dir = f'E:\\ZZZPIC\\{date}亚服\\'
        # src_dir = f'E:\\ZZZPIC\\2024-11-20亚服\\'
    elif server == 10:
        src_dir = f'E:\\ZZZPIC\\{date}美服\\'
    elif server == 15:
        src_dir = f'E:\\ZZZPIC\\{date}欧服\\'

    dst_dir = f'E:\\ZZZPIC\\LEVELINFO\\'
    filename_list = [f'{uid}.bmp' for uid in uid_with_empty_level]

    # 循环读取文件夹下的所有文件
    for root, _, files in os.walk(src_dir):
        for file in files:
            for filename in filename_list:
                if filename in file:
                    logger.debug(file)
                    # 复制文件到指定文件夹
                    shutil.copy(os.path.join(root, file), os.path.join(dst_dir, file))

def tesseract_ocr():
    src_dir = f'E:\\ZZZPIC\\LEVELINFO\\'
    data_list = []

    for root, _, files in os.walk(src_dir):
        for file in files:
            if file.startswith('LEVELINFO'):
                logger.debug(file)
                image = cv2.imread(os.path.join(root, file))
                temp_filename = f"{os.getpid()}.png"
                cv2.imwrite(temp_filename, image)

                custom_config = r'-l eng.num --oem 3 --psm 6'
                text = pytesseract.image_to_string(Image.open(temp_filename), config=custom_config)
                data_list.append({'Name': file, 'OCR': text.replace('\n', '')})

                os.remove(temp_filename)

    df = pd.DataFrame(data_list)
    timestamp = int(time.time())
    excel_file = f'E:/ZZZPIC/{timestamp}.xlsx'
    df.to_excel(excel_file, index=False)
    return excel_file

def process_data(df, server=None):
    names = df['Name'].astype(str)
    ocr_str = df['OCR'].astype(str)

    # 向量化解析 Name 列
    name_split = names.str.replace('.jpg', '', regex=False).str.split('-')
    grab_order = name_split.str.get(0).fillna('').tolist()
    return_times = name_split.str.get(1).fillna('').tolist()
    check_color_times = name_split.str.get(2).fillna('').tolist()
    avatar = name_split.str.get(4).fillna('').tolist()
    card = name_split.str.get(5).fillna('').tolist()

    # 向量化提取 UID
    special = (
        names.str.contains('UID不存在', regex=False)
        | names.str.contains('LEVELINFO', regex=False)
        | ocr_str.str.contains('UID不存在', regex=False)
    )
    special_uid = names.str.extract(r'-(\d+)(?:\.jpg|\.bmp)$', expand=False)
    if server == 1:
        normal_uid = names.str.extract(r'-(\d{8})', expand=False)
    else:
        normal_uid = names.str.extract(r'-(\d{10})-', expand=False)
    uid_raw = special_uid.where(special, normal_uid).tolist()
    uids = [None if pd.isna(x) else int(x) for x in uid_raw]

    # 向量化匹配最后登录
    cond_online = ocr_str.str.contains('在线', regex=False)
    days = ocr_str.str.extract(r'(\d+天前|\d+天)', expand=False)
    today = ocr_str.str.extract(r'(今日内|今白内|令日内|令今日内|今日|含日内|今|令|含|日内|内|日)', expand=False)
    year = ocr_str.str.extract(r'(年)', expand=False)
    days_value = days.where(days.str.contains('前', regex=False), days + '前')
    last_logins = np.select(
        [cond_online.to_numpy(), days.notna().to_numpy(), today.notna().to_numpy(), year.notna().to_numpy()],
        ['在线', days_value.to_numpy(), '今日内', '1年以上'],
        default='None'
    ).tolist()

    # 向量化提取等级
    level_str = ocr_str.str.replace('\n', '', regex=False).str.replace('＇', '', regex=False)
    replacements = {'AC': '10', '92': '22', '95': '22', '99': '39', '72': '12',
                    'o': '0', 'c': '9', 'C': '0', 's': '9', 'S': '9', 'g': '9',
                    '℃': '9', '69': '60'}
    for key, value in replacements.items():
        level_str = level_str.str.replace(key, value, regex=False)
    sliced = level_str.str.slice(0, 2)
    is_digit = sliced.str.isdigit().tolist()
    sliced_list = sliced.tolist()
    levels = [None if not is_digit[i] else int(sliced_list[i]) for i in range(len(df))]

    is_uid_not_exist = ocr_str.str.contains('UID不存在', regex=False).tolist()
    is_levelinfo = names.str.contains('LEVELINFO', regex=False).tolist()
    names_list = names.tolist()

    # 初始化列表和辅助字典
    list1 = []
    list2 = []
    uid_dict = {}
    day_counts = []

    for i in range(len(df)):
        name = names_list[i]
        if is_uid_not_exist[i]:
            list1.append({
                'grab_order': grab_order[i], 'return_times': return_times[i],
                'check_color_times': check_color_times[i], 'uid': uids[i],
                'avatar': avatar[i], 'card': card[i],
                'last_login': 'UID不存在', 'level': 'UID不存在'
            })
        elif not is_levelinfo[i]:
            ll = last_logins[i]
            m = re.search(r'(\d+)天前', ll)
            if m:
                day_counts.append(int(m.group(1)))
            data_dict = {
                'grab_order': grab_order[i], 'return_times': return_times[i],
                'check_color_times': check_color_times[i], 'uid': uids[i],
                'avatar': avatar[i], 'card': card[i], 'last_login': ll
            }
            list1.append(data_dict)
            uid_dict[uids[i]] = data_dict
        else:
            level = levels[i]
            if uids[i] in uid_dict:
                uid_dict[uids[i]]['level'] = level
            else:
                list2.append({'name': name, 'uid': uids[i], 'level': level})

    for item in list2:
        uid = item['uid']
        if uid in uid_dict:
            uid_dict[uid]['level'] = item['level']
        else:
            list1.append(item)

    # 提取list1中level为空的uid，复制到LEVELINFO文件夹
    uid_with_empty_level = [item['uid'] for item in list1 if 'level' not in item or item['level'] is None]
    copy_file(uid_with_empty_level, server)

    # 计算重复次数最多的数字
    if day_counts:
        # most_common_day = int(Counter(day_counts).most_common(1)[0][0])
        # threshold = most_common_day + 2
        threshold = 365

        # 修改大于阈值的数字
        for row in list1:
            if '天数' in row and isinstance(row['天数'], str) and row['天数'].endswith("天前"):
                days = int(row['天数'].replace("天前", ""))
                if days > threshold:
                    row['天数'] = f"{str(days)[1:]}天前"

    return pd.DataFrame(list1)

def process_one_file(file):
    # 读取文件（如果是 Excel 文件）
    df = pd.read_excel(file, sheet_name='处理结果')

    # 如果保存为 CSV/TSV，可改用：
    # df = pd.read_csv('data.csv', sep='|', skipinitialspace=True)

    # ========== 过滤无效行 ==========
    df_valid = df[df['天数'] != 'UID不存在'].copy()

    # ========== 基础参数 ==========
    total_rows = len(df_valid)
    uid_max = df_valid['UID'].max()
    base = (uid_max - 10_000_000) / 10_000
    denominator = total_rows + 390

    def count_login(condition):
        return df['天数'].apply(condition).sum()

    # 今日内 / 在线
    today_online = count_login(lambda x: x in ['今日内', '在线'])

    # 1~6天前
    days_1_6 = count_login(lambda x: isinstance(x, str) and re.match(r'^[1-6]天前$', x) is not None)

    # 1~29天前
    days_1_29 = count_login(lambda x: isinstance(x, str) and re.match(r'^([1-9]|[12][0-9])天前$', x) is not None)

    # 1~365天前
    days_1_365 = count_login(lambda x: isinstance(x, str) and re.match(r'^(\d+)天前$', x) is not None and 1 <= int(re.match(r'^(\d+)天前$', x).group(1)) <= 365)
    # denominator = today_online + days_1_365 + 390

    daily = today_online / denominator * base
    weekly = (today_online + days_1_6) / denominator * base
    monthly = (today_online + days_1_29) / denominator * base

    # print(f"总行数: {denominator}")
    # print(f"uid最大值: {uid_max}")
    # print(f"今日内+在线: {today_online}")
    # print(f"1~6天前: {days_1_6}")
    # print(f"1~29天前: {days_1_29}")
    # print(f"日活: {daily:.2f}")
    # print(f"周活: {weekly:.2f}")
    # print(f"月活: {monthly:.2f}")
    # print(f"==============================")

    return {
        'file': os.path.basename(file),
        'total_valid': denominator,
        'uid_max': uid_max,
        'today_online': today_online,
        'days_1_6': days_1_6,
        'days_1_29': days_1_29,
        'daily': daily,
        'weekly': weekly,
        'monthly': monthly,
    }

# =============================================
# 4. 批量处理并输出 Excel
# =============================================
def batch_process(file_list: List[str], output_excel: str) -> None:
    """Process multiple files and output results to Excel.
    
    Args:
        file_list: List of file paths to process
        output_excel: Output Excel file path
    """
    results = []
    for f in file_list:
        logger.info(f"正在处理: {f}")
        
        # ========== 检查文件是否存在 ==========
        if not os.path.exists(f):
            logger.warning(f"警告: 文件不存在，已跳过 {f}")
            results.append({
                'file': os.path.basename(f),
                'total_valid': 0,
                'uid_max': None,
                'today_online': 0,
                'days_1_6': 0,
                'days_1_29': 0,
                'days_1_365': 0,
                'daily': 0,
                'weekly': 0,
                'monthly': 0,
                'yearly': 0,
                'error': '文件不存在'
            })
            continue
        
        # ========== 正常处理 ==========
        try:
            res = process_one_file(f)
            results.append(res)
        except Exception as e:
            logger.error(f"处理出错: {e}")
            results.append({
                'file': os.path.basename(f),
                'total_valid': 0,
                'uid_max': None,
                'today_online': 0,
                'days_1_6': 0,
                'days_1_29': 0,
                'days_1_365': 0,
                'daily': 0,
                'weekly': 0,
                'monthly': 0,
                'yearly': 0,
                'error': str(e)
            })
    
    # 写入 Excel
    df_out = pd.DataFrame(results)
    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        df_out.to_excel(writer, sheet_name='汇总', index=False)
    logger.info(f"结果已保存至: {output_excel}")

def generate_file_paths(start_date_str, end_date_str, base_dir="E:\\ZZZPIC\\国服\\"):
    """
    生成指定日期范围内的文件路径列表
    start_date_str / end_date_str: 格式 "YYYY-MM-DD"
    """
    start = datetime.strptime(start_date_str, "%Y-%m-%d")
    end = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    paths = []
    current = start
    while current <= end:
        year = current.year % 100  # 取后两位，如 2025 -> 25
        month = current.month
        day = current.day
        # 文件名格式：25年{月}月{日}.xlsx，注意不带前导零
        filename = current.strftime("%Y%m%d") + "绝区零结果.xlsx"
        full_path = base_dir + filename
        paths.append(full_path)
        current += timedelta(days=1)
    return paths

def execute_zzz_file(files: Union[str, List[str]], server: Optional[int] = None) -> None:
    """Execute ZZZ data processing.
    
    Args:
        files: Single file path or list of file paths
        server: Server identifier (optional)
    """
    # If single file, wrap in list
    if isinstance(files, str):
        files = [files]
    
    # Process individual file if it's a single Excel with '处理结果' sheet
    if len(files) == 1 and files[0].endswith('.xlsx'):
        output = files[0].replace('.xlsx', '_output.xlsx')
        df = read_file(files[0])
        df1 = process_data(df, server)
        df1.to_excel(output, index=False)
    else:
        batch_process(files)

if __name__ == "__main__":
    # execute_zzz_file("E:\\ZZZPIC\\国服\\25年11月30.xlsx", 1)

    files = generate_file_paths("2026-09-05", "2026-09-05")

    batch_process(files, "E:\\ZZZPIC\\国服活跃统计汇总.xlsx")
    # execute_zzz_file("E:\\ZZZPIC\\20260712绝区零结果.xlsx", 1)
    # execute_zzz_file("E:\\ZZZPIC\\[OCR]_2026-4-7-3点6绝区零_20260407_0748.csv", 1)
    # execute_zzz_file("E:\\ZZZPIC\\[OCR]_2025-01-04亚服_20250104_1833.csv", 13)
    # execute_zzz_file("E:\\ZZZPIC\\[OCR]_2024-12-22美服_20241222_1346.csv", 10)
    # execute_zzz_file("E:\\ZZZPIC\\[OCR]_2024-12-22欧服_20241222_1755.csv", 15)
    