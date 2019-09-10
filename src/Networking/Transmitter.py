from LogImplementer import LogImplementer
from Message import Message
from NetworkConstants import LISTENING_PORT, TRANSMITING_PORT, MESSAGE_TOTAL_SIZE, BROADCAST_TARGET_NAME, BROADCAST_ADDRESS
from SocketFactory import SocketFactory
from datetime import  datetime
from insTable import InsTable


class Transmitter(LogImplementer):

    def __init__(self):
        LogImplementer.__init__(self)

        self.outputSocket = SocketFactory.createTransmitterSocket()

    def __del__(self):
        SocketFactory.closeAndRelease(self.outputSocket)

    def sendInitMessage(self, message):
        self.sendMessage(message, LISTENING_PORT)

    def sendMessage(self, message, port = LISTENING_PORT):

        bytes = message.toByteBlock()
        messageBytes = self.addPadding(bytes)

        targetIp = InsTable().resolveName(message.target)

        assert  targetIp is not None, f'target not found'

        if targetIp is not None:
            target = (targetIp, port)
            self.outputSocket.sendto(messageBytes, target)

    def addPadding(self, byteArray, expectedLength = MESSAGE_TOTAL_SIZE):
        padding = MESSAGE_TOTAL_SIZE - len(byteArray)

        if (padding > 0):
            byteArray += b'\0' * padding

        return byteArray

    def broadcastInitMessage(self, message):
        message.target = BROADCAST_TARGET_NAME
        self.sendInitMessage(message)

    def broadcastMessage(self, message):
        message.target = BROADCAST_TARGET_NAME
        self.sendMessage(message)

    def listen(self):
        data, sender = self.outputSocket.recvfrom(MESSAGE_TOTAL_SIZE)

        messageReceived = Message()
        messageReceived.logReceipt(datetime.now(), sender)
        messageReceived.fromByteBlock(data)

        return messageReceived

    def setTimeout(self, timeout):
        self.timeout = timeout
        self.outputSocket.settimeout(self.timeout)
