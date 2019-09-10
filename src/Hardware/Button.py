# Defines the Button class and methods for interacting with buttons such as onPress and onHold.

import RPi.GPIO as GPIO
from threading import Thread

class Button(Thread):
    state = False
    isRunning = True

    def __init__(self, gpioPin, name):
        Thread.__init__(self)

        if GPIO.getmode() == -1:
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.getmode()

        self.pin = gpioPin
        self.name = name

        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        print('Created', self.name, 'button on pin', self.pin)

    def onButtonPress(self):
        self.state = True

    def onButtonDepress(self):
        self.state = False

    def getState(self):
        return self.state

    def kill(self):
        self.isRunning = False

    def run(self):
        try:
            while self.isRunning:
                if GPIO.input(self.pin):
                    self.onButtonPress()
                elif not GPIO.input(self.pin):
                    self.onButtonDepress()
        finally:
            print(self.name, 'button finished')
