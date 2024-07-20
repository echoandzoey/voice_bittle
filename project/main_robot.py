from project.llm_interaction.interact_with_memory import *
from project.llm_interaction.memory_robot import *
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
