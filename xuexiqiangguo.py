#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
写了个简单的程序，用来以后讲解如何扩展UAA
声明：我党不要怪我，我也是为了学习而写的，不商业化
""" 

import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterEngLine, filterPersonState
from UniversalAutomaticAnswer.httpImp.search import searchImp
import time

# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)

# 初始化ocr模型
ocr = OCRImp(conf_data)
while(True):
    continue_flag = input("是否继续？(y/n)")
    if(continue_flag == 'n'):
        break
    start = time.time()*1000
    screen = ScreenImp(conf_data)
    win_rect, img= screen.get_screenshot()
    rect = [577,160,1025,900]
    imgrect = img[rect[1]:rect[3], rect[0]:rect[2], :]
    result_imgrect = ocr.ocr(imgrect)
    content_imgrect = ocr.ocr_content(result_imgrect)
    print('ocr耗时：{0:4f}ms'.format(time.time()*1000-start))
    # print(result_imgrect)
    # print(content_imgrect)


    if '题' in content_imgrect[0]:
        question_type = content_imgrect[0]
        question_num = content_imgrect[1].split('/')
    else:
        question_type = content_imgrect[1]
        question_num = content_imgrect[0].split('/')

    if '填空题' in question_type:
        question_type = '填空题'
    elif '判断题' in question_type:
        question_type = '判断题'
    elif '单选题' in question_type:
        question_type = '单选题'
    elif '多选题' in question_type:
        question_type = '多选题'

    # question_cur_num = question_num[0]
    # question_total_num = question_num[1]
    print('题目类型：',question_type)
    # print('题目数量：',question_total_num)
    # print('当前题目：',question_cur_num)


    # content_imgrect = content_imgrect[2:i]
    if question_type == '填空题':
        i=-1
        for idx,x in enumerate(content_imgrect):
            if '来源：' in x:
                i=idx
                break
        # content_imgrect = content_imgrect[2:i]
        # questions = ['1931年，中华苏维埃共和国临时中央政府在', '成立。']
        question = ''.join(questions)
        print('题目：',question)
    elif question_type == '多选题':
        question_cur = -1
        options_cur = -1
        options_end = -1
        for idx,x in enumerate(content_imgrect):
            if '来源：' in x:
                question_cur=idx
                continue
            if 'A.' in x:
                options_cur=idx
                continue
            if '出题：' in x:
                options_end=idx
                break
        # print(question_cur, options_cur, options_end)
        questions = content_imgrect[2:question_cur]
        """
        content_imgrect = ['2/5', '/多选题', '1939年冬至1940年春，国民党顽固派掀起第一次', '反共高潮，中国共产党给坚决回击，并在总结', '仅摩擦斗争经\
    验的基础上，为了坚持、巩固和扩', '大抗日民族统一战线，制定了“', '"的策略方针。', '来源：《中国共产党简史》', '（人民出版社\
    、中共', '党史出版社2021年版', 'A.发展进步势力', 'B.争取中间势力', 'C.孤立顽固势力', '出题：中国人民大学中共党史党建研究院\
    ', '9查看提示']
        """
        question = ''.join(questions)
        if options_end != -1:
            options = content_imgrect[options_cur:options_end]
        else:
            options = content_imgrect[options_cur:]
        print('题目：',question)
        print('选项：',options)
        options = filterEngLine(options)
        # print('过滤后的选项：',options)

        searchimp = searchImp(conf_data)
        ans_baidu = searchimp.baidu(question, options)
        print('百度答案：',ans_baidu)
    elif question_type == '单选题':
        question_cur = -1
        options_cur = -1
        options_end = -1
        for idx,x in enumerate(content_imgrect):
            if '来源：' in x:
                question_cur=idx
                continue
            if 'A.' in x:
                options_cur=idx
                continue
            if '出题：' in x:
                options_end=idx
                break
        # print(question_cur, options_cur, options_end)
        questions = content_imgrect[2:question_cur]
        """
        content_imgrect = ['2/5', '/多选题', '1939年冬至1940年春，国民党顽固派掀起第一次', '反共高潮，中国共产党给坚决回击，并在总结', '仅摩擦斗争经\
    验的基础上，为了坚持、巩固和扩', '大抗日民族统一战线，制定了“', '"的策略方针。', '来源：《中国共产党简史》', '（人民出版社\
    、中共', '党史出版社2021年版', 'A.发展进步势力', 'B.争取中间势力', 'C.孤立顽固势力', '出题：中国人民大学中共党史党建研究院\
    ', '9查看提示']
        """
        question = ''.join(questions)
        if options_end != -1:
            options = content_imgrect[options_cur:options_end]
        else:
            options = content_imgrect[options_cur:]
        print('题目：',question)
        print('选项：',options)
        options = filterEngLine(options)
        # print('过滤后的选项：',options)

        searchimp = searchImp(conf_data)
        ans_baidu = searchimp.baidu(question, options)
        print('百度答案：',ans_baidu)
    print('总耗时：{0:4f}ms'.format(time.time()*1000-start))
    # import matplotlib.pyplot as plt
    # plt.imshow(imgrect) # 577,160,1025,555
    # plt.show()




"""
import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径

