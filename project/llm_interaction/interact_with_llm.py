import time

from api_info import *
from utils.json_operation import *
from zhipuai import ZhipuAI
from openai import OpenAI
from groq import Groq
# 海龟汤prompt
# from project.llm_interaction.turtle_prompt import prompt_judge
from utils.test_time import timing

# 聊天prompt
from llm_interaction.prompt_chat import prompt_judge
from utils.print_format import colored_output
from utils.ParseTools import parse_action_list

# client = OpenAI(api_key=OPENAI_API_KEY)
# client = ZhipuAI(api_key=ZHIPU_API_KEY)
client = Groq(api_key=GROQ_API_KEY)


def construct_prompts(user_input):
    prompts = [
        # 系统提示
        role_content_json("system", prompt_judge),
        #
        # 对话样例
        role_content_json("user","小狗小狗快过来"),
        dog_fewshot_json("主人在叫我，我要过去打个招呼", "come,hi"),
        #
        role_content_json("user","1+1等于几"),
        dog_fewshot_json("1+1=2，所以我应该做2次cnt","cnt,cnt"),

        role_content_json("user", "8-7等于几"),
        dog_fewshot_json("8-7=1，所以我应该做1次cnt", "cnt"),


        # 用户输入
        role_content_json("user", user_input)
    ]
    return prompts


@timing
def tool_choice(user_input):
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
    choice = reply.choices[0].message.content
    # choice = completion.choices[0].message.tool_calls[0].function
    colored_output("🦴 回复内容：" + choice, "yellow")

    # 检查返回的json格式，并解析出动作列表
    choice = ensure_json_wrapped_with_braces(choice)
    tool_list = parse_action_list(choice)

    return tool_list

    # try:
    #     # 选择了返回工具
    #     choice = reply.choices[0].message.content
    #     # choice = completion.choices[0].message.tool_calls[0].function
    #     print(f"-------------\n{choice}\n-------------")
    # fixed_choice = ensure_json_wrapped_with_braces(choice)

    # except Exception as e:
    #     fixed_choice = "none"
    #     print("小狗想说人话，但是失败了，因为建国后动物不许成精。")




