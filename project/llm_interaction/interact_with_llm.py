from config.api_info import ZHIPU_API_KEY
from project.utils.json_operation import *
from zhipuai import ZhipuAI
from project.llm_interaction.turtle_prompt import prompt_judge


def tool_choice(message, history):
    """
    Send the message to the model with a list of tools and prompt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    prompts = [
        # 系统提示
        role_content_json("system", prompt_judge),

        # 对话样例
        user_fewshot_json("看上去不错"),
        dog_fewshot_json("chat",
                         "他不是在对我讲话",
                         "none"),

        user_fewshot_json("看上去不错"),
        dog_fewshot_json("chat",
                         "他在对我讲话，我没有吃饭",
                         "wh"),

        user_fewshot_json("所以这个小学生是不是最后在老师发现的办公室里面"),
        dog_fewshot_json("game",
                         "他在和我玩海龟汤，这个符合正确答案，他答对了",
                         "jmp"),

        user_fewshot_json("跳个舞吧"),
        dog_fewshot_json("chat",
                         "他在对我讲话，我会跳舞",
                         "mw"),

        # 用户输入
        role_content_json("user", message)

        # todo:历史记录
        # role_content_json("user", history)
    ]

    # client = OpenAI(api_key=OPENAI_API_KEY)
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    # 模型交互
    reply = client.chat.completions.create(
        # model="glm-4", messages=messages, tools=tools, tool_choice="auto"
        model="glm-4", messages=prompts,

    )

    try:
        # 结果解析
        choice = reply.choices[0].message.content
        # choice = completion.choices[0].message.tool_calls[0].function
        print(f"-------------{choice}")
        fixed_choice = ensure_json_wrapped_with_braces(choice)

    except Exception as e:
        fixed_choice = "none"
        print("小狗想说人话，但是失败了，因为建国后动物不许成精。")

    return fixed_choice
