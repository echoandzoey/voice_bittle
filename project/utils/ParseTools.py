import json
from utils.json_operation import ensure_json_wrapped_with_braces





# 定义一个函数来解析动作并添加到列表
def parse_combo_actions(actions_str):
    start_marker = "<<"
    end_marker = ">>"
    # 初始化一个空列表
    actions_list = []
    # 循环解析动作字符串中的所有动作
    while True:
        start_index = actions_str.find(start_marker)
        end_index = actions_str.find(end_marker)
        
        if start_index == -1 or end_index == -1:
            break
        
        # 提取动作
            # 提取动作
        action = actions_str[start_index + len(start_marker):end_index]
    
        actions_list.append(action)
        # 更新动作字符串，去掉已经处理的部分
        actions_str = actions_str[end_index + len(end_marker):]
        print(f"---------------解析出来了\n{action}\n---------------")

        # 解析动作字符串并添加到列表 
        

        # 输出结果
    print(f"---------------得到了待做动作列表\n{actions_list}\n---------------")

    return actions_list


def parse_action(action_data):
    try:
        # print(f"Received action_data: {action_data}")  # 添加这行来调试
        # 尝试解析 action 中的 arguments 字段
        #fixed json 处理添加到了这里
        action_data =ensure_json_wrapped_with_braces(action_data)
        action_data = json.loads(action_data)
        name = action_data['action']['name']
        arguments = action_data['action']['arguments']

        # 根据 'name' 字段的值判断动作
        if name == 'none':
            return None  # 没有动作
        else:
            return name, arguments
    except json.JSONDecodeError:
        return None  # 解析错误，视为没有动作