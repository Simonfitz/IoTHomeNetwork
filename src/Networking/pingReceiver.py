import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from Message import Message
from MessageType import MessageType
from NetworkConstants import PING_TIMEOUT
from Transmitter import Transmitter
from NetworkConstants import getMyIpAddress

class PingReceiver(Thread, LogImplementer):
    socket = None
    initialMessage = None

    def __init__(self, pingMessage):
        Thread.__init__(self)
        LogImplementer.__init__(self)
        self.socket = Transmitter()
        self.socket.setTimeout(PING_TIMEOUT)
        self.initialMessage = pingMessage
        self.setName('Ping-Init Thread')

    def run(self):
        initMessage = self.createMessage(MessageType.ACK)
        self.socket.sendMessage(initMessage, self.initialMessage.senderAddress[1])

    def createMessage(self, messageType = MessageType.INVALID):
        newMessage = Message(messageType, self.initialMessage.sender)

        return newMessage