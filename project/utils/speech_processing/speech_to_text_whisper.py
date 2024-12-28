import torch
import whisper
import sounddevice as sd
import numpy as np
import webrtcvad
import time


# 音频缓冲区和其他参数
buffer_size = 16000  # 每个音频块的大小（1秒）
sample_rate = 16000
audio_buffer = np.zeros(buffer_size * 10, dtype=np.float32)  # 预留10秒缓冲区
buffer_offset = 0
silence_threshold = 0.1  # 声音门限

class WhisperStreamer:
    def __init__(self, callback=None):
        self.callback = callback
        self.vad = webrtcvad.Vad(1)
        self.model = whisper.load_model("base").eval()  # 加载预训练的 Whisper 模型，并设置为评模式 可选模型: tiny, base, small, medium, large
        self.stream = sd.InputStream(callback=self.on_message, channels=1, samplerate=16000, blocksize=buffer_size)
        # self.reconnect_thread = threading.Thread(target=self.start_streaming)
        # self.reconnect_thread.daemon = True
        # self.reconnect_thread.start()
        # self.running = False
        # self.start_streaming()
        self.stream.start()
        
    # 定义流式解码函数
    def stream_decode(self, audio_buffer):
        audio_tensor = torch.tensor(audio_buffer).float()
        result = self.model.transcribe(audio_tensor, fp16=False, language='zh')
        return result['text']

    # 麦克风回调函数
    def on_message(self, indata, frames, time, status):
        global audio_buffer, buffer_offset
        
        # 确保音频为单声道，转换为 16-bit PCM 格式
        # pcm_data = (indata[:, 0] * 32767).astype(np.int16).tobytes()

        # # 使用 VAD 检测是否为语音
        # is_speech = self.vad.is_speech(pcm_data, sample_rate)
        is_speech = 1
        # 计算当前音频块的音量
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > silence_threshold and is_speech:
            # 将新音频数据复制到缓冲区
            audio_buffer[buffer_offset:buffer_offset+frames] = indata[:, 0]
            buffer_offset += frames

            # 当缓冲区达到或超过设定的大小时进行处理
            if buffer_offset >= buffer_size:
                text = self.stream_decode(audio_buffer[:buffer_size])
                print(f"Transcription: {text}", flush=True)
                
                
                if self.callback is not None:
                    self.callback(text)

                # 移动缓冲区的数据
                audio_buffer = np.roll(audio_buffer, -buffer_size)
                buffer_offset -= buffer_size
        else:
            # 如果检测到的音量低于门限，将缓冲区位置重置
            buffer_offset = 0
            
    # 启动麦克风流
    def start_streaming(self):
        self.running = True
        # try:
        with self.stream:
            print("Listening...")
            while self.running:
                time.sleep(1)  # 继续监听
        # except KeyboardInterrupt:
        #     print("\n键盘中断，停止运行...")
            # self.close()

    def close(self):
        if self.stream and self.stream.active:
            # self.running = False
            self.stream.abort()
            print("Audio stream stopped.")



    


