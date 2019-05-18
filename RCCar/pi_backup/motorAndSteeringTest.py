import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
motor = GPIO.PWM(13,50)
steer = GPIO.PWM(12, 50)
theta = 0
rev = 0 #theta equivalent for motor
steer.start(theta)
motor.start(rev)
# Right Turn: 5
# Left Turn: 10
motor_cal = [15,7,4] #minimum voltage is 4.4V

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

print('Calibrating...')
for x in range(len(motor_cal)):
    motor.ChangeDutyCycle(motor_cal[x])
    time.sleep(5)

try:
    while True:
        print("What angle would you like? (-30 to 30 deg)")      
       # if (input() == "stop"):
        #    break
        theta = float(input())
        steer.ChangeDutyCycle(pwmMap(theta))  # turn towards 90 degree
        print("What speed would you like? (7 to 15)")
        rev = float(input())
        while rev < 7 or rev > 15:
            print('Speed is out of range please try again:')
            rev = float(input())
        motor.ChangeDutyCycle(rev)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
