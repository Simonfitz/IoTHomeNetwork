from enum import Enum
class MessageType(Enum):
    INVALID = -1
    MARCO = 0
    POLO = 1
    PING = 2
    STAY_ALIVE = 3
    COMMAND = 4
    ACK = 5
    COUNT = 6 # Test function for counting through a sequence