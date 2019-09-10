import sys
sys.path.insert(0, '../Logging')
from LogImplementer import LogImplementer
from MessageType import MessageType
from NetworkConstants import BROADCAST_ADDRESS
from handshakeInitiater import HandshakeInitiater
from pingInitiater import PingInitiater
from countInitiater import CountInitiater
from commandInitiater import CommandInitiater

class InitiatorFactory(LogImplementer):

    def __init__(self):
        LogImplementer.__init__(self)

    def createInitiator(self, message, targetDevice = BROADCAST_ADDRESS):
        initiater = None

        if (message.type == MessageType.MARCO):
            initiater = HandshakeInitiater()
        elif(message.type == MessageType.PING):
            initiater = PingInitiater(targetDevice)
        elif(message.type == MessageType.COUNT):
            initiater = CountInitiater(8, targetDevice)
        elif(message.type == MessageType.COMMAND):
            initiater = CommandInitiater(targetDevice, message)
        else:
            self.logger.error('Unsupported message type given! Can\'t create a message initiater from this.')

        return initiater
