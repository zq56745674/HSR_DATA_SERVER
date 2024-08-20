import cv2
import pyautogui
import numpy as np
import time

def get_screen():
    # 获取屏幕截图
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
    return screen

def match_template(screen, template):
    # 使用模板匹配
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val

def match_template_loc(screen, template):
    # 使用模板匹配
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc

def match_template_all(screen, template):
    # 使用模板匹配
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    # 获取所有匹配位置
    loc = np.where(result >= 0.9)
    return loc

def click_loc(loc):
    # 点击位置
    pyautogui.click(loc[0], loc[1])

def click_template(screen, template):
    # 点击模板
    loc = match_template_loc(screen, template)
    click_loc(loc)

def click_template_all(screen, template):
    # 点击所有模板
    locs = match_template_all(screen, template)
    for loc in zip(*locs[::-1]):
        click_loc(loc)

def input_template(screen, template, text):
    # 输入文本
    loc = match_template_loc(screen, template)
    click_loc(loc)
    pyautogui.typewrite(text)

def screenshot_template(screen, template, save_path):
    # 截图模板
    loc = match_template_loc(screen, template)
    x, y = loc
    w, h = template.shape[::-1]
    cv2.imwrite(save_path, screen[y:y+h, x:x+w])

if __name__ == "__main__":
    time.sleep(3)
    screen = get_screen()
    template = cv2.imread('pic\\zzz_empty_input.png')
    input_template(screen, template, '36600000')

    template = cv2.imread('pic\\zzz_search.png')
    click_template(screen, template)