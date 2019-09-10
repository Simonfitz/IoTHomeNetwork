import sys
sys.path.insert(0, "../Logging")
from LogImplementer import LogImplementer
from MessageType import MessageType
from struct import pack, unpack
import NetworkConstants
# from NetworkConstants import PROTOCOL_VERSION, MESSAGE_TOTAL_SIZE, MESSAGE_HEADER_SIZE, MESSAGE_BODY_SIZE, MY_NAME
from insTable import InsTable

'''
Message format:
< ======== Start Message ======== >
/ ======== Start Header ======== \
    4   BYTES: Protocol Version
    4   BYTES: Message Type
    32  BYTES: Sender Name
    32  BYTES: Target Name
    4   BYTES: Sequence Number
    4   BYTES: Messages in sequence
    2   BYTES: Payload Length

\ ======== End Header ======== /
/ ======== Start Body ======== \

    896 BYTES: PAYLOAD

\ ======== End  Body ======== /
< ======== End Message ======== >
'''


class Message(LogImplementer):
    INT32_FORMAT = '>i'
    UINT16_FORMAT = '>H'
    PROTOCOL_BYTES = 4
    TYPE_BYTES = 4
    NAME_LENGTH = 32
    PAYLOAD_LENGTH_BYTES = 2
    SEQUENCE_NUMBER_BYTES = 4
    sender = NetworkConstants.MY_NAME
    target = ''
    info = ''
    payload = bytearray()
    payloadLength = 0
    type = MessageType(MessageType.INVALID)
    timeReceived = None
    senderAddress = None
    currentSequenceNumber = 0
    messagesInSequence = 1

    def __init__(self, type = MessageType.INVALID, target = 'BROADCAST'):
        LogImplementer.__init__(self)
        self.type = type
        self.info = "test"
        self.target = target

    def getTargetIpAddress(self):
        return InsTable().resolveName(self.target)

    def speak(self):
        self.logger.debug('Message info:\nType: ' + str(self.type) + '\nInfo: ' + self.info + \
            '\nSender: ' + self.sender + '\nTarget: ' + self.target + f'\nTimeReceived: {self.timeReceived}' + \
            '\nSenderAddress: ' + (self.senderAddress[0]) + ':' + str(self.senderAddress[1]))

    def setPayload(self, payload):
        self.payload = payload
        self.payloadLength = len(payload)

    def setSequenceNumbers(self, currentNumberInSequence, totalMessagesInSequence):
        self.currentSequenceNumber = currentNumberInSequence
        self.messagesInSequence = totalMessagesInSequence

    def getProtocolBytes(self):
        return pack(self.INT32_FORMAT, NetworkConstants.PROTOCOL_VERSION)

    def getSequenceNumberBytes(self):
        return pack(self.INT32_FORMAT, self.currentSequenceNumber)

    def getMessageInSequenceBytes(self):
        return pack(self.INT32_FORMAT, self.messagesInSequence)

    def getPayloadLengthBytes(self):
        return pack(self.UINT16_FORMAT, self.payloadLength)

    def getHeaderBytes(self):
        protocolBytes = self.getProtocolBytes()
        typeBytes = self.getTypeBytes()
        senderBytes = self.getSenderBytes()
        targetBytes = self.getTargetBytes()
        sequenceNumberBytes = self.getSequenceNumberBytes()
        totalMessageBytes = self.getMessageInSequenceBytes()
        payloadLengthBytes = self.getPayloadLengthBytes()

        headerBytes = protocolBytes + typeBytes + senderBytes + targetBytes + sequenceNumberBytes + totalMessageBytes \
                      + payloadLengthBytes
        paddingToAdd = NetworkConstants.MESSAGE_HEADER_SIZE - len(headerBytes)
        headerBytes = self.addPadding(headerBytes, paddingToAdd)

        assert  (len(headerBytes) == NetworkConstants.MESSAGE_HEADER_SIZE), 'Message header has incorrect size!'
        return headerBytes

    def getBodyBytes(self):
        paddingToAdd = NetworkConstants.MESSAGE_BODY_SIZE - len(self.payload)

        bodyBytes = self.addPadding(self.payload, paddingToAdd)

        assert  (len(bodyBytes) == NetworkConstants.MESSAGE_BODY_SIZE), 'Message body has incorrect size!'
        return bodyBytes

    def toByteBlock(self):
        headerBytes = self.getHeaderBytes()
        bodyBytes = self.getBodyBytes()
        bytes = headerBytes + bodyBytes

        assert (len(bytes) == NetworkConstants.MESSAGE_TOTAL_SIZE), 'Message has incorrect size!'
        return bytes

    def getTypeBytes(self):
        return pack(self.INT32_FORMAT, self.type.value)

    def getSenderBytes(self):
        return self.convertNameToBytes(self.sender)

    def getTargetBytes(self):
        return self.convertNameToBytes(self.target)

    def convertNameToBytes(self, name):
        stringBytes = bytearray(name, 'UTF-8')

        truncBytes = stringBytes[0:self.NAME_LENGTH]
        numberOfPaddingBytes = self.NAME_LENGTH - len(truncBytes)
        paddedBytes = self.addPadding(truncBytes, numberOfPaddingBytes)
        return paddedBytes

    def addPadding(self, byteArray, bytesToAdd):
        if (bytesToAdd > 0):
            byteArray += b'\0' * bytesToAdd

        return byteArray

    def logReceipt(self, timeReceived, senderAddress):
        self.senderAddress = senderAddress
        self.timeReceived = timeReceived

    def fromByteBlock(self, bytes):
        byteCounter = 0

        ## Parse Header
        protocolBytes = bytes[byteCounter : self.PROTOCOL_BYTES]
        byteCounter += self.PROTOCOL_BYTES

        typeBytes = bytes[byteCounter : byteCounter + self.TYPE_BYTES]
        type = unpack(self.INT32_FORMAT, typeBytes)[0]
        byteCounter += self.TYPE_BYTES

        senderBytes = bytes [byteCounter : byteCounter+self.NAME_LENGTH]
        byteCounter += self.NAME_LENGTH

        targetBytes = bytes[byteCounter : byteCounter+self.NAME_LENGTH]
        byteCounter += self.NAME_LENGTH

        sequenceNumberBytes = bytes[byteCounter : byteCounter + self.SEQUENCE_NUMBER_BYTES]
        byteCounter += self.SEQUENCE_NUMBER_BYTES

        messagesInSequenceBytes = bytes[byteCounter : byteCounter + self.SEQUENCE_NUMBER_BYTES]
        byteCounter += self.SEQUENCE_NUMBER_BYTES

        lengthBytes = bytes[byteCounter : byteCounter + self.PAYLOAD_LENGTH_BYTES]
        byteCounter  += self.PAYLOAD_LENGTH_BYTES

        self.type = MessageType(type)
        self.protocol = unpack(self.INT32_FORMAT, protocolBytes)[0]
        self.sender = senderBytes.decode('UTF-8').strip('\0')
        self.target = targetBytes.decode('UTF-8').strip('\0')
        self.currentSequenceNumber = unpack(self.INT32_FORMAT, sequenceNumberBytes)[0]
        self.messagesInSequence = unpack(self.INT32_FORMAT, messagesInSequenceBytes)[0]
        self.payloadLength = unpack(self.UINT16_FORMAT, lengthBytes)[0]

        # Skip padded header
        if (byteCounter < NetworkConstants.MESSAGE_HEADER_SIZE):
            # self.logger.debug(F'Byte Counter: {byteCounter}, skipping empty header...')
            byteCounter =  NetworkConstants.MESSAGE_HEADER_SIZE

        # Parse Payload
        self.payload = bytes[byteCounter : byteCounter + self.payloadLength]
