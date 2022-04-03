#!/usr/bin/env python
# -*- coding: utf-8 -*-
from paddleocr import PaddleOCR
import time

class OCRImp():
    def __init__(self, conf_data):
        self.init_model(conf_data)

    def init_model(self, conf_data):
        self.conf_data = conf_data
        self.ppocr = PaddleOCR(use_angle_cls=True, lang="ch") # mode load

    def ocr(self, img, det=True, cls=False): # det = True return [['坐标点集', 内容集]]; det = False return [内容集]
        result = self.ppocr.ocr(img, det=det, cls=cls)
        if det == False:
            result = [['',result[0]]]
        return result
    
    def ocr_content(self, ocr_result):
        # content = [x[0] for x in ocr_result[1]]
        content = [x[1][0] for x in ocr_result]
        return content
        
        
if __name__ == '__main__':

    import sys
    sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
    from UniversalAutomaticAnswer.screen.screenImp import ScreenImp # 加入自定义包
    from UniversalAutomaticAnswer.conf.confImp import get_yaml_file
    import cv2

    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)

    start = time.time()*1000
    ppocr = OCRImp(conf_data) # 约定只能由一个OCR实例（有时间变成单例模式）
    print("初始化ocr模型耗时：", time.time()*1000 - start)

    start = time.time()*1000
    screen = ScreenImp(conf_data)
    win_rect, img_bgr= screen.get_screenshot() # 获取屏幕截图
    print("获取截图耗时：", time.time()*1000 - start)

    import time
    start = time.time()*1000

    img = cv2.imread(screen.ravenclaw_imgpath)

    img_path = './img/harry_2022_01_01_12_22_37.png'
    img = cv2.imread(img_path)

    # print(win_rect)
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_questionAndoptionsBtn(img)
    person1State, person2State, person3State = screen.get_ravenclaw_personState(img)
    # result = ocr.ocr(img_bgr)
    # print(result)
    resultq = ppocr.ocr(QBtn)
    resulta = ppocr.ocr(ABtn)
    resultb = ppocr.ocr(BBtn)
    resultc = ppocr.ocr(CBtn)
    resultd = ppocr.ocr(DBtn)
    resultp1 = ppocr.ocr(person1State)
    resultp2 = ppocr.ocr(person2State)
    resultp3 = ppocr.ocr(person3State)
    print(resultp3)

    contentq = ppocr.ocr_content(resultq)
    contenta = ppocr.ocr_content(resulta)
    contentb = ppocr.ocr_content(resultb)
    contentc = ppocr.ocr_content(resultc)
    contentd = ppocr.ocr_content(resultd)
    contentp1 = ppocr.ocr_content(resultp1)
    contentp2 = ppocr.ocr_content(resultp2)
    contentp3 = ppocr.ocr_content(resultp3)

    print(contentq)
    print(contenta)
    print(contentb)
    print(contentc)
    print(contentd)
    print(contentp1)
    print(contentp2)
    print(contentp3)
    print('识别题目和选项总耗时：', time.time()*1000-start)