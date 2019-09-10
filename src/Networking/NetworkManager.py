import sys
sys.path.append("..")
sys.path.append("../Logging")
from queue import Queue
from threading import Thread
from LogImplementer import LogImplementer
from Listener import Listener
from insTable import InsTable
from initiatorFactory import InitiatorFactory
from receiverFactory import ReceiverFactory
from singleton import singleton
from MessageFactory import MessageFactory

MAX_PENDING_MESSAGES = 10

@singleton
class NetworkManager(LogImplementer, Thread):
    isRunning = True
    incomingMessages = Queue(MAX_PENDING_MESSAGES)
    outgoingMessages = Queue(MAX_PENDING_MESSAGES)
    listener = None
    initiaterFactory = None
    receiverFactory = None
    receiverList = []
    initiaterList = []
    threadList = []

    def __init__(self):
        LogImplementer.__init__(self)
        Thread.__init__(self)
        self.listener = Listener(self.incomingMessages)

        self.createReceiverCallbacks()
        assert (self.callbackDict is not None), f'Failed to create dictionary for callback functions!'

        self.initiaterFactory = InitiatorFactory()
        self.receiverFactory = ReceiverFactory(self.callbackDict)
        self.setName('Net-Man Thread')

    def createReceiverCallbacks(self):
        callbacks = dict()
        self.callbackDict = callbacks

    def run(self):
        while self.isRunning:
            if (not self.incomingMessages.empty()):
                message = self.incomingMessages.get_nowait()
                self.processIncomingMessage(message)

            if (not self.outgoingMessages.empty()):
                message = self.outgoingMessages.get_nowait()
                self.createInitiater(message)

        self.cleanup()
        self.logger.info('All cleaned up, terminating...')

    def processIncomingMessage(self, message):
        if message:
            receiver = self.receiverFactory.createReceiver(message)

            receiver.start()
            self.receiverList.append(receiver)
        else:
            self.logger.debug('Empty message received, moving on...')

    def createInitiater(self, message):
        if message:
            self.logger.debug(f'New message to deliver [{message.type}], creating handler')

            initiator = self.initiaterFactory.createInitiator(message, message.sender)
            initiator.start()
            self.initiaterList.append(initiator)
        else:
            self.logger.debug('Empty message received, moving on...')

    def cleanup(self):
        self.logger.info('All finished, joining threads now...')
        self.listener.off()
        self.listener.join()

        self.logger.info('Listener thread joined. Continuing')

        for initiater in self.initiaterList:
            initiater.join()

        for receiver in self.receiverList:
            receiver.join()

    def turnOff(self):
        self.isRunning = False

    def getConnectedDevices(self):
        return InsTable().getNames()

    def initListener(self):
        self.listener.start()
        self.listener.setTimeout(0.05)

    def initialise(self):
        self.initListener()

        handshakeMessage = MessageFactory.createHandshakeMessage()
        self.outgoingMessages.put(handshakeMessage)

        self.start()