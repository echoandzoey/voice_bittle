import openai
import subprocess
import os
import json

# 需要输入你的openai api key
openai.api_key = "sk-xxxxxx"
chat_history = []

functions = [
    {
        "name": "roll_over",
        "description": "Instructs the dog to perform a roll over action",
        "parameters": {
            "type": "object",
            "properties": {
                "speed": {
                    "type": "number",
                    "description": "The speed at which the dog performs the roll over action",
                },
            },
            "required": ["speed"],
        },
    },
    {
        "name": "bark",
        "description": "Instructs the dog to bark",
        "parameters": {
            "type": "object",
            "properties": {
                "volume": {
                    "type": "number",
                    "description": "The volume of the dog's bark",
                },
            },
            "required": ["volume"],
        },
    },
    {
        "name": "shake_head",
        "description": "Instructs the dog to shake its head",
        "parameters": {
            "type": "object",
            "properties": {
                "intensity": {
                    "type": "number",
                    "description": "The intensity of the head shake action",
                },
            },
            "required": ["intensity"],
        },
    },
    {
        "name": "shake_tail",
        "description": "Instructs the dog to shake its tail",
        "parameters": {
            "type": "object",
            "properties": {
                "intensity": {
                    "type": "number",
                    "description": "The intensity of the tail shake action",
                },
            },
            "required": ["intensity"],
        },
    }
]
def roll_over(speed):
    """
    Instructs the dog to perform a roll over action at the specified speed.
    
    :param speed: The speed at which the dog performs the roll over action.
    """
    print(f"The dog rolls over at speed {speed}.")

def bark(volume):
    """
    Instructs the dog to bark at the specified volume.
    
    :param volume: The volume of the dog's bark.
    """
    print(f"The dog barks at volume {volume}.")

def shake_head(intensity):
    """
    Instructs the dog to shake its head at the specified intensity.
    
    :param intensity: The intensity of the head shake action.
    """
    print(f"The dog shakes its head with intensity {intensity}.")

def shake_tail(intensity):
    """
    Instructs the dog to shake its tail at the specified intensity.
    
    :param intensity: The intensity of the tail shake action.
    """
    print(f"The dog shakes its tail with intensity {intensity}.")

prompt= f"""
        你是一只小狗，你不会说话，请不要给response，永远用function_call操作。
        """

while(True):
    user_input = input("User: ")
    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        # model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            *chat_history,
            {"role": "user", "content": user_input}
        ],
        temperature=0,
        functions=functions
    )
    
    # 打印回复
    # print(response)
    gpt_response = response['choices'][0]['message']['content']
    if gpt_response: 
        print("reponse:")
        print(gpt_response)
        function_call = gpt_response
    else:
        gpt_response = f"function_call: {response['choices'][0]['message']['function_call']}"
    
    # 处理function_call
    try:
        function_call = response['choices'][0]['message']['function_call']
    except KeyError:
        function_call = None 
        
    if function_call:
        function_name = function_call['name']
        # print(f"function_call: {function_call}")
        
        # 使用json.loads解析arguments字符串为字典
        arguments = json.loads(function_call['arguments'])

        if function_name == "roll_over":
            # 确保使用正确的参数调用函数
            roll_over(arguments['speed'])
        elif function_name == "bark":
            bark(arguments['volume'])
        elif function_name == "shake_head":
            shake_head(arguments['intensity'])
        elif function_name == "shake_tail":
            shake_tail(arguments['intensity'])
        else:
            print(f"No handler for function {function_name}")
        
    print("---------------------")

    # 保存对话历史
    chat_history.append({"role": "user", "content": user_input})
    chat_history.append({"role": "assistant", "content": gpt_response})
    if user_input == "exit":
        break