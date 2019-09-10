import sys
sys.path.append("..")
sys.path.append("../Hardware")
from time import sleep
from insTable import InsTable
import networkApi
import threading
import HardwareAPI

if __name__ == '__main__':
    hard = None

    def resolveLight(string):
        global hard
        print(f'resolving light:{string} ')
        map = dict()
        map['WIFI'] = hard.wifiLight
        map['POWER'] = hard.powerLight
        map['NETWORK'] = hard.networkLight
        return  map[string]

    def resolveFunction(light, functionString):
        map = dict()
        map['ON'] = light.on
        map['OFF'] = light.off
        map['FLASH'] = light.flash

        print(f'resolving {functionString}')
        return map[functionString]

    def initStuff():
        global hard
        networkApi.initialise() # Initialise the network API
        sleep(1)
        InsTable().printTable()
        hard = HardwareAPI.HardwareAPI()
        hard.start()

    initStuff()
    running = True

    def pullCommands():
        global hard
        global running

        while running:
            try:
                (sender, command) = networkApi.receiveIncomingCommand()
                print(f'Received command: {command} from {sender}')
                [lightId, function] = command.split(' ')

                print(f'lightId: {lightId} is NOT WIFI, function: {function} ')

                light = resolveLight(lightId)
                print('light resolved')

                if light is not None:
                    print(f'light FOUND, resolving function')

                    func = resolveFunction(light, function)
                    func()
                else:
                    print('light not found')

            except:
                None

    threading.Thread(target=pullCommands).start()

    testCommand = 'POWER FLASH'
    commandBytes = bytearray(testCommand, 'UTF-8')
    networkApi.pushIncomingCommand('TEST', commandBytes)
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
                networkApi.sendCommand(targetName, command )
            else:
                print('name not found, doing nothing')

    networkApi.shutdown()
    hard.kill()
