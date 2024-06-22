# todo: 修改动作列表
# 6/15 demo测试动作
# demo_actions = {
#     # 初始，自然状态，【抓挠】
#     'scrh': "Mimic a scratching action",  # 模拟抓挠动作
#     # “小狗小狗”，【靠近：转头，跑过来，坐下】
#     'come': "Signal to come closer or follow",  # 示意靠近或跟随
#     # "你吃饭了吗"【摇头】
#     'wh': "Disagree",  # 不赞同
#     # “这有好吃的"【开心】【期待】
#     'gdb': "Respond to praise or a positive command",  # 对表扬或积极指令的响应
#     'hsk': "Perform a handshake",  # 执行握手，可爱
# }
actions = {
    # 基础动作
    'rest': "Enter a resting or inactive state",  # 进入休息状态
    'sit': "Take a seated position, a common obedience action",  # 坐下，常见的服从动作
    'up': "Stand up or raise the body from a lower position",  # 站起或从低处升起身体
    'balance': "Maintain equilibrium",  # 维持身体平衡

    # 小动作（和自己or环境）
    'scrh': "Mimic a scratching action",  # 模拟抓挠动作
    'ck': "Perform a checking action or look around",  # 检查周围环境或情况
    'snf': "Indicate skepticism or exploration",  # 表示怀疑或探索环境，往前伸头嗅一嗅
    'dg': "Mimic digging action",  # 模拟挖掘动作

    # 和人交互
    'come': "Signal to come closer or follow",  # 示意靠近或跟随
    'hi': "Greet or say hi",  # 打招呼或示意问候
    'hg': "Offer a hug",  # 提供拥抱
    'hsk': "Perform a handshake",  # 执行握手
    # 'cmh': "Signal to come closer or follow",  # 示意靠近或跟随

    # 小狗答复
    # 积极
    'nd': "Nod the head as in agreement",  # 点头，示意同意或理解
    'gdb': "Respond to praise or a positive command",  # 对表扬或积极指令的响应
    'chr': "Celebratory gesture or cheers",  # 庆祝的姿态或动作
    'fiv': "Offer a high five, signaling celebration or friendship",  # 提供高五，示意庆祝或友好
    # 消极
    'wh': "Disagree",  # 不赞同
    'ang': "Show anger or frustration",  # 表现出愤怒或挫败感

    # 小狗整活（高难度）
    'mw': "Perform a moonwalk dance move",  # 模拟月球漫步舞步
    'hds': "Perform a handstand",  # 执行手倒立
    'bf': "Perform a backward flip",  # 执行向后翻滚
    # 'ff': "Perform a forward flip",  # 执行向前翻滚

    # 【需要优化的动作，不好让人理解，或者幅度太大】
    # 动作还行，但是没有场景'kc': "Perform a kicking action",  # 执行踢击动作
    # 'buttUp': "Raise the backside into the air, indicating play or invitation to play",  # 抬起臀部，表示游戏或邀请玩耍
    # 'dropped': "Drop down onto the ground or a lower position, indicating submission or rest",  # 降低身体，示意服从或休息
    # 'lifted': "Raise or lift up from the ground, preparing to jump or pick something up",  # 举起某物或准备跳跃
    # 'lnd': "Perform a landing action after a jump or fall",  # 完成跳跃后的着陆动作
    # 'str': "Perform a stretch, extending the body or limbs, readying for activity or relaxation",  # 伸展身体或四肢，准备活动或放松
    # 'calib': "Calibration action for sensors or motors",  # 传感器或马达的校准动作
    # 'zero': "Reset position or counters to zero",  # 重置位置或计数器至零点
    # 'bx': "Mimic boxing movements",  # 模拟拳击动作
    # 前摇太长'hu': "Raise hands up, indicating harmlessness or as a play action",  # 举手，示意无害或游戏中的动作
    # 跳动太大'jmp': "Perform a jumping action",  # 执行跳跃动作
    # 'pd': "Lie down motionless as if dead, a common play action",  # 躺下装死，游戏中的常见动作
    # 'pee': "Mimic a peeing action",  # 模拟小便动作
    # 'pu': "Perform a push-up",  # 执行俯卧撑
    # 有趣'pu1': "Perform a single-arm push-up",  # 执行单臂俯卧撑
    # 'rc': "Return to a standard position from another action",  # 从其他动作恢复到标准位置
    # 'rl': "Roll over, displaying happiness or playing",  # 翻滚，表现快乐或游戏
    # 不太像'zz': "Sleepy, mimic sleeping or resting"  # 困了，模拟睡眠或休息
}
