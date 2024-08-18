from PIL import Image
import pytesseract
import cv2
import os
import numpy as np
import time
import pandas as pd

preprocess = "thresh"

file = 'D:/ZZZPIC/LEVELINFO'
list = []
# 循环读取文件夹下的所有文件
for root, dirs, files in os.walk(file):
    for file in files:
        # 找到B等级开头的文件
        if file.startswith('LEVELINFO'):
            print(file)
            image = cv2.imread(os.path.join(root, file))
            # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # if preprocess == "thresh":
            #     # 图像阈值处理
            #     # ret,dst = cv2.threshold(src,thresh,maxval,type)
            #     # src:输入图像，只能输入单通道图像，通常来说为灰度图
            #     # dst:输出图像与src图像大小和类型一致
            #     # thresh:阈值
            #     # maxval:当像素值高于（有时小于）阈值时应该被赋予的新的像素值
            #     # type:阈值类型，有以下5种类型
            #     # cv2.THRESH_BINARY:大于阈值的像素点赋予maxval，小于阈值的像素点赋予0
            #     # cv2.THRESH_BINARY_INV:大于阈值的像素点赋予0，小于阈值的像素点赋予maxval
            #     # cv2.THRESH_TRUNC:大于阈值的像素点赋予阈值，小于阈值的像素点不变
            #     # cv2.THRESH_TOZERO:大于阈值的像素点不变，小于阈值的像素点赋予0
            #     # cv2.THRESH_TOZERO_INV:大于阈值的像素点赋予0，小于阈值的像素点不变
            #     gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)[1]

            # if preprocess == "blur":
            #     gray = cv2.medianBlur(gray, 3)

            # # 锐化
            # kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            # gray = cv2.filter2D(gray, -1, kernel)

            filename = "scan\\img\\{}.png".format(os.getpid())
            cv2.imwrite(filename, image)

            # **--oem 3**：OCR 引擎模式（OEM，OCR Engine Mode）。

            # 0：仅使用传统的 Tesseract OCR 引擎。
            # 1：仅使用基于 LSTM 的 OCR 引擎。
            # 2：同时使用传统的 Tesseract OCR 引擎和 LSTM 引擎。
            # 3：默认模式，自动选择最合适的引擎（通常是基于 LSTM 的引擎）。
            # **--psm 10**：页面分割模式（PSM，Page Segmentation Mode）。

            # 0：仅检测方向和脚本。
            # 1：自动页面分割，使用 OSD（方向和脚本检测）。
            # 2：自动页面分割，但不使用 OSD 或 OCR。
            # 3：完全自动页面分割，但不使用 OSD。
            # 4：假设是单列文本的页面。
            # 5：假设是垂直对齐的单个统一块。
            # 6：假设是一个统一的文本块。
            # 7：将图像视为单行文本。
            # 8：将图像视为单个单词。
            # 9：将图像视为单个单词中的单个字符。
            # 10：将图像视为单个文本行中的单个单词。
            # 11：将图像视为单个文本行中的单个单词。
            # custom_config = r'-l chi_sim --oem 3 --psm 3'
            custom_config = r'-l eng.num --oem 3 --psm 6'
            text = pytesseract.image_to_string(Image.open(filename), config=custom_config)
            # print(text.replace('\n', ''))
            dict = {'Name': file, 'OCR': text.replace('\n', '')}
            list.append(dict)

            os.remove(filename)

df = pd.DataFrame(list)
# 当前时间戳
timestamp = int(time.time())

df.to_excel(f'D:/ZZZPIC/{timestamp}.xlsx', index=False) 

# 展示处理前、后的图片
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)