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

sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file # 加入自定义包

class ScreenImp(object):
    """
    屏幕相关算法：
    1. 屏幕进程设置
    2. 屏幕截图并保存
    3. 屏幕点击
    """
    def __init__(self, conf_data):
        self.init_data(conf_data)
    
    def init_data(self,conf_data):
        self.conf_data = conf_data
        self.screen_hwnd = self.conf_data['windowsScreen']['screen_hwnd']

        self.imgpath = self.conf_data['path']['imgpath']
        self.ravenclaw_imgpath = self.conf_data['path']['ravenclaw_imgpath']

        self.rectStart = self.conf_data['imgRect']['rectStart']
        self.ravenclaw_rectStart = self.conf_data['imgRect']['ravenclaw_rectStart']
        self.rectContinue = self.conf_data['imgRect']['rectContinue']
        self.rectCountdown = self.conf_data['imgRect']['rectCountdown']
        self.rectQ = self.conf_data['imgRect']['rectQ']
        self.rectA = self.conf_data['imgRect']['rectA']
        self.rectB = self.conf_data['imgRect']['rectB']
        self.rectC = self.conf_data['imgRect']['rectC']
        self.rectD = self.conf_data['imgRect']['rectD']
        self.rectPerson1State = self.conf_data['imgRect']['rect_person1_state']
        self.rectPerson2State = self.conf_data['imgRect']['rect_person2_state']
        self.rectPerson3State = self.conf_data['imgRect']['rect_person3_state']
        self.ravenclawRectPerson1State = self.conf_data['imgRect']['ravenclaw_rect_person1_state']
        self.ravenclawRectPerson2State = self.conf_data['imgRect']['ravenclaw_rect_person2_state']
        self.ravenclawRectPerson3State = self.conf_data['imgRect']['ravenclaw_rect_person3_state']
    
    def qtpixmap_to_cvimg(self, qtpixmap):
    # pyqt5的图片数据转ndarray
        qimg = qtpixmap.toImage()
        temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        temp_shape += (4,)
        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        result = result[..., :3]
        return result

    def get_screenshot(self): # 截屏时模拟器不要切后台
        """
        根据窗口句柄获取屏幕截图
        """
        hwnd = win32gui.FindWindow(None, self.screen_hwnd)
        if(hwnd):
            win_rect = win32gui.GetWindowRect(hwnd)
            app = QApplication(sys.argv)
            screen = QApplication.primaryScreen()
            pixmap_img = screen.grabWindow(hwnd)
            img = self.qtpixmap_to_cvimg(pixmap_img)
            app.quit()
            return win_rect, img # retur win_rect and win_img
        return None
    
    def get_startMatchBtn(self, img):
        return img[self.rectStart[1]:self.rectStart[3], self.rectStart[0]:self.rectStart[2], :]  # [150,470,940,660]->img[470:660,150:940,:]

    def get_ravenclaw_startMatchBtn(self, img):
        return img[self.rectStart[1]:self.rectStart[3], self.rectStart[0]:self.rectStart[2], :]

    def get_continueBtn(self, img):
        return img[self.rectContinue[1]:self.rectContinue[3], self.rectContinue[0]:self.rectContinue[2], :]

    def get_countdownBtn(self, img):
        return img[self.rectCountdown[1]:self.rectCountdown[3], self.rectCountdown[0]:self.rectCountdown[2], :]

    def get_personState(self, img):
        person1State = img[self.rectPerson1State[1]:self.rectPerson1State[3], self.rectPerson1State[0]:self.rectPerson1State[2], :]
        person2State = img[self.rectPerson2State[1]:self.rectPerson2State[3], self.rectPerson2State[0]:self.rectPerson2State[2], :]
        person3State = img[self.rectPerson3State[1]:self.rectPerson3State[3], self.rectPerson3State[0]:self.rectPerson3State[2], :]
        return person1State, person2State, person3State
    
    def get_ravenclaw_personState(self, img):
        person1State = img[self.ravenclawRectPerson1State[1]:self.ravenclawRectPerson1State[3], self.ravenclawRectPerson1State[0]:self.ravenclawRectPerson1State[2], :]
        person2State = img[self.ravenclawRectPerson2State[1]:self.ravenclawRectPerson2State[3], self.ravenclawRectPerson2State[0]:self.ravenclawRectPerson2State[2], :]
        person3State = img[self.ravenclawRectPerson3State[1]:self.ravenclawRectPerson3State[3], self.ravenclawRectPerson3State[0]:self.ravenclawRectPerson3State[2], :]
        return person1State, person2State, person3State

    def get_questionAndoptionsBtn(self, img):
        QBtn = img[self.rectQ[1]:self.rectQ[3], self.rectQ[0]:self.rectQ[2], :]
        ABtn = img[self.rectA[1]:self.rectA[3], self.rectA[0]:self.rectA[2], :]
        BBtn = img[self.rectB[1]:self.rectB[3], self.rectB[0]:self.rectB[2], :]
        CBtn = img[self.rectC[1]:self.rectC[3], self.rectC[0]:self.rectC[2], :]
        DBtn = img[self.rectD[1]:self.rectD[3], self.rectD[0]:self.rectD[2], :]
        return QBtn, ABtn, BBtn, CBtn, DBtn

    def leftClick(self, x, y):
        pass
        """
        """

if __name__ == '__main__':
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    screen = ScreenImp(conf_data)
    # win_rect, img_bgr= screen.get_screenshot()
    img_bgr = cv2.imread(screen.imgpath)
    # print(win_rect)
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_questionAndoptionsBtn(img_bgr)

    plt.subplot(231)
    plt.title('QBtn')
    plt.xticks([])   # remove ticks
    plt.yticks([])
    plt.imshow(QBtn[:, :, :])
    # plt.imshow(QBtn[:, :, ::-1])

    plt.subplot(232)
    plt.title('ABtn')
    plt.xticks([])   # remove ticks
    plt.yticks([])
    plt.imshow(ABtn[:, :, :])
    # plt.imshow(ABtn[:, :, ::-1])

    plt.subplot(233)
    plt.title('BBtn')
    plt.xticks([])   # remove ticks
    plt.yticks([])
    plt.imshow(BBtn[:, :, ::-1])

    plt.subplot(234)
    plt.title('CBtn')
    plt.xticks([])   # remove ticks
    plt.yticks([])
    plt.imshow(CBtn[:, :, ::-1])

    plt.subplot(235)
    plt.title('DBtn')
    plt.xticks([])   # remove ticks
    plt.yticks([])
    plt.imshow(DBtn[:, :, ::-1])

    plt.show()