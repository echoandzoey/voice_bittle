from utils.speech_processing.speech_to_text import AudioStreamer
from llm_interaction import tools, tool_choice
import json
from utils.send_command import sendCommand, initBittle, closeBittle
import time

prompt = "你是一只机器小狗，你不会说话，请不要给response，永远用tool_choice操作。你只能从给出的tools中进行选择。"
history = []
goodPorts = None


# 打印识别结果
def print_result(message):
    result = ""
    if message:
        for i in message["ws"]:
            for w in i["cw"]:
                result += w["w"]
        result = result.strip("，。！？")
        if result:
            print("识别结果: " + result)
    return result


def on_message(message):
    result = print_result(message)

    # # Beeping to indicate that the robot is listening
    # global goodPorts
    # sendCommand(goodPorts, "b", [10, 4])

    # Ask LLM to choose a tool
    global history
    tool = tool_choice(result, tools, history)
    history.append({"role": "user", "content": result})
    # print(f"选择了{tool["action"]["name"]}")
    name, arguments = parse_action(tool)
    # if name:
    #     print(f"选择了{name}")
    #     print(arguments)

    print(f"选择了{name}")

    # print(f"选择了{arguments}")

    # Send the command to the robot
    if name != 'none':
        print("判断要做动作")
        if arguments == 'none':
            print("只要做动作")
            sendCommand(goodPorts, "k" + name)
            print("成功做了动作")
        else:
            sendCommand(goodPorts, name, eval(arguments["data"]))


def parse_action(action_data):
    try:
        # 尝试解析 action 中的 arguments 字段
        print(f"Received action_data: {action_data}")  # 添加这行来调试
        # global arguments
        action_data = json.loads(action_data)
        #     if isinstance(action_data, dict):
        # # 如果 action_data 是字典
        #          print("action_data is a dictionary")
        #     else:
        #             # 如果 action_data 不是字典
        #         print("action_data is not a dictionary")

        # arguments = action_data.get('arguments', 'none')
        # name = action_data.get('name', 'none')

        name = action_data['action']['name']
        arguments = action_data['action']['arguments']

        print(f'''nameis{name}++++++++++++++''')
        print(f'''arguementis{arguments}++++++++++++++''')
        # print(f'''namevalueis{name_value}++++++++++++++''')
        # 根据 'name' 字段的值判断动作
        if name == 'none':
            return None  # 没有动作
        else:
            return name, arguments
    except json.JSONDecodeError:
        return None  # 解析错误，视为没有动作


if __name__ == "__main__":
    goodPorts = initBittle()
    audio_streamer = AudioStreamer(callback=on_message)
    print("开始录音")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        closeBittle(goodPorts)
        exit(0)
