#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径,可以将对应的文件路径放入下面的自定义包的__init__.py文件中，每次导入的时候会加载

from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState, maguafilterQuestion, filtertimeLine
from UniversalAutomaticAnswer.match.matchImp import DataMatcher, match_options
from UniversalAutomaticAnswer.httpImp.search import searchImp
import cv2
import time
import pandas as pd

import warnings
warnings.filterwarnings('ignore') # warnings有点多，过滤一下
# left click
import win32api
import win32con
import numpy as np
from PIL import ImageGrab,Image
import win32gui

hwnd_title = dict() # 使用upadate的方式更新字典
def get_all_hwnd(hwnd,nouse):
  if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
    hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})
 
def get_Chrome_window_rect(hwnd_title, target_title):
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h,t in hwnd_title.items():
        if target_title in t and 'Chrom' in t:
            # print(hwnd_title)
            return win32gui.GetWindowRect(h)
    return None

def get_Edge_window_rect(hwnd_title, target_title):
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h,t in hwnd_title.items():
        if target_title in t and 'Edge' in t:
            # print(hwnd_title)
            return win32gui.GetWindowRect(h)
    return None

# rect = get_Chrome_window_rect(hwnd_title,'大神云游戏')
# print(rect)
# rect = get_Edge_window_rect(hwnd_title,'大神云游戏')
# print(rect)

# 日志
def make_print_to_file(path='./'):
    '''
    path， it is a path for save your log about fuction print
    example:
    use  make_print_to_file()   and the   all the information of funtion print , will be write in to a log file
    :return:
    '''
    import sys
    import os
    # import config_file as cfg_file
    import sys
    import datetime
 
    class Logger(object):
        def __init__(self, filename="Default.log", path="./"):
            self.terminal = sys.stdout
            import os
            if not os.path.exists(path): # 判断文件夹是否存在，不存在则创建文件夹
                os.mkdir(path)
            self.log = open(os.path.join(path, filename), "a", encoding='utf8',)
 
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

        def flush(self):
            pass

    fileName = datetime.datetime.now().strftime('log_'+'%Y_%m_%d_%H')
    sys.stdout = Logger(fileName + '.log', path=path)

def left_click(x,y,times=1):
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        times -= 1
    # print('左键点击',x,y)


if __name__ == '__main__':
    is_answered = 1
    # 获取配置文件
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    make_print_to_file(path='./log/')
    
    # 初始化ocr模型
    ocr = OCRImp(conf_data)

    # 初始化匹配器(题库)
    data_matcher = DataMatcher(conf_data)

    # 截屏
    screen = ScreenImp(conf_data)
    is_continue = True
    while is_continue:
        val = input('是否继续答题？1表示继续\n')
        if val != '1':
            break
        win_rect, img= screen.get_screenshot()
        # img_path = './img/bili.jpg'
        # img = cv2.imread(img_path)

        import matplotlib.pyplot as plt


        det = True
        img = img[275:708,548:1055]
        result = ocr.ocr(img,cls=True,det=det) # 只识别14.34ms 带检测24.70ms 带角度分类36.48 [[1]] 1=>[[坐标集]，('内容',概率)]
        result_list = []
        for idx, line in enumerate(result):
            result_list.append(line[1][0])

        print(result_list)
        # plt.imshow(img)
        # plt.show()

        searchimp = searchImp(conf_data)
        question = ''.join(x for x in result_list[:-4])
        options = result_list[-4:]

        # question = '金坷垃三人组分别来自哪三个地区或国家'
        # options = ['中非韩','英美非','中日美','美日非']
        # question,options = ret_question_options(img)
        print(question,options)

        ans1 = searchimp.baidu(question, options)
        print('百度结果：',ans1)
        print('百度选：',chr(ord('A')+int(ans1[0][2])))

        ans2 = searchimp.sougou(question, options)
        print('\n搜狗结果：',ans2)

        ans3 = searchimp.bing(question, options)
        print('\n必应结果：',ans3)

        # ['16', '/100', '《甄传》中华妃吃酸黄瓜呕吐时，甄', '是什么位分？', '莞常在', '熹贵妃', '莞嫔', '莞贵人', '本题由UID81455393的用户所出', '倒计时', '1:41:32']
