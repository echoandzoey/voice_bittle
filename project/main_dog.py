# from utils.send_command import *
from speech_processing.speech_to_text import AudioStreamer
from llm_interaction.interact_with_llm import tool_choice
from utils.send_command import sendCommand, initBittle, closeBittle
import time
import os
from print_format import *
import threading
import random

goodPorts = None

# 是否连接机器狗
is_dog_connected = False


def on_message(message):
    # 打印用户语音输入的识别结果
    user_input = print_user_input(message)
    # 等待llm应答，做出padding动作，表示正在思考
    if user_input != "":
        # 暂时取消padding动作
        # padding_thread = threading.Thread(target=padding_action)
        # padding_thread = threading.Thread()
        # padding_thread.start()
        choice = tool_choice(user_input)
        action_list = choice

        for action in action_list:
            send_dog_action(action)


def dog_reaction(llm_input):
    choice = tool_choice(llm_input)
    action_list = choice

    for action in action_list:
        send_dog_action(action)


def auto_reaction(llm_input):
    while True:
        # 生成随机时间间隔
        delay = random.uniform(4, 6)
        # 使用Timer在指定延迟后执行dog_reaction
        timer = threading.Timer(delay, dog_reaction, args=(llm_input,))
        timer.start()
        time.sleep(delay)


# 发送小狗动作命令
def send_dog_action(action_name):
    colored_output("🐶 执行动作：" + action_name, "green")
    if is_dog_connected:
        sendCommand(goodPorts, "k" + action_name)


if __name__ == "__main__":
    original_path = os.getcwd()
    if is_dog_connected:
        goodPorts = initBittle()
    audio_streamer = AudioStreamer(callback=on_message)
    # 开始录音时，示意用户可以说话了
    send_dog_action("scrh")

    # 不定时让小狗执行自主动作
    auto_reaction("暂时没人和你说话，做些自己的事情吧")

    try:
        # 程序代码
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("键盘中断，停止运行...")
    finally:
        os.chdir(original_path)  # 恢复原路径
        # print("恢复原路径")
        if is_dog_connected:
            # print("关闭机器狗")
            closeBittle(goodPorts)
        exit(0)
