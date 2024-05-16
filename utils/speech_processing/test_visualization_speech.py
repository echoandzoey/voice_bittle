#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    可视化声音波形，测试输入
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import wave
import os
import operator
from functools import reduce


class SubplotAnimation(animation.TimedAnimation):
    def __init__(self, static=False, path=None):
        """
        音频波形动态显示，实时显示波形
        :param static: 是否为静态模式
        :param path:   wav 文件路径
        """
        self.static = static
        if static and os.path.isfile(path):
            self.stream = wave.open(path)
            # 采样频率
            self.rate = self.stream.getparams()[2]
            self.chunk = self.rate / 2
            self.read = self.stream.readframes
        else:
            self.rate = 8000  # 采样率
            self.chunk = 200  # 语音块大小
            p = pyaudio.PyAudio()
            self.deviceindex = 0 # 录音设备编号

            # frames_per_buffer=self.chunk 设置音频流的缓冲区大小，即每次从音频设备读取的数据块的大小
            self.stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.rate,
                                 input_device_index=self.deviceindex,
                                 input=True, frames_per_buffer=self.chunk)
            self.read = self.stream.read

        self.chunknum = 40  # 同屏显示语音块的数量
        self.voicedatas = []
        self.zero = [0 for i in range(self.chunk)]
        for index in range(self.chunknum):
            self.voicedatas.insert(0, self.zero)

        # 获取内录设备序号,在windows操作系统上测试通过，hostAPI = 0 表明是MME设备
    # def findInternalRecordingDevice(self, p):
    #     # 要找查的设备名称中的关键字
    #     target = 'Voicemeeter Input'
    #     # 逐一查找声音设备
    #     for i in range(p.get_device_count()):
    #         devInfo = p.get_device_info_by_index(i)
    #         if devInfo['name'].find(target) >= 0 and devInfo['hostApi'] == 0:
    #             # print('已找到内录设备,序号是 ',i)
    #             return i
    #     print('无法找到内录设备!')
    #     return -1

    # 定义波形显示图的横纵坐标大小及类别并选用读取实时音频数据方式显示，设定更新间隔
    def start(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 1, 1)
        ax1.set_xlabel("t")
        ax1.set_ylabel("x")
        ax1.set_xlim(0, 1.0 * (self.chunknum * self.chunk - 1) / self.rate)
        ax1.set_ylim(-16000, 16000)
        self.line1, = ax1.plot([], [], lw=2)

        # 更新间隔/ms
        interval = int(1000 * self.chunk / self.rate)
        animation.TimedAnimation.__init__(self, fig, interval=interval, blit=True)

    # 初始化绘图，l.set_data([], []) 将绘图数据清空，使得动画开始时图像为空白状态
    def _init_draw(self):
        lines = [self.line1]
        for l in lines:
            l.set_data([], [])

    def new_frame_seq(self):
        return iter(range(self.chunk))

    def _draw_frame(self, framedata):
        if self.static:
            # 读取静态wav文件波形
            y = np.fromstring(self.read(self.chunk / 2 + 1), dtype=np.int16)[:-1]
        else:
            # 实时读取声频
            data = np.frombuffer(self.read(self.chunk, exception_on_overflow=False), dtype=np.int16)
            data = data.tolist()
            self.voicedatas.append(data)
            self.voicedatas.pop(0)
            y = reduce(operator.add, self.voicedatas)  # 将 self.voicedatas 中的 40 个列表数据全部放在 1 个列表中
        x = np.linspace(0, 1.0 * (self.chunknum * self.chunk - 1) / self.rate, self.chunknum * self.chunk)

        # 画波形图
        self.line1.set_data(x, y)


if __name__ == "__main__":
    ani = SubplotAnimation()
    ani.start()
    plt.show()
