import RPi.GPIO as GPIO
import time

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    # GPIO.output(7, True)
    pwm = GPIO.PWM(11, 3)  # Flash at 3Hz
    pwm.start(50)
    pwm.stop()
    GPIO.output(11, True)
finally:
    GPIO.cleanup()
