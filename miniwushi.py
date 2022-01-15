# 分析黑魔法防御课界面 
import cv2
import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import random

import warnings
warnings.filterwarnings('ignore') # warnings有点多，过滤一下

walk_coordinate = [[192,287],[95,615],[436,360],[487,538],[717,629],[689,303]]
card_coordinate = [[560,820],[695,820],[842,814],[985,829],[1390,830]]

# sellist ['弗立维','麦格','斯内普','贝拉','哈利','赫敏','罗恩','乔治','纽特','纳威','多比','塞德里克','卢娜','马尔福']
# needsellist = ['弗立维','麦格','斯内普','贝拉']
needsellist = []
def matchlist(needsellist,val):
    for x in needsellist:
        if x in val:
            return True
    return False

# [[[1288.0, 831.0], [1421.0, 831.0], [1421.0, 867.0], [1288.0, 867.0]], ('开始匹配', 0.9985269)]

# [[[454.0, 597.0], [674.0, 601.0], [673.0, 637.0], [453.0, 633.0]], ('德拉科·马尔福', 0.88426673)] [595:640,450:675]
# [[[931.0, 599.0], [1146.0, 599.0], [1146.0, 634.0], [931.0, 634.0]], ('卢娜·洛夫古德', 0.91714483)] [585:650,915:1160]
# [[[649.0, 845.0], [748.0, 845.0], [748.0, 874.0], [649.0, 874.0]], ('透4刷新', 0.765049)]
# [[[850.0, 841.0], [976.0, 841.0], [976.0, 870.0], [850.0, 870.0]], ('确认选择', 0.99763954)] [835:875,845:980]

# 560,820 伙伴或分身
# 695,820 ka1
# 842,814 ka2
# 985,829 ka3
# 11390,830 ka4

# 192,287 dian1
# 95,615 dian2
# 436,360 dian3
# 487,538 dian4
# 717,629 dian5
# 689,303 dian6

# [[[767.0, 850.0], [838.0, 850.0], [838.0, 881.0], [767.0, 881.0]], ('返回', 0.9956496)] [840:890,760:845]
# [[[1158.0, 888.0], [1328.0, 888.0], [1328.0, 912.0], [1158.0, 912.0]], ('?点击继续子', 0.7529184)] [870:930,1190:1300]

# 日志
def make_print_to_file(path='./'):
    '''
    path， it is a path for save your log about fuction print
    example:
    use  make_print_to_file()   and the   all the information of funtion print , will be write in to a log file
    :return:
    '''
    import sys
    import os
    # import config_file as cfg_file
    import sys
    import datetime
 
    class Logger(object):
        def __init__(self, filename="Default.log", path="./"):
            self.terminal = sys.stdout
            import os
            if not os.path.exists(path): # 判断文件夹是否存在，不存在则创建文件夹
                os.mkdir(path)
            self.log = open(os.path.join(path, filename), "a", encoding='utf8',)
 
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

        def flush(self):
            pass

    fileName = datetime.datetime.now().strftime('log_miniwushi'+'%Y_%m_%d_%H')
    sys.stdout = Logger(fileName + '.log', path=path)



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



def is_start(img, str_start):
    img_start = screen.get_startMatchBtn(img)
    result_start = ocr.ocr(img_start)
    content_start = ocr.ocr_content(result_start)
    content_start = filterLine(content_start)
    if len(content_start)>0 and content_start[0] == str_start:
        if epoch_num == 0:
            exit()
        time.sleep(5)
        x, y = 1300, 840
        left_click(win_rect[0]+x,win_rect[1]+y,2)
        time.sleep(15)
        return True
    return False

epoch_num = 3

