# ref:使用Python进行语音活动检测（VAD）
# https://cloud.tencent.com/developer/article/2369279

import threading
import time
import webrtcvad
import pyaudio

def is_speech(frame, sample_rate=16000, mode=3):
    time.sleep(0.1)  # 避免频繁检测
    vad = webrtcvad.Vad(mode)  # mode 0-3, 检测人声宽松到严格
    return vad.is_speech(frame, sample_rate)


sample_rate = 16000
frame_duration_ms = 30  # VAD支持的帧长: 10, 20, 或 30ms
frame_size = int(sample_rate * frame_duration_ms / 1000)


def listen_for_voice(callback):
    """监听麦克风输入，检测人声活动"""
    # 初始化pyaudio和音频流参数
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=frame_size)

    print("开始实时录音，检测说话活动...")
    voice_flag = False
    try:
        while True:
            frame = stream.read(frame_size, exception_on_overflow=False)
            if is_speech(frame, sample_rate):
                if not voice_flag:  # 等待1s再判定这段话是否开始
                    voice_flag = delay_speech_detection(stream, wait_time=0.5)
                    if voice_flag:
                        callback()
                        print("正在说话", end="")
                if voice_flag:
                    print("#", end="")   # 正在语音时，则打印一个"#"
            elif voice_flag:  # 如果检测到非语音，则等待2s判定这段话是否结束
                voice_flag = delay_speech_detection(stream, wait_time=2)
                if not voice_flag:
                    print("end")
                # # 设置一个标志表示准备开始计时
                # timeout_flag = True
                # start_time = time.time()  # 记录开始计时的时间
                #
                # # 等待一定时间并检查期间是否有新的语音输入
                # while (time.time() - start_time) < WAIT_TIME:
                #     frame = stream.read(frame_size, exception_on_overflow=False)
                #     if is_speech(frame, sample_rate):
                #         timeout_flag = False  # 如果有语音输入，则取消计时
                #         break
                # if timeout_flag:  # 如果一定时间内都没有语音输入
                #     print("end")
                #     voice_flag = False
    except KeyboardInterrupt:
        print("\n录音结束")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


# 等待一定时间并检查期间是否有新的语音输入，防止过于敏感导致误检测
def delay_speech_detection(stream, wait_time):
    # 设置一个标志表示准备开始计时
    start_time = time.time()  # 记录开始计时的时间
    while (time.time() - start_time) < wait_time:
        frame = stream.read(frame_size, exception_on_overflow=False)
        if is_speech(frame, sample_rate):
            tmp_voice_flag = True  # 如果有语音输入，则取消计时
            return tmp_voice_flag
    tmp_voice_flag = False
    return tmp_voice_flag  # 如果一定时间内都没有语音输入，返回false


def action_on_speech():
    # 测试
    print("测试：此时小狗应该执行倾听动作")


if __name__ == "__main__":
    voice_thread = threading.Thread(target=listen_for_voice(callback=action_on_speech))
    voice_thread.daemon = True
    voice_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n程序退出")
