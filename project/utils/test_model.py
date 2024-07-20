#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

from project.api_info import *
from project.utils.json_operation import *
# from zhipuai import ZhipuAI
from openai import OpenAI
from groq import Groq
# 海龟汤prompt
# from project.llm_interaction.turtle_prompt import prompt_judge
from project.utils.test_time import timing

# 聊天prompt
from llm_interaction.prompt_design_dog import prompt_judge
from project.utils.print_format import colored_output

# client = OpenAI(api_key=OPENAI_API_KEY)
# client = ZhipuAI(api_key=ZHIPU_API_KEY)
client = Groq(api_key=GROQ_API_KEY)


def construct_prompts(user_input):
    prompts = [
        # 系统提示
        role_content_json("system", "用中文回答"),
        # 用户输入
        role_content_json("user", user_input)
    ]
    return prompts


@timing
def llm_interaction(user_input):
    """
    Send the message to the model with a list of tools and prompt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    # 构造prompts
    prompts = construct_prompts(user_input)

    # 模型交互
    reply = client.chat.completions.create(
        # model="glm-4", messages=prompts,
        # model='gpt-3.5-turbo', messages=prompts,
        model="llama3-8b-8192", messages=prompts,
    )
    # 选择了返回工具
    model_reply = reply.choices[0].message.content
    # choice = completion.choices[0].message.tool_calls[0].function
    colored_output("🤖 Groq:\n" + model_reply, "yellow")

    return model_reply


# 测试：在此处与模型对话
if __name__ == "__main__":
    try:
        while True:
            colored_output("❓ 请输入：", "green")
            user_input = input()
            llm_interaction(user_input)
    # 检查是否退出
    except KeyboardInterrupt:
        colored_output("👋 再见！期待下次与您的交谈。", "yellow")


