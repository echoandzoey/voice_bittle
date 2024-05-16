"""
    无需连接硬件，用文字表示交互行为
"""

from myPetoi.utils.speech_processing.speech_to_text import AudioStreamer
from myPetoi.llm_interaction.turtle_game import tool_choice
from myPetoi.llm_interaction.prompt_file.dog_tools_json import *
import json
import time

prompt = "你是一只机器小狗，你不会说话，请不要给response，永远用tool_choice操作。你只能从给出的tools中进行选择。"
history = []


def on_message(message):
    # 打印用户语音输入的识别结果
    result = print_user_input(message)

    # Ask LLM to choose a tool，并载入历史记录
    global history
    tool = tool_choice(result, tools, history)
    history.append({"role": "user", "content": result})
    # print(f"选择了{tool["action"]["name"]}")

    # 解析小狗动作
    parse_action(tool)
    # name, arguments = parse_action(tool)
    # # if name:
    # #     print(f"选择了{name}")
    # #     print(arguments)
    #
    # print(f"选择了{name}")
    #
    # # print(f"选择了{arguments}")


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
        # 示例：(输入：小狗，你好呀）
        # action_data: {
        #     "type": "chat",
        #     "thoughts": "用户在友好地打招呼",
        #     "action": {"arguments": "none", "name": "hi"}
        # }
        print(f"Received action_data: {action_data}")  # 添加这行来调试

        # 尝试解析 action 中的 arguments 字段
        # global arguments
        action_data = json.loads(action_data)
        name = action_data['action']['name']
        arguments = action_data['action']['arguments']

        # print(f'''nameis{name}++++++++++++++''')
        # print(f'''arguementis{arguments}++++++++++++++''')
        # print(f'''namevalueis{name_value}++++++++++++++''')

        # 根据 'name' 字段的值判断动作
        if name == 'none':
            return None  # 没有动作
        else:
            return name, arguments
    except json.JSONDecodeError:
        return None  # 解析错误，视为没有动作


if __name__ == "__main__":
    audio_streamer = AudioStreamer(callback=on_message)
    print("开始录音")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
