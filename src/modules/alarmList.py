currentAlarms = []

class Alarm:
    def __init__(self, time='', repeat=True):
        self.time = time
        self.repeat = repeat

def addCurrentAlarms(time, repeat = True):
    global currentAlarms
    #create alarm object and append to alarm list
    newAlarm = Alarm(time, repeat)
    currentAlarms.append(newAlarm)
    print('Added time to the alarm list')

def removeCurrentAlarms(alarmTime):
    global currentAlarms
    try:
        for alarm in currentAlarms:
            if alarmTime in alarm.time:
                print('Removing time % sfrom the alarm list' % (alarm.time))
                currentAlarms.remove(alarm)

    except:
        print('Alarm not found in list')

def getCurrentAlarms():
    global currentAlarms
    return currentAlarms

def resetAllAlarms():
    global currentAlarms
    currentAlarms = []