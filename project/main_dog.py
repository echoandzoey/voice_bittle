import threading
from utils.send_command import *
from utils.speech_processing.speech_to_text import AudioStreamer
from llm_interaction.interact_with_llm import tool_choice
import json
import time
from llm_interaction.prompt_action_list import actions

history = []
goodPorts = None

# 是否连接机器狗
is_dog_connected = True

def on_message(message):
    # 打印用户语音输入的识别结果
    result = print_user_input(message)
    if result != "":
        # 收到应答展示padding动作
        padding_thread = threading.Thread(target=padding_action)
        padding_thread.start()

    # Ask LLM to choose a tool
    llm_start_time = time.time()
    tool = tool_choice(result)
    llm_end_time = time.time()
    print('等待llm交互时间：', llm_end_time - llm_start_time)

    global history
    history.append({"role": "user", "content": result})

    # 解析小狗动作, 并发送给机器狗
    name, arguments = parse_action(tool)
    action_info = actions[name]
    print(f"选择了{name}，意思是{action_info}")

    # 需连接机器狗运行
    if is_dog_connected:
        # Send the command to the robot
        if name != 'none':
            print("判断要做动作")
            if arguments == 'none':
                print("只要做动作")
                # test
                action_start_time = time.time()
                send_dog_aciton(name)
                action_end_time = time.time()
                print("成功做了动作", action_end_time - action_start_time)
            else:
                sendCommand(goodPorts, name, eval(arguments["data"]))


# 打印用户语音识别结果
def print_user_input(message):
    result = ""
    if message:
        for i in message["ws"]:
            for w in i["cw"]:
                result += w["w"]
        result = result.strip("，。！？")
        if result:
            print("识别结果: " + result)
    return result


def parse_action(action_data):
    try:
        # print(f"Received action_data: {action_data}")  # 添加这行来调试
        # 尝试解析 action 中的 arguments 字段
        action_data = json.loads(action_data)
        name = action_data['action']['name']
        arguments = action_data['action']['arguments']

        # 根据 'name' 字段的值判断动作
        if name == 'none':
            return None  # 没有动作
        else:
            return name, arguments
    except json.JSONDecodeError:
        return None  # 解析错误，视为没有动作

def padding_action():
    # todo: padding动作，小狗思考如何作出反应
    # test
    if is_dog_connected:
        padding_start = time.time()
        send_dog_aciton("buttUp")
        padding_end = time.time()
        print("执行padding动作时间", padding_end - padding_start)

def listening_action():
    # todo: listening动作，倾听别人说话
    # test
    if is_dog_connected:
        listening_start = time.time()
        send_dog_aciton("ck")
        listening_end = time.time()
        print("执行listening动作时间", listening_end - listening_start)

# 发送小狗动作命令
def send_dog_aciton(action_name):
    sendCommand(goodPorts, "k" + action_name)


if __name__ == "__main__":
    if is_dog_connected:
        goodPorts = initBittle()
        print("连接机器狗")
    audio_streamer = AudioStreamer(callback=on_message)
    print("开始录音")
    # # todo: 检测到语音输入，倾听动作
    # if detect_audio_input():
    #     print("检测到语音输入，执行小狗倾听动作")
    #     listening_thread = threading.Thread(target=listening_action)
    #     listening_thread.start()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if is_dog_connected:
            print("关闭机器狗")
            closeBittle(goodPorts)
        exit(0)
