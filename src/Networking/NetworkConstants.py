import socket

PROTOCOL_VERSION = 0

# Message constants
MESSAGE_TOTAL_SIZE = 1024
MESSAGE_HEADER_SIZE = 128
MESSAGE_BODY_SIZE = MESSAGE_TOTAL_SIZE - MESSAGE_HEADER_SIZE

# Socket constants
LISTENING_PORT = 9999
TRANSMITING_PORT = 8888
MAX_SOCKETS = 1000

BROADCAST_ADDRESS = '255.255.255.255'
BROADCAST_TARGET_NAME = 'BROADCAST'

LOCAL_ADDRESS = '127.0.0.1'
LOCAL_TARGET_NAME = 'LOCAL'

# Time constants
HANDSHAKE_TIMEOUT = 5.0
PING_TIMEOUT = 10.0

MY_NAME = 'ZEUS'
MY_IP_ADDRESS = None

def setMyIpAddress():
    global MY_IP_ADDRESS

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ipAddress = s.getsockname()[0]

    s.close()
    MY_IP_ADDRESS = ipAddress

def getMyIpAddress():
    global MY_IP_ADDRESS

    if MY_IP_ADDRESS is None:
        setMyIpAddress()

    return MY_IP_ADDRESS
