import sys
sys.path.insert(0, '../Logging')
from threading import Thread
from LogImplementer import LogImplementer
from MessageType import MessageType
from Transmitter import Transmitter
from socket import timeout

class CommandInitiater(LogImplementer, Thread):

    transmitter = None

    def __init__(self, targetDevice, initMessage):
        LogImplementer.__init__(self)
        Thread.__init__(self)
        self.targetDevice = targetDevice
        self.initMessage = initMessage

        self.transmitter = Transmitter()

    def run(self):

        isRunning = True
        self.transmitter.setTimeout(5)
        while isRunning:

            self.transmitter.sendInitMessage(self.initMessage)
            try:
                response = self.transmitter.listen()
                self.runSanityChecks(response)
                isRunning = False
            except timeout:
                self.logger.debug(f'No response received, resending message')
            except:
                raise

        self.logger.info("Command sent and response received, finishing up")


    def runSanityChecks(self, message):
        assert(message.target == self.initMessage.sender)
        assert(message.type == MessageType.ACK)
