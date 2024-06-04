# ref:使用Python进行语音活动检测（VAD）
# https://cloud.tencent.com/developer/article/2369279

import pyaudio
import threading
import time

# 音频参数设置
CHUNK = 1024  # 每次读取的音频块大小
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 采样率
THRESHOLD = 2000000  # 声音强度阈值，根据实际情况调整

import webrtcvad
import pyaudio


def on_sound_detected():
    """当检测到声音时执行的动作"""
    print("检测到人声输入！")


def is_speech(frame, sample_rate=16000, mode=1):
    # mode 0-3, 宽松到严格
    vad = webrtcvad.Vad(mode)
    return vad.is_speech(frame, sample_rate)


def listen_for_voice(callback):
    """监听麦克风输入，检测人声活动"""
    # p = pyaudio.PyAudio()
    # stream = p.open(format=FORMAT,
    #                 channels=CHANNELS,
    #                 rate=RATE,
    #                 input=True,
    #                 frames_per_buffer=CHUNK)
    #
    # print("开始监听麦克风...")
    # while True:
    #     data = stream.read(CHUNK)
    #     # 计算数据的强度（简单方法，适用于演示）
    #     rms = abs(int.from_bytes(data, byteorder='little'))
    #     if rms > THRESHOLD:
    #         callback()  # 声音超过阈值，执行回调函数
    # stream.stop_stream()
    # stream.close()
    # p.terminate()

    # 初始化pyaudio和音频流参数
    p = pyaudio.PyAudio()
    sample_rate = 16000
    frame_duration_ms = 30  # VAD支持的帧长: 10, 20, 或 30ms
    frame_size = int(sample_rate * frame_duration_ms / 1000)

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=frame_size)

    print("开始实时录音，检测说话活动...")

    try:
        while True:
            frame = stream.read(frame_size, exception_on_overflow=False)
            if is_speech(frame, sample_rate):
                callback()  # 检测到说话活动，执行回调函数

            else:
                print("未检测到说话活动")
    except KeyboardInterrupt:
        print("\n录音结束")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    voice_thread = threading.Thread(target=listen_for_voice, args=(on_sound_detected,))
    voice_thread.daemon = True
    voice_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序退出")
