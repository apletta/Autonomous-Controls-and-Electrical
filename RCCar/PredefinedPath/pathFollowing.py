import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Setup motor and steering pins
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

motorPin = GPIO.PWM(13,50)
steerPin = GPIO.PWM(12,50)



