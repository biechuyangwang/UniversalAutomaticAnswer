#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""harrypotter magicawakened auto quiz

auto_quiz is the friendly quiz fork by biechuyangwang (and Contributors).
    https://github.com/biechuyangwang/universalautomaticanswer/

usage:
python auto_quiz.py
Interactive input 
    sel:
    {1:大神云游戏麻瓜,2:魔法史,3:院活,4:麻瓜多开,5:魔法史多开,6:院活多开,7:社团, 11:网易云游戏麻瓜,...} 
        # num<=10表示是chrome浏览器的大神云游戏中的截图来识别题目和选项,支持多开选项
        # num> 10表示是chrome浏览器的网易云游戏中的截图来识别题目和选项,不支持多开选项
    epoch:
    {int}
        # 表示运行的轮数
auto_quiz is the Python Library by biechuyangwang (and Contributors).
Copyright (c) 2022.04.18
"""


import sys
import numpy as np
from PIL import ImageGrab,Image
import matplotlib.pyplot as plt
import cv2
import time
import random
import logging
import warnings
warnings.filterwarnings('ignore') # warnings有点多，过滤一下

# 导入自定义包
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState, maguafilterQuestion, filtertimeLine
from UniversalAutomaticAnswer.match.matchImp import DataMatcher, match_options


# 指定logger输出级别
from UniversalAutomaticAnswer.util.logging import get_logger
logger = get_logger() # 写个logger来帮助调试
logger.setLevel(logging.INFO)

# 日志文件，输出重定向
def make_print_to_file(path='./'):
    '''
    path, it is a path for save your log about fuction print
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
            self.log = open(os.path.join(path, filename), "a", encoding='utf8',) # 追加的方式定义log文件
 
        def write(self, message):
            self.terminal.write(message) # 终端打印
            self.log.write(message) # log文件也打印

        def flush(self):
            self.terminal.flush()
            self.log.flush()

    fileName = datetime.datetime.now().strftime('log_'+'%Y_%m_%d_%H')
    sys.stdout = Logger(fileName + '.log', path=path)


# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)
# 初始化ocr模型
ocr = OCRImp(conf_data)
# 初始化匹配器(题库)
data_matcher = DataMatcher(conf_data)
# 初始化屏幕实例
screen = ScreenImp(conf_data)

# 大神全局变量(需要自己根据自己的去设置)
chrom_dashen_left_padding = 244 # chrome浏览器中大神云游戏，游戏界面的左上角横坐标
chrom_dashen_top_padding = 155 # chrome浏览器中大神云游戏，游戏界面的左上角纵坐标
chrom_dashen_right_pading = -244 # chrome浏览器中大神云游戏，游戏界面的右上角横坐标
chrom_dashen_bottom_padding = -120 # chrome浏览器中大神云游戏，游戏界面的右上角纵坐标
chrom_wangyiyun_left_padding = 190
chrom_wangyiyun_top_padding = 155
chrom_wangyiyun_right_pading = -190
chrom_wangyiyun_bottom_padding = -60

rect_start = [705,750,1140,1340] # click 1111,777  # chrome浏览器中大神云游戏，游戏中“准备”按钮的[h1,h2,w1,w2],用于截取按钮,更加小面积的识别,提高响应速度。
rect_failure_back = [715,750,680,755] # click 710,735  # chrome浏览器中大神云游戏，游戏中“返回”按钮的[h1,h2,w1,w2],用于截取按钮,更加小面积的识别,提高响应速度。
rect_magua_countdown = [15,105,670,769]  # chrome浏览器中大神云游戏，游戏中麻瓜研究课的“计时器”[h1,h2,w1,w2],用于截取按钮,更加小面积的识别,提高响应速度。
rect_mofashi_countdown = [7,70,675,760] # 识别不了11 和 3  # chrome浏览器中大神云游戏，游戏中魔法史的“计时器”[h1,h2,w1,w2],用于截取按钮,更加小面积的识别,提高响应速度。
rect_question = [415,518,155,800] # top bottom left right # 问题[415,518,155,800]
rect_question_ex = [415,522,155,800] # top bottom left right # 问题[415,518,155,800]
rect_option_a = [595,655,104,510] # click 510,645 # 选项A
rect_option_b = [595,655,804,1210] # click 1210,645 # 选项B
rect_option_c = [695,755,104,510] # click 510,745 # 选项C
rect_option_d = [695,755,804,1210] # click 1210,745 # 选项D
rect_continue = [755,790,1055,1180] # click 1111,777 # 右下角“继续”按钮
coordinate = [ # 四个选项按钮的点击坐标，和一个中间坐标（用于抢答时出现错误的缓冲）
    [510,645],
    [1210,645],
    [510,745],
    [1210,745],
    [716,687]
]
click_start = [1240,730] # 点击开始坐标
click_continue = [1111,777] # 点击继续坐标
click_failure_back = [710,735] # 点击返回坐标

# 网易云全局变量(与大神云游的变量含义类似)
wangyiyun_rect_start = [755,810,1230,1430] # click
wangyiyun_rect_magua_countdown = [15,125,720,820] # 12 9 8 6稳定识别
wangyiyun_rect_mofashi_countdown = [13,75,730,810]
wangyiyun_rect_question = [450,558,170,890] 
wangyiyun_rect_question_ex = [450,562,170,890]
wangyiyun_rect_option_a = [643,710,110,510] # click
wangyiyun_rect_option_b = [643,710,870,1270] # click
wangyiyun_rect_option_c = [765,808,110,510] # click
wangyiyun_rect_option_d = [765,808,870,1270] # click
wangyiyun_rect_continue = [810,850,1140,1270] # click todo
wangyiyun_coordinate = [
    [510,693],
    [1270,693],
    [510,808],
    [1270,808],
    [770,740]
]
wangyiyun_click_start = [1340,785]
wangyiyun_click_continue = [1205,830]


# multi
coordinate_mul = [
    [366,753],
    [753,753],
    [366,810],
    [753,810]
]
padd2wy = -195 # 指顶110 居中265 -155 网易云游戏300


import win32gui
hwnd_title = dict() # 使用upadate的方式更新字典
def get_all_hwnd(hwnd,nouse):
    """返回系统句柄集合

    Args:
        hwnd (_type_): _description_
        nouse (_type_): _description_
    """
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})


def get_hwnd(hwnd_title:list, target_title:str, brower_type:str='Chrom'): # brower_type:{'Chrom','Edge'} 
    """获取名为target_title的句柄

    Args:
        hwnd_title (list): 系统句柄集合
        target_title (str): 目标标题
        brower_type (str, optional): 浏览器类型. Defaults to 'Chrom'.

    Returns:
        _type_: 存在则返回坐标和图像，不存在则返回空
    """    
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h,t in hwnd_title.items():
        if target_title in t and brower_type in t:
            ret_hwnd = h
            return ret_hwnd
    return None
chrom_dashen_hwnd = get_hwnd(hwnd_title,"大神云游戏",'Chrom') # 获取全局句柄
chrom_wangyiyun_hwnd = get_hwnd(hwnd_title,"网易云游戏",'Chrom') # 获取全局句柄
edge_dashen_hwnd = get_hwnd(hwnd_title,"大神云游戏",'Edge') # 获取全局句柄


def get_rect_img(hwnd,plat_type='dashen'):
    if chrom_dashen_hwnd == chrom_wangyiyun_hwnd:
        plat_type='wangyiyun'
    ret_rect = win32gui.GetWindowRect(hwnd)
    if len(ret_rect)==0:
        return None
    else:
        img = ImageGrab.grab() # 1920 1080
        img = Image.frombytes('RGB', img.size, img.tobytes())
        img = np.array(img)
        # logger.info(ret_img.shape) # hwc={1080, 1920, 3} # width 900 width 954 height 537 left 163 top 0
        # hightpadding 155 -120 -60 960-155=805 leftpadding 244 -244 1920-488=1420+12=1432
        if plat_type=='dashen':
            ret_img = img[chrom_dashen_top_padding:chrom_dashen_bottom_padding,chrom_dashen_left_padding:chrom_dashen_right_pading]
        else:
            ret_img = img[chrom_wangyiyun_top_padding:chrom_wangyiyun_bottom_padding,chrom_wangyiyun_left_padding:chrom_wangyiyun_right_pading]
        # ret_img = img[:,:]
        # logger.info(ret_img.shape) # hw:{805,1432} leftpadding 244 toppadding 155
        return ret_rect, ret_img


import win32api
import win32con
def left_click(x:int, y:int,times:int=1):
    """鼠标点击左键times次

    Args:
        x (int): 横坐标
        y (int): 纵坐标
        times (int, optional): 点击次数. Defaults to 1.
    """    
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        times -= 1


def zoom_left_click(x, y, times:int=1, ratio=1.5): # 去电脑的显示设置里查看文字项目放大率，一般笔记本是150%
    """根据系统放缩比例点击屏幕

    Args:
        x (_type_): 横坐标
        y (_type_): 纵坐标
        ratio (float, optional): 系统放缩比例. Defaults to 1.5.
        times (int, optional): 点击次数. Defaults to 1.
    """    
    rel_x = int((chrom_dashen_left_padding + x)/ratio)
    rel_y = int((chrom_dashen_top_padding + y)/ratio)
    left_click(rel_x, rel_y, times)


def click_instance_center(instance_name:str, ocr_result:list):
    """鼠标单击instance_name

    Args:
        instance_name (str): 实例名称
        ocr_result (list): 识别结果列表
    """
    if len(ocr_result) == 0:
        return
    ret_list = [ line[0] for line in ocr_result if instance_name in line[1][0] ]
    if len(ret_list) == 0:
        logger.info('当前页面不存在{}'.format(instance_name))
        return
    else:
        ret = ret_list[0]
        x = int((ret[0][0]+ret[1][0])/2)
        y = int((ret[1][1]+ret[2][1])/2)
        zoom_left_click(x, y)

def get_countdown(img, class_type='mofashi'):
    countdown = ''
    if class_type=='maguayanjiu':
        img_countdown = img[rect_magua_countdown[0]:rect_magua_countdown[1],rect_magua_countdown[2]:rect_magua_countdown[3]]
    elif class_type=='mofashi':
        img_countdown = img[rect_mofashi_countdown[0]:rect_mofashi_countdown[1],rect_mofashi_countdown[2]:rect_mofashi_countdown[3]]
    result = ocr.ocr(img_countdown)
    content = ocr.ocr_content(result)
    if len(filterLine(content)) != 0:
        countdown = filterLine(content)[0]
    return countdown

def get_question_options(img):
    res = []
    QBtn = img[rect_question[0]:rect_question[1],rect_question[2]:rect_question[3]]
    ABtn = img[rect_option_a[0]:rect_option_a[1],rect_option_a[2]:rect_option_a[3]]
    BBtn = img[rect_option_b[0]:rect_option_b[1],rect_option_b[2]:rect_option_b[3]]
    CBtn = img[rect_option_c[0]:rect_option_c[1],rect_option_c[2]:rect_option_c[3]]
    DBtn = img[rect_option_d[0]:rect_option_d[1],rect_option_d[2]:rect_option_d[3]]
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
        # print(contentq)
        logger.info(contentq)

    question, optiona,optionb,optionc,optiond = '', '', '', '' ,''
    if len(filterQuestion(contentq))>0:
        question = filterQuestion(contentq)[0]
    # print(question)
    if len(question)==0:
        print('题目未识别！')
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
        print('*'*20)
        print('没有匹配到题库')
        # time.sleep(2)
        return res
    else:
        print('题库匹配结果:', answer_list[0])
        if(answer_list[0][1] <= 50):
            print('可能题库匹配错误')
        answer = answer_list[0][0][1]
        res = match_options(answer, options)
        if len(res) == 0:
            print('*'*20)
            print('选项OCR出错')
            return res
        print('选项匹配结果:', res)
        if(res[0][1]<=50):
            print('可能选项错误')
        return res

def get_line_content(img,rect):
    res = ''
    img_rect = img[rect[0]:rect[1],rect[2]:rect[3]]
    result = ocr.ocr(img_rect)
    content = ocr.ocr_content(result)
    if len(filterLine(content))!=0:
        res = filterLine(content)[0]
    return res

# """
# 答题(包括魔法史 麻瓜研究 院活 社团魔法史)
def dati(time_chutdown=15, iter_num=15, epoch_num=1, num_multiple=1, class_type='mofashi', plat_type='dashen'):
    if num_multiple>=2:
        if plat_type == 'mumu':
            win_rect_mul_leftgoogle_yunyouxi = win32gui.GetWindowRect(chrom_dashen_hwnd)
        else:
            win_rect_mul_leftgoogle_yunyouxi = win32gui.GetWindowRect(chrom_wangyiyun_hwnd)
    if num_multiple>=3:
        win_rect_mul_rightgoogle_dashen = win32gui.GetWindowRect(edge_dashen_hwnd)
    question_num = 0
    pre_answer = 0
    is_answered = 0
    total_time = 0
    total_num = 0
    while True:
        if(question_num==iter_num):
            epoch_num -= 1
            question_num = 0
        if epoch_num == 0:
            print('此次答题平均每题耗时: {}'.format(1.0*total_time/total_num))
            break
        _, img = get_rect_img(chrom_dashen_hwnd,plat_type=plat_type) # 截屏

        # 识别计时器
        if class_type == 'maguayanjiu':
            content_countdown = get_countdown(img,'maguayanjiu')
        else:
            content_countdown = get_countdown(img)
        countdown_num = -1
        if len(content_countdown)!=0 and content_countdown.isdigit():
            countdown_num = int(content_countdown)
            # print(countdown_num)
        else: # 没识别到计时器，就识别开始和继续按钮
            # 识别奖励的中下部分继续按钮，然后识别下一轮的匹配按钮
            # if is_answered==1:
            if class_type == 'shetuan': # 社团抢答
                x,y = coordinate[pre_answer]  # 进去，先盲猜A，A没人选，大概率能首抢
                zoom_left_click(x, y, times=4)
                continue
            
            content_continue = get_line_content(img, rect_continue)
            if content_continue == '点击继续': # 655,750,770,790
                x, y = click_continue
                zoom_left_click(x, y, times=2)
                if num_multiple>=2:
                    x, y = 747,830
                    if plat_type=='mumu':
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y+padd2wy,4)
                    else :
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if num_multiple>=3:
                    x, y = 747,830
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                if num_multiple>=1:
                    time.sleep(4)
                    x, y = click_continue
                    zoom_left_click(x, y, times=2)
                if num_multiple>=2:
                    x, y = 747,830
                    if plat_type=='mumu':
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y+padd2wy,4)
                    else :
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                    time.sleep(2)
                    if plat_type=='mumu':
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y+padd2wy,4)
                    else :
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
                if num_multiple>=3:
                    x, y = 747,830
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                    time.sleep(2)
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
                continue
            
            # 识别失败返回按钮
            content_failure_back = get_line_content(img, rect_failure_back)
            if content_failure_back == '返回':
                x,y = click_failure_back
                zoom_left_click(x, y, times=2)
                if num_multiple>=2:
                    pass # 点击继续
                if num_multiple>=3:
                    pass # 点击继续
                if num_multiple>=1:
                    pass # 社团
                if num_multiple>=2:
                    pass # 社团
                if num_multiple>=3:
                    pass # 社团
                continue
            
            # 上课
            content_start = get_line_content(img, rect_start)
            if '匹配上课'==content_start or '上课'==content_start or '学院活动匹配'==content_start or '准备'==content_start:
                x,y = click_start
                zoom_left_click(x, y, times=1)
                time.sleep(3)
                if num_multiple>=2:
                    x, y = 800,800
                    if plat_type=='mumu':
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y+padd2wy,1)
                    else :
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,1)
                if num_multiple>=3:
                    x, y = 800,800
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,1)
                    time.sleep(1)
                continue
            
        if countdown_num == time_chutdown or (countdown_num <=20 and countdown_num > 15):
            if countdown_num != time_chutdown and is_answered==1:
                continue
            question_num += 1
            if class_type == 'shetuan': # 社团抢答
                x,y = coordinate[pre_answer]  # 进去，先盲猜A，A没人选，大概率能首抢
                zoom_left_click(x, y, times=4)
            is_answered = 0
            print('epoch_num:{}, question_num:{}, countdown_num:{} '.format(epoch_num,question_num,countdown_num))
            s_time = time.time()*1000
            time.sleep(0.1) # 尽量扫描到题目
            _, img = get_rect_img(chrom_dashen_hwnd,plat_type=plat_type) # 截屏
            res = get_question_options(img) # 保证优先抢答
            if len(res) == 0: # 保证扫描到题目
                # time.sleep(0.1)
                global rect_question
                tmp = rect_question
                rect_question = rect_question_ex
                _, img = get_rect_img(chrom_dashen_hwnd,plat_type=plat_type) # 保证扫描到题目
                res = get_question_options(img)
                rect_question = tmp

            if len(res) >0:
                countdown_num = -1
                pre_answer = res[0][2]
                x,y = coordinate[res[0][2]]
                zoom_left_click(x, y, times=2)
                if num_multiple>=2:
                    x,y = coordinate_mul[res[0][2]][0], coordinate_mul[res[0][2]][1]
                    if plat_type=='mumu':
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y+padd2wy,2)
                    else :
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,2)
                if num_multiple>=3:
                    x,y = coordinate_mul[res[0][2]][0], coordinate_mul[res[0][2]][1]
                    left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,2)
                print('这题选',chr(ord('A')+int(res[0][2])))
                time.sleep(0.5)

                # 计时模块
                print('ocr时间: {}ms'.format(time.time()*1000-s_time),flush=True)
                total_time += time.time()*1000-s_time
                total_num += 1
                is_answered = 1
                
                # 保存分析错误
                # img = img[:,:,::-1]
                # cv2.imwrite('img/atest_harry_{}_{}.png'.format(plat_type, question_num), img)
                
                time.sleep(0.4)
            else:
                pre_answer = 4 # 一个无关紧要的坐标防止陷入错误抢答
                print('抄答案吧!')
                time.sleep(1)
            continue
        elif (is_answered == 0 and (countdown_num <=20 and countdown_num > 8)):
            is_answered = 2 # 表示没得抄，盲猜
        if is_answered == 2:
            print('这题盲猜D')
            x,y = coordinate[3]
            zoom_left_click(x, y, times=2)
            if num_multiple>=2:
                x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                if plat_type=='mumu':
                        left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y+padd2wy,4)
                else :
                    left_click(win_rect_mul_leftgoogle_yunyouxi[0]+x,win_rect_mul_leftgoogle_yunyouxi[1]+y,4)
            if num_multiple>=3:
                x, y = coordinate_mul[3][0], coordinate_mul[3][1]
                left_click(win_rect_mul_rightgoogle_dashen[0]+x,win_rect_mul_rightgoogle_dashen[1]+y+padd2wy,4)
            _, img = get_rect_img(chrom_dashen_hwnd,plat_type=plat_type)
            import datetime
            fileName = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.png'
            
            img = img[:,:,::-1]
            cv2.imwrite('img/error_harry_{}_'.format(plat_type)+fileName, img)
            is_answered = 3


