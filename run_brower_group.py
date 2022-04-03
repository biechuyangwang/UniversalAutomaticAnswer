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
#     img = img[win_rect_mul_edge[1]:win_rect_mul_edge[3],2869:win_rect_mul_edge[0],::]
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
# import win32gui
# hwnd_mul_google = win32gui.FindWindow(None, "网易云游戏平台 - Google Chrome")
# win_rect_mul_google = win32gui.GetWindowRect(hwnd_mul_google)
win_rect_mul_google = [0,1,2,3]
import win32gui
hwnd_mul_edge = win32gui.FindWindow(None, "大神云游戏 - Google Chrome")
win_rect_mul_dashen = win32gui.GetWindowRect(hwnd_mul_edge)
init_w,init_h = win_rect_mul_dashen[0]+252,win_rect_mul_dashen[1]+162

def screencrop():
    # from ctypes import windll
    # if windll.user32.OpenClipboard(None): # 打开剪切板 
    #     windll.user32.EmptyClipboard() # 清空剪切板
    #     windll.user32.CloseClipboard() # 关闭剪切板
    # win32api.keybd_event(win32con.VK_SNAPSHOT,0)
    # time.sleep(0.5)
    im = ImageGrab.grab()
    # im = ImageGrab.grabclipboard()
    # PIL.BmpImagePlugin.DibImageFile to Image
    im = Image.frombytes('RGB', im.size, im.tobytes())
    img = np.array(im)
    # 245,155, 1676,959
    # img = img[155:959,245:1676] 
    h,w=804,1431
    img = img[init_h:init_h+h,init_w:init_w+w]
    # print(img.shape) # (1080, 1920, 3)
    # print(win_rect_mul_dashen) # (-7, -7, 1288, 688)
    

    # print(win_rect_mul_google) # (1912, -8, 3848, 1048) 2053,103,3704,1040 h,w=937,1651
    # cv2.imwrite('img/harry_brower_group1.png', img) 
    # img = img[win_rect_mul_google[1]+111:win_rect_mul_google[3]-8,win_rect_mul_google[0]+141:win_rect_mul_google[2]-144,::-1]
    return img

