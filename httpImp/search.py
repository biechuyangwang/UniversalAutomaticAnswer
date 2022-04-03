# 测试百度
import requests
class searchImp():
    def __init__(self, conf_data):
        self.init_data(conf_data)

    def init_data(self, conf_data): # 参数初始化
        self.conf_data = conf_data
        self.baidu_rn = self.conf_data['search']['baidu']['rn']
        self.baidu_lm = self.conf_data['search']['baidu']['lm']
        self.baidu_ct = self.conf_data['search']['baidu']['ct']

        self.google_lr = self.conf_data['search']['google']['lr']
        self.google_cr = self.conf_data['search']['google']['cr']
        self.google_as_qdr = self.conf_data['search']['google']['as_qdr']
        self.google_as_occt = self.conf_data['search']['google']['as_occt']

    def baidu(self, question, options): # 百度搜索
        url = 'https://www.baidu.com/s?'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        ret = options.copy()
        # https://www.baidu.com/s?q1=question&rn=10&lm=0&ct=0&tn=baiduadv
        # q1->question rn->每页显示的条数(10,20,50) lm->最近时间内搜索(0,1,7,30,360) ct->搜索语言(0:全部,1:简体,2:繁体) tn->搜索类型('baiduadv':百度高级搜索)
        data = {
            'q1': question,
            'rn': self.baidu_rn,
            'lm': self.baidu_lm,
            'ct': self.baidu_ct,
            'tn': 'baiduadv'
        }
        res = requests.get(url, params=data, headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        for i in range(len(options)):
            ret[i] = (html.count(options[i]), options[i], i)
        ret.sort(reverse=True)
        return ret

    def google(self, question, options): # google搜索
        url = 'https://www.google.com/search?'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        # https://www.baidu.com/s?q1=question&rn=10&lm=0&ct=0&tn=baiduadv
        # q1->question rn->每页显示的条数(10,20,50) lm->最近时间内搜索(0,1,7,30,360) ct->搜索语言(0:全部,1:简体,2:繁体) tn->搜索类型('baiduadv':百度高级搜索)
        data = {
            'as_q': question,
            'lr': self.google_lr,
            'cr': self.google_cr,
            'as_qdr': self.google_as_qdr,
            'safe': 'images',
            'as_occt': self.google_as_occt
        }
        ret = options.copy()
        res = requests.get(url, params=data, headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        for i in range(len(options)):
            ret[i] = (html.count(options[i]), options[i], i)
        ret.sort(reverse=True)
        return ret
    
    def bing(self, question, options): # 百度搜索
        url = 'https://cn.bing.com/search?'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        ret = options.copy()
        # https://www.baidu.com/s?q1=question&rn=10&lm=0&ct=0&tn=baiduadv
        # q1->question rn->每页显示的条数(10,20,50) lm->最近时间内搜索(0,1,7,30,360) ct->搜索语言(0:全部,1:简体,2:繁体) tn->搜索类型('baiduadv':百度高级搜索)
        data = {
            'q': question
        }
        res = requests.get(url, params=data, headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        for i in range(len(options)):
            ret[i] = (html.count(options[i]), options[i], i)
        ret.sort(reverse=True)
        return ret

    def sougou(self, question, options): # 百度搜索
        url = 'https://www.sogou.com/web?'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        ret = options.copy()
        # https://www.baidu.com/s?q1=question&rn=10&lm=0&ct=0&tn=baiduadv
        # q1->question rn->每页显示的条数(10,20,50) lm->最近时间内搜索(0,1,7,30,360) ct->搜索语言(0:全部,1:简体,2:繁体) tn->搜索类型('baiduadv':百度高级搜索)
        data = {
            'query': question
        }
        res = requests.get(url, params=data, headers=headers)
        res.encoding = 'utf-8'
        html = res.text
        for i in range(len(options)):
            ret[i] = (html.count(options[i]), options[i], i)
        ret.sort(reverse=True)
        return ret
if __name__ == '__main__':
    question = '参加斯拉格霍恩教授晚宴的成员们加入了什么团体？'
    options = ['斯拉格霍恩组合', '鼻涕虫俱乐部', '斯拉格霍恩协会', '霍拉斯谁是谁']

    import sys
    sys.path.append(r"C:\\Users\\SAT") # 添加自定义包的路径
    from UniversalAutomaticAnswer.conf.confImp import get_yaml_file # 加入自定义包
    conf_path = 'conf/conf.yml'
    conf_data = get_yaml_file(conf_path)

    searchimp = searchImp(conf_data)
    ans = searchimp.bing(question, options)
    print('bing答案：',ans)

    # ans_google = searchimp.google(question, options) # 暂时访问不了，留给国外的朋友使用
    # print('谷歌答案：',ans_google)