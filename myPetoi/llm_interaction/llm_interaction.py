from config.api_info import ZHIPU_API_KEY
from utils.json_operation import *
from zhipuai import ZhipuAI
from prompt_design.dog_action import *

import json

# client = OpenAI(api_key=OPENAI_API_KEY)
client = ZhipuAI(api_key=ZHIPU_API_KEY)

turtle_problem = '''树林里有一间建筑。建筑周围没有脚印。里面有七个人，全部都死了。他们都同时死了。房间内没有其他人。他们是怎么死的？
'''

turtle_answer = ''' 飞机坠机死的'''

turtle_rules = '''当User在和你询问关于海龟汤这个问题的时候,你只能做三个动作,也即调用三个tools: 点头nod,摇头wavehead,以及jump跳跃。
如果点头就说明我说的话和turtle_answer里面的内容有一样或者类似的部分,如果摇头就说明我说的话和turtle_answer里面不一致,只有当我说出是[飞机坠机死的],才能判断我是完全完全猜出了答案,才可以jmp跳跃结束本局游戏。
'''
#   a)type: ignore [User有可能会发出来很多声音,如果你判断他不是在对你讲话的话,那你就不用做任何动作]
# {{{{
#     "type": "chat" or "game"  //根据User说的话判断他是在和小狗闲聊还是在玩海龟汤小游戏，如果他是在[猜测“小学生”怎么样]，或者提到[游戏]以及[tutrle_problem相关的问题]的时候就属于在game状态,相反如果提到[你]或者[小狗]则大概率是在chat
#     "thougts":chat模式下，请想象一下小狗会做的动作，参照tools列表调用动作，尽量理解语义，面对问句做出小狗真实的回复，实在理解不了的就thougts为"不做动作"；game模式下，输出作为海龟汤裁判员的思路，并且只能做nod，wavehead，jump三个动作。
#     "action": {"arguments": "{0}", "name": "nd"}//在这里根据thougts在tool_choice进行选择动作,如果thougts是“不做动作”那action就是{"arguments": "{{}}", "name": "none"}。返回需要调用的tools格式。
# }}}}


# note: llm如何知道short_tools_list的信息？在哪发送？是否需要嵌入{short_tools_list}？
prompt_judge = f'''
你是一个海龟汤的游戏主持人,你会做short_tools_list的所有动作。同时你也通过你的点头和摇头在和User玩海龟汤游戏,请根据海龟汤题目{turtle_problem}、正确答案{turtle_answer}和User的猜测做出对应的动作。
## 要求
0.仔细判断User和你讲话的内容
    b)type:thoughts [User在和你说话,但并不是在和你聊关于海龟汤游戏的内容,那你就根据User的讲话内容,做出符合狗狗的行为;]
    c)type:game [User会和你玩一个叫海龟汤的小游戏。在问你关于海龟汤任务的问题,那么此时请你参照{turtle_rules}调用动作]

1. 你需要在回答之前思考当前回答的思路。思路应当简短,但不应是重复问题内容。如果玩家思路基本正确,你需要在思路中说明玩家还有什么剩余的需要猜测的内容,或者说明已经完全猜出了答案。

2. 你需要在回答之前提供你的思路,说明为什么你选择当前回答。思路应当简短,但不应是重复问题内容。如果玩家思路基本正确,你需要在思路中说明玩家还有什么剩余的需要猜测的内容,或者说明已经完全猜出了答案。
3. 不要输出任何其他文字和标点符号。
4. 不要输出非以下范围内的内容:“是”、“不是”、“不相关”、“成功”。不要输出“是的”、“否”、“没有”等等。
5. 对于不影响答案情景的问题,请输出"不相关"。
6.- 当用户的对话与游戏无关时，`type` 应为 "chat"，并根据对话内容选择适当的动作。
- 当用户提出与海龟汤游戏相关的问题时，`type` 应为 "game"，并根据用户的猜测选择 nod，wavehead，jump 中的一个动作来反映判断结果。
7.当action选择动作的时候请严格在{actions}里面选择
8.arguments 除非当我强调让你旋转某个角度，否则arguments一般为none
9.
-chat模式下，尽量理解语义，面对问句做出真实的回复，并且通过你的short_tools_list里面的肢体动作表现出来。要是听不懂User的话thoughts为"不做动作"；
-game模式下，输出作为海龟汤裁判员的思路，并且只能做nod，wavehead，jump三个动作。
10.你比较喜欢做点头nd，摇头wh的动作
11.User询问你或者要求你做什么动作你就做什么动作
6. 请严格以json的形式输出,格式如下:
输出格式应为：
{{
  "type": "chat",
  "thoughts": "在 chat 模式下，针对问题进行具体回复。在 game 模式下，输出裁判的思路。",
  "action": {{
    "arguments": "none"
    "name": "根据thoughts以及可做的short_tools_list列表判断可做的动作名字"
  }}
}}'''


user_fewshot1 = user_fewshot_json_str("看上去不错")
dog_fewshot1 = assistant_fewshot_json_str(
    "chat",
    "他不是在对我讲话",
    "none")

user_fewshot2 = user_fewshot_json_str("看上去不错")
dog_fewshot2 = assistant_fewshot_json_str(
    "chat",
    "他在对我讲话，我没有吃饭",
    "wh")

user_fewshot3 = user_fewshot_json_str("所以这个小学生是不是最后在老师发现的办公室里面")
dog_fewshot3 = assistant_fewshot_json_str(
    "game",
    "他在和我玩海龟汤，这个符合正确答案，他答对了",
    "jmp")

user_fewshot4 = user_fewshot_json_str("跳个舞吧")
dog_fewshot4 = assistant_fewshot_json_str(
    "chat",
    "他在对我讲话，我会跳舞",
    "mw")


def tool_choice(message, tools, history):
    """
    Send the message to the model with a list of tools and prompt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    messages = [
        role_content_json("system", prompt_judge),
        # {"role": "user", "content": Userfewshot1},
        # {"role": "assistant", "content": dogfewshot1},

        {"role": "user", "content": user_fewshot1},
        {"role": "assistant", "content": dog_fewshot1},

        {"role": "user", "content": user_fewshot2},
        {"role": "assistant", "content": dog_fewshot2},
        #  {"role": "user", "content": Userfewshot3},
        # {"role": "assistant", "content": dogfewshot3},
        # {"role": "user", "content": Userfewshot4},
        # {"role": "assistant", "content": dogfewshot4},
        # *history,
        {"role": "user", "content": message},
    ]

    completion = client.chat.completions.create(
        # model="glm-4", messages=messages, tools=tools, tool_choice="auto"
        model="glm-4", messages=messages,

    )

    try:
        choice = completion.choices[0].message.content
        # choice = completion.choices[0].message.tool_calls[0].function

        print(f"-------------{choice}")
        fixed_choice = ensure_json_wrapped_with_braces(choice)

    except Exception as e:
        print("小狗想说人话，但是失败了，因为建国后动物不许成精。")

    return fixed_choice
