import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.OUT)

p = GPIO.PWM(6, 50)
pwm = 0
p.start(pwm)
# Right Turn: 5
# Left Turn: 10

def pwmMap(x): #maps input values of (inmin, inmax) for our understood range of angles to output values of(outmin, outmax) that are used for the ChangeDutyCycle
    outmax = 15
    outmin = 10
    inmax = 30
    inmin = -30
    return int((x-inmin)*((outmax-outmin)/(inmax-inmin))+outmin)

try:
    while True:
        pwm = float(input())
        p.ChangeDutyCycle(pwmMap(pwm))  # turn towards 90 degree
       # time.sleep(0.5)
       # p.ChangeDutyCycle(7.5)  # turn towards 90 degree
       # time.sleep(0.5)
       # p.ChangeDutyCycle(10)  # turn towards 0 degree
       # time.sleep(0.5) # sleep 1 second
       # p.ChangeDutyCycle(12.5) # turn towards 180 degree
       # time.sleep(0.5) # sleep 1 second 
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