# 麻瓜研究
def maguayanjiu(time_chutdown=12,iter_num=15,epoch_num=1,num_multiple=1, plat_type='dashen',is_preclick=True):
    if is_preclick == False: # 全自动，从主界面进
        # 点击麻瓜研究
        x, y = 580, 550
        zoom_left_click(x, y)
        time.sleep(2)

        # 点击进入
        x, y = 1122, 720
        zoom_left_click(x, y)
        time.sleep(4)
    dati(time_chutdown=time_chutdown, iter_num=iter_num, epoch_num=epoch_num, num_multiple=num_multiple, class_type='maguayanjiu', plat_type=plat_type)
# """


# 魔法史
def mofashi(time_chutdown=12,iter_num=15,epoch_num=1,num_multiple=1, plat_type='dashen',is_preclick=True):
    if is_preclick == False: # 全自动，从主界面进
        # 点击魔法史
        x, y = 580, 550
        zoom_left_click(x, y)
        time.sleep(2)

        # 点击进入
        x, y = 1122, 720
        zoom_left_click(x, y)
        time.sleep(4)
    dati(time_chutdown=time_chutdown, iter_num=iter_num, epoch_num=epoch_num, num_multiple=num_multiple, class_type='mofashi', plat_type=plat_type)


# 院活
def yuanhuo(time_chutdown=12,iter_num=15,epoch_num=1,num_multiple=1, plat_type='dashen',is_preclick=True):
    if is_preclick == False: # 全自动，从主界面进
        # 点击魔法史
        x, y = 580, 550
        zoom_left_click(x, y)
        time.sleep(2)

        # 点击进入
        x, y = 1122, 720
        zoom_left_click(x, y)
        time.sleep(4)
    dati(time_chutdown=time_chutdown, iter_num=iter_num, epoch_num=epoch_num, num_multiple=num_multiple, class_type='yuanhuo', plat_type=plat_type)

