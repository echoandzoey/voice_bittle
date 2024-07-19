import random
from ParseTools import parse_action_list
from prompt_design import construct_prompts
from dog_class import *
from interact_with_llm import get_llm_msg
from print_format import *
from speech_processing.speech_to_text import AudioStreamer


# 输入方式1：小狗自主动作，定时执行
def auto_reaction():
    while True:
        # 生成随机时间间隔
        delay = random.uniform(4, 6)
        # 使用Timer在指定延迟后执行dog_reaction
        timer = threading.Timer(delay, dog_reaction, args=("做些自己的事情吧",))
        timer.start()
        time.sleep(delay)


# 输入方式2；小狗响应用户输入
def on_message(message):
    # 接收并打印用户输入
    user_input = print_user_input(message)
    if user_input != "":
        dog_reaction(user_input)


# 主程序：与llm通讯并执行动作
def dog_reaction(current_input):
    # 构建输入llm的提示词（记忆功能）
    prompts = construct_prompts(current_input, dog.memory)

    # 获取llm结果(字典类型）
    reply_json = get_llm_msg(prompts)

    # 解析llm结果: 解析出动作列表
    action_list = parse_action_list(reply_json)

    # 执行动作
    for action in action_list:
        dog.action(action)

    # 存储会话
    dialog = [
        role_content_json("user", current_input),
        role_content_json("assistant", reply_json),
    ]
    dog.remember(dialog)


if __name__ == "__main__":
    original_path = os.getcwd()

    # 实例化dog对象，设置是否连接
    dog = Bittle(is_dog_connected=False)

    # 获取用户输入
    audio_streamer = AudioStreamer(callback=on_message)

    # 小狗自主动作
    auto_reaction()

    # try:
    #     # 程序代码
    #     while True:
    #         time.sleep(1)
    #
    # except KeyboardInterrupt:
    #     print("键盘中断，停止运行...")
    # finally:
    #     os.chdir(original_path)  # 恢复原路径
    #     dog.close()
    #     # print("恢复原路径")
    #     exit(0)
