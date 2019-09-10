import logging
from datetime import datetime

from os import path, makedirs


loggers = {}

class Logger:
    global loggers

    fileHandler = None
    streamHandler = None
    logDirectory = path.expanduser('~/.isaac/logs/')
    logger = None
    formatter = logging.Formatter('%(asctime)s [%(threadName)-8.16s] [%(levelname)-3.8s]\
 [%(className)-3.32s] %(message)s')
    className = ""

    def __init__(self, level = logging.INFO, loggerName = "isaac", className = None):

        if className:
             self.className = className

        if loggers.get(loggerName):
            self.logger = loggers.get(loggerName)
        else:
            self.logger = logging.getLogger(loggerName)
            loggers[loggerName] = self.logger

            self.ensureLogDirExists()
            self.setLevel(level)

            self.initHandlers()
            self.addHandlers()



    def setLevel(self, level):
        self.logger.setLevel(level)

    def __del__(self):
        self.removeHandlersFromLogger()

    def removeHandlersFromLogger(self):
        self.logger.removeHandler(self.streamHandler)
        self.logger.removeHandler(self.fileHandler)

    def ensureLogDirExists(self):
        if not path.exists(self.logDirectory):
            makedirs(self.logDirectory)

    def getLogFileName(self):
        currentTime = datetime.now()
        currentTime = str(currentTime).split()
        time = f'{currentTime[0]}-{currentTime[1]}'
        return f'isaac_log-{time}.log'

    def addHandlers(self):
        self.logger.addHandler(self.fileHandler)
        self.logger.addHandler(self.streamHandler)

    def initHandlers(self):
        self.initFileHandler()
        self.initStreamHandler()

    def initFileHandler(self):
        logPath = f'{self.logDirectory}{self.getLogFileName()}'

        fileHandler = logging.FileHandler(logPath)
        fileHandler.setFormatter(self.formatter)
        fileHandler.setLevel(self.logger.level)
        self.fileHandler = fileHandler

    def initStreamHandler(self):
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(self.formatter)
        self.streamHandler = streamHandler


    def log(self, message, level = logging.INFO, className = ''):
        self.logger.log(level, message, className)

    def logWithFunc(self, logFunction, message, className):
        nameToUse = self.className
        if className:
            nameToUse = className

        logFunction(message, extra={'className': nameToUse})

    def debug(self, message, className=''):
        self.logWithFunc(self.logger.debug, message, className)

    def info(self, message, className = ''):
        self.logWithFunc(self.logger.info, message, className)

    def warn(self, message, className = ''):
        self.logWithFunc(self.logger.warning, message, className)

    def error(self, message, className=''):
        self.logWithFunc(self.logger.error, message, className)

    def critical(self, message, className=''):
        self.logWithFunc(self.logger.critical, message, className)
