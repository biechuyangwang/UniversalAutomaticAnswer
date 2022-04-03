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

# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)
ocr = OCRImp(conf_data) # 约定只能由一个OCR实例（有时间变成单例模式）

import  os
def adb_getimg(path,filename):
    os.system("adb shell /system/bin/screencap -p /sdcard/{}".format(filename)) #截取屏幕，图片命名为screen.png
    os.system("adb pull /sdcard/{} {}".format(filename,path))
# x,y=12,12
# os.system("adb shell input tap {}{}".format(x,y))#x ，y为点击处的像素点 2400*1080

start_t = time.time()*1000
path = './img'
filename = 'screen1.png'
adb_getimg(path,filename) # 获取图片
end_t = time.time()*1000
print("截图耗时：{}ms".format(end_t-start_t))
start_t = time.time()*1000
img_path = './img/{}'.format(filename)
# img_path = './img/harrypotter_start_xueyuan.png'
img = cv2.imread(img_path)
import matplotlib.pyplot as plt

# 1950,940,2200,1000
img = img[940:1000,1950:2200]
result = ocr.ocr(img)
print(result)

end_t = time.time()*1000
print("耗时：{}ms".format(end_t-start_t))

plt.imshow(img)
plt.show()