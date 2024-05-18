import sys
sys.path.append('./send_command')

from project.utils.send_command.ardSerial import *

def initBittle():
    goodPorts = {}
    connectPort(goodPorts)
    t=threading.Thread(target = keepCheckingPort, args = (goodPorts,))
    t.start()
    send(goodPorts, ['G',0.1])
    return goodPorts

def closeBittle(goodPorts):
    closeAllSerial(goodPorts)

def sendCommand(goodPorts, command, data = []):
    if data:
        send(goodPorts, [command, data, 0.1])
    else:
        send(goodPorts, [command, 0.1])