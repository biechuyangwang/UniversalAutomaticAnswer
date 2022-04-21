import time

import requests
from selectolax.parser import HTMLParser
from lxml import etree

from io import BytesIO

def make_print_to_file(path='./'): # 标准输出重定向
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

    fileName = datetime.datetime.now().strftime('update_'+'%Y_%m_%d')
    sys.stdout = Logger(fileName + '.md', path=path)


if __name__ == '__main__':

    import datetime
    mon = datetime.datetime.now().month
    day = datetime.datetime.now().day
    t = '{}.{}'.format(mon,day) # 想要查询的时间，例如4.7
    # t = '4.7'

    # 构造cookie和headers
    # cookies = "UM_distinctid=180019cce3772d-03084c56c5ceb-978183a-1fa400-180019cce38cc0; guestJs=1649297100; CNZZDATA30043604=cnzz_eid%3D852467339-1649286274-https%253A%252F%252Fcn.bing.com%252F%26ntime%3D1649296949; lastvisit=1649297117; lastpath=/read.php?tid=27915340; bbsmisccookies=%7B%22pv_count_for_insad%22%3A%7B0%3A-44%2C1%3A1649350874%7D%2C%22insad_views%22%3A%7B0%3A1%2C1%3A1649350874%7D%2C%22uisetting%22%3A%7B0%3A%22b%22%2C1%3A1649297416%7D%7D; _cnzz_CV30043604=forum%7Cfid812%7C0; ngaPassportOid=9a7fa3afbbcae1d8fac6eb43390676c2; ngacn0comUserInfo=%25D0%25C7%25C6%25DA%25C1%25F9%25B5%25C4%25B9%25CA%25CA%25C2%09%25E6%2598%259F%25E6%259C%259F%25E5%2585%25AD%25E7%259A%2584%25E6%2595%2585%25E4%25BA%258B%0939%0939%09%0910%090%094%090%090%09; ngacn0comUserInfoCheck=f9ae8aa0fd86a76c6cc0ef92f1ad72e8; ngacn0comInfoCheckTime=1649297394; ngaPassportUid=64090796; ngaPassportUrlencodedUname=%25D0%25C7%25C6%25DA%25C1%25F9%25B5%25C4%25B9%25CA%25CA%25C2; ngaPassportCid=X9a8t9r9gqhdb3qhj9n6t0k4muko0bduc6d6r49g"
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }
    # jar = requests.cookies.RequestsCookieJar()
    # for cookie in cookies.split(";"):
    #     key, value = cookie.split("=", 1)
    #     jar.set(key, value)
    
    make_print_to_file(path='./log/') # 重定型print

    # login_url = "https://ngabbs.com/nuke/account_copy.html?login"
    # https://ngabbs.com/nuke.php?__lib=login&__act=account&login

    tid = 27915340 # 哈利波特更新资讯页面id
    url = 'https://ngabbs.com/read.php?tid={}'.format(tid) # &rand=22 &rand=22 Math.floor(Math.random()*1000)
    # html = requests.get(url, cookies=jar, headers=headers)
    html = requests.get(url, headers=headers)
    cookies = html.cookies

    html.encoding = 'gbk'
    content = html.text
    # print(content)
    print(html.status_code)
    if html.status_code=='403' or html.status_code==403 :
        time.sleep(10)
        url = 'https://ngabbs.com/read.php?tid={}'.format(tid)
        html = requests.get(url, cookies=cookies, headers=headers)
        cookies = html.cookies
        html.encoding = 'gbk'
        content = html.text
        print(content)
        print(html.status_code)
    tree = etree.HTML(content)
    text_list = tree.xpath('//p/text()')
    res = None
    import datetime
    mon = datetime.datetime.now().month
    day = datetime.datetime.now().day
    if t == '':
        t = '{}.{}'.format(mon,day)
    # print(t)
    for val in text_list:
        if '{} 正式服维护详情'.format(t) in val:
            res = val # [url=/read.php?tid=31373727]4.7 正式服维护详情[/url]
            break
    print(res)
    res = res.split(']')[0].split('/')[1]
    root_path = 'https://ngabbs.com/'
    url = root_path + res
    print(url) # 返回今天更新的链接

    html = requests.get(url, cookies=cookies, headers=headers)
    html.encoding = 'gbk'
    content = html.text
    tree = etree.HTML(content)
    text_list = tree.xpath('//p/text()')
    for val in text_list:
        print(val)