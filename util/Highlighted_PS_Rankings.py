import requests
import pandas as pd
import openpyxl
import shutil
import os
import re
import time
from datetime import datetime
import concurrent.futures
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openpyxl.styles import PatternFill, Alignment
import json
import sys

# ===================== 配置文件读取 =====================

# 获取当前脚本或exe的目录
if getattr(sys, 'frozen', False):
    # 如果是打包成exe文件
    script_dir = os.path.dirname(sys.executable)  # 获取exe所在目录
else:
    # 如果是脚本文件
    script_dir = os.path.dirname(os.path.realpath(__file__))

# 配置文件路径
config_file = os.path.join(script_dir, 'ps_rankings_config.json')

# 确保配置文件存在
if not os.path.exists(config_file):
    print(f"配置文件 {config_file} 未找到，请确保该文件与程序一起存在。")
    sys.exit(1)

# 读取配置文件
with open(config_file, 'r', encoding='utf-8') as f:
    config_data = json.load(f)

# 获取配置文件中的内容
base_urls = config_data['base_urls']
replacement_map = config_data['replacement_map']


# ===================== 配置参数 =====================

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 输出文件的保存路径
output_dir = os.path.join(script_dir, 'ps_rankings_output')

# 重试机制：最大重试次数
max_retries = 3

# 请求之间的延时时间（单位：秒）
request_delay = 0.05

# ===================== 获取用户输入的页面数量 =====================

# 获取用户输入的页面数量
while True:
    try:
        pages_to_scrape_input = input("请输入需要抓取的页面数量（一页24个游戏）：")
        
        # 尝试将输入转为整数
        pages_to_scrape = int(pages_to_scrape_input)
        
        # 检查输入是否在 1 到 40 的范围内
        if 1 <= pages_to_scrape <= 40:
            break  # 输入有效，退出循环
        else:
            print("抓取页面不建议超过40，请重新输入。")
    except ValueError:
        print("无效输入，请输入一个正整数。")

# ===================== 创建会话和重试机制 =====================

# 设置请求的重试机制
def create_session():
    session = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('https://', adapter)
    return session

# ===================== 数据抓取函数 =====================

# 收集每一页数据
def fetch_page_data(session, region, page):
    url = f"{base_urls[region]}/{page}"
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果响应码不是200，则抛出异常
        all_games = []

        html_content = response.text

        # 查找所有游戏信息
        idx = 0
        while idx < len(html_content):
            # 找到游戏名称的位置
            name_marker = ',&quot;name&quot;:&quot;'
            name_start = html_content.find(name_marker, idx)

            if name_start == -1:
                break  # 没有更多的游戏信息

            # 提取游戏名称
            name_end = html_content.find('&quot;', name_start + len(name_marker))
            name = html_content[name_start + len(name_marker):name_end]

            # 查找对应的排名数字
            rank_marker = '&quot;index&quot;:' 
            rank_end = html_content.rfind(rank_marker, 0, name_start)
            rank_start = rank_end + len(rank_marker)
            rank = int(html_content[rank_start:name_start].strip(","))

            # 计算实际排名（每页24个游戏）
            all_games.append({"Rank": rank + 1 + (page - 1) * 24, "Name": name})

            idx = name_end  # 更新索引，继续查找下一个游戏

        return all_games

    except Exception as e:
        print(f"第 {region} 第 {page} 页数据处理失败，原因: {str(e)}")
        return []  # 返回空列表，避免后续处理出错

# ===================== 数据异常检测 =====================

def check_data_integrity(all_region_data, pages_to_scrape):
    for region, games in all_region_data.items():
        # 检测游戏数量是否符合预期
        if len(games) != pages_to_scrape * 24:
            print(f"偶发性代码运行异常(⊙﹏⊙)，文件不保存，请重新运行。{region} 页面的数据没有完整抓取。")
            print(f"重复，偶发性代码运行异常(⊙﹏⊙)，文件不保存，请重新运行。{region} 页面的数据没有完整抓取。")
            print(f"重复，偶发性代码运行异常(⊙﹏⊙)，文件不保存，请重新运行。{region} 页面的数据没有完整抓取。")
            return False

        # 检测重复的游戏名是否超过10对
        game_names = [game['Name'] for game in games]
        duplicate_count = sum(game_names.count(name) > 1 for name in set(game_names))

        if duplicate_count > 10:
            print(f"偶发性代码运行异常(⊙﹏⊙)，文件不保存，请重新运行。{region} 页面的数据没有完整抓取。")
            print(f"重复，偶发性代码运行异常(⊙﹏⊙)，文件不保存，请重新运行。{region} 页面的数据没有完整抓取。")
            print(f"重复，偶发性代码运行异常(⊙﹏⊙)，文件不保存，请重新运行。{region} 页面的数据没有完整抓取。")
            return False

    return True

