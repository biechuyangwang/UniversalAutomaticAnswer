#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径

from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState
from UniversalAutomaticAnswer.match.matchImp import DataMatcher, match_options
import cv2
import time
import pandas as pd

import warnings
warnings.filterwarnings('ignore') # warnings有点多，过滤一下
# left click
import win32api
import win32con

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

# 记录错题
def write_new_question(info, answer_flag=""):
    import time
    # 格式化成2021-12-01形式
    time_str = time.strftime("%Y-%m-%d", time.localtime()) 
    # print(time_str)
    line = info[0] + ' ' + ' '.join(list(info[1])) + ' ' + answer_flag
    d = [line,]
    df = pd.DataFrame(data=d)
    # print(line)
    
    import os
    if not os.path.exists('./new_questions/'): # 判断文件夹是否存在，不存在则创建文件夹
        os.mkdir('./new_questions/')
    # 新题目按时间新建文件，追加的方式保留当天的新题
    df.to_csv('./new_questions/'+time_str+'_harry_questions.csv', mode='a', header=False)

def left_click(x,y,times=1):
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        times -= 1
    # print('左键点击',x,y)

def is_start(img, str_start):
    img_start = screen.get_startMatchBtn(img)
    result_start = ocr.ocr(img_start)
    content_start = ocr.ocr_content(result_start)
    content_start = filterLine(content_start)
    if len(content_start)>0 and str_start in content_start[0]:
        time.sleep(5)
        x, y = 1300, 840
        left_click(win_rect[0]+x,win_rect[1]+y,2)
        return True
    return False

def get_question_answer(img):
    # 一次答题流程
    res = []
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_questionAndoptionsBtn(img)
    resultq = ocr.ocr(QBtn)
    resulta = ocr.ocr(ABtn)
    resultb = ocr.ocr(BBtn)
    resultc = ocr.ocr(CBtn)
    resultd = ocr.ocr(DBtn)

    contentq = ocr.ocr_content(resultq)
    contenta = ocr.ocr_content(resulta)
    contentb = ocr.ocr_content(resultb)
    contentc = ocr.ocr_content(resultc)
    contentd = ocr.ocr_content(resultd)
    print(contentq)

    question, optiona,optionb,optionc,optiond = '', '', '', '' ,''
    if len(filterQuestion(contentq))>0:
        question = filterQuestion(contentq)[0]
    print(question)
    if len(question)==0:
        print('题目未识别！')
        print('源数据为：',resultq)
        return res

    if len(filterLine(contenta))>0:
        optiona = filterLine(contenta)[0]
    if len(filterLine(contentb))>0:
        optionb = filterLine(contentb)[0]
    if len(filterLine(contentc))>0:
        optionc = filterLine(contentc)[0]
    if len(filterLine(contentd))>0:
        optiond = filterLine(contentd)[0]
    options = [optiona, optionb, optionc, optiond]
    print('ocr结果:', [question,options])

    answer_list = list(data_matcher.get_close_match(question))
    if len(answer_list) == 0 or list(answer_list[0])[1] < 40:
        print('没有匹配到题库')
        return res
    else:
        print('题库匹配结果:', answer_list[0])
        answer = answer_list[0][0][1]
        res = match_options(answer, options)
        if len(res) == 0:
            print('选项OCR出错')
            return res
        print('选项匹配结果:', res)
        return res


coordinate = [
    [646,797],
    [1300,797],
    [646,888],
    [1300,888]
]

