import sys
#sys.path.insert(0, '../Logging')
from LogImplementer import LogImplementer
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST
from NetworkConstants import LISTENING_PORT, TRANSMITING_PORT, MESSAGE_TOTAL_SIZE, MAX_SOCKETS
from enum import Enum

class SocketType(Enum):
    TRANSMITTER = 1
    LISTENER = 2

class SocketFactory(LogImplementer):
    socketsInUse = set()
    logger = LogImplementer().logger

    @staticmethod
    def createTransmitterSocket():
        return SocketFactory.createSocket(SocketType.TRANSMITTER)

    @staticmethod
    def createListenerSocket():
        return SocketFactory.createSocket(SocketType.LISTENER)

    @staticmethod
    def createSocket(socketType):

        if (socketType):
            if (len(SocketFactory.socketsInUse) > MAX_SOCKETS):
                SocketFactory.logger.warn('Max sockets in use, cannot acquire a new one')
                return None
            newSocket = socket(AF_INET, SOCK_DGRAM)
            portNumber = SocketFactory.findAvailablePort(socketType)
            newSocket.bind(("", portNumber))

            if (socketType == SocketType.TRANSMITTER):
                newSocket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

            return newSocket
        else:
            SocketFactory.logger.info("Invalid socket type, cannot create socket...")

    @staticmethod
    def findAvailablePort(socketType):
        if (socketType == SocketType.TRANSMITTER):
            startingPort = TRANSMITING_PORT
        else:
            startingPort = LISTENING_PORT

        currentPortNumber = startingPort
        portFound = False
        while (not portFound) and (currentPortNumber < startingPort + MAX_SOCKETS):
            if (currentPortNumber in SocketFactory.socketsInUse):
                currentPortNumber += 1
            else:
                portFound = True
                SocketFactory.socketsInUse.add(currentPortNumber)

        if portFound:
            return currentPortNumber
        else:
            SocketFactory.logger.warn('Could not acquire a port, returning 0...')
            return 0

    @staticmethod
    def closeAndRelease(socket):
        SocketFactory.socketsInUse.remove(socket.getsockname()[1])
        socket.close()