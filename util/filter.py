#!/usr/bin/env python
# -*- coding: utf-8 -*-

def filterQuestion(question_content):
    r0 = "[0-9]+"
    r1 = "[\sa-zA-Z0-9．·“”』。,，！？!\?（）\'\"《》/\-:\.：\*\.\+\$\^\[\]\(\)\{\}\|]+"
    r2 = "[\s．·“”（）#。,！？!\?（）』\'\"《》/\-:\.：\*\.\+\$\^\[\]\(\)\{\}\|]+"
    import re
    # content_list_sub = [re.sub(r1, '', content) for content in question_content]
    content_list_sub = [re.sub(r2, '', content) for content in question_content if (len(re.sub(r1, '', content))>0 or len(re.sub(r0, '', content))==0)] # 只过滤纯英文行
    # question = list(filter(lambda s:len(s) >= 6,content_list_sub)) # 过滤人名 有人名也不怕了
    if len(content_list_sub) >= 2: # 过滤后拼接，修复因断句导致的错误
        return [''.join(x for x in content_list_sub)]
    return content_list_sub

def maguafilterQuestion(question_content):
    r1 = "[\sa-zA-Z0-9．·“”』。,，！？!\?（）\'\"《》/\-:\.：\*\.\+\$\^\[\]\(\)\{\}\|]+"
    r2 = "[\s．·“”。,！？!\?（）』\'\"《》/\-:\.：\*\.\+\$\^\[\]\(\)\{\}\|]+"
    import re
    # content_list_sub = [re.sub(r1, '', content) for content in question_content]
    content_list_sub = [re.sub(r2, '', content) for content in question_content if len(re.sub(r1, '', content))>0] # 只过滤纯英文行
    # question = list(filter(lambda s:len(s) >= 6,content_list_sub)) # 过滤人名 有人名也不怕了
    if len(content_list_sub) >= 2: # 过滤后拼接，修复因断句导致的错误
        return [''.join(x for x in content_list_sub)]
    return content_list_sub

def filterLine(line_content):
    r1 = "[\s．“”（）#\'\"《》，。,!\?（）』/\-:：·\*\+\$\^\[\]\(\)\{\}\|]+"
    import re
    line = [re.sub(r1, '', content) for content in line_content]
    # line = list(dict.fromkeys(line)) # 去重，避免纯数字重复连接
    if len(line) >= 2: # 过滤后拼接，修复因断句导致的错误
        return [''.join(x for x in line)]
    return line

def filtertimeLine(line_content):
    r1 = "[\s．“”（）\'\"《》，。,/\-:\.：·\*\+\$\^\[\]\(\)\{\}\|]+"
    import re
    line = [re.sub(r1, '', content) for content in line_content]
    if len(line) >= 2: # 过滤后拼接，修复因断句导致的错误
        return [''.join(x for x in line)]
    return line

def filterEngLine(line_content):
    r1 = "[\sa-zA-Z．“”（）\'\"《》，。,/\-:\.：·\*\.\+\$\^\[\]\(\)\{\}\|]+"
    import re
    line = [re.sub(r1, '', content) for content in line_content]
    return line

def filterPersonState(state_content):
    import re
    if len(state_content) == 3 and bool(re.search(r'\d', state_content[1])):
        return state_content[2]
    elif len(state_content) == 2 and bool(re.search(r'\d', state_content[0])):
        return state_content[1]
    else: 
        return None

if __name__ == '__main__':
    """
    ([array([[ 24.,  22.],
       [123.,  22.],
       [123.,  47.],
       [ 24.,  47.]], dtype=float32), array([[52., 60.],
       [73., 60.],
       [73., 92.],
       [52., 92.]], dtype=float32)], [('+25×2', 0.8948676), ('B', 0.95725745)])
    """
    question_content = ['封香菜', 'a.b.c.谁的挂坠成了伏地魔的魂器？', 'WhoselocketbecameaHorcruxforVoldemorta123','测试追加内容']
    optiona_content = ['贝拉特里克斯·a.b.c.莱斯特兰奇']
    optionb_content = ['雷古勒斯·布莱克']
    optionc_content = ['萨拉查·斯莱特林']
    optiond_content = ['赫尔加·赫奇帕奇']
    state_content1 = ['(+20', 'A']
    state_content2 = ['连续合周文1', 'V+20', 'B']

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