def play_piano(song=1, sudu = 1):
    win_rect, img = screen.get_screenshot()
    x_start_pos = 236
    x_shap_start_pos = 330
    y_start_pos = 530
    Y_shap_start_pos = 460
    x_off = 189
    y_off = 150
    x_shap_off = 187
    y_shap_off = 50
    x_pad = 50
    y_pad = 13

    # 580 720 870
    if sudu == 1:
        time_interval = 0.175 # 四分音符间隔时间
    elif sudu ==2:
        time_interval = 0.15 # 四分音符间隔时间
    elif sudu ==3:
        time_interval = 0.1 # 四分音符间隔时间

    # 两只老虎
    liangzhilaohu = [2,1,2, 2,2,2, 2,3,2, 2,1,2, 
    2,1,2, 2,2,2, 2,3,2, 2,1,2, 
    2,3,2, 2,4,2, 2,5,4, 
    2,3,2, 2,4,2, 2,5,4, 
    2,5,1, 2,6,1, 2,5,1, 2,4,1, 2,3,2, 2,1,2, 
    2,5,1, 2,6,1, 2,5,1, 2,4,1, 2,3,2, 2,1,2, 
    2,3,2, 3,5,2, 2,1,4, 
    2,3,2, 3,5,2, 2,1,4]
    
    # 天空之城
    tiankongzhicheng = [
        2,6,2, 2,7,2, 1,1,6, 2,7,2, 1,1,4, 1,3,4, 2,7,12, 2,3,2, 2,3,2, 2,6,6, 2,5,2, 2,6,4, 1,1,4, 
        2,5,12, 2,3,4, 2,4,6, 2,3,2, 2,4,4, 1,1,4, 2,3,10, 1,1,2, 1,1,2, 1,1,2, 2,7,6, 2,4,2, 2,4,4, 2,7,4,
        2,7,12, 2,6,2, 2,7,2, 1,1,6, 2,7,2, 1,1,4, 1,3,4, 2,7,12, 2,3,2, 2,3,2, 2,6,6, 2,5,2, 2,6,4, 1,1,4,
        2,5,12, 2,3,4, 2,4,6, 1,1,2, 2,7,4, 1,1,4, 1,2,2, 1,2,4, 1,3,2, 1,1,8, 1,1,2, 2,7,2, 2,6,4, 2,7,4, 2,5,4,
        2,6,12, 1,1,2, 1,2,2, 1,3,6, 1,2,2, 1,3,4, 1,5,4, 2,5,2, 2,5,2, 1,1,6, 2,7,2, 1,1,4, 1,3,4,
        1,3,16, 2,6,2, 2,7,2, 1,1,4, 2,7,2, 1,1,2, 1,2,4, 1,1,6, 2,5,2, 2,5,8, 1,4,4, 1,3,4, 1,2,4, 1,1,4,
        1,3,12, 1,3,4, 1,6,8, 1,5,8, 1,3,2, 1,2,2, 1,1,8, 1,1,4, 1,2,6, 1,1,2, 1,2,4, 1,5,4,
        1,3,12, 1,3,4, 1,6,6, 1,6,2, 1,5,6, 1,5,2, 1,3,2, 1,2,2, 1,1,8, 1,1,4, 1,2,6, 1,1,2, 1,2,4, 2,7,4,
        1,6,12
    ]
    
    # 青花瓷
    qinghuaci = [2,2,1, 2,1,1,3,6,1,
    2,1,2, 2,1,1, 3,6,1, 2,1,2, 2,1,1, 3,6,1, 2,1,1, 3,6,1, 3,5,3, 2,2,1, 2,1,1, 3,6,1,
    2,1,2, 2,1,1, 3,6,1, 2,1,2, 2,1,1, 2,3,1, 2,2,1, 2,1,1, 2,1,3, 3,5,1, 3,6,1, 2,3,1,
    2,3,2, 2,3,1, 2,2,1, 2,3,2, 2,3,1, 2,2,1, 2,3,1, 2,4,1, 2,3,1, 2,3,2, 2,3,1, 2,3,1, 2,3,1,
    2,2,1, 2,2,1, 2,2,1, 2,2,1, 2,2,2, 2,1,1, 2,3,1, 2,1,3, 2,2,4, 2,3,1, 2,1,1, 3,6,1,
    2,1,2, 2,1,1, 3,6,1, 2,1,2, 2,1,1, 3,6,1, 2,1,1, 3,6,1, 3,5,3, 3,5,1, 3,6,1, 2,3,1,
    2,5,2, 2,5,1, 2,3,1, 2,5,2, 2,5,1, 2,3,1, 2,2,1, 2,1,1, 2,1,3, 2,2,1, 2,1,1, 2,2,1,
    2,3,1, 2,2,1, 2,2,1, 2,1,1, 2,2,2, 2,1,1, 3,6,1, 2,2,1, 2,1,1, 2,1,1, 3,6,1, 2,1,2, 2,1,1, 2,1,1]
    
    # 小幸运
    xiaoxingyun = [
        2,3,2, 2,3,2, 2,5,2, 2,5,2, 1,1,2, 1,1,2, 2,7,2, 2,7,2, 2,6,2, 2,3,2, 2,6,12,
        2,6,2, 2,6,2, 2,7,2, 2,7,2, 1,3,2, 1,3,2, 2,7,2, 2,7,2, 2,5,2, 2,3,2, 2,5,12,
        2,3,2, 2,3,2, 2,5,2, 2,5,2, 1,1,2, 1,1,2, 2,7,2, 2,7,2, 2,6,2, 2,3,2, 2,6,6,
        2,6,2, 2,7,4, 2,7,2, 1,1,2, 1,3,4, 1,2,4, 1,1,18,
        2,3,2, 2,3,2, 2,5,2, 2,5,2, 1,1,2, 1,1,2, 2,7,2, 2,7,2, 2,6,2, 2,3,2, 2,6,12,
        2,6,2, 2,6,2, 2,7,2, 2,7,2, 1,3,2, 1,3,2, 2,7,2, 2,7,4, 2,3,2, 2,5,12,
        2,3,2, 2,3,2, 2,5,2, 2,5,2, 1,1,2, 1,1,2, 2,7,2, 2,7,2, 1,1,2, 2,3,2, 2,6,4,
        2,6,2, 1,1,2, 2,7,4, 2,6,2, 2,7,2, 1,3,4, 1,2,4, 1,1,10,
        1,3,2, 1,2,1, 1,1,3, 2,7,2, 2,6,2, 2,6,2, 2,6,2, 2,6,2, 2,6,2, 1,3,6, 1,2,8,
        1,2,2, 1,1,1, 2,7,3, 2,6,2, 2,5,2, 2,5,2, 2,5,2, 2,3,2, 2,5,2, 1,2,4, 1,1,8,
        1,1,2, 1,1,2, 2,5,2, 2,5,2, 2,1,2, 2,3,4, 2,2,2, 2,6,6,
        2,6,4, 2,6,2, 2,6,2, 2,6,1, 1,1,3, 2,6,2, 1,1,2, 2,6,2, 1,1,2, 1,1,2, 1,1,2, 1,1,2, 1,3,2, 1,2,4, 1,2,8,
        2,5,2, 1,3,2, 1,2,1, 1,1,3, 1,2,2, 1,3,2, 2,5,2, 1,2,2, 1,3,4, 2,5,2, 1,2,2, 1,3,4,
        1,2,2, 1,2,2, 1,3,1, 1,4,3, 1,3,2, 1,2,2, 2,7,2, 1,1,2, 2,3,2, 2,6,2, 1,1,4, 2,3,2, 2,6,2, 2,7,4,
        2,7,2, 2,7,2, 1,3,1, 1,5,3, 1,3,2, 1,1,2, 2,7,2, 2,6,2, 1,4,1, 1,4,7,
        1,5,2, 1,4,2, 1,3,2, 2,5,2, 1,3,1, 1,3,7,
        1,4,2, 1,3,2, 1,1,2, 2,4,2, 1,2,1, 1,2,7,
        1,2,2, 1,1,2, 1,3,4, 1,2,2, 1,1,2, 1,3,4, 1,2,4, 1,1,2,
        1,3,2, 2,5,2, 1,2,2, 1,3,4, 2,5,2, 1,2,2, 1,3,4,
        1,2,2, 1,2,2, 1,3,1, 1,4,3, 1,3,2, 1,2,2, 2,7,2, 1,1,2, 2,3,2, 2,6,2, 1,1,4, 2,3,2, 2,6,2, 2,7,4,
        2,7,2, 2,7,2, 1,3,1, 1,5,3, 1,3,2, 1,1,2, 2,7,2, 2,6,2, 1,4,1, 1,4,7,
        1,5,2, 1,4,2, 1,3,2, 2,5,2, 1,3,1, 1,3,7,
        1,4,2, 1,3,2, 1,1,2, 2,4,2, 1,2,1, 1,2,15,
        1,3,2, 1,1,2, 1,1,2, 1,3,4, 1,2,4, 1,1,16
    ]

    # 玛丽有只小羊羔
    maliyanggao = [
        1,3,2, 1,2,2, 1,1,2, 1,2,2, 1,3,2, 1,3,2, 1,3,4,
        1,2,2, 1,2,2, 1,2,4, 1,3,2, 1,5,2, 1,5,4,
        1,3,2, 1,2,2, 1,1,2, 1,2,2, 1,3,2, 1,3,2, 1,3,4,
        1,2,2, 1,2,2, 1,3,2, 1,2,2, 1,1,8
    ]

    # 起风了
    qifengle = [
        1,2,0, 2,1,2, 2,3,1, 1,1,1, 1,2,2, 2,5,1, 1,1,1, 1,2,0, 2,1,2, 1,3,2, 1,5,2, 1,3,2,
        1,2,0, 2,7,0, 2,5,2, 2,2,1, 1,1,1, 1,2,2, 2,5,1, 1,1,1, 1,2,1, 1,3,1, 1,2,1, 1,1,1, 2,5,4,
        1,2,0, 2,2,2, 2,5,1, 1,1,1, 1,2,2, 2,5,1, 1,1,1, 1,2,0, 2,2,2, 1,3,2, 1,5,2, 1,3,2,
        1,2,0, 2,4,2, 2,6,1, 1,3,1, 1,2,2, 1,1,2, 1,2,0, 2,4,2, 2,6,2, 1,1,2, 2,6,2,
        1,2,0, 2,2,2, 2,4,1, 1,1,1, 1,2,2, 2,4,1, 1,1,1, 1,2,0, 2,5,2, 1,3,2, 1,5,2, 1,3,2,
        1,2,0, 2,6,2, 2,3,1, 1,3,1, 1,2,2, 1,1,2, 2,6,0, 2,3,2, 1,1,2, 1,3,1, 1,2,1, 1,1,1, 1,2,1,
        1,1,0, 2,6,0, 2,4,2, 2,6,2, 1,3,1, 1,2,1, 1,1,1, 1,2,1, 1,1,0, 2,5,2, 2,7,1, 1,5,1, 1,3,1, 1,2,1, 1,1,1, 1,2,1,
        1,1,0, 2,1,2, 2,3,2, 2,5,2, 2,3,2, 1,1,0, 2,1,2, 1,2,2, 1,3,2, 1,1,2,
        1,6,0, 2,4,2, 1,5,1, 1,6,1, 2,4,2, 2,6,1, 1,1,1, 1,7,0, 2,5,2, 1,6,1, 1,7,1, 2,5,2, 2,7,2,
        1,7,0, 2,3,2, 1,6,1, 1,7,1, 2,5,2, 1,3,2, 1,1,0, 2,6,1, 1,2,1, 1,1,1, 1,7,1, 1,6,2, 1,5,2,
        1,6,0, 2,4,2, 1,5,1, 1,6,1, 2,6,1, 1,5,1, 1,6,1, 1,5,1, 1,6,0, 2,2,2, 1,5,1, 1,2,1, 2,5,2, 1,5,2,
        1,3,0, 2,1,2, 2,3,2, 2,5,2, 2,3,2, 1,1,0, 2,1,2, 1,2,2, 1,3,2, 1,1,2,
        1,6,0, 2,4,2, 1,5,1, 1,6,1, 2,4,2, 2,6,1, 1,1,1, 1,7,0, 2,5,2, 1,6,1, 1,7,1, 2,5,2, 2,7,2,
        1,7,0, 2,3,2, 1,6,1, 1,7,1, 2,5,2, 1,3,2, 1,1,0, 2,6,1, 1,2,1, 1,1,1, 1,7,1, 1,6,2, 1,5,2,
        1,6,0, 2,4,2, 1,3,1, 1,3,1, 2,6,2, 1,5,2, 1,6,0, 2,2,2, 1,3,1, 1,3,1, 2,5,2, 1,5,2,
        1,6,0, 2,6,2, 2,3,2, 2,6,2, 1,1,2, 1,3,4, 1,1,2, 1,2,2,
        1,3,0, 1,1,0, 2,6,0, 2,4,2, 1,6,1, 1,5,1, 2,6,2, 1,6,1, 2,5,1, 1,5,2, 1,6,1, 1,5,1, 2,5,2, 1,2,1, 1,3,1,
        2,3,2, 1,6,1, 1,5,1, 2,3,2, 1,6,1, 1,5,1, 2,6,2, 1,6,1, 1,5,1, 2,6,2, 1,3,2,
        1,2,0, 2,4,2, 1,1,1, 2,6,1, 2,4,1, 1,1,2, 2,6,1, 1,2,0, 2,2,1, 1,1,1, 2,6,2, 2,5,2, 1,1,2,
        1,3,0, 2,1,2, 2,3,2, 2,5,1, 1,4,1, 1,3,1, 1,2,1, 1,3,1, 1,2,3, 1,1,2, 1,2,2,
        1,3,0, 1,1,0, 2,6,0, 2,4,2, 2,6,1, 1,5,1, 2,6,2, 1,6,1, 1,5,1, 2,5,2, 1,6,1, 1,5,1, 2,5,2, 1,2,2,
        1,3,0, 2,3,2, 1,6,1, 1,5,1, 2,3,2, 1,6,1, 1,5,1, 2,6,2, 1,6,1, 1,5,1, 2,6,2, 1,3,2,
        1,2,0, 2,4,2, 1,1,1, 2,6,1, 2,4,1, 1,3,3, 1,2,0, 2,7,0, 2,5,2, 1,1,1, 2,6,1, 2,5,1, 1,1,3,
        1,1,0, 2,6,2, 2,1,2, 2,3,2, 2,6,2, 1,1,4, 2,6,1, 1,3,3,
        1,2,0, 2,4,2, 1,1,1, 2,6,1, 2,4,1, 1,3,3, 1,2,0, 2,7,0, 2,5,2, 1,1,1, 2,6,1, 2,5,1, 1,1,3,
        2,1,0, 1,5,0, 1,3,0, 1,1,4
    ]

    # 花海（没做完
    huahai = [
        1,1,2, 1,2,2, 1,3,2, 1,5,1, 1,5,1,
        2,1,2, 2,4,2, 2,6,2, 1,1,2, 1,3,0, 2,5,2, 1,2,2, 1,1,2, 1,2,1, 1,3,1,
        2,1,2, 2,3,2, 2,5,2, 2,3,2, 1,1,0, 2,1,2, 1,2,2, 1,3,2, 1,7,1, 1,1,1,
        2,4,2, 2,6,2, 1,1,2, 1,1,2, 1,7,2, 1,1,1, 1,7,3, 1,5,1, 1,6,1,
        2,1,2, 2,3,2, 2,5,2, 2,3,2, 1,1,0, 2,1,2, 1,2,2, 1,3,2, 1,5,1, 1,5,1,
        2,1,2, 2,4,2, 2,6,2, 1,1,2, 1,3,0, 2,3,2, 1,2,2, 1,1,2, 1,2,1, 1,1,1,
        2,3,2, 2,6,2, 1,1,4, 1,1,2, 1,2,2, 1,3,2, 1,5,1, 1,1,1,
        2,2,2, 2,4,2, 2,6,2, 1,1,2, 1,1,2, 2,7,2, 2,6,2, 2,7,2, 1,1,0, 2,1,2, 2,5,2, 1,4,4, 1,3,0, 2,5,0, 2,3,0, 2,1,4
    ]

    # 送别(长亭外古道边)
    songbie = [
        2,5,0, 2,1,0, 2,3,4, 2,3,2, 2,5,2, 1,1,0, 2,6,8,
        2,6,0, 2,4,4, 1,1,2, 2,6,2, 2,5,0, 2,1,0, 2,3,8,
        2,5,0, 2,1,0, 2,3,4, 2,1,2, 2,2,2, 2,3,0, 2,1,4, 2,2,2, 2,1,2,
        2,2,4, 2,5,4, 2,4,4, 2,3,4,
        2,5,0, 2,1,0, 2,3,2, 2,1,2, 2,3,2, 2,5,2, 1,1,2, 2,5,2, 2,3,2, 2,1,2,
        2,6,0, 2,3,2, 2,4,2, 1,1,2, 2,6,2, 2,5,0, 2,3,2, 2,3,2, 2,1,2, 2,3,2,
        2,5,0, 2,2,4, 2,2,2, 2,3,2, 2,4,2, 2,2,2,
        2,1,2, 2,3,2, 2,5,2, 1,1,2, 1,3,2, 1,1,2, 2,5,2, 2,3,2,
        2,6,0, 2,3,2, 2,1,2, 1,1,2, 2,4,2, 1,1,2, 2,6,2, 2,4,2, 2,6,2,
        2,7,0, 2,5,2, 2,2,2, 2,6,2, 2,7,2, 1,1,0, 2,1,2, 2,3,2, 2,5,2, 2,3,2,
        2,6,0, 2,4,2, 2,7,2, 1,1,2, 2,6,2, 2,6,0, 2,3,2, 2,5,2, 2,3,2, 2,1,2,
        2,2,2, 2,5,2, 2,7,2, 1,2,2, 2,7,2, 2,5,2, 2,4,2, 2,3,2,
        2,5,0, 2,3,0, 2,1,2, 2,1,2, 2,3,2, 2,5,2, 1,1,2, 2,5,2, 2,3,2, 2,1,2,
        2,6,0, 2,3,2, 2,4,2, 1,1,2, 2,6,2, 2,5,0, 2,3,2, 2,3,2, 2,1,2, 2,3,2,
        2,5,0, 2,2,4, 2,2,2, 2,3,2, 2,4,2, 2,2,2,
        2,1,6
    ]
    # 新年好
    xinnianhao = [
        1,1,2, 1,1,2,
        1,1,0, 2,1,2, 2,3,2, 2,5,2, 2,3,2, 1,3,2, 1,3,2,
        1,3,0, 2,1,2, 2,3,2, 1,1,0, 2,5,2, 2,3,2, 1,1,2, 1,3,2,
        1,5,0, 2,1,2, 2,3,2, 2,5,0, 1,5,2, 2,3,2, 1,4,2, 1,3,2,
        2,5,0, 2,7,0, 1,2,2, 2,5,2, 2,7,2, 2,5,2, 1,2,2, 1,3,2,
        2,4,0, 1,4,2, 2,6,2, 1,1,0, 1,4,2, 2,6,2, 1,3,2, 1,2,2,
        1,3,0, 2,1,2, 2,3,2, 1,1,0, 2,5,2, 2,3,2, 1,1,2, 1,3,2,
        1,2,0, 2,7,0, 2,5,0, 2,4,2, 2,2,2, 2,5,2, 2,2,2, 2,7,2, 1,2,2,
        1,1,0, 2,5,0, 2,3,0, 2,1,8
    ]
    # 欢乐颂
    huanlesong = [
        1,3,0, 2,1,2, 2,3,2, 1,3,2, 2,3,2, 1,4,2, 2,3,2, 1,5,2, 2,3,2,
        2,5,0, 1,5,2, 2,7,2, 1,4,2, 2,7,2, 1,3,2, 2,7,2, 1,2,2, 2,7,2,
        1,1,0, 2,6,2, 2,3,2, 1,1,2, 2,3,2, 1,2,2, 2,3,2, 1,3,2, 2,3,2,
        1,3,0, 2,5,2, 2,7,2, 2,5,2, 1,2,2, 1,2,0, 2,2,2, 2,7,2, 2,5,2, 2,2,2,
        1,3,0, 2,1,2, 2,3,2, 1,3,2, 2,3,2, 1,4,2, 2,3,2, 1,5,2, 2,3,2,
        2,5,0, 1,5,2, 2,7,2, 1,4,2, 2,7,2, 1,3,2, 2,7,2, 1,2,2, 2,7,2,
        1,1,0, 2,6,2, 2,3,2, 1,1,2, 2,3,2, 1,2,2, 2,3,2, 1,3,2, 2,3,2,
        1,2,0, 2,7,0, 2,5,2, 2,2,2, 2,5,2, 1,1,2, 1,1,0, 2,1,2, 2,3,2, 2,5,2, 2,3,2,
        1,2,0, 2,7,0, 2,5,2, 2,2,2, 1,2,2, 2,2,2, 1,3,0, 1,1,0, 2,6,2, 2,3,2, 1,1,2, 2,3,2,
        1,2,0, 2,7,0, 2,5,2, 2,2,2, 1,3,2, 1,4,2, 1,3,0, 1,1,0, 2,6,2, 2,3,2, 1,1,2, 2,3,2,
        1,2,0, 2,7,0, 2,5,2, 2,2,2, 1,3,2, 1,4,2, 1,3,0, 1,1,0, 2,6,2, 2,3,2, 1,2,2, 2,3,2,
        1,1,0, 2,2,2, 2,4,2, 1,2,2, 2,4,2, 2,5,0, 2,2,2, 2,4,2, 2,3,2, 2,2,2,
        1,3,0, 2,1,2, 2,3,2, 1,3,2, 2,3,2, 1,4,2, 2,3,2, 1,5,2, 2,3,2,
        2,5,0, 1,5,2, 2,7,2, 1,4,2, 2,7,2, 1,3,2, 2,7,2, 1,2,2, 2,7,2,
        1,1,0, 2,6,2, 2,3,2, 1,1,2, 2,3,2, 1,2,2, 2,3,2, 1,3,2, 2,3,2,
        1,2,0, 2,7,0, 2,5,2, 2,2,2, 2,5,2, 1,1,2, 1,1,0, 2,5,0, 2,3,0, 2,1,2
    ]
    guyongzhe = [
        # 2,2,2, 3,7,2, 2,1,2, 3,6,2, 2,2,2, 3,7,2, 2,1,2, 3,6,2,
        # 2,2,2, 3,7,2, 2,1,2, 3,6,2, 2,2,2, 3,7,2, 2,1,2, 3,6,2,
        # 2,2,2, 3,7,2, 2,1,2, 3,6,2, 2,2,2, 3,7,2, 2,1,2, 3,6,2,
        # 2,2,2, 3,7,2, 2,1,2, 3,6,2, 2,2,2, 3,7,2, 2,1,2, 3,6,2,
        # 2,3,13, 2,1,1, 2,2,1, 2,1,1, 2,3,11, 2,1,1, 2,2,1, 2,1,1, 2,2,1, 2,3,1, 3,6,3, 2,1,1, 3,6,3, 2,1,1, 3,6,3, 2,1,1, 2,2,2, 2,1,2, 
        # 3,7,16, 2,3,13, 2,1,1, 2,2,1, 2,1,1, 2,3,11, 2,1,1, 2,2,1, 2,1,1, 2,2,1, 2,3,1, 3,6,3, 2,1,1, 3,6,3, 2,1,1, 3,6,3, 2,1,1, 2,3,2, 2,2,2,
        3,7,16, 3,6,1, 2,1,1, 2,6,3, 2,6,1, 2,6,1, 2,5,1, 2,6,2, 2,6,1, 2,5,1, 2,6,1, 2,5,1, 2,6,1, 2,5,2, 2,3,13, 3,6,1, 2,1,1, 2,6,3, 2,6,1, 2,6,1, 2,5,1, 2,6,1, 2,5,1, 2,7,3, 2,7,1, 2,7,1, 2,6,1, 2,7,3,
        2,6,2, 2,3,10, 2,3,1, 2,5,1, 2,3,1, 2,2,3, 2,3,1, 2,2,3, 2,3,1, 2,2,3, 2,3,1, 2,5,1, 2,3,1, 2,5,1, 2,3,1, 2,2,3, 2,3,1, 2,2,3, 2,3,1, 2,2,6, 2,1,1, 2,2,1, 2,3,2, 3,6,2, 2,1,2, 2,3,2, 2,2,3, 2,3,1, 2,2,2, 2,1,2,
        3,6,14, 2,6,1, 2,7,1, 1,1,1, 1,2,1, 2,7,1, 1,1,1, 1,1,2, 1,1,1, 2,7,1, 1,1,1, 1,2,1, 1,7,1, 1,1,1, 1,1,2, 1,1,1, 1,2,1, 1,3,1, 1,2,1, 1,3,1, 1,2,1, 1,3,2, 1,3,1, 1,2,1, 1,3,2, 1,5,2, 1,3,2, 2,6,1, 2,7,1, 1,1,1, 1,2,1, 2,7,1, 1,1,1, 1,1,2, 1,1,1, 2,7,1, 1,1,1, 1,2,1, 2,7,1, 1,1,1, 1,1,2, 1,1,1, 1,2,1,
        1,3,1, 1,2,1, 1,3,1, 1,2,1, 1,3,2, 1,3,1, 1,2,1, 1,3,2, 1,5,2, 1,3,2, 1,5,2, 1,3,3, 1,5,1, 1,3,3, 1,5,1, 1,3,1, 1,5,1, 1,6,1, 1,3,1, 1,5,2, 1,5,2, 1,3,3, 1,5,1, 1,3,3, 1,5,1, 1,3,1, 1,5,1, 1,6,1, 1,3,1, 1,5,2, 1,5,1, 1,5,1, 1,3,2, 1,2,2, 1,2,2, 1,1,1, 1,3,3, 1,2,2, 1,2,2, 1,1,1, 1,1,15,
        1,5,1, 1,5,1, 1,3,2, 1,2,2, 1,2,2, 1,1,1, 1,3,3, 1,2,2, 1,2,2, 1,1,1, 1,1,1
    ]
    quku = [liangzhilaohu,tiankongzhicheng,qinghuaci,xiaoxingyun,maliyanggao,qifengle,huahai,songbie,xinnianhao,huanlesong,guyongzhe]
    time.sleep(5)
    # if song == 'liangzhilaohu':
    #     puzi = liangzhilaohu
    # if song == 'tiankongzhicheng':
    #     puzi = tiankongzhicheng
    # if song == 'qinghuaci':
    #     puzi = qinghuaci
    # if song == 'xiaoxingyun':
    #     puzi = xiaoxingyun
    # if song == 'maliyanggao':
    #     puzi = maliyanggao
    # if song == 'qifengle':
    #     puzi = qifengle
    for i,val in enumerate(quku[song-1]):
        if i%3==0:
            y_pos = y_start_pos + (val-1) * y_off
        if i%3==1:
            x_pos = x_start_pos + (val-1) * x_off
        if i%3==2:
            t_interval = val * time_interval
            x,y = x_pos,y_pos
            left_click(win_rect[0]+x+x_pad,win_rect[1]+y+y_pad,1)
            print(x_pos,y_pos)
            time.sleep(t_interval)
            # break
