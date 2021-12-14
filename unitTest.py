# 处理哈利题库
import csv
with open('csvImp/哈利波特题库_12_15.csv','r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile,delimiter=' ')
    reader = list(reader)
    for idx, row in enumerate(reader):
        if len(row) != len(reader[0]):
            print(row)
	# raw_data = list(map(lambda row: (row[1], row[2]), reader))

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