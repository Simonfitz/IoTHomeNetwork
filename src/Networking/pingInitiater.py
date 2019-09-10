import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from Message import Message
from MessageType import MessageType
from NetworkConstants import PING_TIMEOUT
from NetworkConstants import getMyIpAddress
from Transmitter import Transmitter
from socket import timeout

class PingInitiater(Thread, LogImplementer):
    socket = None
    pingTargetName = 'BROADCAST'

    def __init__(self, targetIpAddress):
        Thread.__init__(self)
        LogImplementer.__init__(self)
        self.socket = Transmitter()
        self.socket.setTimeout(PING_TIMEOUT)
        self.pingTargetName = targetIpAddress
        self.setName('Ping-Init Thread')

    def run(self):
        initMessage = self.CreateMessage(MessageType.PING)
        self.socket.sendInitMessage(initMessage)
        loop = True
        while loop:
            try:
                response = self.socket.listen()

                if response.type == MessageType.ACK:
                    loop = False

            except timeout:
                self.logger.warn('Ping timed out, Isaac unit unresponsive.')
                loop = False

        self.logger.debug('Pinging complete')

    def CreateMessage(self, messageType = MessageType.INVALID):
        newMessage = Message(messageType, self.pingTargetName)

        return newMessage