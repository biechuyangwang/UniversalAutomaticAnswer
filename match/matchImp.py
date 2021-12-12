#!/usr/bin/env python
# -*- coding: utf-8 -*-

# fuzz match
import time
import csv
from thefuzz import process, fuzz
import pandas as pd

import sys
sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
from UniversalAutomaticAnswer.conf.confImp import get_yaml_file # 加入自定义包

class DataMatcher(object): # 拼音匹配算法对的解决方案
	"""
	题目数据的初始化, 提供模糊查询功能.
	"""
	# DATA_FILE = './harrypotter_questions.csv'
	def __init__(self, conf_data):
		self.init_data(conf_data)
		# self.init_data(self.DATA_FILE)

	def init_data(self, conf_data): # 先加载题库
		self.conf_data = conf_data
		self.data_path = self.conf_data['path']['data_path']
		with open(self.data_path, 'r', encoding='utf-8-sig') as csvfile:
			reader = csv.reader(csvfile,delimiter=' ')
			self.raw_data = list(map(lambda row: (row[1], row[2]), reader))

	def get_close_match(self, words):
		dataset = {x: idx for idx, x in enumerate(self.raw_data)}
		results = process.extractBests(words, dataset.keys(), scorer=fuzz.token_set_ratio)
		results.extend(process.extractBests(words, dataset.keys(), scorer=fuzz.token_sort_ratio))
		scored = {}
		for result in results:
			scored[result[0]] = max(result[1], scored.get(result[0], 0))
			if scored[result[0]] == 0:
				scored.pop(result[0])
		# print(scored)
		results = sorted([(self.raw_data[dataset[sent]], score, dataset[sent]) for sent, score in scored.items()], key=lambda x: x[1], reverse=True)
		return results # [([question, answer], score, idx)]

def match_options(answer, options): # answer, options
    dataset = {x: idx for idx, x in enumerate(options)}
    results = process.extractBests(answer, dataset.keys(), scorer=fuzz.token_set_ratio)
    results.extend(process.extractBests(answer, dataset.keys(), scorer=fuzz.token_sort_ratio))
    scored = {}
    for result in results:
        scored[result[0]] = max(result[1], scored.get(result[0], 0))
        # if scored[result[0]] < 50:
        #     scored.pop(result[0])
    # print(scored)
    results = sorted([(options[dataset[sent]], score, dataset[sent]) for sent, score in scored.items()], key=lambda x: x[1], reverse=True)
    return results # [(sent, score, idx)]


if __name__ == '__main__':
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)
    data_matcher = DataMatcher(conf_data)
    info = '伸缩眼酸味爆爆糖'
    options = ['伸缩眼', '糖', '发烧糖', '拼写检查羽毛笔']

    answer_list = list(data_matcher.get_close_match(info))
    answer = answer_list[0][0][1]
    res = match_options(answer, options)
    print(res)
    