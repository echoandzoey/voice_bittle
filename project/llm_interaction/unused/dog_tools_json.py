short_tools_list = [
    {
        'balance': 'balance',  # Maintain equilibrium
        'buttUp': 'buttUp',  # Raise the backside into the air
        'dropped': 'dropped',  # Drop down onto the ground or a lower position
        'lifted': 'lifted',  # Raise or lift from the ground
        'lnd': 'landing',  # Perform a landing action after a jump or fall
        'rest': 'rest',  # Enter a resting or inactive state
        'sit': 'sit',  # Take a seated position
        'up': 'up',  # Stand up or raise the body from a lower position
        'str': 'stretch',  # Perform a stretch, extending the body or limbs
        'calib': 'calib',  # Calibration action for sensors or motors
        'zero': 'zero',  # Reset position or counters to zero
        'ang': 'angry',  # Show anger or frustration
        'bf': 'backFlip',  # Perform a backward flip
        'bx': 'boxing',  # Mimic boxing movements
        'ck': 'check',  # Perform a checking action or look around
        'cmh': 'comeHere',  # Signal to come closer or follow
        'dg': 'dig',  # Mimic digging action
        'ff': 'frontFlip',  # Perform a forward flip
        'fiv': 'highFive',  # Offer a high five
        'gdb': 'goodboy',  # Respond to praise or a positive command
        'hds': 'handStand',  # Perform a handstand
        'hi': 'hi',  # Greet or say hi
        'hg': 'hug',  # Offer a hug
        'hsk': 'handShake',  # Perform a handshake
        'hu': 'handsUp',  # Raise hands up
        'jmp': 'jump',  # Perform a jumping action
        'chr': 'cheers',  # Celebratory gesture or cheers
        'kc': 'kick',  # Perform a kicking action
        'mw': 'moonWalk',  # Perform a moonwalk dance move dance
        'nd': 'nod',  # Nod the head as in agreement
        'pd': 'playDead',  # Lie down motionless as if dead
        'pee': 'pee',  # Mimic a peeing action
        'pu': 'pushUp',  # Perform a push-up
        'pu1': 'pushUpSingleArm',  # Perform a single-arm push-up
        'rc': 'recover',  # Return to a standard position from another action
        'rl': 'roll',  # Roll over
        'scrh': 'scratch',  # Mimic a scratching action
        'snf': 'sniff',  # 表示怀疑
        # 'tbl': 'table', # Form a table-like shape with the body
        # 'ts': 'testServo', # Test servo mechanisms
        'wh': 'waveHead',  # 不赞同
        'zz': 'zz',  # 困了
    }  # Mimic sleeping or resting
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
    'ang': 'angry',
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

