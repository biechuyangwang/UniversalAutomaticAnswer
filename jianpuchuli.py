# 使用方法
# 函数jianpujiakg，适用于自己写的数字谱格式不好看转为好看且能用
#   输入范例：
    # jianpu = "262 272, 116 272 114 134, 232 232, 266 252 264 114,\n\
    #         234, 246 232 244 114,112 112 112, 276 242 244 274,\n\
    #         262 272, 116 272 114 134, 232 232, 266 252 264 114,\n\
    #         234, 246 112 274 114, 122 124 132 118, 112 272 264 274 254,\n\
    #         112 122, 136 122 134 154,252 252, 116 272 114 134,\n\
    #         262 272 114 272 112 124, 116 252 258, 144 134 124 114,\n\
    #         134, 168 158, 132 122 118 114, 126 112 124 154,\n\
    #         134, 166 162 156 152, 132 122 118 114, 126 112 124 274,\n\
    # "
# 函数zimupu2shuzipu，适用于将字母谱转化为数字简谱
#   输入范例：
    # zimupu = "[e/C/]E/ e/E/ f/E/ g/E/ |[G/g/]B/ f/B/ e/B/ d/B/ |\
    #         [c/A/]E/ c/E/ d/E/ e/E/ |[e/G/]B/ G/d/ [d/D/]B/ G/D/ |[e/C/]E/ e/E/ f/E/ g/E/ |\
    #         [G/g/]B/ f/B/ e/B/ d/B/ |[c/A/]E/ c/E/ d/E/ e/E/ |[d/B/G/]D/ G/c/ [c/C/]E/ G/E/ |\
    #         [d/B/G/]D/ d/D/ [e/c/A/]E/ c/E/ |[d/B/G/]D/ e/f/ [e/c/A/]E/ c/E/ |\
    #         [d/B/G/]D/ e/f/ [e/c/A/]E/ d/E/ |[c/D/]F/ d/F/ [G/D/]F/ E/D/ |[e/C/]E/ e/E/ f/E/ g/E/ |\
    #         [G/g/]B/ f/B/ e/B/ d/B/ |[c/A/]E/ c/E/ d/E/ e/E/ |[d/B/G/]D/ G/c/ [c2G2E2C/]||"

# 简谱加逗号和空格
def jianpujiakg(jianpu=None):
    result = ""
    idx=0
    for i,v in enumerate(jianpu):
        if v=='\n':
            result += '\n'
            idx = 0-i-1
        elif v==' ' or v==',':
            idx -= 1
        elif (i+idx)%3==2:
            result += v+', '
        else:
            result += v+','
    return result

# jianpu = "1234567"
# result = jianpujiakg(jianpu)
# print(result)

# C谱转数字谱 C=21(第二排第一个音)
def zimu2shuzi(v):
    result = ""
    if v.isalpha():
        if v.islower():
            if ord(v)-ord('b')>0:
                result += '1'
                result += chr(ord('0')+ord(v)-ord('b'))
                # print(result)
                return result
            else:
                result += '1'
                result += chr(ord('0')+ord(v)-ord('b')+7)
                # print(result)
                return result
        else:
            if ord(v)-ord('B')>0:
                result += '2'
                result += chr(ord('0')+ord(v)-ord('B'))
                # print(result)
                return result
            else:
                result += '2'
                result += chr(ord('0')+ord(v)-ord('B')+7)
                # print(result)
                return result
    return result

# 字母谱转数字谱(/等于半拍 纯字母等于一拍 数字x等于x拍 数字x/y等于y分之x拍) a6+b7+c1+d2+e3+f4+g5+ A6B7C1D2E3F4G5 +代表高8度-代表低8度
def zimupu2shuzipu(zimupu=None):
    result = ""
    jiepai = 4
    for i,v in enumerate(zimupu):
        if v=='|':
            result += '\n'
        elif v=='[':
            jiepai = 0
        elif v==']':
            jiepai = 4
        elif jiepai == 0  and v.isalpha() and \
                (zimupu[i+1]==']' \
                or (zimupu[i+1].isdigit() and zimupu[i+2]==']') \
                or (zimupu[i+1]=='/' and zimupu[i+2]==']') \
                or (zimupu[i+1].isdigit() and zimupu[i+2]=='/' and zimupu[i+1].isdigit() and zimupu[i+4]==']')):
            result += zimu2shuzi(v)
            if zimupu[i+1]==']':
                result += '4'
            elif zimupu[i+1].isdigit() and zimupu[i+2]==']':
                result += chr(ord('0')+2*4%10)
            elif zimupu[i+1]=='/' and zimupu[i+2]==']':
                result += chr(ord('0')+2)
            elif zimupu[i+1].isdigit() and zimupu[i+2]=='/' and zimupu[i+3].isdigit() and zimupu[i+4]==']':
                result += chr(ord('0')+4*int(zimupu[i+1])/int(zimupu[i+3]))
            else :
                result += '4'
        elif jiepai == 0 and v.isalpha():
            result += zimu2shuzi(v)
            result += '0'
            print(result)
        elif jiepai != 0 and v.isalpha():
            result += zimu2shuzi(v)
            # if zimupu[i+1] == '|':
            #     result += '4'
            if zimupu[i+1].isdigit():
                result += chr(ord('0')+int(zimupu[i+1])*4%10)
            elif zimupu[i+1]=='/':
                result += chr(ord('0')+2)
            elif zimupu[i+1].isdigit() and zimupu[i+2]=='/' and zimupu[i+3].isdigit():
                result += chr(ord('0')+4*int(zimupu[i+1])/int(zimupu[i+3]))
            else :
                result += '4'
    return result

