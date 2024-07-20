from llm_interaction.interact_with_memory import *
from llm_interaction.memory_robot import *
from llm_interaction.interact_with_llm import get_llm_msg
from utils.speech_processing.speech_to_text import AudioStreamer
import threading
import time
import os
import json
from dog_class import*

# def on_message(message):
    # global last_reaction_time, pause_auto_reaction

    # # 更新最后消息时间
    # last_reaction_time = time.time()

    # # 设置标志，指示auto_reaction应暂停运行
    # pause_auto_reaction = True

    # # 打印用户输入
    # user_input = print_user_input(message)
    # if user_input != "":
    #     robot_reaction(user_input)

    # # 清除标志，允许auto_reaction再次运行
    # pause_auto_reaction = False

# def robot_reaction(current_input):
#     # 构建输入llm的提示词
#     prompts = construct_prompts(current_input, robot.memory)

#     # 获取llm结果
#     reply_json = get_llm_msg(prompts)

#     # 将llm结果转换为字典，便于解析
#     reply_dict = json.loads(reply_json)
#     # 解析llm结果: 解析出动作列表
#     action_list = parse_action_list(reply_dict)

#     # 执行动作
#     for action in action_list:
#         if action != "none":
#             robot.action(action)
            
# def main():
#     agent = Agent()
#     agent.greet_master()
#     # agent.clear_memory()
#     # agent.add_memories(robot_memory_templates)
#     agent.chat()
    
#     agent.peek_memory()

def main():
    original_path = os.getcwd()
    global last_reaction_time, pause_auto_reaction
    last_reaction_time = time.time()
    pause_auto_reaction = False

    agent = Agent()
    agent.greet_master()

    # 实例化robot对象，设置是否连接
    robot = Bittle(is_dog_connected=False)

    # 获取用户输入
    # audio_streamer = AudioStreamer(callback=on_message)

    

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("键盘中断，停止运行...")
    finally:
        os.chdir(original_path)  # 恢复原路径
        robot.close()
        exit(0)