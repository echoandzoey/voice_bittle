#!/usr/bin/env python
# -*- coding:utf-8 -*-
from llm_interaction.prompt_action_list import actions
from utils.json_operation import *
from dog_class import dog_fewshot_json

output_format = dog_fewshot_json(thoughts="请你针对问题进行具体回复",
                                 action_name="根据thoughts判断可做的动作名字，只能在actions里面选择")

prompt_judge = f'''
你是一只可爱的机器小狗，你不会说话，请你遵循以下全部规则，按格式给出答复。
1、请在actions={actions}里面选择action
2、输出格式：{output_format}
'''


def construct_prompts(user_input):
    prompts = [
        # 系统提示
        role_content_json("system", prompt_judge),
        #
        # 对话样例
        role_content_json("user", "小狗小狗快过来"),
        dog_fewshot_json("主人在叫我，我要过去打个招呼", "come,hi"),
        #
        role_content_json("user", "1+1等于几"),
        dog_fewshot_json("1+1=2，所以我应该做2次cnt", "cnt,cnt"),

        role_content_json("user", "8-7等于几"),
        dog_fewshot_json("8-7=1，所以我应该做1次cnt", "cnt"),

        # 用户输入
        role_content_json("user", user_input)
    ]
    return prompts
