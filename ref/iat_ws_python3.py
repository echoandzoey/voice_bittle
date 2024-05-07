# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  本demo测试时运行的环境为：Windows + Python3.7
#  本demo测试成功运行时所安装的第三方库及其版本如下，您可自行逐一或者复制到一个新的txt文件利用pip一次性安装：
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#
#  语音听写流式 WebAPI 接口调用示例 接口文档（必看）：https://doc.xfyun.cn/rest_api/语音听写（流式版）.html
#  webapi 听写服务参考帖子（必看）：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=38947&extra=
#  语音听写流式WebAPI 服务，热词使用方式：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--个性化热词，
#  设置热词
#  注意：热词只能在识别的时候会增加热词的识别权重，需要注意的是增加相应词条的识别率，但并不是绝对的，具体效果以您测试为准。
#  语音听写流式WebAPI 服务，方言试用方法：登陆开放平台https://www.xfyun.cn/后，找到控制台--我的应用---语音听写（流式）---服务管理--识别语种列表
#  可添加语种或方言，添加后会显示该方言的参数值
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread

import pyaudio

import json

import zhipuai
from zhipuai import ZhipuAI

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

results =[]

chat_history = []
DogPrompt = '''你是一个有点不耐烦的凶凶的小狗，当我说话的时候你会说[[sit]],只需要返回[[ ]]里面的东西即可，不要加标点或者其它
'''
Userfewshot ='''过来过来小狗
'''
Dogfewshot = ''' sit'''

apikey = "APIKEY"



class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
       
        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":100}
        #vad_eos 指的是静默检测，当超过这个值就认为句子结束

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


# 收到websocket消息的处理
# def on_message(ws, message):
#     try:
#         code = json.loads(message)["code"]
#         sid = json.loads(message)["sid"]
#         if code != 0:
#             errMsg = json.loads(message)["message"]
#             print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

#         else:
#             data = json.loads(message)["data"]["result"]["ws"]
#             # print(json.loads(message))
#             result = ""
#             for i in data:
#                 for w in i["cw"]:
#                     result += w["w"]
#             print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))
           
#     except Exception as e:
#         print("receive msg,but parse exception:", e)
def on_message(ws, message):
    global results  # 确保使用全局变量
    try:
        data = json.loads(message)
        code = data.get("code")
        sid = data.get("sid")
        if code != 0:
            errMsg = data.get("message")
            print(f"sid:{sid} call error:{errMsg} code is:{code}")
        else:
            data = data.get("data", {}).get("result", {}).get("ws", [])
            for i in data:
                for w in i.get("cw", []):
                    word = w.get("w")
                    print("实时反馈词语:", word)  # 即时反馈每个识别出的词语
                    results.append(word)  # 继续累积词语以构建完整句子
            
            # 检测是否识别到句子的结束标志
            if any(word.endswith(("。", "！", "？", "，")) for word in results):
                
                complete_sentence = "".join(results)
                print("完整的句子:", complete_sentence)
                # 这里可以将完整的句子发送给其他服务
                if len(complete_sentence.strip()) > 1 or not complete_sentence.strip() in "。！？，":
                    print("这条消息有效，准备发送给别的服务")
                    handle_llm_request(complete_sentence)  # 发送句子给LLM进行处理
                    
                results.clear()  # 清空累积的结果以准备下一个句子
    except Exception as e:
        print("接收消息时发生异常:", e)




# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,a,b):
    print("### closed ###")





def on_open(ws):
    def run(*args):
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        #调增了缓冲区的大小，这会使每次发送给服务器的数据量减少，从而可能减少处理单个数据包的时间。
        stream.start_stream()

        print("开始录音，请说话...")

        status = STATUS_FIRST_FRAME
        while True:
            #本来是8000，现在改成1024，提高转化速率
            #参数指定了每次从音频输入设备读取的帧数，较小的值意味着数据会更频繁地被发送
            buf = stream.read(1024)
            # # 文件结束
            # if not buf:
            #     status = STATUS_LAST_FRAME  # 假设 STATUS_LAST_FRAME 的值为 2
            if status == STATUS_FIRST_FRAME:

                        d = {"common": wsParam.CommonArgs,
                            "business": wsParam.BusinessArgs,
                            "data": {"status": 0, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"}}
                        d = json.dumps(d)
                        ws.send(d)
                        status = STATUS_CONTINUE_FRAME
            elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                    "audio": str(base64.b64encode(buf), 'utf-8'),
                                    "encoding": "raw"}}
                        ws.send(json.dumps(d))
            else:
                    break

        stream.stop_stream()
        stream.close()
        p.terminate()
        ws.close()

    thread.start_new_thread(run, ())
 



#-----------------llm处理段
#现在要实现的是多次逗弄小狗它就会生气
#所以加入了历史对话效果

    

def handle_llm_request(sentence):   
# 假设你已经定义了发送请求到LLM并处理响应的函数
    chat_history.append({"role": "user", "content": sentence})
    response = ZhipuSingleRequestwithHistory(chat_history)
    chat_history.append({"role": "assistant", "content": response})
    print("LLM响应：", response)
    print("\n当前对话历史：")
    for message in chat_history:
        print(f"{message['role']}: {message['content']}")
    
    

def Prompt_engineering():
    #在一开始初始化的时候加入prompt
    global chat_history
    chat_history =[]
    chat_history.append({"role": "system", "content": DogPrompt})
    chat_history.append({"role": "user", "content": Userfewshot})
    chat_history.append({"role": "user", "content": Dogfewshot})    
    
#改成发送历史消息过去
def ZhipuSingleRequestwithHistory(chat_history):
    client = ZhipuAI(api_key=apikey)
    try:
        # 发送包含对话历史的请求
        response = client.chat.completions.create(
            model="glm-4",
            messages=chat_history,
            temperature=0.95,
            max_tokens=240
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"请求错误: {e}")
        return ""

 


if __name__ == "__main__":


    Prompt_engineering()
    wsParam = Ws_Param(APPID='APPID', APIKey='APIKey', APISecret='APISecret')
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




# def ZhipuSingleRequest():
#     # print("发起单次智谱请求")
#     client = ZhipuAI(api_key=apikey)
#     response = client.chat.completions.create(
#         # model="glm-3-turbo",
#         model="glm-4",
#         # kingPrompt
#         messages=[
#             {"role": "system", "content": DogPrompt},

#         ],
        
#         temperature = 0.95,
#         max_tokens = 240
#     )
#     # for chunk in response:
#     #  print(chunk.choices[0].delta)
    
#     message_str = response.choices[0].message.content
#     print (f"系统：{message_str}")# Adjusted to correctly extract the string
#     return message_str
#   # 将response对象转换为字符串并打印出来
    
  
  


# #多次请求

# def main():
#     chat_history = []  # 初始化对话历史记录
   
#     #添加prompt对话以及fewshot对话
#     chat_history.append({"role": "system", "content":DogPrompt})
    

#     print("聊天程序已启动。输入 '退出' 来结束对话。")

#     while True:
        
        

# if __name__ == "__main__":
#     main()


