import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)

p = GPIO.PWM(4, 50)

pwm = 0
p.start(pwm)

# Right Turn: 5
# Left Turn: 10

try:
    while True:
        pwm = float(input())
        p.ChangeDutyCycle(pwm)  # turn towards 90 degree
        #time.sleep(1)
        #p.ChangeDutyCycle(5)  # turn towards 90 degree
        #time.sleep(1)
        #p.ChangeDutyCycle(pwm/2)  # turn towards 0 degree
        #time.sleep(1) # sleep 1 second
        #p.ChangeDutyCycle(pwm*2) # turn towards 180 degree
        #time.sleep(1) # sleep 1 second 
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
