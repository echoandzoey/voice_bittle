from llm_interaction.interact_with_llm import get_llm_msg
from print_format import *
from project.llm_interaction.construct_prompt import *
from utils.ParseTools import parse_action_list
from utils.send_command import *

"""
    与小狗相关的自定义属性与方法
"""

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
        # 初始化机器狗的记忆、想法和心情
        self.memory = []  # 存储过去的事件或经验
        self.thoughts = "Just booted up."  # 当前的想法

        # 连接机器狗
        self.is_dog_connected = is_dog_connected
        if self.is_dog_connected:
            self.goodPorts = initBittle()

        # 初始动作
        self.action("scrh")

    """
        【小狗行为】
    """

    def remember(self, event):
        """记录一个新事件到记忆中"""
        self.memory.append(event)

    def think(self, thought):
        """更新当前的想法"""
        self.thoughts = thought

    def action(self, action_name):
        """执行动作"""
        colored_output("🐶 执行动作：" + action_name, "green")
        if self.is_dog_connected:
            sendCommand(self.goodPorts, "k" + action_name)

    # 与llm通讯并响应
    def dog_reaction(self, user_input):
        # 构建输入llm的提示词
        prompts = construct_prompts(user_input)

        # 获取llm结果(字典类型）
        reply_dict = get_llm_msg(prompts)

        # 解析llm结果: 解析出动作列表
        action_list = parse_action_list(reply_dict)

        # 执行动作
        for action in action_list:
            self.action(action)

    def close(self):
        """关闭连接"""
        if self.is_dog_connected:
            # print("关闭机器狗")
            closeBittle(self.goodPorts)

    """
        【获取小狗属性】
    """

    def get_memory(self):
        """获取当前的记忆列表"""
        return self.memory

    def get_thoughts(self):
        """获取当前的想法"""
        return self.thoughts

    """
        【输出小狗状态，管理json格式】
    """

    def describe(self):
        """描述当前的机器狗状态"""
        return f"Memory: {self.memory}\nThoughts: {self.thoughts}"

