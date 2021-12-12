# UniversalAutomaticAnswer
windows下通用自动答题（学习向，本教程需要一定基础，当然会百度也是可以的，不适合伸手党）
## 0 说明
- 本仓库的核心代码都封装成接口了，可直接调用。对应接口文件下有使用示例
- 运行示例程序(run.py)前,需要几点准备
    - 安装夜神模拟器（分辨率设置为1600*900，夜神打钱）
    - 模拟器里安装哈利波特-魔法觉醒程序
    - 运行游戏至进入魔法史答题（开始匹配界面即可）
    - cd 到根目录/your_root_path/
    - 运行 python run.py 然后根据提示输入，然后alt+tab切换到模拟器界面（保证模拟器在最前端） 
## 1 项目结构与效果展示
### 1.1 项目目录及说明
```
UniversalAutomaticAnswer  # 根目录
|   README.md
|   run.py
|   __init__.py
|
+---conf  # 配置文件
|   |   conf.yml
|   |   confImp.py
|   \---__init__.py
|
+---csvImp  # 存放题库
|       csvImp.py
|       harrypotter_questions.csv
|       __init__.py
|
+---data  # 数据处理模块
|       dataImp.py
|       __init__.py
|
+---httpImp  # 网络模块(搜索引擎)
|       search.py
|       __init__.py
|
+---img  # 存放图片文件
|       harrypotter_question.jpg
|       harrypotter_question_xueyuan.jpg
|       哈利答题375分.jpg
|
+---log  # 存放log文件
|
+---match  # 匹配模块
|   |   matchImp.py
|   \---__init__.py
|
+---ocr  # ocr模块
|   |   ocrImp.py
|   \---__init__.py
|
+---screen  # screen模块
|   |   ocrImp.py
|   \---__init__.py
|
+---script  # 常用脚本
|   |   getWindowsHwnd.py  # 遍历输出windows窗口句柄
|   \---mergecsv.py
|
\---util  # 常用工具
    |   filter.py
    |   mouse.py
    \---__init__.py
```
### 1.2 效果展示
![满分图](img/哈利答题375分.jpg)
## 2 环境安装
### 2.0 基础模块版本
- python: 3.8
- 其他模块及版本见requirement.txt
### 2.1 依赖包包安装
```
pip install -r requirement.txt
```
### 2.2 出现的问题及解决方案
- pywin32的win32gui报错
    ```
    # 由于我使用python3.6，使用过pip安装了pywin32，应该存在了缓存
    # 在python3.8安装的时候也直接使用了缓存，但是DLL是和版本有关的，需要对应版本的make
    # 所以清除pip的缓存，或者跳过缓存安装或者换conda装都是可以的
    pip uninstall pywin32 # 清除缓存（不懂就百度）
    pip install pywin32 --no-cache-dir # 如果实在太懒了，建议使用conda安装（前提是你一直用的conda）
    # conda install pywin32 懒得清缓存可以使用conda安装
    ```
## 3 UAA的使用
- 第0节说明里已经介绍了基本使用方法
- 进阶使用（自己的答题程序）
    - python script/getWindowsHwnd.py # 查看windows窗口句柄，找到自己需要使用的窗口名
    - 替换conf/conf.yml的windowsScreen下的screen_hwnd就可以捕捉对应窗口的截图了
    - 替换conf/conf.yml的path下的data_path，使用自己的题库
    - 替换conf/conf.yml的imgRect下的RectQ/RectA/RectB/RectC/RectD，分别对应问题和四个选项的左上和右下坐标
    - run.py中的coordinate变量修改为你自己对应需要点击ABCD选项的坐标
    - 或者模仿示例中的run.py另写一个run.py，这个工作量稍微大一点，但是不难，主要是判断流程要符合你自己的需求，毕竟接口都封装好了。
### 3.0 几个简单的测试
几个接口都是可以单独运行的
```
python script/getWindowsHwnd.py # 获取所有windows下正在运行的窗口句柄
python screen/screenImp.py # 截取屏幕，并裁剪出需要识别的模块
python ocr/ocrImp.py # 图片转文字，并果过滤提取文本
python util/filter.py # 文本过滤
python match/matchImp.py # 利用题库匹配结果
python httpImp/search.py # 利用搜索引擎搜索结果
```
### 3.1 配置文件
### 3.2 run
环境配置好了，直接run即可
```
git clone git@github.com:biechuyangwang/UniversalAutomaticAnswer.git
cd UniversalAutomaticAnswer
python run.py
```
## 4 注意事项
## 5 问题讨论与版权
- 关于社团答题
大同小异，有能力的同学可以自己定制run.py（提示，去掉抄答案部分，得到题目先盲选一个有助于提高成绩）
- 关于移动端
有一个自用的基于autojs的答题，暂不公开（因为没有使用本地的ocr，使用的百度的在线ocr）
- 关于更详细的教程
本来这个项目，我预计周六周日两天就做完了。确实，花了两个下午就搞定了，但是代码是面向过程的，自己看都看不懂，自用当然没有问题，但是想要扩展的难度就太大了，所以又花了一个下午重构了一下。然后写文档花了3个下午，所以说，写文档写教程这种事太花时间了，我后面还有很多事要做，感兴趣的可以自己研究一下，毕竟不是很难。等有空了回头在弄个详细点的全流程教程以及如何演示如何扩展。
- 关于接下来的工作
    - 服务器上开放几个知识图谱用于问答系统
    - 语音模仿：用你的一段录音（最好是1分钟到2分钟），然后输入你要生成语音的文本，得到一段模仿你声音、语气的语音文件。
    - LSP：在线演讲，用于驱动虚拟形象（可用于视频时使用虚拟形象演讲，面部捕捉对口型啥的，配合上一个图灵机器人和语音模仿，可以弄一个人工智障来做女朋友了）
    - 超分辨（当然不是去马赛克，别想多）
    - 实时的目标检测（拿和平精英或者pubg开刀吧）
    - 目标跟踪（这个是我的老本行，等我想做这个的时候在来搞个无人机自动跟踪，PS：我不是跟踪狂）
### 5.1 讨论群
暂时没有，请issue或者邮箱1101049446@qq.com
### 5.2 引用与非商业化
@misc{UAA2021,
title={UAA, Universal Automatic Answer.},
author={biechuyangwang},
howpublished = {\url{https://github.com/biechuyangwang/UniversalAutomaticAnswer}},
year={2021}
}

UAA is provided under the Apache-2.0 license.