"""
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

    # 初始化屏幕实例
    screen = ScreenImp(conf_data)

    # win32api.keybd_event(win32con.VK_SNAPSHOT,0)
    # time.sleep(0.1)
    # im = ImageGrab.grabclipboard()
    # # PIL.BmpImagePlugin.DibImageFile to Image
    # im = Image.frombytes('RGB', im.size, im.tobytes())
    # img = np.array(im)
    # print(img.shape) # (1080, 3840, 3)
    # print(win_rect_mul_google) # (1912, -8, 3848, 1048) 2053,103,3704,1040 h,w=937,1651
    # # cv2.imwrite('img/harry_brower_group1.png', img) 
    # img = img[win_rect_mul_google[1]+111:win_rect_mul_google[3]-8,win_rect_mul_google[0]+141:win_rect_mul_google[2]-144,::-1]
    img = screencrop() # 截图
    img_path = './img/harry_brower_dashen_crop{}.png'.format('1_shibai')
    img = cv2.imread(img_path)

    # cv2.imwrite('img/harry_brower_dashen_crop1_shibai.png', img)

    # 大神浏览器全屏魔法史
    # 1140,700,1340,750 匹配上课
    # img = img[700:750,1140:1340]
    # 680,10,740,70 # 计时器 11和2识别不了
    # img = img[10:70,680:740]
    # 160,422,780,525 # 问题
    # img = img[422:525,160:780]
    # 105,600,455,655 选项A 点击640,640
    # img = img[600:655,105:455]
    # 805,600,1155,655 选项B 点击1340,640
    # img = img[600:655,805:1155]
    # 105,700,455,755 选项C 点击640,740
    # img = img[700:755,105:455]
    # 805,700,1155,755 选项D 点击1340,740
    # img = img[700:755,805:1155]
    # 465,310,565,410 玩家1
    # 885,265,985,365 玩家2
    # 1035,230,1135,330 玩家3
    # img = img[310:410,465:565]
    # img = img[265:365,885:985]
    # img = img[230:330,1035:1135]
    # 1060,750,1175,790 点击继续 点击1180,770
    # img = img[750:790,1060:1175]
    # 655,750,770,790 # 中下点击继续
    # img = img[750:790,655:770]
    # 大神浏览器全屏麻瓜研究
    # 665,10,765,110 # 计时器 3和1识别不了
    # img = img[10:110,665:765]
    # 200,180,300,280
    # img = img[180:280,200:310,::-1]
    # 390,140,490,250
    # img = img[135:250,385:490]
    # 900,285,1000,395
    # img = img[285:395,890:1000]

    # 465,310,565,410 玩家1
    # 885,265,985,365 玩家2
    # 1035,230,1135,330 玩家3

    # 1300,830,1500,880 匹配上课
    # 1220,885,1340,920 课程结束后的点击继续
    # 783,23,870,110 计时器
    # 215,560,895,690 问题
    # 205,730,655,775 选项A 不包括英文 205,730,655,800 包括英文
    # 920,730,1370,775 选项B
    # 205,835,655,880 选项C
    # 920,835,1370,880 选项D
    # 260,215,370,320 玩家1
    # 460,185,560,290 玩家2
    # 1040,350,1140,455 玩家3
    # img = img[830:880,1300:1500]
    # img = img[885:920,1220:1340]
    # img = img[23:110,783:870] # 计时器
    # img = img[560:690,215:895] # 问题
    # img = img[730:800,205:655] # A
    # img = img[730:800,920:1370] # B
    # img = img[835:905,205:655] # C
    # img = img[835:905,920:1370] # D
    # img = img[215:320,260:370] # 玩家1
    # img = img[185:290,460:560] # 玩家2
    # img = img[350:455,1040:1140] # 玩家3
    # 660,715,760,755 失败返回 点击(671, 594)
    img = img[715:755,660:760]
    # cpos = win32api.GetCursorPos()
    # print(cpos)
    # 魔法史
    # 789,17,859,64 计时器
    # img = img[17:64,777:877,::-1] # 计时器
    # (46.3468085106383, 42.178936170212765, 24.879574468085107, 0.0) 12
    # (43.97468085106383, 40.09340425531915, 24.120212765957447, 0.0) 11
    # (57.38, 53.27872340425532, 33.282978723404256, 0.0) 10
    # (46.38404255319149, 43.12893617021277, 27.912340425531916, 0.0) 8
    # x = mean(img)
    # print(x)
    result = ocr.ocr(img)
    print(result)
    content = ocr.ocr_content(result)
    content = filterLine(content)
    # x,y = 1300,860
    # left_click(x+win_rect_mul_google[0]+141,y+win_rect_mul_google[1]+111,2) # 点击匹配上课
    # x,y = 1300,860
    # left_click(x+win_rect_mul_google[0]+141,y+win_rect_mul_google[1]+111,2) # 点击继续
    # time.sleep(20)
    # x = input('继续\n')
    # for i in range(30):
    #     img = screencrop()
    #     cv2.imwrite('img/harry_brower_dashen_crop_magua_'+str(i)+'.png', img)
    #     time.sleep(0.9)
    print(content)
    plt.imshow(img)
    plt.show()
"""

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
        import win32gui
        hwnd_mul_google = win32gui.FindWindow(None, "网易云游戏平台 - Google Chrome")
        win_rect_mul_google = win32gui.GetWindowRect(hwnd_mul_google)
    if sel == '5' or sel == '7':
        import win32gui
        hwnd_mul_edge = win32gui.FindWindow(None, "大神云游戏 - Google Chrome")
        win_rect_mul_edge = win32gui.GetWindowRect(hwnd_mul_edge)
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
            if len(content_continue)>0 and content_continue[0] == '点击继续': # 655,750,770,790
                x, y = 639, 617
                left_click(x,y,4)
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                if sel == '2' or sel == '6' or sel == '7':
                    time.sleep(4)
                    x, y = 639, 617
                    left_click(x,y,2)
                if sel == '6' or sel == '7':
                    x, y = 803, 903
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                    time.sleep(2)
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '7':
                    x, y = 803, 903
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                    time.sleep(2)
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                continue
                
            # 识别右下点击继续按钮
            img_continue = screen.get_brower_continueBtn(img)
            result_continue = ocr.ocr(img_continue)
            content_continue = ocr.ocr_content(result_continue)
            content_continue = filterLine(content_continue)
            if len(content_continue)>0 and content_continue[0] == '点击继续':
                x,y = 908, 617
                left_click(x,y,2) # 点击继续
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                if sel == '2' or sel == '6' or sel == '7':
                    time.sleep(4)
                    x, y = 908, 617
                    left_click(x,y,2) # 点击继续
                if sel == '6' or sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                    time.sleep(2)
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                    time.sleep(2)
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
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
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = 747,830
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                if sel == '2' or sel == '6' or sel == '7':
                    time.sleep(4)
                    x, y = 671, 594
                    left_click(x,y,2) # 点击继续
                if sel == '6' or sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                    time.sleep(2)
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '7':
                    x, y = 1200, 890
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                    time.sleep(2)
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
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
                        left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,1)
                    if sel == '5' or sel == '7':
                        x, y = 800,800
                        left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,1)
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
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,2)
                if sel == '5' or sel == '7':
                    x,y = coordinate_mul[res[0][2]][0], coordinate_mul[res[0][2]][1]
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,2)
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
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[0][0], coordinate_mul[0][1]
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                is_answered = 1
            elif state1 == 'B' or state2 == 'B' or state3 == 'B':
                print('这题抄B')
                relstate = 1
                x,y = coordinate[1][0], coordinate[1][1]
                left_click(x,y,2) # 点击选项 # 抄答案
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = coordinate_mul[1][0], coordinate_mul[1][1]
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[1][0], coordinate_mul[1][1]
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                is_answered = 1
            elif state1 == 'C' or state2 == 'C' or state3 == 'C' or state1 == 'c' or state2 == 'c' or state3 == 'c':
                print('这题抄C')
                relstate = 2
                x,y = coordinate[2][0], coordinate[2][1]
                left_click(x,y,2) # 点击选项 # 抄答案
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = coordinate_mul[2][0], coordinate_mul[2][1]
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[2][0], coordinate_mul[2][1]
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
                is_answered = 1
            elif state1 == 'D' or state2 == 'D' or state3 == 'D':
                print('这题抄D')
                relstate = 3
                x,y = coordinate[3][0], coordinate[3][1]
                left_click(x,y,2) # 点击选项 # 抄答案
                if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                    x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                    left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
                if sel == '5' or sel == '7':
                    x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                    left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
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
        #         left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,2)

            # print('这题盲猜C')
            # x,y = coordinate[2][0], coordinate[2][1]
            # left_click(win_rect[0]+x,win_rect[1]+y,2)
            # if sel == '4' or sel == '5' or sel == '6' or sel == '7':
            #     x, y = coordinate_mul[2][0], coordinate_mul[2][1]
            #     left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
            # if sel == '5' or sel == '7':
            #     x, y = coordinate_mul[2][0], coordinate_mul[2][1]
            #     left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
            is_answered = 2 # 表示没得抄，盲猜
        if is_answered == 2:
            print('这题盲猜D')
            x,y = coordinate[3][0], coordinate[3][1]
            left_click(x,y,2) # 点击选项 # 盲猜
            if sel == '4' or sel == '5' or sel == '6' or sel == '7':
                x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                left_click(win_rect_mul_google[0]+x,win_rect_mul_google[1]+y,4)
            if sel == '5' or sel == '7':
                x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                left_click(win_rect_mul_edge[0]+x,win_rect_mul_edge[1]+y+padd2wy,4)
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