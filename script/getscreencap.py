#!/usr/bin/env python
# -*- coding: utf-8 -*-

# get_screenshot
import win32gui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QRect
from PyQt5 import QtCore, QtWidgets,QtGui
import win32gui
import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2

def qtpixmap_to_cvimg(qtpixmap):
# pyqt5的图片数据转ndarray
    qimg = qtpixmap.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]
    return result

def get_screenshot(screen_hwnd): # 截屏时模拟器不要切后台
        """
        根据窗口句柄获取屏幕截图
        """
        hwnd = win32gui.FindWindow(None, screen_hwnd)
        if(hwnd):
            win_rect = win32gui.GetWindowRect(hwnd)
            app = QApplication(sys.argv)
            screen = QApplication.primaryScreen()
            pixmap_img = screen.grabWindow(hwnd)
            img = qtpixmap_to_cvimg(pixmap_img)
            app.quit()
            return win_rect, img # retur win_rect and win_img
        return None

if __name__ == '__main__':
    screen_hwnd = "android9"
    win_rect, img = get_screenshot(screen_hwnd)
    argvs = sys.argv
    # print(argvs)
    fileName = argvs[1] + '.png'
    cv2.imwrite('img/harry_'+fileName, img)