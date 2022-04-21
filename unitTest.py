import cv2
import sys
import win32gui
from paddleocr import draw_ocr
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
from UniversalAutomaticAnswer.ocr.ocrImp import OCRImp
from UniversalAutomaticAnswer.util.filter import filterQuestion, filterLine, filterPersonState, maguafilterQuestion
from UniversalAutomaticAnswer.httpImp.search import searchImp

# 获取配置文件
conf_path = 'conf/conf.yml'
conf_data = get_yaml_file(conf_path)
ocr = OCRImp(conf_data) # 约定只能由一个OCR实例（有时间变成单例模式）
screen = ScreenImp(conf_path)
import win32api
import win32con

def ret_question_options(img):
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
    # print(contentq)

    question, optiona,optionb,optionc,optiond = '', '', '', '' ,''
    if len(filterQuestion(contentq))>0:
        question = maguafilterQuestion(contentq)[0]
    # print(question)
    if len(question)==0:
        print('题目未识别！')
        print('源数据为：',resultq)
        return res

    if len(filterLine(contenta))>0:
        optiona = filterLine(contenta)[0]
    if len(filterLine(contentb))>0:
        optionb = filterLine(contentb)[0]
    if len(filterLine(contentc))>0:
        optionc = filterLine(contentc)[0]
    if len(filterLine(contentd))>0:
        optiond = filterLine(contentd)[0]
    options = [optiona, optionb, optionc, optiond]
    # print('ocr结果:', [question,options])
    return question,options

def left_click(x,y,times=4):
    win32api.SetCursorPos((x,y))
    import time
    while times:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

img_path = './img/harry_2022_03_26_10_00_44.png'

img = cv2.imread(img_path)
import matplotlib.pyplot as plt
img = img[:,:,::-1]
img_test = img[40:100,770:840] # [770,40,840,100]

import time
start_t = time.time()*1000
det = False
result = ocr.ocr(img_test,cls=True,det=det) # 只识别14.34ms 带检测24.70ms 带角度分类36.48
# 只识别的返回值 [('4', 0.94007367)]
# 带检测的返回值 [ [[[20.0, 17.0], [48.0, 17.0], [48.0, 47.0], [20.0, 47.0]], ('4', 0.9891465)] ] 即[ ['坐标点集',()] ]
# 带角度不影响返回值
print(time.time()*1000-start_t)
print(result)

plt.imshow(img)
plt.show()


# from paddleocr import PaddleOCR,draw_ocr
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
# ocr = PaddleOCR(use_angle_cls=True, lang='ch') # need to run only once to download and load model into memory
# img_path = './imgs_en/img_12.jpg'
# import time
# start_time = time.time()*1000
# result = ocr.ocr(img_path, cls=True)
# print(time.time()*1000-start_time) # cls=False 1476ms cls=True 1616.45ms
# print(result)
# for line in result:
#     print(line)
# imshow = img_test
# from PIL import Image
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# if det != False:
#     im_show = draw_ocr(imshow, boxes, txts, scores, font_path='./fonts/simfang.ttf')
#     im_show = Image.fromarray(im_show)
#     im_show.show()
# """