import json
from utils.json_operation import ensure_json_wrapped_with_braces


# 解析回复json中action属性的多个动作，并提取出动作列表
def parse_action_list(actions_string):
    # 将JSON字符串转换为Python字典
    actions_json = json.loads(actions_string)
    # 提取action_name，多个动作用逗号拆开，返回列表
    action_list = actions_json.get("action").split(',')
    return action_list


# def parse_action(action_data):
#     try:
#         # print(f"Received action_data: {action_data}")  # 添加这行来调试
#         # 尝试解析 action 中的 arguments 字段
#         # fixed json 处理添加到了这里
#         action_data = ensure_json_wrapped_with_braces(action_data)
#         action_data = json.loads(action_data)
#         name = action_data['action']['name']
#         arguments = action_data['action']['arguments']
#
#         # 根据 'name' 字段的值判断动作
#         if name == 'none':
#             return None  # 没有动作
#         else:
#             return name, arguments
#     except json.JSONDecodeError:
#         return None  # 解析错误，视为没有动作
