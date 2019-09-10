import sys
sys.path.insert(0, '../Logging')
from LogImplementer import LogImplementer
from datetime import datetime
from singleton import singleton
from NetworkConstants import getMyIpAddress, BROADCAST_TARGET_NAME, BROADCAST_ADDRESS, LOCAL_TARGET_NAME, LOCAL_ADDRESS

class InsRecord(LogImplementer):
    name = None
    ipAddress = None
    timestamp = None

    def __init__(self, name, ipAddress, timestamp):
        LogImplementer.__init__(self)
        self.name = name
        self.ipAddress = ipAddress
        self.timestamp = timestamp

@singleton
class InsTable(LogImplementer):
    table = dict()
    lastUpdate = datetime.now()

    def __init__(self):
        LogImplementer.__init__(self)

    def isEmpty(self):
        return len(self.table) == 0

    def insertRecord(self, newRecord):

        self.logger.info(f'New record: Name:{newRecord.name}, address: {newRecord.ipAddress}, time: {newRecord.timestamp}')
        if newRecord.name in self.table:
            self.logger.debug('Record already present, updating table anyway')
        self.table[newRecord.name] = newRecord
        self.updateTimestamp()

    def isNameInTable(self, name):
        return name in self.table

    def updateTimestamp(self):
        self.lastUpdate = datetime.now()

    def newHandshakeInitiated(self, message):

        # For debugging purposes it's useful to allow the local machine to recognise itself. In future this should be changed.
        if message.senderAddress[0] == getMyIpAddress():
            self.logger.debug(f'>>>>> my IP address detected, we should ignore this, but for testing we\'ll let it slide')

        self.insertRecord(InsRecord(message.sender, message.senderAddress[0], message.timeReceived))

    def printTable(self):
        tableString = '\nDEVICE NAME\t|| DEVICE IP\t|| TIMESTAMP'
        for key in self.table:
            record = self.table[key]
            tableString += f'\n{record.name}:\t|| {record.ipAddress}\t|| {record.timestamp}'
        self.logger.info(tableString)

    def getNames(self):
        return list(self.table.keys())

    def resolveName(self, name):
        if name == None:
            self.logger.warn('Empty name given, can\'t resolve...')
            raise Exception('Incorrect type')
        elif name == BROADCAST_TARGET_NAME:
            self.logger.debug('Broadcast target chosen, short circuiting with constant...')
            return BROADCAST_ADDRESS
        elif name == LOCAL_TARGET_NAME:
            self.logger.debug('Local target chosen, short circuiting with constant...')
            return LOCAL_ADDRESS
        else:
            if name in self.table:
                return self.table[name].ipAddress
            else:
                self.logger.warn(f'Name ({name}) not in table, can\'t really return anything here...')
                return None
