#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径

from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState, maguafilterQuestion, filtertimeLine
from UniversalAutomaticAnswer.match.matchImp import DataMatcher, match_options
# from UniversalAutomaticAnswer.httpImp.search import searchImp
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
def write_new_question(question=None, options=None, answer_flag=None):
    import time
    # 格式化成2021-12-01形式
    time_str = time.strftime("%Y-%m-%d", time.localtime()) 
    # print(time_str)
    line = '0 ' + question + ' ' + options[answer_flag] + ' '
    d = [line,]
    df = pd.DataFrame(data=d)
    # print(line)
    
    import os
    if not os.path.exists('./new_questions/'): # 判断文件夹是否存在，不存在则创建文件夹
        os.mkdir('./new_questions/')
    # 新题目按时间新建文件，追加的方式保留当天的新题
    df.to_csv('./new_questions/'+time_str+'_harry_questions.csv', mode='a', header=False, index=None)

def left_click(x,y,times=1):
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        times -= 1
    # print('左键点击',x,y)

def is_start(img, str_start):
    img_start = screen.get_brower_startMatchBtn(img)
    result_start = ocr.ocr(img_start)
    content_start = ocr.ocr_content(result_start)
    content_start = filterLine(content_start)
    if len(content_start)>0 and str_start == content_start[0]:
        x,y = 925,588
        left_click(x,y,2)
        # left_click(x+init_w,y+init_h,2) # 点击匹配上课
        time.sleep(3)
        return True
    return False

def ret_question_options(img):
    # 一次答题流程
    res = []
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_brower_questionAndoptionsBtn(img)
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
    # print(contentq)

    question, optiona,optionb,optionc,optiond = '', '', '', '' ,''
    if len(filterQuestion(contentq))>0:
        question = maguafilterQuestion(contentq)[0]
    # print(question)
    if len(question)==0:
        # print('题目未识别！')
        # print('源数据为：',resultq)
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
    # print('ocr结果:', [question,options])
    return question,options

def get_question_answer(img):
    # 一次答题流程
    res = []
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_brower_questionAndoptionsBtn(img)
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
    if(len(contentq)>0):
        print(contentq)

    question, optiona,optionb,optionc,optiond = '', '', '', '' ,''
    if len(filterQuestion(contentq))>0:
        question = filterQuestion(contentq)[0]
    print(question)
    if len(question)==0:
        # print('题目未识别！')
        # print('源数据为：',resultq)
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
        # time.sleep(2)
        return res
    else:
        print('题库匹配结果:', answer_list[0])
        answer = answer_list[0][0][1]
        res = match_options(answer, options)
        if len(res) == 0:
            print('选项OCR出错')
            # time.sleep(2)
            return res
        print('选项匹配结果:', res)
        return res

# def getclipboardimg():
#     win32api.keybd_event(win32con.VK_SNAPSHOT,0)
#     time.sleep(0.1)
#     from PIL import ImageGrab,Image
#     im = ImageGrab.grabclipboard()
#     # PIL.BmpImagePlugin.DibImageFile to Image
#     im = Image.frombytes('RGB', im.size, im.tobytes())
#     import numpy as np
#     img = np.array(im)
#     print(img.shape)
#     img = img[win_rect_mul_rightgoogle_dashen[1]:win_rect_mul_rightgoogle_dashen[3],2869:win_rect_mul_rightgoogle_dashen[0],::]
#     return img


coordinate = [
    [474,530],
    [954,530],
    [474,600],
    [954,600]
]
coordinate_mul = [
    [366,753],
    [753,753],
    [366,810],
    [753,810]
]
padd2slef = -155
padd2wy = -195 # 指顶110 居中265 -155 网易云游戏300
time_chutdown = 12
hwnd_title = dict() # 使用upadate的方式更新字典


import win32gui
def get_all_hwnd(hwnd,nouse):
  if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
    hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})

def get_Chrome_window_rect(hwnd_title, target_title):
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h,t in hwnd_title.items():
        if target_title in t and 'Chrom' in t: # 使用模糊搜索，需要的话可以改成正则
            return win32gui.GetWindowRect(h)
    return None

def get_Edge_window_rect(hwnd_title, target_title):
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h,t in hwnd_title.items():
        if target_title in t and 'Edge' in t:
            return win32gui.GetWindowRect(h)
    return None
win_rect_mul_fulledge_dashen = get_Chrome_window_rect(hwnd_title,"大神云游戏")
# win_rect_mul_fulledge_dashen = get_Edge_window_rect(hwnd_title,"大神云游戏")
if win_rect_mul_fulledge_dashen is not None:
    init_w = win_rect_mul_fulledge_dashen[0]+252
    init_h = win_rect_mul_fulledge_dashen[1]+162
