import datetime, time
import os
import sys
from urllib.request import urlopen
import constants
import alarmList
import audioAPI
from threading import Thread
from alarmList import Alarm

alarmState = False

def alarmCheck():
    currentAlarms = alarmList.getCurrentAlarms()
    currentTime = getTime()

    #check if there are any alarms
    if len(currentAlarms):
        for alarm in currentAlarms:
        #check current alarms for a match to current time
            if currentTime in alarm.time:
                print('The current time of %s was found to match an alarm %s' % (currentTime, alarm.time))
                #remove alarm from list if not set to repeat
                print(alarmList.getCurrentAlarms)
                if alarm.repeat == False:
                    alarmList.removeCurrentAlarms(alarm.time)
                return True
    #return flase if no alarm set or no match found
    print('no alarms matched')
    return False

def getTimeOnline():
    res = urlopen('http://just-the-time.appspot.com/')
    result = res.read().strip()
    result = result.decode('utf-8')
    print(result)
    return result

def setTime(time, date):
    #set system clock
    os.system('date --set="%s %s"' %(date, time))
    #sync up HW clock with SW clock
    os.system('hwclock --systohc')

def getTime():
    currentTime = datetime.datetime.now()
    currentHour = currentTime.hour
    currentMin = currentTime.minute
    currentSec = currentTime.second
    timeString = str(currentHour) + ':' + str(currentMin)
    return timeString

def getDate():
    currentDate = datetime.datetime.now()
    currentDay = currentDate.day
    currentMonth = currentDate.month
    currentYear = currentDate.year
    dateString = str(currentYear) + '-' + str(currentMonth) + '-' + str(currentDay)
    return dateString

def setDefaultAlarmSound(newSound):
    constants.defaultAlarmSound = newSound

def getDefaultAlarmSound():
    return constants.defaultAlarmSound

def getActiveAlarms():
    alarmTimes =[]
    currentAlarms = alarmList.getCurrentAlarms()
    for alarm in currentAlarms:
        alarmTimes.append[alarm.time]
    print(alarmTimes)
    return alarmTimes

def functionSelect(command, alarmInfo):
    switcher = {
        'set': alarmList.addCurrentAlarms,
        'remove': alarmList.removeCurrentAlarms,
        'start' : alarmBegin,
        'stop' : alarmStop
    }
    # Get the function from switcher dictionary
    func = switcher.get(command, lambda: 'Invalid Command')
    func(alarmInfo)

def alarmLoop():
    global alarmState
    while alarmState == True:
        if alarmCheck() == True:
            audioAPI.playSound(getDefaultAlarmSound())
            print("Alarm has been triggered at %s" %(getTime()))
        else:
            print("TESTING - no alarm triggered")
        time.sleep(15)
    return

def alarmBegin(doNothing):
    global alarmState
    alarmState = True
    Thread(target=alarmLoop).start()

def alarmStop(doNothing):
    global alarmState
    alarmState = False

def handlerAlarm(alarmDetails):

    alarmDetails = alarmDetails.split(' ', 1)
    alarmCommand = alarmDetails[0]
    alarmInfo = alarmDetails[1]

    #exit if inproper args given
    if len(alarmDetails) < 2:
        print('invalid arguments for alarm')
        return

    functionSelect(alarmCommand, alarmInfo)