if __name__ == '__main__':
    is_answered = 1
    # 获取配置文件
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    make_print_to_file(path='./log/')
    
    # 初始化ocr模型
    # ocr = OCRImp(conf_data)

    # 初始化匹配器(题库)
    data_matcher = DataMatcher(conf_data)

    # 截屏
    screen = ScreenImp(conf_data)
    sel = '1'
    epoch_num = 20

    sel = input('魔法史还是学院活动？\n1.魔法史 2.学院活动 3.退出 4.弹钢琴\n')
    if sel == '3':
        exit()
    if sel == '4':
        song = input('选曲？\n1.两只老虎 2.天空之城 3.青花瓷 4.小幸运 5.玛丽羊 6.起风了 7.花海 8.送别 9.新年好 10.欢乐颂 11.孤勇者\n')
        sudu = input('速度？\n1.慢 2.正常 3.快\n')
        play_piano(song=int(song), sudu=int(sudu)) # 歌名
        exit()
    iter = '0'
    iter = input("一轮多少题？\n0-10题1-15题\n")
    if iter == '0':
        iter_num = 15
    else:
        iter_num = 10
    
    epoch = input('进行几次？\n默认3次\n')
    
    if(epoch != ''):
        epoch_num = int(epoch)
    question_num = 0
    while True:
        if(question_num==iter_num):
            epoch_num -= 1
            question_num = 0
        if epoch_num == 0:
            break
        # time.sleep(0.1)
        win_rect, img= screen.get_screenshot()
        # img = cv2.imread(screen.ravenclaw_imgpath)

        # 识别计时器
        img_countdown = screen.get_countdownBtn(img)
        result_countdown = ocr.ocr(img_countdown)
        content_countdown = ocr.ocr_content(result_countdown)
        content_countdown = filterLine(content_countdown)
        # print(content_countdown)
        countdown_num = -1
        if (content_countdown!=None) and len(content_countdown) > 0 and content_countdown[0].isdigit():
            countdown_num = int(content_countdown[0])
        else: # 没识别到计时器，就识别开始和继续按钮
            if sel == '1': # 魔法史
                flag1 = is_start(img, '匹配上课')
                flag2 = is_start(img, '准备')
                flag3 = is_start(img, '上课')
                if flag1 or flag2 or flag3: # 识别到了就跳过，重新截图
                    time.sleep(1)
                    continue
            elif sel == '2': # 学院活动
                flag1 = is_start(img, '学院活动匹配')
                flag2 = is_start(img, '准备')
                flag3 = is_start(img, '上课')
                if flag1 or flag2 or flag3: # 识别到了就跳过，重新截图
                    time.sleep(1)
                    continue
            # 识别继续按钮
            img_continue = screen.get_continueBtn(img)
            result_continue = ocr.ocr(img_continue)
            content_continue = ocr.ocr_content(result_continue)
            content_continue = filterLine(content_continue)
            if len(content_continue)>0 and content_continue[0] == '点击继续':
                x, y = 1200, 890
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                if sel == '2':
                    time.sleep(10)
                    left_click(win_rect[0]+x,win_rect[1]+y,1)
                continue
        # cv2.imwrite('./img/harry_state_1216.png',img)
        if countdown_num == 12:
            question_num += 1
            # print('第%d题'%question_num)
            is_answered = 0
            time.sleep(0.1) #学院活动出题满了这一会，不然扫描不到题目
            win_rect, img= screen.get_screenshot()
            # img = cv2.imread(screen.ravenclaw_imgpath)

            # cv2.imwrite('./img/harry1216.png',img)

            res = get_question_answer(img)
            if len(res) >0:
                print('这题选',chr(ord('A')+int(res[0][2])))
                x,y = coordinate[res[0][2]][0], coordinate[res[0][2]][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
                time.sleep(8)
                # win_rect, img = screen.get_screenshot() # 别人的答案没稳定下来，重新截图
                # import datetime
                # fileName = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.png'
                # cv2.imwrite('img/harry_'+fileName,img) # 测试状态图（抄答案坐标）
            else:
                time.sleep(1)
                print('抄答案吧！')
            continue
        if (is_answered == 0 and countdown_num > 3):
            if countdown_num >=10:
                win_rect, img = screen.get_screenshot() # 别人的答案没稳定下来，重新截图
            # img = cv2.imread(screen.ravenclaw_imgpath)
            if sel == '1':
                person1State, person2State, person3State = screen.get_personState(img)
            elif sel == '2':
                person1State, person2State, person3State = screen.get_ravenclaw_personState(img)
            resultPerson1 = ocr.ocr(person1State)
            resultPerson2 = ocr.ocr(person2State)
            resultPerson3 = ocr.ocr(person3State)
            contentPerson1 = ocr.ocr_content(resultPerson1)
            contentPerson2 = ocr.ocr_content(resultPerson2)
            contentPerson3 = ocr.ocr_content(resultPerson3)
            state1 = filterPersonState(contentPerson1)
            state2 = filterPersonState(contentPerson2)
            state3 = filterPersonState(contentPerson3)
            if state1 == 'A' or state2 == 'A' or state3 == 'A':
                print('这题抄A')
                x,y = coordinate[0][0], coordinate[0][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            elif state1 == 'B' or state2 == 'B' or state3 == 'B':
                print('这题抄B')
                x,y = coordinate[1][0], coordinate[1][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            elif state1 == 'C' or state2 == 'C' or state3 == 'C':
                print('这题抄C')
                x,y = coordinate[2][0], coordinate[2][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            elif state1 == 'D' or state2 == 'D' or state3 == 'D':
                print('这题抄D')
                x,y = coordinate[3][0], coordinate[3][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            else:
            #     pass
                print('state1:',contentPerson1)
                print('state2:',contentPerson2)
                print('state3:',contentPerson3)
                print('答案都没得抄！')
            # 错题就先不计了
            time.sleep(0.9)
            continue
        elif (is_answered == 0 and countdown_num == 3):
            print('这题盲猜C')
            x,y = coordinate[2][0], coordinate[2][1]
            left_click(win_rect[0]+x,win_rect[1]+y,2)
            is_answered = 2 # 表示没得抄，盲猜
        if is_answered == 2 and countdown_num == 0:
            in_rect, img = screen.get_screenshot()
            import datetime
            fileName = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.png'
            
            # from PIL import Image
            # im = Image.fromarray(img)
            # im.save('img/harry_'+fileName)
            cv2.imwrite('img/harry_'+fileName, img)
            time.sleep(2)