else:
    exit()
# init_w,init_h = win_rect_mul_fulledge_dashen[0]+252,win_rect_mul_fulledge_dashen[1]+162

def screencrop():
    im = ImageGrab.grab()
    im = Image.frombytes('RGB', im.size, im.tobytes())
    img = np.array(im)
    h,w=804,1431
    img = img[init_h:init_h+h,init_w:init_w+w]
    return img

# """
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
    sel = '1'
    epoch_num = 1

    sel = input('魔法史还是学院活动？\n1.魔法史 2.学院活动 3.退出 4.魔法史双开 5.魔法史多开 6.学院活动双开 7.学院活动多开 8.麻瓜研究 9.社团答题\n')
    if sel == '3':
        exit()
    
    if sel == '4' or sel == '5' or sel == '6' or sel == '7':
        win_rect_mul_leftgoogle_yunyouxi = get_Chrome_window_rect(hwnd_title,"网易云游戏平台 - Google Chrome")
    if sel == '5' or sel == '7':
        win_rect_mul_rightgoogle_dashen = get_Edge_window_rect(hwnd_title,"大神云游戏")
    # if sel == '4' or sel == '5' or sel == '6' or sel == '7':
    #     import win32gui
    #     hwnd_mul_google = win32gui.FindWindow(None, "网易云游戏平台 - Google Chrome")
    #     win_rect_mul_google = win32gui.GetWindowRect(hwnd_mul_google)
    # if sel == '5' or sel == '7':
    #     import win32gui
    #     hwnd_mul_edge = win32gui.FindWindow(None, "大神云游戏 - Google Chrome")
    #     win_rect_mul_rightgoogle_dashen = win32gui.GetWindowRect(hwnd_mul_edge)
    # 网易云游戏平台 - 个人 - Microsoft​ Edge
    chutdown = '1'
    chutdown = input('一题多少秒？\n0、10秒 1、12秒 2、20秒\n')
    if chutdown == '0':
        time_chutdown=10
    if sel == '9':
        time_chutdown=20
    iter = '1'
    iter = input("一轮多少题？\n0-10题1-15题2-25\n")
    if iter == '0':
        iter_num = 10
    elif iter == '2':
        iter_num = 25
    else: iter_num = 15
    epoch = input('进行几次？\n默认3次\n')
    
    if(epoch != ''):
        epoch_num = int(epoch)
    question_num = 0
    chao_question,chao_options = None,None
    while True:
        if(question_num==iter_num):
            epoch_num -= 1
            question_num = 0
        if epoch_num == 0:
            break
        img = screencrop()

        # 识别计时器
        if sel == '8':
            img_countdown = screen.get_brower_maguacountdownBtn(img)
        else:
            img_countdown = screen.get_brower_countdownBtn(img)
        result_countdown = ocr.ocr(img_countdown)
        content_countdown = ocr.ocr_content(result_countdown)
        content_countdown = filterLine(content_countdown)
        # print(content_countdown)
        countdown_num = -1
        if (content_countdown!=None) and len(content_countdown) > 0 and content_countdown[0].isdigit():
            countdown_num = int(content_countdown[0])
            # print(countdown_num)
        else: # 没识别到计时器，就识别开始和继续按钮
            # 识别奖励的中下部分继续按钮，然后识别下一轮的匹配按钮
            img_continue = screen.get_brower_centercontinueBtn(img)
            result_continue = ocr.ocr(img_continue)
            content_continue = ocr.ocr_content(result_continue)
            content_continue = filterLine(content_continue)
            if len(content_continue)>0 and content_continue[0] in '点击继续': # 655,750,770,790
                x, y = 639, 617
                left_click(x,y,4)
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                if sel == '2' or sel == '6' or sel == '7':
                    time.sleep(4)
                    x, y = 639, 617
                    left_click(x,y,2)
                if sel == '6' or sel == '7':
                    x, y = 803, 903
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                    time.sleep(2)
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '7':
                    x, y = 803, 903
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                    time.sleep(2)
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                continue
                
            # 识别右下点击继续按钮
            img_continue = screen.get_brower_continueBtn(img)
            result_continue = ocr.ocr(img_continue)
            content_continue = ocr.ocr_content(result_continue)
            content_continue = filterLine(content_continue)
            if len(content_continue)>0:
                print(content_continue)
            if len(content_continue)>0 and content_continue[0] == '点击继续':
                x,y = 908, 617
                left_click(x,y,2) # 点击继续
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                if sel == '2' or sel == '6' or sel == '7':
                    time.sleep(4)
                    x, y = 908, 617
                    left_click(x,y,2) # 点击继续
                if sel == '6' or sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                    time.sleep(2)
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                    time.sleep(2)
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                continue
            
            # 识别失败返回按钮
            img_continue = screen.get_brower_returnBtn(img)
            result_continue = ocr.ocr(img_continue)
            content_continue = ocr.ocr_content(result_continue)
            content_continue = filterLine(content_continue)
            if len(content_continue)>0 and content_continue[0] == '返回':
                x,y = 671, 594
                left_click(x,y,2) # 点击继续
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                if sel == '2' or sel == '6' or sel == '7':
                    time.sleep(4)
                    x, y = 671, 594
                    left_click(x,y,2) # 点击继续
                if sel == '6' or sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                    time.sleep(2)
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                    time.sleep(2)
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                continue

            if sel == '1' or sel == '4' or sel == '5' or sel == '6' or sel == '7' or sel == '8': # 魔法史
                flag0 = is_start(img, '学院活动匹配')
                flag1 = is_start(img, '匹配上课')
                flag2 = is_start(img, '准备')
                flag3 = is_start(img, '上课')
                if flag0 or flag1 or flag2 or flag3: # 识别到了就跳过，重新截图
                    time.sleep(1)
                    if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                        x, y = 800,800
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,1)
                    if sel == '5' or sel == '7':
                        x, y = 800,800
                        left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,1)
                    continue
            elif sel == '2': # 学院活动
                flag1 = is_start(img, '学院活动匹配')
                flag2 = is_start(img, '准备')
                flag3 = is_start(img, '上课')
                if flag1 or flag2 or flag3: # 识别到了就跳过，重新截图
                    time.sleep(1)
                    continue
            
            
        # cv2.imwrite('./img/harry_state_1216.png',img)
        if countdown_num == time_chutdown:
            question_num += 1
            if sel == '9':
                x,y = coordinate[0][0], coordinate[0][1]  # 进去，先盲猜A，A没人选，大概率能首抢
                left_click(x,y,2) # 点击选项
            # print('第%d题'%question_num)
            is_answered = 0
            # time.sleep(0.1) # 测试 学院活动出题满了这一会，不然扫描不到题目
            # img = screencrop() # 测试 
            # cv2.imwrite('./img/harry1216.png',img)
            s_time = time.time()*1000
            res = get_question_answer(img) # 保证优先抢答
            if len(res) ==0:
                img = screencrop() # 保证扫描到题目
                res = get_question_answer(img)
            print('ocr时间: {}ms'.format(time.time()*1000-s_time))
            if len(res) >0:
                print('这题选',chr(ord('A')+int(res[0][2])))
                x,y = coordinate[res[0][2]][0], coordinate[res[0][2]][1]
                left_click(x,y,2) # 点击选项
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x,y = coordinate_mul[res[0][2]][0], coordinate_mul[res[0][2]][1]
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,2)
                if sel == '5' or sel == '7':
                    x,y = coordinate_mul[res[0][2]][0], coordinate_mul[res[0][2]][1]
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,2)
                is_answered = 1
                chao_question,chao_options = ret_question_options(img)
                time.sleep(2)
                # win_rect, img = screen.get_screenshot() # 别人的答案没稳定下来，重新截图
                # cv2.imwrite('./img/harry_test_1218.png',img)
            else:
                chao_question,chao_options = ['',['','','','']]
                time.sleep(1)
                print('抄答案吧！')
            continue
        if (is_answered == 0 and countdown_num >= 5):
            # if countdown_num >=10:
            #     win_rect, img = screen.get_screenshot() # 别人的答案没稳定下来，重新截图
            # img = cv2.imread(screen.ravenclaw_imgpath)
            if sel == '1' or sel == '4' or sel == '5': # 魔法史
                person1State, person2State, person3State = screen.get_brower_personState(img)
            elif sel == '2' or sel == '6' or sel == '7':
                person1State, person2State, person3State = screen.get_ravenclaw_personState(img)
            elif sel == '8':
                person1State, person2State, person3State = screen.get_brower_maguapersonState(img)
            resultPerson1 = ocr.ocr(person1State)
            resultPerson2 = ocr.ocr(person2State)
            resultPerson3 = ocr.ocr(person3State)
            # print(resultPerson1)
            # print(resultPerson2)
            # print(resultPerson3)
            contentPerson1 = ocr.ocr_content(resultPerson1)
            contentPerson2 = ocr.ocr_content(resultPerson2)
            contentPerson3 = ocr.ocr_content(resultPerson3)
            state1 = filterPersonState(contentPerson1)
            state2 = filterPersonState(contentPerson2)
            state3 = filterPersonState(contentPerson3)
            relstate = -1
            if state1 == 'A' or state2 == 'A' or state3 == 'A':
                print('这题抄A')
                relstate = 0
                x,y = coordinate[0][0], coordinate[0][1]
                left_click(x,y,2) # 点击选项 # 抄答案
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = coordinate_mul[0][0], coordinate_mul[0][1]
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[0][0], coordinate_mul[0][1]
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                is_answered = 1
            elif state1 == 'B' or state2 == 'B' or state3 == 'B':
                print('这题抄B')
                relstate = 1
                x,y = coordinate[1][0], coordinate[1][1]
                left_click(x,y,2) # 点击选项 # 抄答案
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = coordinate_mul[1][0], coordinate_mul[1][1]
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[1][0], coordinate_mul[1][1]
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                is_answered = 1
            elif state1 == 'C' or state2 == 'C' or state3 == 'C' or state1 == 'c' or state2 == 'c' or state3 == 'c':
                print('这题抄C')
                relstate = 2
                x,y = coordinate[2][0], coordinate[2][1]
                left_click(x,y,2) # 点击选项 # 抄答案
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = coordinate_mul[2][0], coordinate_mul[2][1]
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[2][0], coordinate_mul[2][1]
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                is_answered = 1
            elif state1 == 'D' or state2 == 'D' or state3 == 'D':
                print('这题抄D')
                relstate = 3
                x,y = coordinate[3][0], coordinate[3][1]
                left_click(x,y,2) # 点击选项 # 抄答案
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                is_answered = 1
            else:
            #     pass
                print('state1:',contentPerson1)
                print('state2:',contentPerson2)
                print('state3:',contentPerson3)
                print('答案都没得抄！')
            # 错题就先不计了
            if is_answered == 1:
                question,options = ret_question_options(img)
                write_new_question(question, options, relstate)
            time.sleep(0.5)
            continue
        elif (is_answered == 0 and countdown_num == 4):
        #     searchimp = searchImp(conf_data)
        #     question,options = ret_question_options(img)
        #     print(question,options)
        #     ans_baidu = searchimp.baidu(question, options)
        #     print('百度答案：',ans_baidu)
        #     print('百度选：',chr(ord('A')+int(ans_baidu[0][2])))
        #     tmp = int(ans_baidu[0][2])
        #     x,y = coordinate[tmp][0], coordinate[tmp][1]
        #     left_click(win_rect[0]+x,win_rect[1]+y,2)
        #     if sel == '4' or sel == '5' or sel == '6' or sel == '7':
        #         x,y = coordinate[tmp][0], coordinate[tmp][1]
        #         left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,2)
        #     if sel == '5' or sel == '7':
        #         x,y = coordinate[tmp][0], coordinate[tmp][1]
        #         left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,2)

            # print('这题盲猜C')
            # x,y = coordinate[2][0], coordinate[2][1]
            # left_click(win_rect[0]+x,win_rect[1]+y,2)
            # if sel == '4' or sel == '5' or sel == '6' or sel == '7':
            #     x, y = coordinate_mul[2][0], coordinate_mul[2][1]
            #     left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
            # if sel == '5' or sel == '7':
            #     x, y = coordinate_mul[2][0], coordinate_mul[2][1]
            #     left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
            is_answered = 2 # 表示没得抄，盲猜
        if is_answered == 2:
            print('这题盲猜D')
            x,y = coordinate[3][0], coordinate[3][1]
            left_click(x,y,2) # 点击选项 # 盲猜
            if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
            if sel == '5' or sel == '7':
                x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
            # in_rect, img = screen.get_screenshot()
            # time.sleep(3)
            img = screencrop()
            import datetime
            fileName = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.png'
            
            # from PIL import Image
            # im = Image.fromarray(img)
            # im.save('img/harry_'+fileName)
            img = img[:,:,::-1]
            cv2.imwrite('img/harry_dashen_'+fileName, img)
            # time.sleep(2)
            is_answered = 3
            if chao_question == '':
                continue
            correctA = img[610:670,607:667] 
            correctB = img[610:670,1307:1367]
            correctC = img[710:770,607:667] 
            correctD = img[710:770,1307:1367] 
            # print(np.mean(correctA)) # 44.67 # 74.64
            # print(np.mean(correctB)) # 83.39 # 100.87
            # print(np.mean(correctC)) # 51.57 # 78.90
            # print(np.mean(correctD)) # # 92.98 # 82.33
            # question,options = ret_question_options(img)
            print(chao_question,chao_options)
            if 69<np.mean(correctA)<70:
                print('记录A')
                write_new_question(chao_question, chao_options, 0)
            elif 95<np.mean(correctB)<105:
                print('记录B')
                write_new_question(chao_question, chao_options, 1)
            elif 70<np.mean(correctC)<85:
                print('记录C')
                write_new_question(chao_question, chao_options, 2)
            elif 87<np.mean(correctD)<97:
                print('记录D')
                write_new_question(chao_question, chao_options, 3)             
            
# """