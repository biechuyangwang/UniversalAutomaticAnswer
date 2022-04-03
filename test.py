# A completely innocent attempt to borrow proprietary Microsoft technology for a much better TTS experience
import requests
import websockets
import asyncio
from datetime import datetime
import re
import time
import re
import uuid
from pydub import AudioSegment

import os,pilk
from pydub import AudioSegment

def convert_to_silk(media_path: str) -> str:
    """将输入的媒体文件转出为 silk, 并返回silk路径"""
    media = AudioSegment.from_file(media_path)
    pcm_path = os.path.basename(media_path)
    pcm_path = os.path.splitext(pcm_path)[0]
    silk_path = pcm_path + '.silk'
    pcm_path += '.pcm'
    media.export(pcm_path, 's16le', parameters=['-ar', str(media.frame_rate), '-ac', '1']).close()
    pilk.encode(pcm_path, silk_path, pcm_rate=media.frame_rate, tencent=True)
    return silk_path

voice_dict = {'晓晓' : 'zh-CN-XiaoxiaoNeural', '云扬' : 'zh-CN-YunyangNeural', 
              '晓辰' : 'zh-CN-XiaochenNeural', '晓涵' : 'zh-CN-XiaohanNeural',
              '晓墨' : 'zh-CN-XiaomoNeural', '晓秋' : 'zh-CN-XiaoqiuNeural',
              '晓睿' : 'zh-CN-XiaoruiNeural', '晓双' : 'XiaoshuangNeural', 
              '晓萱' : 'zh-CN-XiaoxuanNeural', '晓颜' : 'zh-CN-XiaoyanNeural',
              '晓悠' : 'zh-CN-XiaoyouNeural'
              }
voicestyle_dict = {'正常':'general', '助手':'assistant',
                   '聊天':'chat', '客服':'customerservice',
                   '广播':'newscast', '深情':'affectionate',
                   '生气':'angry', '冷静':'calm',
                   '愉快':'cheerful', '不满':'disgruntled',
                   '害怕':'fearful', '温和':'gentle',
                   '抒情':'lyrical', '伤心':'sad',
                   '严肃':'serious'
                  }
speed_num = 0 # 语速 [-100, 200]
pitch_num = 0 # 语调 [-50, 50]

#Fix the time to match Americanisms
def hr_cr(hr):
    corrected = (hr - 1) % 24
    return str(corrected)

#Add zeros in the right places i.e 22:1:5 -> 22:01:05
def fr(input_string):
    corr = ''
    i = 2 - len(input_string)
    while (i > 0):
        corr += '0'
        i -= 1
    return corr + input_string

#Generate X-Timestamp all correctly formatted
def getXTime():
    now = datetime.now()
    return fr(str(now.year)) + '-' + fr(str(now.month)) + '-' + fr(str(now.day)) + 'T' + fr(hr_cr(int(now.hour))) + ':' + fr(str(now.minute)) + ':' + fr(str(now.second)) + '.' + str(now.microsecond)[:3] + 'Z'

