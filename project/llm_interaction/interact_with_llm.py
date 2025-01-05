from groq import Groq
import openai
import zhipuai

from project.api_info import *
from project.utils.json_operation import *
# 聊天prompt
from project.utils.print_format import colored_output
# 海龟汤prompt
# from project.llm_interaction.turtle_prompt import prompt_judge
from project.utils.test_time import timing

# client = OpenAI(api_key=OPENAI_API_KEY)
# client = ZhipuAI(api_key=ZHIPU_API_KEY)
client = Groq(api_key=GROQ_API_KEY)


@timing
def get_llm_msg(prompts):
    """
    Send the message to the model with a list of tools and prompt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """

    # 模型交互
    reply = client.chat.completions.create(
        # model="glm-4", messages=prompts,
        # model='gpt-3.5-turbo', messages=prompts,
        model="llama3-8b-8192", messages=prompts,
    )
    # 提取回复内容
    reply_content = reply.choices[0].message.content

    # 打印
    colored_output("🦴 回复内容：" + reply_content, "yellow")

    # 格式化回复内容：检查json格式，并将json字符串变为字典
    reply_json = format_json(reply_content)


    return reply_json
