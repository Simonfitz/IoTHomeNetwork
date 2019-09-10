import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from Message import Message
from MessageType import MessageType
from Transmitter import Transmitter
from struct import pack, unpack

class CountReceiver(LogImplementer, Thread):

    counter = 0
    target = 0
    currentSequenceNumber = 0
    socket = Transmitter()
    targetPort = None

    def __init__(self, initialMessage):
        LogImplementer.__init__(self)
        Thread.__init__(self)
        self.targetDevice = initialMessage.sender
        self.targetPort = initialMessage.senderAddress[1]
        self.target = unpack('>i', initialMessage.payload[4:])[0]
        self.counter = 1

    def run(self):

        self.logger.debug(f'>>>>> Received init count.')
        while self.counter < self.target:
            # Create next ack
            self.logger.debug((f'>>>> Counter: {self.counter} Sending ack'))
            self.sendNextAck()

            if self.counter < self.target:
                # listen for message
                message = self.listenForNext()

                self.logger.debug(f'>>>>> Received updated count: {unpack(">i", message.payload)[0]} Need to increment counter ({self.counter})')
                # assert
                self.runSanityChecks(message)
                self.counter += 1
                self.currentSequenceNumber = message.currentSequenceNumber

        self.logger.debug(f'>>>> Counting complete, counter: {self.counter}/{self.target}')

    def createNextAck(self):
        message = Message(MessageType.ACK, self.targetDevice)
        payload = pack('>i', self.counter)
        message.setPayload(payload)
        message.setSequenceNumbers(self.currentSequenceNumber, int(self.target / 2))

        return message

    def sendNextAck(self):
        message = self.createNextAck()
        # self.logger.info(f'sending ack to {self.targetDevice}: {self.targetPort}')
        self.socket.sendMessage(message, self.targetPort)
        self.counter += 1

    def listenForNext(self):
        try:
            return self.socket.listen()
        except:
            raise

    def runSanityChecks(self, response):
        assert len(response.payload) > 0, 'Response must have a payload'

        seqNumber = unpack(">i", response.payload)[0]
        assert (seqNumber == self.counter)
        assert (response.currentSequenceNumber == self.currentSequenceNumber + 1)
        assert (response.sender == self.targetDevice)