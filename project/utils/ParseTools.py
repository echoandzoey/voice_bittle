import json


# 解析回复json中action属性的多个动作，并提取出动作列表
def parse_action_list(reply_json):
    # 将JSON字符串转换为Python字典
    reply_dict = json.loads(reply_json)
    # 提取action_name，进行预处理，确保只有单词和逗号，没有空格
    action_names = reply_dict.get("action").replace(" ", "")
    # 多个动作用逗号拆开，返回列表
    action_list = action_names.split(',')
    return action_list
