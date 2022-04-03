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
import numpy as np
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore') # warnings有点多，过滤一下
# left click
import win32api
import win32con
import pyautogui
from PIL import ImageGrab,Image

# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)
# 初始化ocr模型
ocr = OCRImp(conf_data)
# 初始化匹配器(题库)
data_matcher = DataMatcher(conf_data)
# 截屏
screen = ScreenImp(conf_data)

import win32gui
hwnd_mul_google = win32gui.FindWindow(None, "网易云游戏平台 - Google Chrome")
win_rect_mul_google = win32gui.GetWindowRect(hwnd_mul_google)
print(win_rect_mul_google)

hwnd_mul_edge = win32gui.FindWindow(None, "大神云游戏 - Google Chrome")
win_rect_mul_edge = win32gui.GetWindowRect(hwnd_mul_edge)
print(win_rect_mul_edge)
# (2869, 0, 4330, 1571)
# (4310, 0, 5771, 1571)
# (1080, 3840, 3)

def get_question_answer(img):
    # 一次答题流程
    res = []
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_brower_questionAndoptionsBtn(img)
    resultq = ocr.ocr(QBtn)
    resulta = ocr.ocr(ABtn)
    resultb = ocr.ocr(BBtn)
    resultc = ocr.ocr(CBtn)
    resultd = ocr.ocr(DBtn)
    print(resultq)
    print(resulta)
    print(resultb)
    print(resultc)
    print(resultd)

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

start = time.time()*1000
win32api.keybd_event(win32con.VK_SNAPSHOT,0)
time.sleep(0.1)
im = ImageGrab.grabclipboard()
# PIL.BmpImagePlugin.DibImageFile to Image
im = Image.frombytes('RGB', im.size, im.tobytes())
img = np.array(im)
print(img.shape)
img = img[win_rect_mul_edge[1]:win_rect_mul_edge[3],2869:win_rect_mul_edge[0],::-1]
img_path = './img/harry_google_fullimg.png'
img = cv2.imread(img_path)
img = img[112:652,10:970,::-1]
# cv2.imwrite('img/harry_google_fullimg5.png', img) # 10,112,970,652
# result = ocr.ocr(img)
# print(result)
# plt.imshow(img)
# plt.show()

# 识别计时器
img_countdown = screen.get_brower_countdownBtn(img)
plt.imshow(img_countdown)
plt.show()
result_countdown = ocr.ocr(img_countdown)
print(result_countdown)
content_countdown = ocr.ocr_content(result_countdown)
content_countdown = filterLine(content_countdown)
# print(content_countdown)
countdown_num = -1
if (content_countdown!=None) and len(content_countdown) > 0 and content_countdown[0].isdigit():
    countdown_num = int(content_countdown[0])
print(countdown_num)

# res = get_question_answer(img) # 获取题干和选项
# print(res)

if isinstance(im,Image.Image):
    print("Image: size : %s, mode: %s" % (im.size, im.mode))
elif im:
    for filename in im:
        try:
            print("filename: %s" % filename)
            im = Image.open(filename)            
        except IOError:
            pass #ignore this file
        else:
            print("ImageList: size : %s, mode: %s" % (im.size, im.mode))
else:
    print("clipboard is empty.")
end = time.time()*1000
print(end-start)
