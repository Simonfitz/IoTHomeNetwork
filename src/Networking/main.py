from NetworkManager import NetworkManager
from time import sleep
from insTable import InsTable
from MessageFactory import MessageFactory
from networkApi import sendCommand, pingDevice, initialise, shutdown
import NetworkConstants

if __name__ == '__main__':
    global MY_NAME
    MY_NAME = 'CHRONOS'

    def SendCommandMessage(target):
        commandMessage = MessageFactory.createCommandMessage(target, 'hello world')
        NetworkManager().outgoingMessages.put(commandMessage)

    initialise() # Initialise the network API
    sleep(1)
    InsTable().printTable()

    otherIsaacs = NetworkManager().getConnectedDevices()
    if (len(otherIsaacs) > 0):
        target = otherIsaacs[0]

        pingDevice(target)
        sendCommand(target, 'KILL SELF')

    sleep(5)


    running = True

    while running:

        userInput = input('Enter command (type QUIT or EXIT to terminate):\n')
        userInput = userInput.upper()

        if userInput == 'QUIT' or userInput == 'EXIT':
            running = False
        else:
            [targetName, command] = userInput.split(' ', 1)
            # print(f'target: {targetName}, {command}'

            if InsTable().isNameInTable(targetName):
                print('Name found, sending command')
                sendCommand(targetName, command )
            else:
                print('name not found, doing nothing')

    shutdown()
