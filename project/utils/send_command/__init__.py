import sys
from project.utils.test_time import timing

# sys.path.append('./send_command')

sys.path.append('K:\\UnityProjects2024\\voice_bittle\\project\\utils\\send_command')

from project.utils.send_command.ardSerial import *


def initBittle():
    goodPorts = {}
    connectPort(goodPorts)
    t = threading.Thread(target=keepCheckingPort, args=(goodPorts,))
    t.start()
    send(goodPorts, ['G', 0.1])
    return goodPorts


def closeBittle(goodPorts):
    closeAllSerial(goodPorts)

# @timing
def sendCommand(goodPorts, command, data=[]):
    if data:
        send(goodPorts, [command, data, 0.1])
    else:
        send(goodPorts, [command, 0.1])
