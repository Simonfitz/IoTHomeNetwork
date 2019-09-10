import sys
sys.path.insert(0, '../Logging')
from generalLogger import GeneralLogger
from MessageFactory import MessageFactory
from queue import Queue
from enum import Enum
from insTable import InsTable
import NetworkManager

class NetworkState(Enum):
    UNKNOWN = -1
    UNINITIALISED = 0
    INITIALISING = 1
    STABLE = 2
    CONNECTED = 3
    SHUTTING_DOWN = 4
    SHUT_DOWN = 5

state = NetworkState.UNINITIALISED

incomingCommandQueue = Queue()

def sendCommand(targetName, commandString):
    commandMessage = MessageFactory.createCommandMessage(targetName, commandString)
    NetworkManager.NetworkManager().outgoingMessages.put(commandMessage)

def completeInitialisation(newState):
    global state
    assert state == NetworkState.INITIALISING, f'State is not INITIALISING, (is {state}), can\'t complete initialisation!'
    assert newState != NetworkState.INITIALISING, f'Cannot complete to INITIALISING state.'

    state = newState

def initialise():
    global state
    if state != NetworkState.UNINITIALISED:
        GeneralLogger().logger.warn(f'Network API already initialised, can\'t initialise now. [State={state}]')
    else:
        state = NetworkState.INITIALISING
        networkManager = NetworkManager.NetworkManager()
        networkManager.initialise()

def pushIncomingCommand(commandingDevice, commandBytes):
    global incomingCommandQueue
    command = commandBytes.decode('UTF-8')

    # GeneralLogger().logger.info(f'command from {commandingDevice}: {command}')

    incomingCommandQueue.put((commandingDevice, command))

def receiveIncomingCommand():
    global incomingCommandQueue
    return incomingCommandQueue.get_nowait()

def getConnectedDevices():
    return InsTable().getNames()

def pingDevice(target):
    pingMessage = MessageFactory.createPingMessage(target)
    NetworkManager.NetworkManager().outgoingMessages.put(pingMessage)

def shutdown():
    global state
    state = NetworkState.SHUTTING_DOWN

    netManager = NetworkManager.NetworkManager()
    netManager.turnOff()
    netManager.join()

    state = NetworkState.SHUT_DOWN
