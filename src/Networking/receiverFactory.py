import sys
sys.path.insert(0, '../Logging')
from LogImplementer import LogImplementer
from MessageType import MessageType
from handshakeReceiver import HandshakeReceiver
from pingReceiver import PingReceiver
from countReceiver import CountReceiver
from commandReceiver import CommandReceiver

class ReceiverFactory(LogImplementer):

    callbackDict = dict()

    def __init__(self, callbackDict = None):
        LogImplementer.__init__(self)

        if (callbackDict is not None):
            self.callbackDict = callbackDict

    def createReceiver(self, message):
        receiver = None

        if (message.type == MessageType.MARCO):
            receiver = HandshakeReceiver(message)

        elif(message.type == MessageType.PING):
            receiver = PingReceiver(message)
        elif (message.type == MessageType.COUNT):
            receiver = CountReceiver(message)
        elif(message.type == MessageType.COMMAND):
            receiver = CommandReceiver(message,)
        elif(message.type == MessageType.ACK):
            self.logger.warn(f'ACK received, shoudln\'t be going to listener port. Other Isaac, made a mistake, ignoring, not our problem (hoperfully)')
        else:
            self.logger.error('Unsupported message type given! Can\'t create a message receiver from this.')

        return receiver
