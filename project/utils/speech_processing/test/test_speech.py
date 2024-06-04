import time

import webrtcvad
import pyaudio


WAIT_TIME = 1.5  # 若一定时间不再说话，则判定这段话结束，单位为s

def is_speech(frame, sample_rate=16000, mode=3):
    # mode 0-3, 宽松到严格
    vad = webrtcvad.Vad(mode)
    return vad.is_speech(frame, sample_rate)


def main():
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

    voice_flag = False
    try:
        while True:
            frame = stream.read(frame_size, exception_on_overflow=False)
            if is_speech(frame, sample_rate):
                # 如果检测到语音，则打印一个"#"
                if not voice_flag:
                    voice_flag = True
                    print("正在说话", end="")
                print("#", end="")
            elif voice_flag:  # 如果检测到非语音，则等待2s判定这段话是否结束
                # 设置一个标志表示准备开始计时
                timeout_flag = True
                start_time = time.time()  # 记录开始计时的时间

                # 等待一定时间并检查期间是否有新的语音输入
                while (time.time() - start_time) < WAIT_TIME:
                    frame = stream.read(frame_size, exception_on_overflow=False)
                    if is_speech(frame, sample_rate):
                        timeout_flag = False  # 如果有语音输入，则取消计时
                        break
                if timeout_flag:  # 如果2秒内都没有语音输入
                    print("end")
                    voice_flag = False
    except KeyboardInterrupt:
        print("\n录音结束")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    main()
