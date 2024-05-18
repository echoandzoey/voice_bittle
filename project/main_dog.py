from utils.send_command import *
from utils.speech_processing.speech_to_text import AudioStreamer
from llm_interaction.interact_with_llm import tool_choice
import json
import time
from llm_interaction.prompt_action_list import actions

history = []
goodPorts = None

# 是否连接机器狗
is_dog_connected = False


def on_message(message):
    # 打印用户语音输入的识别结果
    result = print_user_input(message)

    # Ask LLM to choose a tool
    tool = tool_choice(result)
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
                sendCommand(goodPorts, "k" + name)
                print("成功做了动作")
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


if __name__ == "__main__":
    if is_dog_connected:
        goodPorts = initBittle()
        print("连接机器狗")
    audio_streamer = AudioStreamer(callback=on_message)
    print("开始录音")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if is_dog_connected:
            print("关闭机器狗")
            closeBittle(goodPorts)
        exit(0)
