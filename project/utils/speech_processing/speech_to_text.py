import threading
import websocket
import pyaudio
import time
import sys
from datetime import datetime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
from project.api_info import *
import json
import webrtcvad

# import logging
# logging.getLogger('httpx').setLevel(logging.WARNING)

# Configuration
SERVER_URL = "wss: //iat-api.xfyun.cn/v2/iat"
RECONNECT_TIME = 55  # seconds
# CHUNK = 1280
INTERVAL = 0.04
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
frame_duration_ms = 30
CHUNK = int(RATE * frame_duration_ms / 1000)

# The status of the connection, 1 for continuing, 2 for closing
status = 2


class AudioStreamer:
    def __init__(self, callback=None):
        self.ws = None
        self.callback = callback
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)
        print("🔴 ︎开始录音...")
        self.reconnect_thread = threading.Thread(target=self.handle_reconnection)
        self.reconnect_thread.daemon = True
        self.reconnect_thread.start()

    def on_message(self, ws, message):
        # print(f"Received message: {message}")

        # Parse the message
        data = json.loads(message)["data"]

        # Update status
        global status
        status = data["status"]

        # Call the callback function
        if self.callback is not None:
            self.callback(data["result"])

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws):
        # print("### closed ###")
        pass

    def on_open(self, ws: websocket.WebSocketApp):
        def run(*args):
            data_template = {
                "common": {"app_id": APPID},
                "business": {
                    "domain": "iat",
                    "language": "zh_cn",
                    "accent": "mandarin",
                    "vinfo": 1,
                    "vad_eos": 48000  # 单次检测时长
                },
                "data": {
                    "status": 0,
                    "format": "audio/L16;rate=8000",
                    "encoding": "raw"
                }
            }
                        
            vad = webrtcvad.Vad(1)

            # First Frame
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            data_template["data"]["audio"] = str(base64.b64encode(data), 'utf-8')
            ws.send(json.dumps(data_template))
            time.sleep(INTERVAL)
            del data_template["business"]
            del data_template["common"]

            # Update status
            global status
            status = 1
            data_template["data"]["status"] = status

            # Continous Frames
            while status != 2:
                data = self.stream.read(CHUNK, exception_on_overflow=False)
                if not vad.is_speech(data, RATE):
                    continue
                data_template["data"]["audio"] = str(base64.b64encode(data), 'utf-8')
                try:
                    ws.send(json.dumps(data_template))
                except Exception:
                    break
                    # status = 2
                time.sleep(INTERVAL)

            # Close the connection
            time.sleep(1)
            ws.close()
            status = 2
            print("Thread terminating...")

        threading.Thread(target=run).start()

    def create_url(self):
        url = 'wss://iat-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(time.mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + "iat-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(APISERECT.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            XF_APIKEY, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "iat-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        return url

    def start_streaming(self):
        # websocket.enableTrace(True)
        self.ws_url = self.create_url()
        self.ws = websocket.WebSocketApp(self.ws_url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        # print("Starting streaming...")
        self.ws.run_forever()

    def handle_reconnection(self):
        while True:
            global status
            if status == 2:
                self.start_streaming()
                time.sleep(1)

    def close(self):
        # Clean up
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.ws.close()


if __name__ == "__main__":
    audio_streamer = AudioStreamer()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        audio_streamer.close()
        print("Exiting...")