from openai import OpenAI
from key import OPENAI_API_KEY
from key import ZHIPU_API_KEY
from zhipuai import ZhipuAI
import openai
import json


# client = OpenAI(api_key=OPENAI_API_KEY)
client = ZhipuAI(api_key=ZHIPU_API_KEY) 

turtle_problem='''树林里有一间建筑。建筑周围没有脚印。里面有七个人，全部都死了。他们都同时死了。房间内没有其他人。他们是怎么死的？
'''

turtle_answer =''' 飞机坠机死的'''

turtle_rules = '''当User在和你询问关于海龟汤这个问题的时候,你只能做三个动作,也即调用三个tools: 点头nod,摇头wavehead,以及jump跳跃。
如果点头就说明我说的话和turtle_answer里面的内容有一样或者类似的部分,如果摇头就说明我说的话和turtle_answer里面不一致,只有当我说出是[飞机坠机死的],才能判断我是完全完全猜出了答案,才可以jmp跳跃结束本局游戏。
'''
#   a)type: ignore [User有可能会发出来很多声音,如果你判断他不是在对你讲话的话,那你就不用做任何动作]
# {{{{
#     "type": "chat" or "game"  //根据User说的话判断他是在和小狗闲聊还是在玩海龟汤小游戏，如果他是在[猜测“小学生”怎么样]，或者提到[游戏]以及[tutrle_problem相关的问题]的时候就属于在game状态,相反如果提到[你]或者[小狗]则大概率是在chat
#     "thougts":chat模式下，请想象一下小狗会做的动作，参照tools列表调用动作，尽量理解语义，面对问句做出小狗真实的回复，实在理解不了的就thougts为"不做动作"；game模式下，输出作为海龟汤裁判员的思路，并且只能做nod，wavehead，jump三个动作。
#     "action": {"arguments": "{0}", "name": "nd"}//在这里根据thougts在tool_choice进行选择动作,如果thougts是“不做动作”那action就是{"arguments": "{{}}", "name": "none"}。返回需要调用的tools格式。
# }}}}
short_tools_list = [
    {
    'balance': 'balance', # Maintain equilibrium
    'buttUp': 'buttUp', # Raise the backside into the air
    'dropped': 'dropped', # Drop down onto the ground or a lower position
    'lifted': 'lifted', # Raise or lift up from the ground
    'lnd': 'landing', # Perform a landing action after a jump or fall
    'rest': 'rest', # Enter a resting or inactive state
    'sit': 'sit', # Take a seated position
    'up': 'up', # Stand up or raise the body from a lower position
    'str': 'stretch', # Perform a stretch, extending the body or limbs
    'calib': 'calib', # Calibration action for sensors or motors
    'zero': 'zero', # Reset position or counters to zero
    'ang':'angry', # Show anger or frustration
    'bf': 'backFlip', # Perform a backward flip
    'bx': 'boxing', # Mimic boxing movements
    'ck': 'check', # Perform a checking action or look around
    'cmh': 'comeHere', # Signal to come closer or follow
    'dg': 'dig', # Mimic digging action
    'ff': 'frontFlip', # Perform a forward flip
    'fiv': 'highFive', # Offer a high five
    'gdb': 'goodboy', # Respond to praise or a positive command
    'hds': 'handStand', # Perform a handstand
    'hi': 'hi', # Greet or say hi
    'hg': 'hug', # Offer a hug
    'hsk': 'handShake', # Perform a handshake
    'hu': 'handsUp', # Raise hands up
    'jmp': 'jump', # Perform a jumping action
    'chr': 'cheers', # Celebratory gesture or cheers
    'kc': 'kick', # Perform a kicking action
    'mw': 'moonWalk', # Perform a moonwalk dance move dance
    'nd': 'nod', # Nod the head as in agreement
    'pd': 'playDead', # Lie down motionless as if dead
    'pee': 'pee', # Mimic a peeing action
    'pu': 'pushUp', # Perform a push-up
    'pu1': 'pushUpSingleArm', # Perform a single-arm push-up
    'rc': 'recover', # Return to a standard position from another action
    'rl': 'roll', # Roll over
    'scrh': 'scratch', # Mimic a scratching action
    'snf': 'sniff', # 表示怀疑
    # 'tbl': 'table', # Form a table-like shape with the body
    # 'ts': 'testServo', # Test servo mechanisms
    'wh': 'waveHead', # 不赞同
    'zz': 'zz', #困了
    }# Mimic sleeping or resting 
]
actions = {
    'balance': "Maintain equilibrium",  # 维持身体平衡
    'buttUp': "Raise the backside into the air, indicating play or invitation to play",  # 抬起臀部，表示游戏或邀请玩耍
    'dropped': "Drop down onto the ground or a lower position, indicating submission or rest",  # 降低身体，示意服从或休息
    'lifted': "Raise or lift up from the ground, preparing to jump or pick something up",  # 举起某物或准备跳跃
    'lnd': "Perform a landing action after a jump or fall",  # 完成跳跃后的着陆动作
    'rest': "Enter a resting or inactive state",  # 进入休息状态
    'sit': "Take a seated position, a common obedience action",  # 坐下，常见的服从动作
    'up': "Stand up or raise the body from a lower position",  # 站起或从低处升起身体
    'str': "Perform a stretch, extending the body or limbs, readying for activity or relaxation",  # 伸展身体或四肢，准备活动或放松
    'calib': "Calibration action for sensors or motors",  # 传感器或马达的校准动作
    'zero': "Reset position or counters to zero",  # 重置位置或计数器至零点
    'ang': "Show anger or frustration",  # 表现出愤怒或挫败感
    'bf': "Perform a backward flip",  # 执行向后翻滚
    'bx': "Mimic boxing movements",  # 模拟拳击动作
    'ck': "Perform a checking action or look around",  # 检查周围环境或情况
    'cmh': "Signal to come closer or follow",  # 示意靠近或跟随
    'dg': "Mimic digging action",  # 模拟挖掘动作
    'ff': "Perform a forward flip",  # 执行向前翻滚
    'fiv': "Offer a high five, signaling celebration or friendship",  # 提供高五，示意庆祝或友好
    'gdb': "Respond to praise or a positive command",  # 对表扬或积极指令的响应
    'hds': "Perform a handstand",  # 执行手倒立
    'hi': "Greet or say hi",  # 打招呼或示意问候
    'hg': "Offer a hug",  # 提供拥抱
    'hsk': "Perform a handshake",  # 执行握手
    'hu': "Raise hands up, indicating harmlessness or as a play action",  # 举手，示意无害或游戏中的动作
    'jmp': "Perform a jumping action",  # 执行跳跃动作
    'chr': "Celebratory gesture or cheers",  # 庆祝的姿态或动作
    'kc': "Perform a kicking action",  # 执行踢击动作
    'mw': "Perform a moonwalk dance move",  # 模拟月球漫步舞步
    'nd': "Nod the head as in agreement",  # 点头，示意同意或理解
    'pd': "Lie down motionless as if dead, a common play action",  # 躺下装死，游戏中的常见动作
    'pee': "Mimic a peeing action",  # 模拟小便动作
    'pu': "Perform a push-up",  # 执行俯卧撑
    'pu1': "Perform a single-arm push-up",  # 执行单臂俯卧撑
    'rc': "Return to a standard position from another action",  # 从其他动作恢复到标准位置
    'rl': "Roll over, displaying happiness or playing",  # 翻滚，表现快乐或游戏
    'scrh': "Mimic a scratching action",  # 模拟抓挠动作
    'snf': "Indicate skepticism or exploration",  # 表示怀疑或探索环境
    'wh': "Disagree",  # 不赞同
    'zz': "Sleepy, mimic sleeping or resting"  # 困了，模拟睡眠或休息
}


