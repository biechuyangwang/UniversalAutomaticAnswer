# x = [(33,'A',0),(44,'B',1),(55,'C',2),(66,'D',3)]
# print(x[1][2])

# 测试其他模拟器的点击，证明有些模拟器上点击时，需要管理员权限
import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包

import win32api, win32con
import pyautogui
def left_click(x,y,times=1):
    pyautogui.click(x,y,duration=0.5)
    # win32api.SetCursorPos((x,y))
    # import time
    # while times:
    #     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    #     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    #     times -= 1

# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)

screen = ScreenImp(conf_data)
win_rect, img= screen.get_screenshot() 

# click 774,754
import time
time.sleep(10)
x, y = 774, 754
left_click(win_rect[0]+x,win_rect[1]+y,2)

import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()