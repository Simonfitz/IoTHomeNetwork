import sys
sys.path.insert(0, '../Logging')
from LogImplementer import LogImplementer
from MessageType import MessageType
from Message import Message
from NetworkConstants import getMyIpAddress, BROADCAST_TARGET_NAME

class MessageFactory(LogImplementer):

    def __init__(self):
        LogImplementer.__init__(self)

    @staticmethod
    def createMessage(messageType, target, payload = bytearray()):
        message = Message(messageType, target)

        if (len(payload) > 0):
            message.setPayload(payload)
        return message

    @staticmethod
    def createHandshakeMessage():
        return MessageFactory.createMessage(MessageType.MARCO, BROADCAST_TARGET_NAME)

    @staticmethod
    def createPingMessage(target):
        return MessageFactory.createMessage(MessageType.PING, target)

    @staticmethod
    def createCommandMessage(target, commandString):
        commandPayload = bytearray(commandString, 'UTF-8')
        return MessageFactory.createMessage(MessageType.COMMAND, target, commandPayload)

    @staticmethod
    def createCountMessage(target, countNumber):
        return  MessageFactory.createMessage(MessageType.COUNT, target)