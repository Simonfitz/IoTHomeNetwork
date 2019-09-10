# Acts as the main interface between the hardware files(button.py, light.py, etc.) and the main program.
from threading import Thread
from Light import Light
from Button import Button
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
threads = list()


class HardwareAPI(Thread):
    isRunning = True

    powerLight = Light(3, 'Power')
    wifiLight = Light(5, 'Wifi')
    networkLight = Light(7, 'Network')

    resetButton = Button(11, 'Reset')
    volumeButton = Button(13, 'Volume')
    alarmButton = Button(15, 'Alarm')
    intercomButton = Button(19, 'Intercom')

    threads.append(powerLight)
    threads.append(wifiLight)
    threads.append(networkLight)
    threads.append(resetButton)
    threads.append(volumeButton)
    threads.append(alarmButton)
    threads.append(intercomButton)

    def __init__(self):
        Thread.__init__(self)

        # Start lights
        self.powerLight.start()
        self.wifiLight.start()
        self.networkLight.start()

        # Start buttons
        self.resetButton.start()
        self.volumeButton.start()
        self.alarmButton.start()
        self.intercomButton.start()

        print('Hardware API Initialized!')

    def kill(self):
        self.isRunning = False
        self.powerLight.kill()
        self.wifiLight.kill()
        self.networkLight.kill()
        self.resetButton.kill()
        self.volumeButton.kill()
        self.alarmButton.kill()
        self.intercomButton.kill()

    def run(self):
        try:
            while self.isRunning:
                None
        finally:
            print('Hardware API - Waiting for threads to finish')
            for i, t in enumerate(threads):
                t.join()
                print('Hardware API - Thread {} Stopped'.format(i))
            GPIO.cleanup()
            print('Hardware API Finished')
