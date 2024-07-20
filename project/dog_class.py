import json
import random
from datetime import datetime

from utils.json_operation import role_content_json
from utils.print_format import *
from llm_interaction.prompt_action_list import random_actions
from utils.send_command import *

"""
    与小狗相关的自定义属性与方法
"""


def create_dialog(user_input, dog_json):
    """创建对话"""
    dialog = {
        role_content_json("user", user_input),
        dog_json
    }

    return dialog


def dog_fewshot_json(thoughts, action_name):
    """
    构造小狗回复JSON样例。

    参数:
    - thoughts: 思考内容。
    - action: 动作名称。

    """
    message = {
        "thoughts": thoughts,
        "action": action_name,
    }

    # 使用json.dumps格式化输出为字符串，并禁止ASCII转义
    content = json.dumps(message, indent=4, ensure_ascii=False)

    return role_content_json("assistant", content)


class Bittle:
    """
        创建小狗对象，初始化小狗
    """

    def __init__(self, is_dog_connected=False):
        # 初始化机器狗的记忆、想法
        self.memory = []  # 存储过去的事件或经验
        self.thoughts = "I'm a cute dog."  # 当前的想法

        # 连接机器狗
        self.is_dog_connected = is_dog_connected
        if self.is_dog_connected:
            self.goodPorts = initBittle()

        # 初始动作
        self.action("scrh")

    """
        【小狗行为】
    """

    # def remember(self, thoughts, action_list):
    #     """记录一个新事件到记忆中，控制记忆容量"""
    #     # 获取当前时间并格式化为"HH:MM"
    #     current_time = datetime.now().strftime("%H:%M")
    #     # 在memory前添加时间信息
    #     memory_with_time = f"在{current_time}的时候，我当时在想：{thoughts}，我已经做了{action_list}动作，我无需再重复了"
    #     self.memory.append(memory_with_time)        # 如果列表过长，移除第一个元素（最旧的事件）
    #     if len(self.memory) > 5:
    #         self.memory.pop(0)
    #
    # # 使用示例
    #
    # def think(self, thought):
    #     """更新当前的想法"""
    #     self.thoughts = thought

    def action(self, action_name):
        """执行动作"""
        colored_output("🐶 执行动作：" + action_name, "green")
        if self.is_dog_connected:
            sendCommand(self.goodPorts, "k" + action_name)

    def random_action(self):
        # 随机决定抽取条目的数量
        num_items_to_pick = random.randint(1, 2)

        # 获取所有的键
        keys = list(random_actions.keys())

        # 随机抽取指定数量的键
        selected_keys = random.sample(keys, num_items_to_pick)

        colored_output("┌─RANDOM", "purple")
        for key in selected_keys:
            print("│", end="")
            self.action(key)
        colored_output("└──────", "purple")

    def close(self):
        """关闭连接"""
        if self.is_dog_connected:
            # print("关闭机器狗")
            closeBittle(self.goodPorts)

    # """
    #     【获取小狗属性】
    # """

    # def get_memory(self):
    #     """获取当前的记忆列表"""
    #     return self.memory
    #
    # def get_thoughts(self):
    #     """获取当前的想法"""
    #     return self.thoughts

    """
        【输出小狗状态，管理json格式】
    """

    # def describe(self):
    #     """描述当前的机器狗状态"""
    #     return f"Memory: {self.memory}\nThoughts: {self.thoughts}"
    #
