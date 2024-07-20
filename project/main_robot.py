from project.llm_interaction.interact_with_memory import *
from project.llm_interaction.memory_robot import *
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
