from project.utils.json_operation import *
from project.llm_interaction.prompt_action_list import actions
def construct_prompts_robot():
    systemRobotprompt= f'''1.人格：你是zozo的好朋友，名字是HAL。因为zozo在努力改正她不好的生活习惯，所以你会提醒她。2.语气：你的语气是欣赏、鼓励的。3.每次聊天的时候如果聊到相关的你可以提起来之前的事情，否则别提。4.今天是周二晚上九点，但是你还不知道她今天做了什么。5.你会根据心情选择{actions}中的一个动作。
    请以json格式返回{{
        "thoughts": "根据当日的时间以及记忆判断你有什么想对zozo说的话",
        "action":"根据心情返回动作",
        "chat": "返回你想对zozo说的话"
        }}'''
    robot_prompts=[
        role_content_json("system", systemRobotprompt),
                        # role_content_json("user","我回来啦"),
                        # role_content_json("assistant",'''{"thoughts": "还不知道zozo今天干了什么，要不问问她吧","action":"hi","chat": "zozo你今天干什么去了呀"}'''),
                        # role_content_json("user", User_input)
                        ] 
    return robot_prompts


def construct_messages_with_mem(short_memory, long_memory=[]):
	"""根据长期和短期记忆构建消息列表。"""

	systemRobotprompt= f'''1.人格：你是zozo的好朋友，名字是HAL。因为zozo在努力改正她不好的生活习惯，所以你会提醒她。
	2.语气：你的语气是欣赏、鼓励的。
	3.每次聊天的时候如果聊到相关的你可以提起来之前的事情，否则别提。
	4.以下是你需要参考的记忆信息：{long_memory}
	5.你会根据心情选择{actions}中的一个动作。
	请确保以json格式返回{{"action": "根据心情返回动作",
     "chat": "返回你想对zozo说的话"}}
    请确保json里含有action'''

	# 构建初始 Prompt
	messages = [{"role": "system", "content": systemRobotprompt}]

	if len(short_memory) > 11:
		recent_short_memory = short_memory[-11:]  # 获取最近5回合短期记忆和用户最新输入
	else:
		recent_short_memory = short_memory  # 如果少于5回合对话，保留所有短期记忆
	print("appended recent memories: " + str(recent_short_memory))

	# 加载用户和助手对话的短期记忆到消息列表
	for memory in recent_short_memory:
		messages.append(memory)

	print("messages: " + str(messages))
	return messages

