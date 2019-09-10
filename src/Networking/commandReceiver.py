import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from Message import Message
from MessageType import MessageType
from Transmitter import Transmitter
import networkApi

class CommandReceiver(LogImplementer, Thread):

    responseSocket = Transmitter()
    targetPort = None

    def __init__(self, initialMessage):
        LogImplementer.__init__(self)
        Thread.__init__(self)
        self.targetDevice = initialMessage.sender
        self.targetPort = initialMessage.senderAddress[1]
        self.initialMessage = initialMessage

    def run(self):
        payload = self.initialMessage.payload

        response = self.createNextAck()
        self.responseSocket.sendMessage(response, self.targetPort)

        self.logger.debug(f'<<<<<Response sent, closing up for the night')
        networkApi.pushIncomingCommand(self.initialMessage.sender, payload)

    def createNextAck(self):
        message = Message(MessageType.ACK, self.targetDevice)

        return message

    def sendNextAck(self):
        message = self.createNextAck()
        self.socket.sendMessage(message, self.targetPort)
        self.counter += 1
