# from utils.send_command import *
from speech_processing.speech_to_text import AudioStreamer
from llm_interaction.interact_with_llm import tool_choice
from utils.send_command import sendCommand, initBittle, closeBittle
import time
import os
from print_format import colored_output
import logging

# history = []
goodPorts = None

# 是否连接机器狗
is_dog_connected = True


def on_message(message):
    # 打印用户语音输入的识别结果
    user_input = print_user_input(message)
    # 等待llm应答，做出padding动作，表示正在思考
    if user_input != "":
        # 暂时取消padding动作
        # padding_thread = threading.Thread(target=padding_action)
        # padding_thread = threading.Thread()
        # padding_thread.start()

        # 与llm交互
        choice = tool_choice(user_input)
        action_list = choice

        for action in action_list:
            send_dog_action(action)


# 打印用户语音识别结果
def print_user_input(message):
    result = ""
    if message:
        for i in message["ws"]:
            for w in i["cw"]:
                result += w["w"]
        result = result.strip(". ，。！？")
        if result:
            # 计算边框长度，基于result的实际长度
            border_length = len(result) + 4  # 两边各加2个空格和边框字符的宽度
            # 上边框
            top_border = " ┌" + "─" * border_length + "┐\n"
            # 内容部分，两边添加空格以保持居中
            content = "<│" + result + "\n"
            # 下边框
            bottom_border = " └" + "─" * border_length + "┘"
            print(top_border + content + bottom_border)

    return result



# 发送小狗动作命令
def send_dog_action(action_name):
    colored_output("🐶 执行动作：" + action_name, "green")
    if is_dog_connected:
        sendCommand(goodPorts, "k" + action_name)


if __name__ == "__main__":
    # 配置日志级别,之后的logging.info()调用将不会显示
    logging.basicConfig(level=logging.WARNING)

    original_path = os.getcwd()
    if is_dog_connected:
        goodPorts = initBittle()
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
        # print("恢复原路径")
        if is_dog_connected:
            # print("关闭机器狗")
            closeBittle(goodPorts)
        exit(0)
