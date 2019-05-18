import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)

p = GPIO.PWM(4, 50)
theta = 0
p.start(theta)
# Right Turn: 5
# Left Turn: 10

def pwmMap(x): #maps input values of (inmin, inmax) for our understood range of angles to output values of(outmin, outmax) that are used for the ChangeDutyCycle
    outmax = float(5)
    outmin = float(10)
    inmax = float(30)
    inmin = float(-30)
    A = float(outmax-outmin)
    B = float(inmax - inmin)
    C = float(x - inmin)
    D = float(outmin)
    return float(float(A/B)*C+D)

try:
    while True:
        theta = float(input())
        p.ChangeDutyCycle(pwmMap(theta))  # turn towards 90 degree
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
