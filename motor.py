#import relevant motor control libraries
import RPi.GPIO as GPIO
import time

def unlock():

    # initialize outputs
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)

    motor = GPIO.PWM(7,50)
    motor.start(7.5)

    motor.ChangeDutyCycle(2.5)
    time.sleep(2)
    motor.stop()
    GPIO.cleanup()
    return

def lock():

    # initialize outputs
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)

    motor = GPIO.PWM(7,50)
    motor.start(2.5)

    motor.ChangeDutyCycle(7.5)
    time.sleep(2)
    motor.stop()
    GPIO.cleanup()
    return


