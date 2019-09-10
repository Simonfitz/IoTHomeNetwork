import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from Message import Message
from MessageType import MessageType
from Transmitter import Transmitter
from struct import pack, unpack

class CountInitiater(LogImplementer, Thread):

    counter = 0
    target = 0
    currentSequenceNumber = 0
    socket = Transmitter()
    targetDevice = None
    targetPort = None

    def __init__(self, n = 8, targetDevice = 'BROADCAST'):
        LogImplementer.__init__(self)
        Thread.__init__(self)
        self.target = n
        self.targetDevice = targetDevice

    def run(self):

        self.sendInitMessage()

        self.listenForInitAck()

        while self.counter < self.target:
            # Create next message
            self.sendNextMessage()

            # listen for message
            message = self.listenForAck()

            # assert
            self.runSanityChecks(message)
            self.counter += 2
        self.logger.debug(f'>>>> Counting complete, counter: {self.counter}/{self.target}')

    def createNextMessage(self):
        message = Message(MessageType.COUNT, self.targetDevice)
        payload = self.packInt(self.counter)
        message.setPayload(payload)
        message.setSequenceNumbers(self.currentSequenceNumber, int(self.target / 2))

        return message

    def packInt(self, n):
        return pack('>i', n)

    def sendInitMessage(self):
        message = self.createNextMessage()
        newPayload = message.payload + self.packInt(self.target)
        message.setPayload(newPayload)
        self.socket.sendInitMessage(message)

    def listenForInitAck(self):
        responseMessage = self.socket.listen()
        self.runSanityChecks(responseMessage)
        self.targetPort = responseMessage.senderAddress[1]
        self.counter += 2

    def sendNextMessage(self):
        self.currentSequenceNumber += 1
        message = self.createNextMessage()
        self.socket.sendMessage(message, self.targetPort)

    def listenForAck(self):
        try:
            return self.socket.listen()
        except:
            raise

    def runSanityChecks(self, response):
        assert len(response.payload) > 0, 'Response must have a payload'

        seqNumber = unpack(">i", response.payload)[0]
        assert (seqNumber == self.counter + 1)
        assert (response.currentSequenceNumber == self.currentSequenceNumber)
        assert (response.sender == self.targetDevice), F'{response.sender} is not the target ({self.target})'