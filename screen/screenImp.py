#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get_screenshot
import win32gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect
from PyQt5 import QtCore, QtWidgets,QtGui
import win32gui
import sys

# 
# 将包含parent包的路径添加进系统路径
sys.path.append(r"C:\\Users\\SAT")
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file

class ScreenImp(object): # 拼音匹配算法对的解决方案
    """
    屏幕相关算法：
    1. 屏幕进程设置
    2. 屏幕截图
    3. 屏幕保存
    4. 屏幕点击
    """
    def __init__(self, conf_data):
        self.init_data(conf_data)
    
    def init_data(self,conf_data):
        self.conf_data = conf_data
        self.screen_hwnd = self.conf_data['windowsScreen']['screen_hwnd']
        self.imgpath = self.conf_data['path']['imgpath']
    
    def get_screenshot(self): # 截屏时模拟器不要切后台
        """
        根据窗口句柄获取屏幕截图
        """
        hwnd = win32gui.FindWindow(None, self.screen_hwnd)
        # hwnd = win32gui.FindWindow(None, "哈利波特:魔法觉醒 - MuMu模拟器") # 1600*937(1600*900)
        if(hwnd):
            win_rect = win32gui.GetWindowRect(hwnd)
            app = QApplication(sys.argv)
            screen = QApplication.primaryScreen()
            pixmap_img = screen.grabWindow(hwnd)
            img = pixmap_img.toImage() # 图片转QImage
            import os
            root_path = os.path.dirname(os.path.abspath(__file__)) # 获取当前文件的绝对路径
            # print(root_path)
            imgpath = root_path + '/' + self.imgpath # 获取图片路径
            img.save(imgpath)
            app.quit()
            return win_rect
        return None

if __name__ == '__main__':
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    screen = ScreenImp(conf_data)
    win_rect = screen.get_screenshot()
    print(win_rect)