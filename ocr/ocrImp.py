#!/usr/bin/env python
# -*- coding: utf-8 -*-
from paddleocr import PaddleOCR
import time

class OCRImp():
    def __init__(self, conf_data):
        self.init_model(conf_data)

    def init_model(self, conf_data):
        self.conf_data = conf_data
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch") # mode load

    def ocr(self, img):
        return self.ocr.ocr(img, det=True, cls=False)
    
    def ocr_content(self, ocr_result):
        content = [x[0] for x in ocr_result[1]]
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
    ocr = OCRImp(conf_data) # 约定只能由一个OCR实例（有时间变成单例模式）
    print("初始化ocr模型耗时：", time.time()*1000 - start)

    start = time.time()*1000
    screen = ScreenImp(conf_data)
    win_rect, img_bgr= screen.get_screenshot() # 获取屏幕截图
    print("获取截图耗时：", time.time()*1000 - start)

    import time
    start = time.time()*1000

    img = cv2.imread(screen.imgpath)
    # print(win_rect)
    QBtn, ABtn, BBtn, CBtn, DBtn = screen.get_questionAndoptionsBtn(img)
    # result = ocr.ocr(img_bgr)
    # print(result)
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
    print(contenta)
    print(contentb)
    print(contentc)
    print(contentd)
    print('识别题目和选项总耗时：', time.time()*1000-start)