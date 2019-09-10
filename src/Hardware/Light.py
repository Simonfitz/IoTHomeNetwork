# Defines the Light class and methods for interacting with lights such as on, off and flashing.

import RPi.GPIO as GPIO
import time
from threading import Thread


class Light(Thread):
    pin = ''
    state = 'off'
    previousState = 'off'
    pwm = False
    isRunning = True

    def __init__(self, gpioPin, name):
        Thread.__init__(self)

        if GPIO.getmode() == -1:
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.getmode()

        self.pin = gpioPin
        self.name = name

        GPIO.setup(self.pin, GPIO.OUT)

        self.healthCheck()

        print('Created', self.name, 'light on pin', self.pin)

    def healthCheck(self):
        print('Health Check Started on', self.name, 'light')
        GPIO.output(self.pin, True)
        time.sleep(1)
        GPIO.output(self.pin, False)
        print('Health Check Complete on', self.name, 'light')

    def on(self):
        if self.pwm is not False:
            print('self.pwm detected!')
            self.pwm.stop()
            self.pwm = False
        self.state = 'on'
        print('Light', self.name, 'is on')

    def checkState(self):
        if self.previousState is not self.state:
            if self.state == 'on':
                print(self.name, 'light turning on')
                GPIO.output(self.pin, True)
            elif self.state == 'off':
                print(self.name, 'light turning off')
                GPIO.output(self.pin, False)
            elif self.state == 'flashing':
                print(self.name, 'light flashing')
                self.flash()
            self.previousState = self.state

    def off(self):
        if self.pwm is not False:
            print('self.pwm detected!')
            self.pwm.stop()
            self.pwm = False
        self.state = 'off'
        print('Light', self.name, 'is off')

    def getState(self):
        return self.state

    def flash(self):
        self.pwm = GPIO.PWM(self.pin, 3)  # Flash at 3Hz
        self.pwm.start(50)

    def kill(self):
        self.isRunning = False

    def run(self):
        try:
            while self.isRunning:
                self.checkState()
        finally:
            print(self.name, 'light finished')
