#import relevant motor control libraries
import RPi.GPIO as GPIO
import time

# initialize the signal pin
signal_pin = 5

# initialize outputs
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.out)

# initialize the motor
motor = GPIO.PWM(signal_pin, 50)
motor.start(7.5)

# try to rotate the servo to its neutral position
try:
    while True:
        GPIO.output(7, 1)
        time.sleep(0.0015)
        GPIO.output(7, 0)
        time.sleep(2)

# stop after a keyboard interrupt
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