if __name__ == '__main__':
    # 获取配置文件
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    make_print_to_file(path='./log/')

    # 初始化ocr模型
    ocr = OCRImp(conf_data)

    # 初始化屏幕操作模块
    screen = ScreenImp(conf_data)

    
    count_steps = 0
    
    epoch = input('请输入轮数:\n')
    if(epoch!=''):
        epoch_num = int(epoch)
    # count_steps = 0
    # epoch_num = 3
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
        flag1 = is_start(img, '开始匹配')
        flag2 = is_start(img, '准备')
        if flag1 or flag2: # 识别到了就跳过，重新截图
            epoch_num -= 1
            continue
        
        # 选定角色
        btnok = img[835:875,845:980]
        result_btnok = ocr.ocr(btnok)
        content_btnok = ocr.ocr_content(result_btnok)
        content_btnok = filterLine(content_btnok)
        if len(content_btnok)>0 and content_btnok[0] == '确认选择':
            sel1 = img[585:650,420:700]
            result_sel1 = ocr.ocr(sel1)
            content_sel1 = ocr.ocr_content(result_sel1)
            content_sel1 = filterLine(content_sel1)
            issel1inlist = matchlist(needsellist,content_sel1[0])

            sel2 = img[585:650,885:1190]
            result_sel2 = ocr.ocr(sel2)
            content_sel2 = ocr.ocr_content(result_sel2)
            content_sel2 = filterLine(content_sel2)
            issel2inlist = matchlist(needsellist,content_sel2[0])

            if issel1inlist and not issel2inlist:
                x, y = 521, 521
                print('优先选择了'+content_sel1[0])
            elif issel2inlist and not issel1inlist:
                x, y = 1000, 521
                print('优先选择了'+content_sel2[0])
            else:
                idx = random.randint(1, 2)
                if idx == 1:
                    # sel = img[585:650,420:700]
                    # result_sel = ocr.ocr(sel)
                    # content_sel = ocr.ocr_content(result_sel)
                    # content_sel = filterLine(content_sel)
                    x, y = 521, 521
                    print('随机选择了'+content_sel1[0])
                else:
                    # sel = img[585:650,885:1190]
                    # result_sel = ocr.ocr(sel)
                    # content_sel = ocr.ocr_content(result_sel)
                    # content_sel = filterLine(content_sel)
                    x, y = 1000, 521
                    print('随机选择了'+content_sel2[0])
            left_click(win_rect[0]+x,win_rect[1]+y,2) # 选定角色
            time.sleep(2)

            x, y = 900, 855
            left_click(win_rect[0]+x,win_rect[1]+y,2) # 按确定
            time.sleep(20)
            continue

        # 识别返回按钮
        img_continue = img[840:890,760:845]
        result_continue = ocr.ocr(img_continue)
        content_continue = ocr.ocr_content(result_continue)
        content_continue = filterLine(content_continue)
        if len(content_continue)>0 and content_continue[0] == '返回':
            print('失败')
            x, y = 800, 865
            left_click(win_rect[0]+x,win_rect[1]+y,2)
            time.sleep(6)
            continue

        # 识别继续按钮
        img_continue = img[870:930,1190:1300]
        result_continue = ocr.ocr(img_continue)
        content_continue = ocr.ocr_content(result_continue)
        content_continue = filterLine(content_continue)
        if len(content_continue)>0 and content_continue[0] == '点击继续':
            x, y = 1250, 900
            left_click(win_rect[0]+x,win_rect[1]+y,2)
            time.sleep(6)
            continue
        

        img_steps, img_5 = '-1', '11'
        img_steps = img[800:850, 200:265]
        img_5 = img[878:932,556:637] # 蓝条
        result_steps = ocr.ocr(img_steps)
        result_5 = ocr.ocr(img_5)
        result_steps = ocr.ocr_content(result_steps)
        result_steps = filterLine(result_steps)
        result_5 = ocr.ocr_content(result_5)
        result_5 = filterLine(result_5)

        if (result_steps!=None) and len(result_steps) > 0 and result_steps[0].isdigit():
            result_steps = int(result_steps[0][0][0])
        else:
            result_steps = 0

        if (result_5!=None) and len(result_5) > 0 and result_5[0].isdigit():
            result_5 = int(result_5[0][0][0])
        else:
            result_5 = -1
        
        idx = random.randint(1, 4)
        walk_idx = random.randint(0,3)
        x_walk, y_walk = walk_coordinate[walk_idx][0], walk_coordinate[walk_idx][1]
        x_0, y_0 = card_coordinate[0][0], card_coordinate[0][1] # 伙伴卡
        x, y = card_coordinate[idx][0], card_coordinate[idx][1]
        # if result_5 == -1 or result_5 > 5:
        if count_steps % 10 == 3:
            left_click(win_rect[0]+x_0,win_rect[1]+y_0,4) # 放10个技能 点击伙伴卡
        count_steps += 1
        left_click(win_rect[0]+x,win_rect[1]+y,4) # 点击目标卡
        left_click(win_rect[0]+x_walk,win_rect[1]+y_walk,2) # 1个技能走一步
        # print('所剩步数：',result_steps)
        # print('剩余费用：',result_5)
        # print('点击位置：', x, y)