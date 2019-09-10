import sys
#sys.path.insert(0, 'modules')

##Modules##
from modules import systemAdapter
from modules import alarm
from modules import intercom

def runModuleSystem(data):
    print('system')
    systemAdapter.handlerSystem(data)

def runModuleAlarm(data):
    print('alarm')
    alarm.handlerAlarm(data)

def runModuleIntercom(data):
    print('intercom')
    intercom.handlerIntercom(data)

def moduleSelect(module, data):
    switcher = {
        'system': runModuleSystem,
        'alarm': runModuleAlarm,
        'intercom': runModuleIntercom,
    }
    # Get the function from switcher dictionary
    func = switcher.get(module, lambda: "Invalid")
    func(data)

def commandHandler(commandDetails):
    print("Received Command:" + commandDetails)
    commandDetails = commandDetails.split(' ', 1)
    #make sure command is in correct format
    if len(commandDetails) == 2:
        module = commandDetails[0]
        data = commandDetails[1]
        moduleSelect(module, data)