# zimupu = "[e/C/]E/ e/E/ f/E/ g/E/ |[G/g/]B/ f/B/ e/B/ d/B/ |[c/A/]E/ c/E/ d/E/ e/E/ |[e/G/]B/ G/d/ [d/D/]B/ G/D/ |[e/C/]E/ e/E/ f/E/ g/E/ |[G/g/]B/ f/B/ e/B/ d/B/ |[c/A/]E/ c/E/ d/E/ e/E/ |[d/B/G/]D/ G/c/ [c/C/]E/ G/E/ |[d/B/G/]D/ d/D/ [e/c/A/]E/ c/E/ |[d/B/G/]D/ e/f/ [e/c/A/]E/ c/E/ |[d/B/G/]D/ e/f/ [e/c/A/]E/ d/E/ |[c/D/]F/ d/F/ [G/D/]F/ E/D/ |[e/C/]E/ e/E/ f/E/ g/E/ |[G/g/]B/ f/B/ e/B/ d/B/ |[c/A/]E/ c/E/ d/E/ e/E/ |[d/B/G/]D/ G/c/ [c2G2E2C/]||"
# jianpu = zimupu2shuzipu(zimupu=zimupu)
# print(jianpu)
jianpu = "\
        211 221 211, 211 221 211 221 231, 363 211 363 211 363 211 222 212,\n\
        , 211 221 211, 211 221 211 221 231, 363 211 363 211 363 211 232 222,\n\
        , 361 211 263 261 261 251 262 261 251 261 251 261 252, 361 211, 263 261 261 251 261 251 273 271 271 261 273,\n\
        262 231 251 231, 223 231 223 231 223 231 251 231 251 231, 223 231 223 231 226 211 221, 232 362 212 232 223 231 222 212,\n\
        261 271, 111 121 271 111 112 111 271 111 121 171 111 112 111 121, 131 121 131 121 132 131 121 132 152 132 261 271, 111 121 271 111 112 111 271 111 121 271 111 112 111 121,\n\
        131 121 131 121 132 131 121 132 152 132 152, 133 151 133 151 131 151 161 131 152 152, 133 151 133 151 131 151 161 131 152 151 151, 132 122 122 111 133 122 122 111,\n\
        151 151 132 122 122 111 133 122 122 111 111\n\
        "
        # 2313 211 221 211, 2311 211 221 211 221 231, 363 211 363 211 363 211 222 212,\n\
        # 3716, 2313 211 221 211, 2311 211 221 211 221 231, 363 211 363 211 363 211 232 222,\n\
        # 3716, 361 211 263 261 261 251 262 261 251 261 251 261 252, 2313 361 211, 263 261 261 251 261 251 273 271 271 261 273,\n\
        # 262 2310 231 251 231, 223 231 223 231 223 231 251 231 251 231, 223 231 223 231 226 211 221, 232 362 212 232 223 231 222 212,\n\
        # 3614 261 271, 111 121 271 111 112 111 271 111 121 171 111 112 111 121, 131 121 131 121 132 131 121 132 152 132 261 271, 111 121 271 111 112 111 271 111 121 271 111 112 111 121,\n\
        # 131 121 131 121 132 131 121 132 152 132 152, 133 151 133 151 131 151 161 131 152 152, 133 151 133 151 131 151 161 131 152 151 151, 132 122 122 111 133 122 122 111 1115,\n\
        # 151 151 132 122 122 111 133 122 122 111 111\n\

        # "262 272, 116 272 114 134, 2712 232 232, 266 252 264 114,\n2512 234, 246 232 244 114, 2310 112 112 112, 276 242 244 274,\n\
        # 2712 262 272, 116 272 114 134, 2712 232 232, 266 252 264 114,\n\
        # 2512 234, 246 112 274 114, 122 124 132 118, 112 272 264 274 254,\n\
        # 2612 112 122, 136 122 134 154, 1212 252 252, 116 272 114 134,\n\
        # 1316, 262 272 114 272 112 124, 116 252 258, 144 134 124 114,\n\
        # 1312 134, 168 158, 132 122 118 114, 126 112 124 154,\n\
        # 1312 134, 166 162 156 152, 132 122 118 114, 126 112 124 274,\n\
        # 1612"
result = jianpujiakg(jianpu)
print(result)
