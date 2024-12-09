# 智能机器狗交互系统

本项目实现了基于大语言模型(LLM)的机器狗以及机器人交互系统，支持语音对话、动作控制等功能。
- 小狗dog支持串口通信，动作输出；
- 机器人robot支持记忆功能，在console里文字交互；
- 如想单独测试记忆功能模块，可在此链接里测试：https://github.com/lng205/agent



## 功能特性

### 1. LLM集成与对话系统
- 集成大语言模型，实现自然语言理解与生成
- 支持多轮对话记忆
- 动作指令解析与执行

相关文件:
- `project/llm_interaction/interact_with_llm.py` - LLM接口实现
- `project/llm_interaction/interact_with_memory.py` - LLM记忆功能实现
- `project/llm_interaction/memory_robot.py` - 记忆字段存储
- `project/llm_interaction/prompt_design_dog.py` - 小狗提示词设计
- `project/llm_interaction/prompt_design_robot.py` - 机器人提示词设计
- `project/llm_interaction/prompt_action_list.py` - 动作指令列表

### 2. 语音交互
- 语音识别(Speech-to-Text)
- 服务器端语音处理

相关文件:
- `project/utils/speech_processing/speech_to_text.py` - 语音转文本实现

### 3. 机器狗控制
- 动作控制接口
- 硬件通信
- 状态管理

相关文件:
- `project/dog_class.py` - 机器狗类实现
- `project/utils/send_command.py` - 硬件通信接口



## 系统架构
```
project/
├── api_info.py                  # API密钥配置文件
├── requirements.txt             # 项目依赖
├── README.md                    # 项目说明文档
├── dog_class.py                # 机器狗核心类
├── main_dog.py                 # 机器狗主程序入口
├── main_robot.py               # 机器人主程序入口
│
├── llm_interaction/            # LLM交互模块
│   ├── interact_with_llm.py    # LLM接口
│   ├── interact_with_memory.py # LLM记忆功能
│   ├── memory_robot.py         # 记忆字段存储
│   ├── prompt_design_dog.py    # dog提示词设计
│   ├── prompt_design_robot.py  # robot提示词设计
│   ├── prompt_action_list.py   # 动作指令列表
│   └── unused/                 # 未使用的历史文件
│       ├── old_prompt_action_list.py
│       └── dog_tools_json.py
│
├── utils/                      # 工具模块
│   ├── speech_processing/      # 语音处理
│   │   ├── __init__.py
│   │   ├── speech_to_text.py  # 语音转文本
│   │   └── audio_config.py    # 音频配置
│   │
│   ├── ParseTools.py          # 解析工具
│   ├── json_operation.py      # JSON操作
│   ├── print_format.py        # 输出格式化
│   └── send_command.py        # 硬件通信
│
├── memory/                     # 记忆数据存储
│   └── chroma/                # 向量数据库存储
│
└── tests/                     # 测试目录
    ├── __init__.py
    ├── test_dog_class.py     # 机器狗类测试
    ├── test_llm.py           # LLM功能测试
    └── test_memory.py        # 记忆功能测试
```


## 使用方法

### 1. 环境配置

#### Linux环境

- Linux环境下可能需要安装额外的依赖库，已知的额外依赖包括：
   1. 用于音频处理的pyaudio需要依赖`portaudio`库：`sudo apt install portaudio19-dev python3-dev`。
   2. 用于给机器狗发送命令的脚本使用了`tkinter`库生成GUI界面，可能需要安装`tkinter`库：`sudo apt install python3-tk`。

pip install -r requirements.txt


### 2. 启动系统
python project/main_dog.py


### 3. 交互方式

1. 语音交互:
   - 启动后系统自动开启语音识别
   - 说出指令即可与机器狗对话

2. 文本交互:
   - 直接在控制台输入文本指令
   - 系统将解析并执行相应动作

## 主要功能模块说明

### LLM交互模块
- `interact_with_llm.py`: 实现与大语言模型的通信
- `interact_with_memory.py`: 实现LLM记忆功能
- `memory_robot.py`: 记忆字段存储
- `prompt_design_dog.py`: 定义小狗的对话模板和提示词
- `prompt_design_robot.py`: 定义机器人的对话模板和提示词
- `prompt_action_list.py`: 管理可执行动作列表


### 机器狗控制模块
- `dog_class.py`: 
  - `Bittle类`: 机器狗核心控制类
  - `action()`: 执行具体动作
  - `random_action()`: 随机动作生成
  - `create_dialog()`: 对话管理

### 语音处理模块
- `speech_to_text.py`: 实现语音识别功能
- 支持实时语音输入转换

### 工具模块
- `json_operation.py`: JSON数据处理
- `print_format.py`: 输出格式化
- `send_command.py`: 硬件通信接口

## 注意事项

1. 首次使用需配置API密钥:
   - 在`api_info.py`中配置LLM API密钥
   - 配置语音识别服务密钥

2. 硬件连接:
   - 确保机器狗已正确连接
   - 检查串口通信状态

3. 内存管理:
   - 系统会自动管理对话历史
   - 可在配置中调整记忆容量

## 开发说明

### 扩展动作
在`prompt_action_list.py`中添加新的动作指令:
random_actions = {
"sit": "坐下",
"stand": "站立",
//添加新动作...
}


### 自定义提示词
在`prompt_design_dog.py`中修改对话模板:
DOG_PROMPT = """
你是一只可爱的机器狗...
"""
# 相关API申请
- OPENAI KEY：https://openai.com/api/
- GROQ KEY（回复快速）：https://groq.com/
- ZHIPU KEY（国内大模型，无需翻墙）：https://www.zhipuai.cn/
- 讯飞语音转写：https://www.iflyrec.com/