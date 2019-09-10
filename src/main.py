#! /bin/env python3
import os
import sys
import time
import configparser
import constants
import commandHandler
import NetworkConstants

sys.path.insert(0, 'modules')
from modules import alarm

def firstTimeSetup():
    print('Performing all that necessary goodness')

    if os.path.isfile(constants.defaultConfigPath):
        config = configparser.ConfigParser()
        config.read(constants.defaultConfigPath)
        NetworkConstants.MY_NAME = config.get('DEFAULT', 'device_name')
        print(NetworkConstants.MY_NAME, 'Online')
    else:
        print("ERROR: Config file not found. Exiting!")
        sys.exit()

if __name__ == '__main__':

    # testing - sample received command
    #####
    messageReceived = 'command system message HELLO WORLD ' + str(alarm.getTime())
    #####

    firstTimeSetup()

    #core loop - conntinues forever
    print('- Starting Core Loop -')
    while True:
        #if new command present in command received variable pass to command handler
        if messageReceived:
            messageReceived = messageReceived.split(' ', 1)

            if messageReceived[0] == 'command':
                commandHandler.commandHandler(messageReceived[1])
                #reset message received
                messageReceived = None

        #wait for 1 minute
        print('sleeping')
        time.sleep(2)
    print('ERROR: should not get here')
    sys.exit()