from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState
from UniversalAutomaticAnswer.match.matchImp import DataMatcher, match_options
import cv2
import time
import pandas as pd

import warnings
warnings.filterwarnings('ignore') # warnings有点多，过滤一下
# left click
import win32api
import win32con

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

    fileName = datetime.datetime.now().strftime('log_'+'%Y_%m_%d_%H')
    sys.stdout = Logger(fileName + '.log', path=path)

# 记录错题
def write_new_question(info, answer_flag=""):
    import time
    # 格式化成2021-12-01形式
    time_str = time.strftime("%Y-%m-%d", time.localtime()) 
    # print(time_str)
    line = info[0] + ' ' + ' '.join(list(info[1])) + ' ' + answer_flag
    d = [line,]
    df = pd.DataFrame(data=d)
    # print(line)
    
    import os
    if not os.path.exists('./new_questions/'): # 判断文件夹是否存在，不存在则创建文件夹
        os.mkdir('./new_questions/')
    # 新题目按时间新建文件，追加的方式保留当天的新题
    df.to_csv('./new_questions/'+time_str+'_harry_questions.csv', mode='a', header=False)

def left_click(x,y,times=1):
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
        times -= 1
    # print('左键点击',x,y)

def is_start(img, str_start):
    img_start = screen.get_startMatchBtn(img)
    result_start = ocr.ocr(img_start)
    content_start = ocr.ocr_content(result_start)
    content_start = filterLine(content_start)
    if len(content_start)>0 and content_start[0] == str_start:
        time.sleep(5)
        x, y = 1300, 840
        left_click(win_rect[0]+x,win_rect[1]+y,2)
        return True
    return False

def get_question_answer(img):
    # 一次答题流程
    res = []
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_questionAndoptionsBtn(img)
    resultq = ocr.ocr(QBtn)
    resulta = ocr.ocr(ABtn)
    resultb = ocr.ocr(BBtn)
    resultc = ocr.ocr(CBtn)
    resultd = ocr.ocr(DBtn)

    contentq = ocr.ocr_content(resultq)
    contenta = ocr.ocr_content(resulta)
    contentb = ocr.ocr_content(resultb)
    contentc = ocr.ocr_content(resultc)
    contentd = ocr.ocr_content(resultd)
    print(contentq)

    optiona,optionb,optionc,optiond = '', '', '', ''
    question = filterQuestion(contentq)[0]
    print(question)

    if len(filterLine(contenta))>0:
        optiona = filterLine(contenta)[0]
    if len(filterLine(contentb))>0:
        optionb = filterLine(contentb)[0]
    if len(filterLine(contentc))>0:
        optionc = filterLine(contentc)[0]
    if len(filterLine(contentd))>0:
        optiond = filterLine(contentd)[0]
    options = [optiona, optionb, optionc, optiond]
    print('ocr结果:', [question,options])

    answer_list = list(data_matcher.get_close_match(question))
    if len(answer_list) == 0 or list(answer_list[0])[1] < 40:
        print('没有匹配到题库')
        return res
    else:
        print('题库匹配结果:', answer_list[0])
        answer = answer_list[0][0][1]
        res = match_options(answer, options)
        print('选项匹配结果:', res)
        return res


