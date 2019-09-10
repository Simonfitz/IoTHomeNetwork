import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from socket import socket, AF_INET, SOCK_DGRAM, timeout
from LogImplementer import LogImplementer
import NetworkConstants
from Message import Message
from datetime import datetime
from SocketFactory import SocketFactory

class Listener(LogImplementer, Thread):

    isRunning = True
    messageQueue = None
    timeout = 0

    def __init__(self, messageQueue):
        LogImplementer.__init__(self)
        Thread.__init__(self)
        self.logger.debug('Created listener!')
        self.setName('List-Sock Thread')
        self.inputSocket = SocketFactory.createListenerSocket()
        self.messageQueue = messageQueue

    def run(self):
        self.listen()

    def setTimeout(self, timeout):
        self.timeout = timeout
        self.inputSocket.settimeout(self.timeout)

    def listen(self):

        while self.isRunning:

            try:
                data, sender = self.inputSocket.recvfrom(NetworkConstants.MESSAGE_TOTAL_SIZE)
                self.logger.debug(f'Packet (length {len(data)}) received from: {str(sender)}')

                messageReceived = Message()
                messageReceived.logReceipt(datetime.now(), sender)
                messageReceived.fromByteBlock(data)

                queueTimeout = 0.2
                self.messageQueue.put(messageReceived, True, queueTimeout)
            except timeout as t:
                None
            except:
                self.logger.warn('Some unknown error has occurred')
                raise

        self.logger.info('All finished. Cleaning up...')

    def __del__(self):
        SocketFactory.closeAndRelease(self.inputSocket)

    def off(self):
        self.setTimeout(0)
        self.isRunning = False

    def on(self):
        self.isRunning = True
