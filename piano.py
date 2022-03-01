#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径

# 参数
"""
速度：默认60
节拍：默认44拍
调：默认C调

全音符用44表示
半音符用24表示
四分之一音符用14表示
八分之一音符用18表示

(236,680) (1370,680) (1370-236)/6= 189
236 425 614 803 992 1181 1370
(236,830) (1370,830)

530 680 830 # 460 610 760
330 1265 (1265-330)/5=187
"""

# 谱子
# 参数0表示 第几排 简单模式只有第2和第3排
# 参数1表示 第几个音
# 参数2表示 间隔

x_start_pos = 236
x_shap_start_pos = 330
y_start_pos = 530
Y_shap_start_pos = 460
x_off = 189
y_off = 50
x_shap_off = 187
y_shap_off = 50

time_interval = 0.25 # 四分音符间隔时间

puzi = [1,1,2, 1,2,2, 1,3,2, 1,1,2, 
1,1,2, 1,2,2, 1,3,2, 1,1,2, 
1,3,2, 1,4,2, 1,5,4, 
1,3,2, 1,4,2, 1,5,4, 
1,5,1, 1,6,1, 1,5,1, 1,4,1, 1,3,2, 1,1,2, 
1,5,1, 1,6,1, 1,5,1, 1,4,1, 1,3,2, 1,1,2, 
1,3,2, 2,5,2, 1,1,4, 
1,3,2, 2,5,2, 1,1,4]

import win32api,win32con
import time
def left_click_1(x,y,times=1):
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        times -= 1
    print('左键点击',x,y)

if __name__ == '__main__':
    import time
    time.sleep(10)
    import win32gui
    screen_hwnd = "android9"
    hwnd = win32gui.FindWindow(None, screen_hwnd)
    if hwnd:
        win_rect = win32gui.GetWindowRect(hwnd)
    print(win_rect[0],win_rect[1])
    time.sleep(5)
    for i,val in enumerate(puzi):
        if i%3==0:
            y_pos = y_start_pos + val * y_off
        if i%3==1:
            x_pos = x_start_pos + (val-1) * x_off
        if i%3==2:
            t_interval = val * time_interval
            left_click_1(x_pos+win_rect[0],y_pos+win_rect[1])
            print(x_pos+win_rect[0],y_pos+win_rect[1])
            time.sleep(t_interval)
            break