# ===================== 第二部分：替换和高亮 =====================

# 设置单元格背景颜色为黄色
yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

# 编译所有的正则表达式，避免重复编译
compiled_patterns = {key: [re.compile(pattern) for pattern in patterns] for key, patterns in replacement_map.items()}

# ===================== 主执行部分 =====================

# 使用 session 来进行请求并抓取数据
all_region_data = {}

# 创建会话，只在循环外部执行一次
session = create_session()

# 使用 session 来处理所有地区的数据
for region in base_urls.keys():
    all_games = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 使用线程池并发处理各页面的抓取，直接传递函数，避免使用lambda
        results = executor.map(fetch_page_data, [session] * pages_to_scrape, [region] * pages_to_scrape, range(1, pages_to_scrape + 1))

        # 收集所有页面的数据
        for result in results:
            all_games.extend(result)
            print(f"{region} 第{len(all_games)//24}页数据处理完成")  # 提示当前页面处理完成
            time.sleep(request_delay)  # 每次抓取后的延时时间

    # 排序数据
    all_games = sorted(all_games, key=lambda x: x['Rank'])
    all_region_data[region] = all_games

# 检查数据完整性
if not check_data_integrity(all_region_data, pages_to_scrape):
    input("按下 Enter 键退出...")  # 等待用户按下 Enter 键
    exit()  # 退出程序


# 创建 Excel 文件并初始化工作表
wb = openpyxl.Workbook()

# 删除默认创建的空白 sheet
del wb['Sheet']

# 复制原始数据并将其直接传递给第二部分处理
for region, all_games in all_region_data.items():
    ws = wb.create_sheet(region)
    for idx, game in enumerate(all_games, start=1):
        ws.append([game['Rank'], game['Name']])

# 创建 Summary 工作表
ws_summary = wb.create_sheet("Summary")

# 填充 A 列为被替换的元素
row_num = 2
for replacement in replacement_map:  # 使用 replacement_map 中的顺序
    ws_summary[f"A{row_num}"] = replacement
    row_num += 1

# 填充 C1 及其后的列为原始 Sheet 名
column_num = 3
for sheet_name in wb.sheetnames:
    if sheet_name != "Summary":  # 跳过 Summary sheet
        ws_summary.cell(row=1, column=column_num, value=sheet_name)
        column_num += 1

# 遍历工作表，进行替换与高亮
replaced_elements = {}

# 遍历所有sheet
for sheet_name in wb.sheetnames:
    if sheet_name != "Summary":
        ws = wb[sheet_name]
        for row_idx, row in enumerate(ws.iter_rows(), start=1):
            for cell in row:
                if cell.value:
                    for replacement, patterns in compiled_patterns.items():
                        for pattern in patterns:
                            if pattern.search(str(cell.value)):
                                if cell.fill.start_color != "FFFF00":
                                    cell.value = replacement
                                    cell.fill = yellow_fill
                                    if replacement not in replaced_elements:
                                        replaced_elements[replacement] = {}
                                    if sheet_name not in replaced_elements[replacement]:
                                        replaced_elements[replacement][sheet_name] = []
                                    replaced_elements[replacement][sheet_name].append(row_idx)

# 填充替换数据
for replacement_row, replacement in enumerate(replacement_map, start=2):
    for column_num, sheet_name in enumerate(wb.sheetnames, start=3):
        if sheet_name != "Summary":
            ranks = list(set(replaced_elements.get(replacement, {}).get(sheet_name, [])))
            if ranks:
                if len(ranks) > 1:
                    ws_summary.cell(row=replacement_row, column=column_num, value="大于一项")
                else:
                    ws_summary.cell(row=replacement_row, column=column_num, value=ranks[0])

# 设置居中
for col in range(3, column_num):
    for row in range(1, row_num):
        ws_summary.cell(row=row, column=col).alignment = Alignment(horizontal="center", vertical="center")


# 生成文件名时，确保路径存在
highlight_file_name = os.path.join(output_dir, f"高亮_PS排行_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")

# 确保输出路径的文件夹存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 保存 Excel 文件
wb.save(highlight_file_name)


print(f"新文件已保存：{highlight_file_name}")

input("按下 Enter 键退出")



#能力有限，代码是ChatGPT写的
