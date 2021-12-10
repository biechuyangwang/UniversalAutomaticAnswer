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

    fileName = datetime.datetime.now().strftime('day'+'%Y_%m_%d')
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
    if len(content_start)>0 and content_start[0] == str_start:
        time.sleep(5)
        x, y = 1300, 840
        left_click(win_rect[0]+x,win_rect[1]+y,2)
        return True
    return False

def get_question_answer(img):
    # 一次答题流程
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

    question = filterQuestion(contentq)[0]
    optiona = filterLine(contenta)[0]
    optionb = filterLine(contentb)[0]
    optionc = filterLine(contentc)[0]
    optiond = filterLine(contentd)[0]
    options = [optiona, optionb, optionc, optiond]
    print('ocr结果:', [question,options])

    answer_list = list(data_matcher.get_close_match(question))
    if len(answer_list) == 0 or list(answer_list[0])[1] < 60:
        print('没有匹配到题库')
        return []
    print('题库匹配结果:', answer_list[0])
    answer = answer_list[0][0][1]
    res = match_options(answer, options)
    print('选项匹配结果:', res)
    return res

is_answered = True
coordinate = [
    [500,734],
    [1200,734],
    [500,846],
    [1200,848]
]
if __name__ == '__main__':

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

    sel = input('魔法史还是学院活动？1.魔法史 2.学院活动 3.退出\n')
    while True:
        win_rect, img= screen.get_screenshot()
        # img = cv2.imread(screen.ravenclaw_imgpath)

        if is_answered and sel == '1': # 魔法史
            flag = is_start(img, '匹配上课')
            if(flag): # 识别到了就跳过，重新截图
                continue
        elif is_answered and sel == '2': # 学院活动
            flag = is_start(img, '学院活动匹配')
            if(flag): # 识别到了就跳过，重新截图
                continue
        else:
            exit()
        # 点击继续
        if is_answered:
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
        
        img_countdown = screen.get_countdownBtn(img)
        result_countdown = ocr.ocr(img_countdown)
        content_countdown = ocr.ocr_content(result_countdown)
        content_countdown = filterLine(content_countdown)
        # print(content_countdown)
        countdown_num = 0
        if content_countdown!=None and len(content_countdown) > 0 and content_countdown[0].isdigit():
            countdown_num = int(content_countdown[0])         
        if countdown_num == 12:
            is_answered = False
            time.sleep(0.1)
            win_rect, img= screen.get_screenshot()
            # img = cv2.imread(screen.ravenclaw_imgpath)
            res = get_question_answer(img)
            if len(res) >0:
                print('这题选',chr(ord('A')+int(res[0][2])))
                x,y = coordinate[res[0][2]][0], coordinate[res[0][2]][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = True
                time.sleep(8)
            continue
        elif is_answered == False and countdown_num >=3:
            if countdown_num >=10:
                win_rect, img = screen.get_screenshot() # 别人的答案没稳定下来，重新截图
            # img = cv2.imread(screen.ravenclaw_imgpath)
            if sel == '1':
                person1State, person2State, person3State = screen.get_personState(img)
            elif sel == '2':
                person1State, person2State, person3State = screen.get_ravenclaw_personState(img)
            contentPerson1 = ocr.ocr_content(person1State)
            contentPerson2 = ocr.ocr_content(person2State)
            contentPerson3 = ocr.ocr_content(person3State)
            state1 = filterPersonState(contentPerson1)
            state2 = filterPersonState(contentPerson2)
            state3 = filterPersonState(contentPerson3)
            if state1 == 'A' or state2 == 'A' or state3 == 'A':
                print('这题抄A')
                x,y = coordinate[0][0], coordinate[0][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = True
            elif state1 == 'B' or state2 == 'B' or state3 == 'B':
                print('这题抄B')
                x,y = coordinate[1][0], coordinate[1][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = True
            elif state1 == 'C' or state2 == 'C' or state3 == 'C':
                print('这题抄C')
                x,y = coordinate[2][0], coordinate[2][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = True
            elif state1 == 'D' or state2 == 'D' or state3 == 'D':
                print('这题抄D')
                x,y = coordinate[3][0], coordinate[3][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = True
            # 错题就先不计了
            continue
        elif is_answered == False:
            print('这题盲猜C')
            x,y = coordinate[2][0], coordinate[2][1]
            left_click(win_rect[0]+x,win_rect[1]+y,2)
            is_answered = True

            







    