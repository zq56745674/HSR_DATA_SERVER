import os
import pandas as pd

file = f'D:\\ZZZPIC\\2024-08-19\\'
dst = f'D:\\ZZZPIC\\LEVELINFO\\'
uid_file = 'C:\\Users\\momo\Desktop\\BTUID.xlsx'

# 读取excel文件
df = pd.read_excel(uid_file)
filename_list = []
# 循环表格
for index, row in df.iterrows():
    uid = str(row['uid'])
    file_name = f'{uid}.bmp'
    filename_list.append(file_name)

# 循环读取文件夹下的所有文件
for root, dirs, files in os.walk(file):
    for file in files:
        for filename in filename_list:
            if filename in file:
                print(file)
                # 复制文件到指定文件夹
                os.rename(os.path.join(root, file), os.path.join(dst, file))
            




# 循环读取文件夹下的所有文件
# for root, dirs, files in os.walk(file):
#     for file in files:
#         print(file)
#         # 找到B等级开头的文件
#         if file.startswith('B等级'):
#             print(file)
#             # 重命名文件将B等级替换为LEVELINFO
#             os.rename(os.path.join(root, file), os.path.join(root, file.replace('B等级', 'LEVELINFO')))
            






