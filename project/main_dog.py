# from utils.send_command import *
import sys
from utils.speech_processing.speech_to_text import AudioStreamer
from llm_interaction.interact_with_llm import tool_choice
import json
from llm_interaction.prompt_action_list import actions
from utils.send_command import sendCommand, initBittle, closeBittle
from utils.ParseTools import parse_action, parse_combo_actions
import time
import threading
import os


history = []
goodPorts = None

# 是否连接机器狗
is_dog_connected = False


def on_message(message):
    # todo:考虑加入唤醒词？

    # 打印用户语音输入的识别结果
    user_input = print_user_input(message)
    # 等待llm应答，做出padding动作，表示正在思考
    if user_input != "":
        # 暂时取消padding动作
        # padding_thread = threading.Thread(target=padding_action)
        padding_thread = threading.Thread()
        padding_thread.start()
        # 与llm交互
        tool = tool_choice(user_input)
        # 小狗做出反应
        # dog_reaction(tool)
        dog_reaction_combo(tool)


# 打印用户语音识别结果
def print_user_input(message):
    result = ""
    if message:
        for i in message["ws"]:
            for w in i["cw"]:
                result += w["w"]
        result = result.strip(". ，。！？")
        if result:
            print("识别结果: " + result)
    return result


# 解析小狗动作, 并发送给机器狗
# def dog_reaction(tool):
#     name, arguments = parse_action(tool)
#     action_info = actions[name]
#     print(f"选择了{name}，意思是{action_info}")
#     if is_dog_connected:
#         # Send the command to the robot
#         if name != 'none':
#             # print("判断要做动作")
#             if arguments == 'none':
#                 # print("只要做动作")
#                 # test
#                 action_start_time = time.time()
#                 send_dog_action(name)
#                 action_end_time = time.time()
#                 print("执行应答动作耗时：", action_end_time - action_start_time)
#             else:
#                 sendCommand(goodPorts, name, eval(arguments["data"]))

# 支持组合动作版
def dog_reaction_combo(tool):
    # actions_list = []
    actions_list = parse_combo_actions(tool)
    # print(f"待做列表里面有不为零的参数: {len([action for action in actions_list if action])}")
    while actions_list:
        action = actions_list.pop(0)  # 取出第一个动作
        if action == '':
            break
        print(f"Processing action: {action}")
        send_dog_action(action)


def padding_action():
    # todo: padding动作，小狗思考如何作出反应
    # test
    print("小狗正在思考...\n")
    if is_dog_connected:
        padding_start = time.time()
        # send_dog_action("reply")
        padding_end = time.time()
        print("执行padding动作耗时", padding_end - padding_start)


# 发送小狗动作命令
def send_dog_action(action_name):
    print("向小狗发送指令：", action_name)
    if is_dog_connected:
        sendCommand(goodPorts, "k" + action_name)


if __name__ == "__main__":
    original_path = os.getcwd()
    if is_dog_connected:
        goodPorts = initBittle()
        print("连接机器狗")
    audio_streamer = AudioStreamer(callback=on_message)
    start_time = time.time()
    # 开始录音时，示意用户可以说话了
    send_dog_action("scrh")

    try:
        # 程序代码
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("键盘中断，停止运行...")
    finally:
        os.chdir(original_path)  # 恢复原路径
        print("恢复原路径")
        if is_dog_connected:
            print("关闭机器狗")
            closeBittle(goodPorts)
        exit(0)
