import time

from api_info import *
from utils.json_operation import *
from zhipuai import ZhipuAI
from openai import OpenAI
from groq import Groq
# 海龟汤prompt
# from project.llm_interaction.turtle_prompt import prompt_judge

# 聊天prompt
from llm_interaction.prompt_chat import prompt_judge

# client = OpenAI(api_key=OPENAI_API_KEY)
# client = ZhipuAI(api_key=ZHIPU_API_KEY)
client = Groq(api_key=GROQ_API_KEY)

def construct_prompts(user_input):
    prompts = [
        # 系统提示
        role_content_json("system", prompt_judge),

        # 对话样例
        # user_fewshot_json("看上去不错"),
        # dog_fewshot_json("chat",
        #                  "他不是在对我讲话",
        #                  "none"),

        # user_fewshot_json("看上去不错"),
        # dog_fewshot_json("chat",
        #                  "他在对我讲话，我没有吃饭",
        #                  "wh"),

        # user_fewshot_json("所以这个小学生是不是最后在老师发现的办公室里面"),
        # dog_fewshot_json("game",
        #                  "他在和我玩海龟汤，这个符合正确答案，他答对了",
        #                  "jmp"),

        # user_fewshot_json("跳个舞吧"),
        # dog_fewshot_json("chat",
        #                  "他在对我讲话，我会跳舞",
        #                  "mw"),

        # 用户输入
        role_content_json("user", user_input)

        # todo:历史记录
        # role_content_json("user", history)
    ]
    return prompts


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

    try:
        # 选择了返回工具
        choice = reply.choices[0].message.content
        # choice = completion.choices[0].message.tool_calls[0].function
        print(f"-------------\n{choice}\n-------------")
        fixed_choice = ensure_json_wrapped_with_braces(choice)
   
        

    except Exception as e:
        fixed_choice = "none"
        print("小狗想说人话，但是失败了，因为建国后动物不许成精。")

    return fixed_choice
