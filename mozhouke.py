# 分析黑魔法防御课界面 
# """
import cv2
import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState
from paddleocr import PaddleOCR

# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)
    
# 初始化ocr模型
ocr = OCRImp(conf_data)

# 初始化屏幕操作模块
screen = ScreenImp(conf_data)

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
# walk_coordinate = [[330,640],[1260,630],[740,550]] # 左 右 中
# card_coordinate = [[522,820],[695,798],[838,821],[987,818],[1185,830]] # ~ 1 2 3 4
charms_coordinate = [[200,770,300,855],[630,700,676,777],[765,690,818,778],[910,700,960,775],[1060,700,1108,786],[556, 878,637, 922]] # states: steps 1 2 3 4 HP
# copy_coordinate = [[540,400,650,500],[980,345,1090,445],[1160,320,1260,420]]

win_rect, img= screen.get_screenshot()

# img_path = './img/harry_charmsclass.png'
# img = cv2.imread(img_path)
# img_steps = img[770:855,200:300]
# img1 = img[700:800,600:700]
# img2 = img[690:778,765:818] # 点击 850 716
# img3 = img[700:775,910:960]
# img4 = img[700:786,1060:1108]
# img5 = img[878:932,556:637] # 蓝条
walk_coordinate = [[1360,650],[850,712],[340,680]]
card_coordinate = [[522,820],[695,798],[838,821],[987,818],[1122,830]] # ~ 1 2 3 4
import matplotlib.pyplot as plt

# result = ocr.ocr(img, det=True, cls=True)
# print(result)
# plt.imshow(img)
# plt.show()
# """

def is_start(img, str_start):
    img_start = screen.get_startMatchBtn(img)
    result_start = ocr.ocr(img_start)
    content_start = ocr.ocr_content(result_start)
    content_start = filterLine(content_start)
    if len(content_start)>0 and str_start in content_start[0]:
        time.sleep(5)
        global epoch_num
        epoch_num -= 1
        if epoch_num == -1:
            exit()
        x, y = 1300, 840
        left_click(win_rect[0]+x,win_rect[1]+y,2)
        return True
    return False
count_steps = 0
epoch_num = 3
epoch = input('请输入轮数:')
if(epoch!=''):
    epoch_num = int(epoch)
while True:
    import time
    time.sleep(2)
    win_rect, img= screen.get_screenshot() 
    # img_path = './img/harry_darkclass3.png' # 

    # img = cv2.imread(img_path)
    # print(img.shape)
    # img = img[875:920,1185:1300] # [1185, 875, 1300, 920] 点击继续
    # img = img[830:880, 1234:1414] # [1234,830,1414,880] 匹配上课

    # 识别匹配上课
    flag0 = is_start(img, '准备')
    flag1 = is_start(img, '匹配上课')
    flag2 = is_start(img, '上课')
    flag3 = is_start(img, '学院活动匹配')
    if flag0 or flag1 or flag2 or flag3: # 识别到了就跳过，重新截图
        time.sleep(1)
        continue
    
    # 识别继续按钮
    img_continue = img[875:920,1185:1300]
    result_continue = ocr.ocr(img_continue)
    content_continue = ocr.ocr_content(result_continue)
    content_continue = filterLine(content_continue)
    if len(content_continue)>0 and content_continue[0] == '点击继续':
        x, y = 1200, 890
        left_click(win_rect[0]+x,win_rect[1]+y,2)
        continue
    
    img_steps, img_1, img_2, img_3, img_4, img_5 = '-1', '15', '15', '15', '15', '11'
    img_steps = img[770:855,200:300]
    img_1 = img[700:800,600:700]
    img_2 = img[690:778,765:818] # 点击 850 716
    img_3 = img[700:775,910:960]
    img_4 = img[700:786,1060:1108]
    img_5 = img[878:932,556:637] # 蓝条
    result_steps = ocr.ocr(img_steps)
    result_1 = ocr.ocr(img_1)
    result_2 = ocr.ocr(img_2)
    result_3 = ocr.ocr(img_3)
    result_4 = ocr.ocr(img_4)
    result_5 = ocr.ocr(img_5)
    result_steps = ocr.ocr_content(result_steps)
    result_steps = filterLine(result_steps)
    result_1 = ocr.ocr_content(result_1)
    result_1 = filterLine(result_1)
    result_2 = ocr.ocr_content(result_2)
    result_2 = filterLine(result_2)
    result_3 = ocr.ocr_content(result_3)
    result_3 = filterLine(result_3)
    result_4 = ocr.ocr_content(result_4)
    result_4 = filterLine(result_4)
    result_5 = ocr.ocr_content(result_5)
    result_5 = filterLine(result_5)
    if (result_steps!=None) and len(result_steps) > 0 and result_steps[0].isdigit():
        result_steps = int(result_steps[0][0][0])
    else:
        result_steps = 0
    if (result_1!=None) and len(result_1) > 0 and result_1[0].isdigit():
        result_1 = int(result_1[0][0][0])
    else:
        result_1 = 15
    if (result_2!=None) and len(result_2) > 0 and result_2[0].isdigit():
        result_2 = int(result_2[0][0][0])
    else:
        result_2 = 15
    if (result_3!=None) and len(result_3) > 0 and result_3[0].isdigit():
        result_3 = int(result_3[0][0][0])
    else:
        result_3 = 15
    if (result_4!=None) and len(result_4) > 0 and result_4[0].isdigit():
        result_4 = int(result_4[0][0][0])
    else:
        result_4 = 15
    if (result_5!=None) and len(result_5) > 0 and result_5[0].isdigit():
        result_5 = int(result_5[0][0][0])
    else:
        result_5 = -1
    fee = [result_1,result_2,result_3,result_4]
    # idx = fee.index(min(fee))
    import random
    # idx = random.randint(0, 3)
    # if fee[idx]>7:
    #     continue
    walk_idx = random.randint(0, 2)
    idx = random.randint(0, 3)
    x_walk, y_walk = walk_coordinate[walk_idx][0], walk_coordinate[walk_idx][1]
    x_0, y_0 = card_coordinate[0][0], card_coordinate[0][1] # 伙伴卡
    x, y = card_coordinate[idx+1][0], card_coordinate[idx+1][1]
    print('***********剩余费用：',result_5)
    if result_5 == -1 or result_5 == 1 or result_5 > 7:
        if count_steps % 3 == 0:
            left_click(win_rect[0]+x_walk,win_rect[1]+y_walk,4) # 走一步
            left_click(win_rect[0]+x_0,win_rect[1]+y_0,4) # 点击伙伴卡
        count_steps += 1
        # left_click(win_rect[0]+x_walk,win_rect[1]+y_walk,4) # 走一步
        # left_click(win_rect[0]+x_0,win_rect[1]+y_0,4) # 点击伙伴卡
        left_click(win_rect[0]+x,win_rect[1]+y,4) # 点击目标卡
        print('所剩步数：',result_steps)
        print('卡1费用：',result_1)
        print('卡2费用：',result_2)
        print('卡3费用：',result_3)
        print('卡4费用：',result_4)
        print('剩余费用：',result_5)
        print('点击位置：', x, y)

# """
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# import matplotlib.pyplot as plt
# plt.imshow(img)
# plt.show()
# cv2.imwrite('./img/harry_charmsclass.png',img)