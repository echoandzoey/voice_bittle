import random
from project.utils.ParseTools import parse_action_list
from project.llm_interaction.prompt_design_dog import construct_prompts
from project.dog_class import *
from project.llm_interaction.interact_with_llm import get_llm_msg
from project.utils.print_format import *
from project.utils.speech_processing.speech_to_text import AudioStreamer
from project.utils.speech_processing.speech_to_text_whisper import WhisperStreamer

# 全局变量记录最后消息时间、控制auto_reaction的标志
last_reaction_time = time.time()
pause_auto_reaction = False

# 输入方式1；小狗响应用户输入
def on_message(message):
    global last_reaction_time, pause_auto_reaction

    # 更新最后消息时间
    last_reaction_time = time.time()

    # 设置标志，指示auto_reaction应暂停运行
    pause_auto_reaction = True

    # 打印用户输入
    print_user_input(message)
    if message != "":
        dog_reaction(message)

    # 清除标志，允许auto_reaction再次运行
    pause_auto_reaction = False


# 输入方式2：若长时间无动作，自主动作
def auto_reaction():
    wait_time = 12  # 随机动作触发时间
    while is_random_running:
        # 检查是否应暂停运行
        if pause_auto_reaction:
            time.sleep(0.1)  # 短暂休眠，减少CPU占用
            continue

        # 检查是否超时
        if time.time() - last_reaction_time > wait_time:
            # 随机抽取动作
            dog.random_action()

            # 调用dog_reaction
            # dog_reaction("（系统提示：当前无需与人互动，继续你自己的故事吧。当然，在这时你喜欢穿插些小动作，表示你没有睡着。只回复1~2个动作）")

            time.sleep(wait_time)  # 已做动作，等待下次触发

        # 避免高频率检查
        time.sleep(1.5)


# 主程序：与llm通讯并执行动作
def dog_reaction(current_input):
    # 构建输入llm的提示词
    prompts = construct_prompts(current_input, dog.memory)

    # 获取llm结果
    reply_json = get_llm_msg(prompts)

    # 将llm结果转换为字典，便于解析
    reply_dict = json.loads(reply_json)
    # 解析llm结果: 解析出动作列表
    action_list = parse_action_list(reply_dict)

    # 执行动作
    for action in action_list:
        if action != "none":
            dog.action(action)

    # # 记忆
    # thoughts = reply_dict.get("thoughts")
    # dog.remember(thoughts, action_list)


if __name__ == "__main__":
    is_random_running = True
    original_path = os.getcwd()

    # 实例化dog对象，设置是否连接
    dog = Bittle(is_dog_connected=True)

    user_message = input("请输入1或2选择你的小狗：[1]聪明小狗 [2]胡言乱语的小狗")
    time.sleep(1)
    
    while user_message not in ["1", "2"]:
        print("请输入正确的选项")
        user_message = input("请输入1或2选择你的小狗：[1]聪明小狗 [2]胡言乱语的小狗")
    
    # main loop
    if user_message == "1":
        audio_streamer = AudioStreamer(callback=on_message)
    else:
        audio_streamer = WhisperStreamer(callback=on_message)

    # 小狗自主动作
    auto_reaction_thread = threading.Thread(target=auto_reaction)
    auto_reaction_thread.daemon = True  # 设置为守护线程，主程序退出时自动终止
    auto_reaction_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        audio_streamer.close()
        print("\n键盘中断，停止运行...")
    finally:
        os.chdir(original_path)  # 恢复原路径
        print("set is_random_running")
        is_random_running = False
        dog.close()
        print("stream close")
        # print("恢复原路径")
        exit(0)
