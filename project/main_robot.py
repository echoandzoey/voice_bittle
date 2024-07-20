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

    # # ���������Ϣʱ��
    # last_reaction_time = time.time()

    # # ���ñ�־��ָʾauto_reactionӦ��ͣ����
    # pause_auto_reaction = True

    # # ��ӡ�û�����
    # user_input = print_user_input(message)
    # if user_input != "":
    #     robot_reaction(user_input)

    # # �����־������auto_reaction�ٴ�����
    # pause_auto_reaction = False

# def robot_reaction(current_input):
#     # ��������llm����ʾ��
#     prompts = construct_prompts(current_input, robot.memory)

#     # ��ȡllm���
#     reply_json = get_llm_msg(prompts)

#     # ��llm���ת��Ϊ�ֵ䣬���ڽ���
#     reply_dict = json.loads(reply_json)
#     # ����llm���: �����������б�
#     action_list = parse_action_list(reply_dict)

#     # ִ�ж���
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

    # ʵ����robot���������Ƿ�����
    robot = Bittle(is_dog_connected=False)

    # ��ȡ�û�����
    # audio_streamer = AudioStreamer(callback=on_message)

    

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("�����жϣ�ֹͣ����...")
    finally:
        os.chdir(original_path)  # �ָ�ԭ·��
        robot.close()
        exit(0)