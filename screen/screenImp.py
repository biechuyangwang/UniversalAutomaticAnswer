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
        self.maguabrowergrouprectStart = self.conf_data['maguabrowergroupimgRect']['rectStart']
        self.browerrectStart = self.conf_data['browerimgRect']['rectStart']
        self.ravenclaw_rectStart = self.conf_data['imgRect']['ravenclaw_rectStart']

        self.rectCenterContinu = self.conf_data['imgRect']['rectCenterContinu']
        self.rectContinue = self.conf_data['imgRect']['rectContinue']
        self.browerectcenterContinue = self.conf_data['browerimgRect']['rectcenterContinue']
        self.browerectContinue = self.conf_data['browerimgRect']['rectContinue']
        self.maguabrowergrouprectContinue = self.conf_data['maguabrowergroupimgRect']['rectContinue']

        self.rectReturn = self.conf_data['imgRect']['rectReturn']
        self.browerectReturn = self.conf_data['browerimgRect']['rectReturn']

        self.rect_magua_Countdown = self.conf_data['imgRect']['rect_magua_Countdown']
        self.rectCountdown = self.conf_data['imgRect']['rectCountdown']
        self.maguabrowergrouprectCountdown = self.conf_data['maguabrowergroupimgRect']['rectCountdown']
        self.browerrectCountdown = self.conf_data['browerimgRect']['rectCountdown']
        self.browermaguarectCountdown = self.conf_data['browerimgRect']['maguarectCountdown']

        self.rectScore = self.conf_data['imgRect']['rect_magua_score']

        self.rectQ = self.conf_data['imgRect']['rectQ']
        self.rectA = self.conf_data['imgRect']['rectA']
        self.rectB = self.conf_data['imgRect']['rectB']
        self.rectC = self.conf_data['imgRect']['rectC']
        self.rectD = self.conf_data['imgRect']['rectD']
        self.maguabrowergrouprectQ = self.conf_data['maguabrowergroupimgRect']['rectQ']
        self.maguabrowergrouprectA = self.conf_data['maguabrowergroupimgRect']['rectA']
        self.maguabrowergrouprectB = self.conf_data['maguabrowergroupimgRect']['rectB']
        self.maguabrowergrouprectC = self.conf_data['maguabrowergroupimgRect']['rectC']
        self.maguabrowergrouprectD = self.conf_data['maguabrowergroupimgRect']['rectD']
        self.browerrectQ = self.conf_data['browerimgRect']['rectQ']
        self.browerrectA = self.conf_data['browerimgRect']['rectA']
        self.browerrectB = self.conf_data['browerimgRect']['rectB']
        self.browerrectC = self.conf_data['browerimgRect']['rectC']
        self.browerrectD = self.conf_data['browerimgRect']['rectD']

        self.rectPerson1State = self.conf_data['imgRect']['rect_person1_state']
        self.rectPerson2State = self.conf_data['imgRect']['rect_person2_state']
        self.rectPerson3State = self.conf_data['imgRect']['rect_person3_state']
        self.maguabrowergrouprectPerson1State = self.conf_data['maguabrowergroupimgRect']['rect_person1_state']
        self.maguabrowergrouprectPerson2State = self.conf_data['maguabrowergroupimgRect']['rect_person2_state']
        self.maguabrowergrouprectPerson3State = self.conf_data['maguabrowergroupimgRect']['rect_person3_state']
        self.rectmaguaperson1state = self.conf_data['imgRect']['rect_magua_person1_state']
        self.rectmaguaperson2state = self.conf_data['imgRect']['rect_magua_person2_state']
        self.rectmaguaperson3state = self.conf_data['imgRect']['rect_magua_person3_state']
        self.browerrectPerson1State = self.conf_data['browerimgRect']['rect_person1_state']
        self.browerrectPerson2State = self.conf_data['browerimgRect']['rect_person2_state']
        self.browerrectPerson3State = self.conf_data['browerimgRect']['rect_person3_state']
        self.browermaguarectPerson1State = self.conf_data['browerimgRect']['magua_rect_person1_state']
        self.browermaguarectPerson2State = self.conf_data['browerimgRect']['magua_rect_person2_state']
        self.browermaguarectPerson3State = self.conf_data['browerimgRect']['magua_rect_person3_state']
        self.ravenclawRectPerson1State = self.conf_data['imgRect']['ravenclaw_rect_person1_state']
        self.ravenclawRectPerson2State = self.conf_data['imgRect']['ravenclaw_rect_person2_state']
        self.ravenclawRectPerson3State = self.conf_data['imgRect']['ravenclaw_rect_person3_state']
        self.browerravenclawRectPerson1State = self.conf_data['browerimgRect']['ravenclaw_rect_person1_state']
        self.browerravenclawRectPerson2State = self.conf_data['browerimgRect']['ravenclaw_rect_person2_state']
        self.browerravenclawRectPerson3State = self.conf_data['browerimgRect']['ravenclaw_rect_person3_state']
    
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
    # def get_screenshot(self): # 截屏时模拟器不要切后台
    def get_startMatchBtn(self, img):
        return img[self.rectStart[1]:self.rectStart[3], self.rectStart[0]:self.rectStart[2], :]  # [150,470,940,660]->img[470:660,150:940,:]
    
    def get_maguabrowergroupstartMatchBtn(self, img):
        return img[self.maguabrowergrouprectStart[1]:self.maguabrowergrouprectStart[3], self.maguabrowergrouprectStart[0]:self.maguabrowergrouprectStart[2], :]

    def get_brower_startMatchBtn(self, img):
        return img[self.browerrectStart[1]:self.browerrectStart[3], self.browerrectStart[0]:self.browerrectStart[2], :]

    def get_ravenclaw_startMatchBtn(self, img):
        return img[self.rectStart[1]:self.rectStart[3], self.rectStart[0]:self.rectStart[2], :]

    def get_CenterContinuBtn(self, img):
        return img[self.rectCenterContinu[1]:self.rectCenterContinu[3], self.rectCenterContinu[0]:self.rectCenterContinu[2], :]

    def get_brower_centercontinueBtn(self, img):
        return img[self.browerectcenterContinue[1]:self.browerectcenterContinue[3], self.browerectcenterContinue[0]:self.browerectcenterContinue[2], :]
    
    def get_brower_continueBtn(self, img):
        return img[self.browerectContinue[1]:self.browerectContinue[3], self.browerectContinue[0]:self.browerectContinue[2], :]
    
    def get_returnBtn(self, img):
        return img[self.rectReturn[1]:self.rectReturn[3], self.rectReturn[0]:self.rectReturn[2], :]

    def get_brower_returnBtn(self, img):
        return img[self.browerectReturn[1]:self.browerectReturn[3], self.browerectReturn[0]:self.browerectReturn[2], :]
    
    def get_continueBtn(self, img):
        return img[self.rectContinue[1]:self.rectContinue[3], self.rectContinue[0]:self.rectContinue[2], :]
    
    def get_maguabrowergroupcontinueBtn(self, img):
        return img[self.maguabrowergrouprectContinue[1]:self.maguabrowergrouprectContinue[3], self.maguabrowergrouprectContinue[0]:self.maguabrowergrouprectContinue[2], :]
    
    def get_countdownBtn(self, img):
        return img[self.rectCountdown[1]:self.rectCountdown[3], self.rectCountdown[0]:self.rectCountdown[2], :]
    
    def get_magua_countdownBtn(self, img):
        return img[self.rect_magua_Countdown[1]:self.rect_magua_Countdown[3], self.rect_magua_Countdown[0]:self.rect_magua_Countdown[2], :]

    def get_brower_countdownBtn(self, img):
        return img[self.browerrectCountdown[1]:self.browerrectCountdown[3], self.browerrectCountdown[0]:self.browerrectCountdown[2], :]

    def get_brower_maguacountdownBtn(self, img):
        return img[self.browermaguarectCountdown[1]:self.browermaguarectCountdown[3], self.browermaguarectCountdown[0]:self.browermaguarectCountdown[2], :]

    def get_maguascoreBtn(self, img):
        return img[self.rectScore[1]:self.rectScore[3], self.rectScore[0]:self.rectScore[2], :]
    
    def get_personState(self, img):
        person1State = img[self.rectPerson1State[1]:self.rectPerson1State[3], self.rectPerson1State[0]:self.rectPerson1State[2], :]
        person2State = img[self.rectPerson2State[1]:self.rectPerson2State[3], self.rectPerson2State[0]:self.rectPerson2State[2], :]
        person3State = img[self.rectPerson3State[1]:self.rectPerson3State[3], self.rectPerson3State[0]:self.rectPerson3State[2], :]
        return person1State, person2State, person3State

    def get_brower_personState(self, img):
        person1State = img[self.browerrectPerson1State[1]:self.browerrectPerson1State[3], self.browerrectPerson1State[0]:self.browerrectPerson1State[2], :]
        person2State = img[self.browerrectPerson2State[1]:self.browerrectPerson2State[3], self.browerrectPerson2State[0]:self.browerrectPerson2State[2], :]
        person3State = img[self.browerrectPerson3State[1]:self.browerrectPerson3State[3], self.browerrectPerson3State[0]:self.browerrectPerson3State[2], :]
        return person1State, person2State, person3State

    def get_brower_maguapersonState(self, img):
        person1State = img[self.browermaguarectPerson1State[1]:self.browermaguarectPerson1State[3], self.browermaguarectPerson1State[0]:self.browermaguarectPerson1State[2], :]
        person2State = img[self.browermaguarectPerson2State[1]:self.browermaguarectPerson2State[3], self.browermaguarectPerson2State[0]:self.browermaguarectPerson2State[2], :]
        person3State = img[self.browermaguarectPerson3State[1]:self.browermaguarectPerson3State[3], self.browermaguarectPerson3State[0]:self.browermaguarectPerson3State[2], :]
        return person1State, person2State, person3State
    
    def get_maguabrowergrouppersonState(self, img):
        person1State = img[self.maguabrowergrouprectPerson1State[1]:self.maguabrowergrouprectPerson1State[3], self.maguabrowergrouprectPerson1State[0]:self.maguabrowergrouprectPerson1State[2], :]
        person2State = img[self.maguabrowergrouprectPerson2State[1]:self.maguabrowergrouprectPerson2State[3], self.maguabrowergrouprectPerson2State[0]:self.maguabrowergrouprectPerson2State[2], :]
        person3State = img[self.maguabrowergrouprectPerson3State[1]:self.maguabrowergrouprectPerson3State[3], self.maguabrowergrouprectPerson3State[0]:self.maguabrowergrouprectPerson3State[2], :]
        return person1State, person2State, person3State
    
    def get_magua_personState(self, img):
        person1State = img[self.rectmaguaperson1state[1]:self.rectmaguaperson1state[3], self.rectmaguaperson1state[0]:self.rectmaguaperson1state[2], :]
        person2State = img[self.rectmaguaperson2state[1]:self.rectmaguaperson2state[3], self.rectmaguaperson2state[0]:self.rectmaguaperson2state[2], :]
        person3State = img[self.rectmaguaperson3state[1]:self.rectmaguaperson3state[3], self.rectmaguaperson3state[0]:self.rectmaguaperson3state[2], :]
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

    def get_maguabrowergroupquestionAndoptionsBtn(self, img):
        QBtn = img[self.maguabrowergrouprectQ[1]:self.maguabrowergrouprectQ[3], self.maguabrowergrouprectQ[0]:self.maguabrowergrouprectQ[2], :]
        ABtn = img[self.maguabrowergrouprectA[1]:self.maguabrowergrouprectA[3], self.maguabrowergrouprectA[0]:self.maguabrowergrouprectA[2], :]
        BBtn = img[self.maguabrowergrouprectB[1]:self.maguabrowergrouprectB[3], self.maguabrowergrouprectB[0]:self.maguabrowergrouprectB[2], :]
        CBtn = img[self.maguabrowergrouprectC[1]:self.maguabrowergrouprectC[3], self.maguabrowergrouprectC[0]:self.maguabrowergrouprectC[2], :]
        DBtn = img[self.maguabrowergrouprectD[1]:self.maguabrowergrouprectD[3], self.maguabrowergrouprectD[0]:self.maguabrowergrouprectD[2], :]
        return QBtn, ABtn, BBtn, CBtn, DBtn
    
    def get_brower_questionAndoptionsBtn(self, img):
        QBtn = img[self.browerrectQ[1]:self.browerrectQ[3], self.browerrectQ[0]:self.browerrectQ[2], :]
        ABtn = img[self.browerrectA[1]:self.browerrectA[3], self.browerrectA[0]:self.browerrectA[2], :]
        BBtn = img[self.browerrectB[1]:self.browerrectB[3], self.browerrectB[0]:self.browerrectB[2], :]
        CBtn = img[self.browerrectC[1]:self.browerrectC[3], self.browerrectC[0]:self.browerrectC[2], :]
        DBtn = img[self.browerrectD[1]:self.browerrectD[3], self.browerrectD[0]:self.browerrectD[2], :]
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