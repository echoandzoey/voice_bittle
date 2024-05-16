import webrtcvad
import pyaudio
import numpy as np

def is_speech(frame, sample_rate=16000, mode=1):
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

    try:
        while True:
            frame = stream.read(frame_size, exception_on_overflow=False)
            if is_speech(frame, sample_rate):
                print("检测到说话活动")
            else:
                print("未检测到说话活动")
    except KeyboardInterrupt:
        print("\n录音结束")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == '__main__':
    main()