coordinate = [
    [500,734],
    [1200,734],
    [500,846],
    [1200,848]
]
if __name__ == '__main__':
    is_answered = 1
    # 获取配置文件
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    make_print_to_file(path='./log/')
    
    # 初始化ocr模型
    ocr = OCRImp(conf_data)

    # 初始化匹配器(题库)
    data_matcher = DataMatcher(conf_data)

    # 截屏
    screen = ScreenImp(conf_data)
    sel = '1'
    sel = input('魔法史还是学院活动？1.魔法史 2.学院活动 3.退出\n')
    if sel == '3':
        exit()
    while True:
        win_rect, img= screen.get_screenshot()
        # img = cv2.imread(screen.ravenclaw_imgpath)

        # 识别计时器
        img_countdown = screen.get_countdownBtn(img)
        result_countdown = ocr.ocr(img_countdown)
        content_countdown = ocr.ocr_content(result_countdown)
        content_countdown = filterLine(content_countdown)
        # print(content_countdown)
        countdown_num = -1
        if (content_countdown!=None) and len(content_countdown) > 0 and content_countdown[0].isdigit():
            countdown_num = int(content_countdown[0])
        else: # 没识别到计时器，就识别开始和继续按钮
            if sel == '1': # 魔法史
                flag = is_start(img, '匹配上课')
                if(flag): # 识别到了就跳过，重新截图
                    continue
            elif sel == '2': # 学院活动
                flag = is_start(img, '学院活动匹配')
                if(flag): # 识别到了就跳过，重新截图
                    continue
            # 识别继续按钮
            img_continue = screen.get_continueBtn(img)
            result_continue = ocr.ocr(img_continue)
            content_continue = ocr.ocr_content(result_continue)
            content_continue = filterLine(content_continue)
            if len(content_continue)>0 and content_continue[0] == '点击继续':
                x, y = 1200, 890
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                if sel == '2':
                    time.sleep(10)
                    left_click(win_rect[0]+x,win_rect[1]+y,1)
                continue
        if countdown_num == 12:
            is_answered = 0
            time.sleep(0.1)
            win_rect, img= screen.get_screenshot()
            # img = cv2.imread(screen.ravenclaw_imgpath)
            res = get_question_answer(img)
            if len(res) >0:
                print('这题选',chr(ord('A')+int(res[0][2])))
                x,y = coordinate[res[0][2]][0], coordinate[res[0][2]][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
                time.sleep(8)
            else:
                print('抄答案吧！')
            continue
        if (is_answered == 0 and countdown_num > 3):
            if countdown_num >=10:
                win_rect, img = screen.get_screenshot() # 别人的答案没稳定下来，重新截图
            # img = cv2.imread(screen.ravenclaw_imgpath)
            if sel == '1':
                person1State, person2State, person3State = screen.get_personState(img)
            elif sel == '2':
                person1State, person2State, person3State = screen.get_ravenclaw_personState(img)
            contentPerson1 = ocr.ocr_content(person1State)
            contentPerson2 = ocr.ocr_content(person2State)
            contentPerson3 = ocr.ocr_content(person3State)
            state1 = filterPersonState(contentPerson1)
            state2 = filterPersonState(contentPerson2)
            state3 = filterPersonState(contentPerson3)
            if state1 == 'A' or state2 == 'A' or state3 == 'A':
                print('这题抄A')
                x,y = coordinate[0][0], coordinate[0][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            elif state1 == 'B' or state2 == 'B' or state3 == 'B':
                print('这题抄B')
                x,y = coordinate[1][0], coordinate[1][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            elif state1 == 'C' or state2 == 'C' or state3 == 'C':
                print('这题抄C')
                x,y = coordinate[2][0], coordinate[2][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            elif state1 == 'D' or state2 == 'D' or state3 == 'D':
                print('这题抄D')
                x,y = coordinate[3][0], coordinate[3][1]
                left_click(win_rect[0]+x,win_rect[1]+y,2)
                is_answered = 1
            else:
                pass
                # print('答案都没得抄！')
            # 错题就先不计了
            time.sleep(0.9)
            continue
        elif (is_answered == 0 and countdown_num == 0):
            print('这题盲猜C')
            x,y = coordinate[2][0], coordinate[2][1]
            left_click(win_rect[0]+x,win_rect[1]+y,2)
            is_answered = 2 # 表示没得抄，盲猜
        if is_answered == 2 and countdown_num == 0:
            in_rect, img = screen.get_screenshot()
            import datetime
            fileName = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.png'
            
            # from PIL import Image
            # im = Image.fromarray(img)
            # im.save('img/harry_'+fileName)
            cv2.imwrite('img/harry_'+fileName, img)
            time.sleep(2)
"""