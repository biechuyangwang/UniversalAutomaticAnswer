# 通用截屏
import numpy as np
import win32gui
import win32ui
import win32con
import matplotlib.pyplot as plt
from PIL import Image

def get_windows_screen():
    hwnd = win32gui.FindWindow(None, "网易云游戏平台 - Google Chrome")
    # hwnd = 24928
    win_rect = win32gui.GetWindowRect(hwnd)
    print(win_rect)
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    width = win_rect[2] - win_rect[0]
    height = win_rect[3] - win_rect[1]
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0), (width, height), dcObj, (win_rect[0], win_rect[0]), win32con.SRCCOPY)

    dataBitMap.SaveBitmapFile(cDC,'test.bmp')

    bmInfo = dataBitMap.GetInfo()
    bmpstr = dataBitMap.GetBitmapBits(True)

    # im = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype = np.uint8)
    im = Image.frombuffer("RGB", (bmInfo["bmWidth"], bmInfo["bmHeight"]), bmpstr, "raw", "BGRX", 0, 1)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    # return im.reshape(bmInfo['bmHeight'], bmInfo['bmWidth'], 4)[:,:,:]
    return im

im = get_windows_screen()
# print(im.shape)
plt.imshow(im)
plt.show()
# 分析黑魔法防御课界面 
"""


import cv2
import sys
import win32gui
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch") # mode load
# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)

screen = ScreenImp(conf_data)
win_rect, img= screen.get_screenshot()

# left click
import win32api
import win32con
def left_click(x,y,times=4):
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        times -= 1
walk_coordinate = [[330,640],[1260,630],[740,550]] # 左 右 中
card_coordinate = [[522,820],[695,798],[838,821],[987,818],[1185,830]] # ~ 1 2 3 4
copy_coordinate = [[540,400,650,500],[980,345,1090,445],[1160,320,1260,420]]
# img_path = './img/harry_test_state.png'
# img_path = './img/harry_2021_12_26_01_05_17.png'
# img = cv2.imread(img_path)
import matplotlib.pyplot as plt
# img = img[720:920,131:1460,::-1] # 131 720 1460 920
# option1 = img[720:820,131:520,::-1]
# option2 = img[720:820,831:1260,::-1]
# option3 = img[820:920,131:520,::-1]
# option4 = img[820:920,831:1260,::-1]
# img1 = img[400:500,540:650,::-1]
# img2 = img[345:445,980:1090]
# img3 = img[320:420,1160:1260]
# status1 = img[390:490,540:640] # [[[568.0, 397.0], [625.0, 397.0], [625.0, 421.0], [568.0, 421.0]], ('/+15', 0.86291903)]
# status2 = img[350:450,990:1090] # [[[999.0, 355.0], [1079.0, 355.0], [1079.0, 381.0], [999.0, 381.0]], ('V+15', 0.87752867)]
# status3 = img[330:430,1165:1265] # [[[1177.0, 333.0], [1259.0, 333.0], [1259.0, 359.0], [1177.0, 359.0]], ('<+20', 0.8773143)]
result = ocr.ocr(img, det=True, cls=True)
print(result)
plt.imshow(img)
plt.show()
"""
"""
while True:
    import time
    time.sleep(2)
    win_rect, img= screen.get_screenshot() 
    # img_path = './img/harry_darkclass3.png' # 

    # img = cv2.imread(img_path)
    # print(img.shape)
    # img = img[875:920,1185:1300] # [1185, 875, 1300, 920] 点击继续
    # img = img[830:880, 1234:1414] # [1234,830,1414,880] 匹配上课
    img_steps, img_1, img_2, img_3, img_4, img_5 = '0', '14', '14', '14', '14', '14'
    img_steps = img[800:850, 200:265] # steps
    img_1 = img[710:777, 615:665] # 1
    img_2 = img[710:777, 770:820] # 2
    img_3 = img[710:777, 920:970] # 3
    img_4 = img[720:787, 1060:1110] # 4
    img_5 = img[768:816, 1205:1246,::-1] # 5 1206 768 1236 816

    result_steps = ocr.ocr(img, det=True, cls=True)
    result_1 = ocr.ocr(img_1, det=True, cls=True)
    result_2 = ocr.ocr(img_2, det=True, cls=True)
    result_3 = ocr.ocr(img_3, det=True, cls=True)
    result_4 = ocr.ocr(img_4, det=True, cls=True)
    result_5 = ocr.ocr(img_5, det=True, cls=True)
    if len(result_steps)>0 and result_steps[0][1][0].isdigit():
        result_steps = int(result_steps[0][1][0])
    else:
        result_steps = 0
    if len(result_1)>0 and result_1[0][1][0].isdigit():
        result_1 = int(result_1[0][1][0])
    else:
        result_1 = 15
    if len(result_2)>0 and result_2[0][1][0].isdigit():
        result_2 = int(result_2[0][1][0])
    else:
        result_2 = 15
    if len(result_3)>0 and result_3[0][1][0].isdigit():
        result_3 = int(result_3[0][1][0])
    else:
        result_3 = 15
    if len(result_4)>0 and result_4[0][1][0].isdigit():
        result_4 = int(result_4[0][1][0])
    else:
        result_4 = 15
    if len(result_5)>0 and result_5[0][1][0].isdigit():
        result_5 = int(result_5[0][1][0])
    else:
        result_5 = 15
    fee = [result_1,result_2,result_3,result_4]
    idx = fee.index(min(fee))
    import random
    # idx = random.randint(0, 3)
    # if fee[idx]>7:
    #     continue
    walk_idx = random.randint(0, 2)
    x_walk, y_walk = walk_coordinate[walk_idx][0], walk_coordinate[walk_idx][1]
    x_0, y_0 = card_coordinate[0][0], card_coordinate[0][1] # 伙伴卡
    x, y = card_coordinate[idx+1][0], card_coordinate[idx+1][1]
    left_click(win_rect[0]+x_walk,win_rect[1]+y_walk,4) # 点击伙伴卡
    left_click(win_rect[0]+x_0,win_rect[1]+y_0,4) # 点击伙伴卡
    left_click(win_rect[0]+x,win_rect[1]+y,4) # 点击目标卡
    print('所剩步数：',result_steps)
    print('卡1费用：',result_1)
    print('卡2费用：',result_2)
    print('卡3费用：',result_3)
    print('卡4费用：',result_4)
    print('卡5费用：',result_5)
    print('点击：', x, y)


# cv2.imshow('img', img)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
import matplotlib.pyplot as plt
plt.imshow(img)
plt.show()
# cv2.imwrite('./img/harry_darkclass.png',img)

"""

