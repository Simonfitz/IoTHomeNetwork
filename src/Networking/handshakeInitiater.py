import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from Message import Message
from MessageType import MessageType
from NetworkConstants import LISTENING_PORT, HANDSHAKE_TIMEOUT, getMyIpAddress
from Transmitter import Transmitter
from socket import timeout
from insTable import InsTable
import networkApi

class HandshakeInitiater(Thread, LogImplementer):
    socket = None
    partnerIpAddress = 'BROADCAST'
    def __init__(self):
        Thread.__init__(self)
        LogImplementer.__init__(self)
        self.socket = Transmitter()
        self.socket.setTimeout(HANDSHAKE_TIMEOUT)
        self.setName('Hand-Init Thread')

    def run(self):
        initMessage = self.CreateMessage(MessageType.MARCO)
        self.socket.broadcastInitMessage(initMessage)
        loop = True
        while loop:
            try:
                response = self.socket.listen()

                if response.type == MessageType.POLO:
                    InsTable().newHandshakeInitiated(response)

            except timeout as err:
                self.logger.info('Listening timed out, no other Isaac units found.')
                loop = False

        self.logger.debug('Handshake complete')
        self.finish()

    def CreateMessage(self, messageType = MessageType.INVALID):
        newMessage = Message(messageType, self.partnerIpAddress)

        return newMessage

    def finish(self):
        newState = networkApi.NetworkState.STABLE
        if (len(InsTable().getNames()) > 0):
            newState = networkApi.NetworkState.CONNECTED

        networkApi.completeInitialisation(newState)
        InsTable().printTable()