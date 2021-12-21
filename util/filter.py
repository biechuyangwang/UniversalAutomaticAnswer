#!/usr/bin/env python
# -*- coding: utf-8 -*-

def filterQuestion(question_content):
    r1 = "[\sa-zA-Z．·“”』。！（）\'\"《》\-:\.：\*\.\+\$\^\[\]\(\)\{\}\|]+"
    r2 = "[\s．·“”。！（）』\'\"《》\-:：\*\+\$\^\[\]\(\)\{\}\|]+"
    import re
    # content_list_sub = [re.sub(r1, '', content) for content in question_content]
    content_list_sub = [re.sub(r2, '', content) for content in question_content if len(re.sub(r1, '', content))>0] # 只过滤纯英文行
    question = list(filter(lambda s:len(s) >= 7,content_list_sub)) # 过滤人名
    return question

def filterLine(line_content):
    r1 = "[\s．“”（）\'\"《》\-:\.：·\*\+\$\^\[\]\(\)\{\}\|]+"
    import re
    line = [re.sub(r1, '', content) for content in line_content]
    return line

def filterEngLine(line_content):
    r1 = "[\sa-zA-Z．“”（）\'\"《》\-:\.：·\*\.\+\$\^\[\]\(\)\{\}\|]+"
    import re
    line = [re.sub(r1, '', content) for content in line_content]
    return line

def filterPersonState(state_content):
    import re
    if len(state_content) == 2 and bool(re.search(r'\d', state_content[0])):
        return state_content[1]
    else: 
        return None

if __name__ == '__main__':
    question_content = ['封香菜', 'a.b.c.谁的挂坠成了伏地魔的魂器？', 'WhoselocketbecameaHorcruxforVoldemorta']
    optiona_content = ['贝拉特里克斯·a.b.c.莱斯特兰奇']
    optionb_content = ['雷古勒斯·布莱克']
    optionc_content = ['萨拉查·斯莱特林']
    optiond_content = ['赫尔加·赫奇帕奇']
    state_content1 = ['(+20', 'A']
    state_content2 = ['A']

    question = filterQuestion(question_content)
    optiona = filterLine(optiona_content)
    optionb = filterLine(optionb_content)
    optionc = filterLine(optionc_content)
    optiond = filterLine(optiond_content)
    state1 = filterPersonState(state_content1)
    state2 = filterPersonState(state_content2)

    print(question)
    print(optiona)
    print(optionb)
    print(optionc)
    print(optiond)
    print(state1)
    print(state2)