#Async function for actually communicating with the websocket
# async def transferMsTTSData(msg_content, spd, ptc, voice):
async def transferMsTTSData(voice='zh-CN-XiaoxiaoNeural', voicestyle='general', spd='0', ptc='0', msg_content='星期六到底有什么故事呢？', output_filename='out_filename'):
    endpoint1 = "https://azure.microsoft.com/en-gb/services/cognitive-services/text-to-speech/"

    r = requests.get(endpoint1)
    main_web_content = r.text

    #They hid the Auth key assignment for the websocket in the main body of the webpage....
    token_expr = re.compile('token: \"(.*?)\"', re.DOTALL)
    Auth_Token = re.findall(token_expr, main_web_content)[0]
    # req_id = str('%032x' % random.getrandbits(128)).upper() #I don't know if it matters if we reuse these, going to generate one anyway
    req_id = uuid.uuid4().hex.upper()
    endpoint2 = "wss://eastus.tts.speech.microsoft.com/cognitiveservices/websocket/v1?Authorization=" + Auth_Token +"&X-ConnectionId=" + req_id[::-1]

    # async with websockets.client.connect(endpoint2, ssl=True) as client_conn:
    async with websockets.connect(endpoint2) as websocket:
        payload_1 = '{"context":{"system":{"name":"SpeechSDK","version":"1.12.1-rc.1","build":"JavaScript","lang":"JavaScript","os":{"platform":"Browser/Linux x86_64","name":"Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0","version":"5.0 (X11)"}}}}'
        message_1 = 'Path : speech.config\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + getXTime() + '\r\nContent-Type: application/json\r\n\r\n' + payload_1
        await websocket.send(message_1)
        
        payload_2 = '{"synthesis":{"audio":{"metadataOptions":{"sentenceBoundaryEnabled":false,"wordBoundaryEnabled":false},"outputFormat":"audio-16khz-32kbitrate-mono-mp3"}}}'
        message_2 = 'Path : synthesis.context\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + getXTime() + '\r\nContent-Type: application/json\r\n\r\n' + payload_2
        await websocket.send(message_2)

        payload_3 = '<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US"><voice name="' + voice + '"><mstts:express-as style="' + voicestyle +'"><prosody rate="'+spd+'%" pitch="'+ptc+'%">'+ msg_content +'</prosody></mstts:express-as></voice></speak>'
        message_3 = 'Path: ssml\r\nX-RequestId: ' + req_id + '\r\nX-Timestamp: ' + getXTime() + '\r\nContent-Type: application/ssml+xml\r\n\r\n' + payload_3
        await websocket.send(message_3)
       
        end_resp_pat = re.compile('Path:turn.end') #Checks for close connection message
        audio_stream = b''
        audio_string = ''
        while(True):
            response = await websocket.recv()
            # Make sure the message isn't telling us to stop
            if (re.search(end_resp_pat, str(response)) == None):
                #Check if our response is text data or the audio bytes
                if type(response) == type(bytes()):
                    # Extract binary data
                    try:
                        # print('提取二进制文件')
                        start_ind = str(response).find('Path:audio')
                        # audio_string += str(response)[start_ind+14:-1]
                        audio_stream += response[start_ind-2:]
                    except:
                        pass        
            else:
                break
        with open(output_filename+'.mp3', 'wb') as audio_out:
            audio_out.write(audio_stream)
            convert_to_silk(output_filename+'.mp3')
            # song = AudioSegment.from_mp3(output_filename+'.mp3')
            # song.export(output_filename+'.wav', format="wav")
            # print(str(audio_stream))
            # print('NOW STRING FORM')
            # print(audio_string)


async def mainSeq(voice='晓晓',  voicestyle='正常', spd=0, ptc=0, msg_content='星期六到底有什么故事呢？', output_filename='out_filename'):
    voice = voice_dict[voice]
    voicestyle = voicestyle_dict[voicestyle]
    spd = str(spd)
    ptc = str(ptc)
    # print('voice:{}\nvoicestyle:{}\nspd:{}\nptc:{}\nmsg_content:{}\n'.format(voice,voicestyle,spd,ptc,msg_content))
    await transferMsTTSData(voice, voicestyle, spd, ptc, msg_content,output_filename)
if __name__ == "__main__":
    voice = '晓晓'
    msg_content = '你今天的作业写完了没？就开始肆无忌惮的玩了。'
    asyncio.run(mainSeq(voice, msg_content=msg_content, output_filename='test2'))
    print('成功生成')
    # if len(sys.argv) == 1:
    #     print(voice_dict)
    # elif len(sys.argv) == 5:
    #     say = sys.argv[1]
    #     speed = sys.argv[2]
    #     pitch = sys.argv[3]
    #     voice = sys.argv[4]
    #     mainSeq(say, speed, pitch, voice)
    # else:
    #     print("Incorrect arg sequence")
    #     quit()