# # 处理哈利题库
# import csv
# with open('csvImp/哈利波特题库_12_15.csv','r', encoding='utf-8-sig') as csvfile:
#     reader = csv.reader(csvfile,delimiter=' ')
#     reader = list(reader)
#     for idx, row in enumerate(reader):
#         if len(row) != len(reader[0]):
#             print(row)
# 	# raw_data = list(map(lambda row: (row[1], row[2]), reader))

# 测试题目包含英语处理
# contentq = ['开始', '是谁创建了S.P.E.W.一', '家养小精灵权益促进会吗？', 'WhocreatedS.P.E.W.-SocietyforthePromotionofElfishWelfare?']
# r1 = "[\sa-zA-Z．：“”（）\?\'\"《》\-:\.：·\*\.\+\$\^\[\]\(\)\{\}\|]+"
# import re
# content_list_sub = [content for content in contentq if len(re.sub(r1, '', content))>0]
# print(content_list_sub)
# output
# ['开始', '是谁创建了S.P.E.W.一', '家养小精灵权益促进会吗？']

# x = [(33,'A',0),(44,'B',1),(55,'C',2),(66,'D',3)]
# print(x[1][2])

# 测试其他模拟器的点击，证明有些模拟器上点击时，需要管理员权限
# import sys
# sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
# from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
# from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包

# import win32api, win32con
# import pyautogui
# def left_click(x,y,times=1):
#     pyautogui.click(x,y,duration=0.5)
#     # win32api.SetCursorPos((x,y))
#     # import time
#     # while times:
#     #     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
#     #     win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
#     #     times -= 1

# # 获取配置文件
# conf_path = 'conf/conf.yml'
# conf_data = get_yaml_file(conf_path)

# screen = ScreenImp(conf_data)
# win_rect, img= screen.get_screenshot() 

# # click 774,754
# import time
# time.sleep(10)
# x, y = 774, 754
# left_click(win_rect[0]+x,win_rect[1]+y,2)

# import matplotlib.pyplot as plt
# plt.imshow(img)
# plt.show()