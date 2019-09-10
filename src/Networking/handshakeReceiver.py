import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from Message import Message
from MessageType import MessageType
from insTable import InsTable
from Transmitter import Transmitter

class HandshakeReceiver(Thread, LogImplementer):

    communicationSocket = None
    initialMessage = None
    targetPort = None
    targetIpAddress = ""
    def __init__(self, initialMessage):
        Thread.__init__(self)
        LogImplementer.__init__(self)

        self.initialMessage = initialMessage
        self.targetPort = initialMessage.senderAddress[1]
        self.communicationSocket = Transmitter()
        self.setName('Hand-Handler Thread')

    def run(self):
        self.logger.info('Handshake protocol Initiated')

        InsTable().newHandshakeInitiated(self.initialMessage)

        self.SendAck()


    def SendAck(self):
        ackMessage = self.CreateMessage(MessageType.POLO)
        self.communicationSocket.sendMessage(ackMessage, self.targetPort)

    def CreateMessage(self, messageType = MessageType.INVALID):
        newMessage = Message(messageType, self.initialMessage.sender)

        return newMessage