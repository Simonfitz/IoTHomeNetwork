from Logger import Logger
import logging

class LogImplementer:
    logger = None

    def __init__(self, logLevel = logging.DEBUG):

        myClassName = self.__class__.__name__
        self.logger = Logger(level= logLevel, className= myClassName)