# 社团
def shetuan(time_chutdown=20,iter_num=20,epoch_num=1,num_multiple=1, plat_type='dashen',is_preclick=True):
    if is_preclick == False: # 全自动，从主界面进
        # 点击魔法史
        x, y = 580, 550
        zoom_left_click(x, y)
        time.sleep(2)

        # 点击进入
        x, y = 1122, 720
        zoom_left_click(x, y)
        time.sleep(4)
    dati(time_chutdown=time_chutdown, iter_num=iter_num, epoch_num=epoch_num, num_multiple=num_multiple, class_type='shetuan', plat_type=plat_type)

# left_padding, top_padding = 244, 155
if __name__ == '__main__':
    # 设置log文件
    make_print_to_file(path='./log/')

    plat_list = ['dashen','wangyiyun']

    sel = '1'
    sel = input('1.麻瓜研究（大神） 2.魔法史 3.院活 4.麻瓜多开 5.魔法史多开 6.院活多开 7.社团(抢) 8.社团多开(抢) 9.社团 11.麻瓜研究（网易云游戏）\n')
    num_sel = int(sel)
    if num_sel > 10:
        plat_type = plat_list[1] # 定义平台，控制截图大小
    else:
        plat_type = plat_list[0] # 定义平台，控制截图大小

    if plat_type =='wangyiyun': # 切换全局参数
        chrom_dashen_hwnd = chrom_wangyiyun_hwnd # 切换句柄
        chrom_dashen_left_padding = chrom_wangyiyun_left_padding
        chrom_dashen_top_padding = chrom_wangyiyun_top_padding
        chrom_dashen_right_pading = chrom_wangyiyun_right_pading
        chrom_dashen_bottom_padding = chrom_wangyiyun_bottom_padding
        rect_start = wangyiyun_rect_start
        rect_question = wangyiyun_rect_question
        rect_question_ex = wangyiyun_rect_question_ex
        rect_option_a = wangyiyun_rect_option_a
        rect_option_b = wangyiyun_rect_option_b
        rect_option_c = wangyiyun_rect_option_c
        rect_option_d = wangyiyun_rect_option_d
        rect_continue = wangyiyun_rect_continue
        coordinate = wangyiyun_coordinate
        rect_magua_countdown = wangyiyun_rect_magua_countdown
        rect_mofashi_countdown = wangyiyun_rect_mofashi_countdown
        click_start = wangyiyun_click_start
        click_continue = wangyiyun_click_continue
    
    
    epoch_num = 1
    epoch = input('几次？\n')
    if epoch!='':
        epoch_num=int(epoch)
    # 麻瓜研究
    if num_sel == 1 or num_sel==11:
        maguayanjiu(epoch_num=epoch_num, plat_type=plat_type)

    # 魔法史
    if num_sel == 2 or num_sel==12:
        mofashi(epoch_num=epoch_num, plat_type=plat_type)

    # 院活
    if num_sel == 3 or num_sel==13:
        yuanhuo(epoch_num=epoch_num, num_multiple=1, plat_type=plat_type)

    # 麻瓜研究多开
    if num_sel == 4:
        maguayanjiu(epoch_num=epoch_num, num_multiple=3, plat_type=plat_type)
    
    # 魔法史多开
    if num_sel == 5:
        mofashi(epoch_num=epoch_num, num_multiple=3, plat_type=plat_type)

    # 学院多开
    if num_sel == 6:
        epoch_num=15
        yuanhuo(epoch_num=epoch_num, num_multiple=3, plat_type=plat_type)

    # 社团(抢)
    if num_sel == 7 or num_sel==17:
        epoch_num=1
        shetuan(time_chutdown=20,iter_num=22,epoch_num=epoch_num, plat_type=plat_type)
    
    # 社团多开(抢)
    if num_sel == 8:
        epoch_num=1
        shetuan(time_chutdown=20,iter_num=22, num_multiple=3, epoch_num=epoch_num, plat_type=plat_type)
    
    # 社团
    if num_sel == 9 or num_sel==19:
        epoch_num=1
        mofashi(time_chutdown=20,iter_num=22, epoch_num=epoch_num, plat_type=plat_type)
    
    # 单图测试
    # idx = 3
    # img_path = 'img/atest_harry_{}_{}.png'.format(plat_type,idx)
    # img_path = 'img/error_harry_dashen_2022_04_19_07_16_04.png'
    # img = cv2.imread(img_path)

    # ret_rect, img = get_rect_img(chrom_dashen_hwnd,plat_type=plat_type) # 截屏


    # [[[1105.0, 816.0], [1261.0, 816.0], [1261.0, 844.0], [1105.0, 844.0]], ('#点击继续', 0.81634045)]
    # imgcrop = img[415:522,155:800] #  测试区域识别 #  q[415,518,155,800] [816:844,1105:1261]
    # imgcrop = img
    # det = True
    # result = ocr.ocr(imgcrop,cls=True,det=det) # 只识别14.34ms 带检测24.70ms 带角度分类36.48
    # if len(result)==0:
    #     imgcrop = img[415:530,155:800]
    #     result = ocr.ocr(imgcrop,cls=True,det=det) # 只识别14.34ms 带检测24.70ms 带角度分类36.48
    # logger.info(result)
    # plt.imshow(imgcrop)
    # plt.show()


    # 批量读图
    # ret_rect, ret_img = get_rect_img(chrom_dashen_hwnd,plat_type=plat_type) # 截屏
    # ret_img = ret_img[:,:,::-1]
    # cv2.imwrite('img/atest_harry_dashen_50.png', ret_img)
    # for i in range(0,20):
    #     ret_rect, ret_img = get_rect_img(chrom_dashen_hwnd,plat_type=plat_type) # 截屏
    #     ret_img = ret_img[:,:,::-1]
    #     cv2.imwrite('img/atest_harry_wangyiyun_{}.png'.format(i), ret_img)
    #     time.sleep(0.7)

    # 
    # instance_name = '进入'
    # click_instance_center(instance_name, result)

    # 城堡 1340 740
    # x, y = 1340, 740
    # zoom_left_click(x, y)
    # 活动 1380 230
    # x, y = 1380, 230
    # zoom_left_click(x, y)
    # 作业 1380 310
    # x, y = 1380, 310
    # zoom_left_click(x, y)
    # 宝箱 85 185
    # x, y = 85, 185
    # zoom_left_click(x, y)
    # 返回 50 46
    # x, y = 50, 46
    # zoom_left_click(x, y)