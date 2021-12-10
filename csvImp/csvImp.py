#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file # 加入自定义包

class Csv(object):
    def __init__(self, conf_data):
        self.init_data(conf_data)

    def init_data(self,conf_data):
        self.conf_data = conf_data
        self.data_path = self.conf_data['path']['data_path']
    
    def read_csv(self,data_path):
        with open(data_path, 'r', encoding='utf-8-sig') as csvfile:
            import csv
            reader = csv.reader(csvfile,delimiter=' ')
            raw_data = list(map(lambda row: (row[1], row[2]), reader)) # ('序号', '题目', '答案')
            csvfile.close()
            return raw_data
        return None

if __name__ == '__main__':
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    csvfile = Csv(conf_data)
    raw_data = csvfile.read_csv(csvfile.data_path)
    words = {x[0]: idx for idx, x in enumerate(raw_data[1:])}

    new_words = {}
    for i,(k,v) in enumerate(words.items()): # 查看部分字典数据
        new_words[k]=v
        if i==4:
            print(new_words)
            break