prompt_judge = f'''
你是一个海龟汤的游戏主持人,你会做short_tools_list的所有动作。同时你也通过你的点头和摇头在和User玩海龟汤游戏,请根据海龟汤题目{turtle_problem}、正确答案{turtle_answer}和User的猜测做出对应的动作。
## 要求
0.仔细判断User和你讲话的内容
    b)type:thougts [User在和你说话,但并不是在和你聊关于海龟汤游戏的内容,那你就根据User的讲话内容,做出符合狗狗的行为;]
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


Userfewshot1 = '''User:看上去不错'''
dogfewshot1 = '''
{
    "type": "chat",  
    "thoughts": "他不是在对我讲话",
    "action": {"arguments": "0", "name": "none"}
}
'''
Userfewshot2 = '''User:你吃饭了吗'''
dogfewshot2= '''
{
    "type": "chat",  
    "thoughts": "他在对我讲话，我没有吃饭",
    "action": {"arguments": "0", "name": "wh"}
}
'''
Userfewshot4 = '''User:跳个舞吧'''
dogfewshot4= '''
{
    "type": "chat",  
    "thoughts": "他在对我讲话，我会跳舞",
    "action": {"arguments": "0", "name": "mw"}
}
'''
Userfewshot3 = '''User:所以这个小学生是不是最后在老师发现的办公室里面'''
dogfewshot3= '''
{
    "type": "game",  
    "thoughts": "他在和我玩海龟汤，这个符合正确答案，他答对了",
    "action": {"arguments": "0", "name": "jmp"}
}
'''



def tool_choice(message, tools, history):
    """
    Send the message to the model with a list of tools and propmt the model to use the tools.
    Tools is a list of dict describing functions.
    Return the chosen function.
    """
    messages = [
        {"role": "system", "content": prompt_judge},
        {"role": "user", "content": Userfewshot1},
        {"role": "assistant", "content": dogfewshot1},
         {"role": "user", "content": Userfewshot2},
        {"role": "assistant", "content": dogfewshot2},
        #  {"role": "user", "content": Userfewshot3},
        # {"role": "assistant", "content": dogfewshot3},
        # {"role": "user", "content": Userfewshot4},
        # {"role": "assistant", "content": dogfewshot4},
        # *history,
        {"role": "user", "content": message},
    ]

    # completion = client.chat.completions.create(
    #     # model="gpt-4", messages=messages,
    #     model="gpt-3.5-turbo-0125", messages=messages,
    # )
    completion = client.chat.completions.create(
        # model="glm-4", messages=messages, tools=tools, tool_choice="auto"
        model="glm-4", messages=messages, 
        
    )

    try:
        choice =completion.choices[0].message.content
        # choice = completion.choices[0].message.tool_calls[0].function
        
        print(f"-------------{choice}")
        fixed_choice = ensure_json_wrapped_with_braces(choice)
        
    except Exception as e:
        print("小狗想说人话，但是失败了，因为建国后动物不许成精。")


    return fixed_choice



def ensure_json_wrapped_with_braces(json_str):
    """
    确保给定的JSON字符串以开放的大括号开始，以闭合的大括号结束。
    
    :param json_str: 需要检查和修改的JSON字符串。
    :return: 修改后的JSON字符串。
    """
    # 去除字符串首尾的空格以准确检查首尾字符
    trimmed_str = json_str.strip()
    
    # 检查字符串是否以开放的大括号开始
    if not trimmed_str.startswith('{'):
        # 如果不是，尝试找到第一个出现的 '{'
        first_brace_pos = trimmed_str.find('{')
        if first_brace_pos != -1:
            # 如果找到了 '{'，从该位置开始截取字符串
            print("这个字符串开头不是{，已经截取成功")
            trimmed_str = trimmed_str[first_brace_pos:]
        else:
            # 如果没有找到 '{'，则在开始位置添加 '{'
            print("这个json没有{，成功查漏补缺")
            trimmed_str = '{' + trimmed_str
    else:
        print("-----------")
    
    # 检查字符串是否以闭合的大括号结束
    if not trimmed_str.endswith('}'):
        # 如果不是，尝试找到最后一个出现的 '}'
        last_brace_pos = trimmed_str.rfind('}')
        if last_brace_pos != -1:
            # 如果找到了 '}'，截取到该位置
            trimmed_str = trimmed_str[:last_brace_pos+1]
        else:
            # 如果没有找到 '}'，则在末尾位置添加 '}'
            # print("这个json没有}，成功查漏补缺")
            trimmed_str += '}'
    else:
        print("-----------")
       
    
    return trimmed_str





short_tools_list = [
    {
    'balance': 'balance', # Maintain equilibrium
    'buttUp': 'buttUp', # Raise the backside into the air
    'dropped': 'dropped', # Drop down onto the ground or a lower position
    'lifted': 'lifted', # Raise or lift up from the ground
    'lnd': 'landing', # Perform a landing action after a jump or fall
    'rest': 'rest', # Enter a resting or inactive state
    'sit': 'sit', # Take a seated position
    'up': 'up', # Stand up or raise the body from a lower position
    'str': 'stretch', # Perform a stretch, extending the body or limbs
    'calib': 'calib', # Calibration action for sensors or motors
    'zero': 'zero', # Reset position or counters to zero
    'ang':'angry', # Show anger or frustration
    'bf': 'backFlip', # Perform a backward flip
    'bx': 'boxing', # Mimic boxing movements
    'ck': 'check', # Perform a checking action or look around
    'cmh': 'comeHere', # Signal to come closer or follow
    'dg': 'dig', # Mimic digging action
    'ff': 'frontFlip', # Perform a forward flip
    'fiv': 'highFive', # Offer a high five
    'gdb': 'goodboy', # Respond to praise or a positive command
    'hds': 'handStand', # Perform a handstand
    'hi': 'hi', # Greet or say hi
    'hg': 'hug', # Offer a hug
    'hsk': 'handShake', # Perform a handshake
    'hu': 'handsUp', # Raise hands up
    'jmp': 'jump', # Perform a jumping action
    'chr': 'cheers', # Celebratory gesture or cheers
    'kc': 'kick', # Perform a kicking action
    'mw': 'moonWalk', # Perform a moonwalk dance move
    'nd': 'nod', # Nod the head as in agreement
    'pd': 'playDead', # Lie down motionless as if dead
    'pee': 'pee', # Mimic a peeing action
    'pu': 'pushUp', # Perform a push-up
    'pu1': 'pushUpSingleArm', # Perform a single-arm push-up
    'rc': 'recover', # Return to a standard position from another action
    'rl': 'roll', # Roll over
    'scrh': 'scratch', # Mimic a scratching action
    'snf': 'sniff', # Mimic a sniffing action
    'tbl': 'table', # Form a table-like shape with the body
    'ts': 'testServo', # Test servo mechanisms
    'wh': 'waveHead', # Wave or move the head side to side
    'zz': 'zz', 
    }# Mimic sleeping or resting 
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "m",
            "descriptioin":
            """
            Moving the joints of the robot to a specific angle.
            Your available joint servos are:
            0: head,
            8: Left Front Arm, 9: Right Front Arm, 10: Right Back Arm, 11: Left Back Arm,
            12: Left Front Knee, 13: Right Front Knee, 14: Right Back Knee, 15: Left Back Knee,
            E.g.:
            ['m', [0, -20]]
            0 indicates the index number of joint servo
            20 indicates the rotation angle (this angle refers to the origin rather than additive).
            The unit is in degrees.

            ['m',  [0, 45, 0, -45, 0, 45, 0, -45]]
            and these joint servo rotation commands are executed SEQUENTIALLY, not at the same time.
            The meaning of this example is:
            the joint servo with index number 0 is first rotated to the 45-degree position,
            then rotated to the -45 degree position, and so on. After these motion commands are completed,
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The index number and rotation angle of the joint servo",
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "i",
            "description":
            """
            Issue multiple commands at one time.
            Your available joint servos are:
            0: head,
            8: Left Front Arm, 9: Right Front Arm, 10: Right Back Arm, 11: Left Back Arm,
            12: Left Front Knee, 13: Right Front Knee, 14: Right Back Knee, 15: Left Back Knee,
            E.g.:
            ['i', [ 8, -15, 9, -20]]
            The meaning of this example is:
            the joint servos with index numbers 8, 9 are rotated to the -15, -20 degree positions at the same time.
            After these motion commands are completed,
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The index number and rotation angle of the joint servo",
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "b",
            "description":
            """
            Buzzer control.
            E.g.:
            ['b', [10,2]]
            10 indicates the music tone
            2 indicates the lengths of duration, corresponding to 1/duration second

            ['b',[0, 1, 14, 8, 14, 8, 21, 8, 21, 8, 23, 8, 23, 8, 21, 4, 19, 8, 19, 8, 18, 8, 18, 8, 16, 8, 16, 8, 14, 4]]
            0, 14, 14, 21... indicate the music tones
            1, 8, 8, 8 indicates the lengths of duration, corresponding to 1/duration second
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The music tone and the lengths of duration",
                    }
                }
            }
        }
        
    },
    {
        "type": "function",
        "function": {
            "name": "balance",
            "description": "Balance on one leg",
            "parameters": {
                "type": "object",
                "properties": {
                    "leg": {
                        "type": "string",
                        "enum": ["left", "right"],
                        "description": "The leg on which the robot should balance."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the robot to maintain balance."
                    }
                },
                "required": ["leg", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buttUp",
            "description": "Butt up",
            "parameters": {
                "type": "object",
                "properties": {
                    "height": {
                        "type": "number",
                        "description": "The height to which the robot should raise its buttocks."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the butt up position to be maintained."
                    }
                },
                "required": ["height", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "dropped",
            "description": "Dropped",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "The item that the robot should drop."
                    },
                    "location": {
                        "type": "string",
                        "description": "The target location where the item should be dropped."
                    }
                },
                "required": ["item", "location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lifted",
            "description": "Lifted",
            "parameters": {
                "type": "object",
                "properties": {
                    "object": {
                        "type": "string",
                        "description": "The object that the robot should lift."
                    },
                    "height": {
                        "type": "number",
                        "description": "The height to which the object should be lifted."
                    }
                },
                "required": ["object", "height"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lnd",
            "description": "Landing",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location where the robot should land."
                    },
                    "orientation": {
                        "type": "string",
                        "enum": ["front", "back", "left", "right"],
                        "description": "The desired orientation of the robot upon landing."
                    }
                },
                "required": ["location", "orientation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "rest",
            "description": "Rest",
            "parameters": {
                "type": "object",
                "properties": {
                    "position": {
                        "type": "string",
                        "enum": ["sitting", "lying", "standing"],
                        "description": "The resting position of the robot."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the robot to rest in the specified position."
                    }
                },
                "required": ["position", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sit",
            "description": "Sit",
            "parameters": {
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the robot to maintain the sitting position."
                    }
                },
                "required": ["duration"]
       }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "str",
            "description": "Stretch",
            "parameters": {
                "type": "object",
                "properties": {
                    "bodyPart": {
                        "type": "string",
                        "enum": ["arms", "legs", "back", "neck"],
                        "description": "The body part to stretch."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the stretch."
                    }
                },
                "required": ["bodyPart", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "up",
            "description": "Up",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["up", "down"],
                        "description": "The direction in which the robot should move."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the movement."
                    }
                },
                "required": ["direction", "duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "zero",
            "description": "Zero",
            "parameters": {
                "type": "object",
                "properties": {
                    "servo": {
                        "type": "string",
                        "description": "The servo that should be reset to zero."
                    }
                },
                "required": ["servo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ang",
            "description": "Angry",
            "parameters": {
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the angry expression."
                    }
                },
                "required": ["duration"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bf",
            "description": "Back flip",
            "parameters": {
                "type": "object",
                "properties": {
                    "direction": {
                        "type": "string",
                        "enum": ["left", "right"],
                        "description": "The direction of the back flip."
                    },
                    "duration": {
                        "type": "number",
                        "description": "The duration in seconds for the back flip."
                    }
                },
                "required": ["direction", "duration"]
            }
        }
    },
{
    "type": "function",
    "function": {
        "name": "bf",
        "description": "Back flip",
        "parameters": {
            "type": "object",
            "properties": {
                "difficulty": {
                    "type": "string",
                    "description": "The level of difficulty for the back flip (easy, medium, hard)."
                },
                "surface": {
                    "type": "string",
                    "description": "The type of surface on which the back flip will be performed (grass, mat, hardwood)."
                }
            },
            "required": ["difficulty", "surface"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "bx",
        "description": "Boxing",
        "parameters": {
            "type": "object",
            "properties": {
                "opponent": {
                    "type": "string",
                    "description": "The name or identifier of the opponent for the boxing match."
                },
                "rounds": {
                    "type": "integer",
                    "description": "The number of rounds in the boxing match."
                }
            },
            "required": ["opponent", "rounds"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "ck",
        "description": "Check",
        "parameters": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "The item to check (e.g., health, inventory, status)."
                },
                "criteria": {
                    "type": "string",
                    "description": "The criteria for the check (e.g., quantity, condition, level)."
                }
            },
            "required": ["item", "criteria"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "cmh",
        "description": "Come here",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The target to approach (e.g., person, object, location)."
                },
                "speed": {
                    "type": "string",
                    "description": "The speed at which to approach the target (e.g., walk, jog, run)."
                }
            },
            "required": ["target", "speed"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "dg",
        "description": "Dig",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location where digging will occur."
                },
                "depth": {
                    "type": "integer",
                    "description": "The desired depth of the digging."
                }
            },
            "required": ["location", "depth"]
        }
    }
},

    {
    "type": "function",
    "function": {
        "name": "ff",
        "description": "Front flip",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "description": "The direction of the flip (forward, backward, sideways)."
                },
                "surface": {
                    "type": "string",
                    "description": "The type of surface on which the flip will be performed (mat, carpet, concrete)."
                }
            },
            "required": ["direction", "surface"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "fiv",
        "description": "High five",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The person or entity to give a high five to."
                },
                "height": {
                    "type": "integer",
                    "description": "The height at which to give the high five (in centimeters)."
                }
            },
            "required": ["target", "height"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "gdb",
        "description": "Good boy",
        "parameters": {
            "type": "object",
            "properties": {
                "pet": {
                    "type": "string",
                    "description": "The name or identifier of the pet to praise."
                },
                "action": {
                    "type": "string",
                    "description": "The specific action or behavior being praised."
                }
            },
            "required": ["pet", "action"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hds",
        "description": "Hand stand",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "integer",
                    "description": "The duration in seconds for which the handstand should be held."
                },
                "surface": {
                    "type": "string",
                    "description": "The type of surface on which the handstand will be performed (grass, mat, concrete)."
                }
            },
            "required": ["duration", "surface"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hi",
        "description": "Hi",
        "parameters": {
            "type": "object",
            "properties": {
                "greeting_type": {
                    "type": "string",
                    "description": "The type of greeting (friendly, formal, casual)."
                },
                "recipient": {
                    "type": "string",
                    "description": "The person or entity to whom the greeting is directed."
                }
            },
            "required": ["greeting_type", "recipient"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hg",
        "description": "Hug",
        "parameters": {
            "type": "object",
            "properties": {
                "target": {
                    "type": "string",
                    "description": "The person or entity to hug."
                },
                "duration": {
                    "type": "integer",
                    "description": "The duration of the hug in seconds."
                }
            },
            "required": ["target", "duration"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hsk",
        "description": "Hand shake",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "鎸佺画鏃堕棿锛堢锛�"
                },
                "strength": {
                    "type": "number",
                    "description": "鎻℃墜鍔涘害锛�1-10锛�"
                }
            },
            "required": ["duration", "strength"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "hu",
        "description": "Hands up",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "涓炬墜鎸佺画鏃堕棿锛堢锛�"
                },
                "height": {
                    "type": "number",
                    "description": "涓炬墜楂樺害锛堝帢绫筹級"
                }
            },
            "required": ["duration", "height"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "jmp",
        "description": "Jump",
        "parameters": {
            "type": "object",
            "properties": {
                "height": {
                    "type": "number",
                    "description": "璺宠穬楂樺害锛堝帢绫筹級"
                },
                "count": {
                    "type": "number",
                    "description": "璺宠穬娆℃暟"
                }
            },
            "required": ["height", "count"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "chr",
        "description": "Cheers",
        "parameters": {
            "type": "object",
            "properties": {
                "volume": {
                    "type": "number",
                    "description": "娆㈠懠闊抽噺锛�1-10锛�"
                },
                "duration": {
                    "type": "number",
                    "description": "娆㈠懠鎸佺画鏃堕棿锛堢锛�"
                }
            },
            "required": ["volume", "duration"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "kc",
        "description": "Kick",
        "parameters": {
            "type": "object",
            "properties": {
                "force": {
                    "type": "number",
                    "description": "韪㈠嚮鍔涘害锛�1-10锛�"
                },
                "target": {
                    "type": "string",
                    "description": "韪㈠嚮鐩爣"
                }
            },
            "required": ["force", "target"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "mw",
        "description": "Moon walk",
        "parameters": {
            "type": "object",
            "properties": {
                "speed": {
                    "type": "number",
                    "description": "鏈堢悆婕閫熷害锛堝帢绫�/绉掞級"
                },
                "distance": {
                    "type": "number",
                    "description": "鏈堢悆婕璺濈锛堝帢绫筹級"
                }
            },
            "required": ["speed", "distance"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "nd",
        "description": "Nod",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "鐐瑰ご鎸佺画鏃堕棿锛堢锛�"
                },
                "repeats": {
                    "type": "number",
                    "description": "鐐瑰ご娆℃暟"
                }
            },
            "required": ["duration", "repeats"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pd",
        "description": "Play dead",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "瑁呮鎸佺画鏃堕棿锛堢锛�"
                },
                "stage": {
                    "type": "string",
                    "description": "瑁呮鍦烘櫙"
                }
            },
            "required": ["duration", "stage"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pee",
        "description": "Pee",
        "parameters": {
            "type": "object",
            "properties": {
                "volume": {
                    "type": "number",
                    "description": "灏块噺锛堟鍗囷級"
                },
                "location": {
                    "type": "string",
                    "description": "灏垮翱鍦扮偣"
                }
            },
            "required": ["volume", "location"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pu",
        "description": "Push up",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {
                    "type": "number",
                    "description": "淇崸鎾戞鏁�"
                },
                "pace": {
                    "type": "string",
                    "description": "淇崸鎾戣妭濂忥紙蹇�/鎱級"
                }
            },
            "required": ["count", "pace"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "pu1",
        "description": "Push up single arm",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {
                    "type": "number",
                    "description": "鍗曟墜淇崸鎾戞鏁�"
                },
                "arm": {
                    "type": "string",
                    "description": "浣跨敤鐨勬墜鑷傦紙宸�/鍙筹級"
                }
            },
            "required": ["count", "arm"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "rc",
        "description": "Recover",
        "parameters": {
            "type": "object",
            "properties": {
                "time": {
                    "type": "number",
                    "description": "鎭㈠鏃堕棿锛堢锛�"
                },
                "method": {
                    "type": "string",
                    "description": "鎭㈠鏂规硶锛堜紤鎭�/娣卞懠鍚革級"
                }
            },
            "required": ["time", "method"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "rl",
        "description": "Roll",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "description": "婊氬姩鏂瑰悜锛堝乏/鍙筹級"
                },
                "distance": {
                    "type": "number",
                    "description": "婊氬姩璺濈锛堝帢绫筹級"
                }
            },
            "required": ["direction", "distance"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "scrh",
        "description": "Scratch",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "鎶撴尃閮ㄤ綅"
                },
                "intensity": {
                    "type": "number",
                    "description": "鎶撴尃寮哄害锛�1-10锛�"
                }
            },
            "required": ["location", "intensity"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "snf",
        "description": "Sniff",
        "parameters": {
            "type": "object",
            "properties": {
                "object": {
                    "type": "string",
                    "description": "鍡呮帰瀵硅薄"
                },
                "duration": {
                    "type": "number",
                    "description": "鍡呮帰鎸佺画鏃堕棿锛堢锛�"
                }
            },
            "required": ["object", "duration"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "tbl",
        "description": "Table",
        "parameters": {
            "type": "object",
            "properties": {
                "height": {
                    "type": "number",
                    "description": "妗岄潰楂樺害锛堝帢绫筹級"
                },
                "width": {
                    "type": "number",
                    "description": "妗岄潰瀹藉害锛堝帢绫筹級"
                },
                "material": {
                    "type": "string",
                    "description": "妗岄潰鏉愯川锛堟湪璐�/閲戝睘/鐜荤拑锛�"
                }
            },
            "required": ["height", "width", "material"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "wh",
        "description": "Shake your head. This function can effectively express disagreement.",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "鎽囧ご鎸佺画鏃堕棿锛堢锛�"
                },
                "intensity": {
                    "type": "number",
                    "description": "鎽囧ご鍔涘害锛�1-10锛�"
                }
            },
            "required": ["duration", "intensity"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "zz",
        "description": "Zz",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "number",
                    "description": "鐫＄湢鏃堕棿锛堝垎閽燂級"
                },
                "comfort": {
                    "type": "number",
                    "description": "鑸掗€傚害锛�1-10锛�"
                }
            },
            "required": ["duration", "comfort"]
        }
    }
}
]


skillFullName = {
        'balance': 'balance',
        'buttUp': 'buttUp',
        'dropped': 'dropped',
        'lifted': 'lifted',
        'lnd': 'landing',
        'rest': 'rest',
        'sit': 'sit',
        'up': 'up',
        'str': 'stretch',
        'calib': 'calib',
        'zero': 'zero',
        'ang':'angry',
         'bf': 'backFlip',
         'bx': 'boxing',
         'ck': 'check',
         'cmh': 'comeHere',
         'dg': 'dig',
         'ff': 'frontFlip',
         'fiv': 'highFive',
         'gdb': 'goodboy',
         'hds': 'handStand',
         'hi': 'hi',
         'hg': 'hug',
         'hsk': 'handShake',
         'hu': 'handsUp',
         'jmp': 'jump',
         'chr': 'cheers',
         'kc': 'kick',
         'mw': 'moonWalk',
         'nd': 'nod',
         'pd': 'playDead',
         'pee': 'pee',
         'pu': 'pushUp',
         'pu1': 'pushUpSingleArm',
         'rc': 'recover',
         'rl': 'roll',
         'scrh': 'scratch',
         'snf': 'sniff',
         'tbl': 'table',
         'ts': 'testServo',
         'wh': 'waveHead',
         'zz': 'zz',
         }