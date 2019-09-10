import sys
sys.path.insert(0, '../Networking')
from LogImplementer import LogImplementer
from singleton import singleton

@singleton
class GeneralLogger(LogImplementer):

    def __init__(self):
        LogImplementer.__init__(self)
