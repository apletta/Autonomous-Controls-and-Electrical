import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
motorPin = GPIO.PWM(13,50)
steerPin = GPIO.PWM(12, 50)
theta = 0
rev = 0 #theta equivalent for motor
steerPin.start(theta)
motorPin.start(rev)
# Right Turn: 5
# Left Turn: 10
motor_cal = [15,7,4] #minimum voltage is 4.4V
#userInput = ''
def steerMap(x): #maps input values of (inmin, inmax) for our understood range of angles to output values of(outmin, outmax) that are used for the ChangeDutyCycle
    outmax = float(5)
    outmin = float(10)
    inmax = float(30)
    inmin = float(-30)
    A = float(outmax-outmin)
    B = float(inmax - inmin)
    C = float(x - inmin)
    D = float(outmin)
    return float(float(A/B)*C+D)

def motorMap(x):
    outmax = float(10)
    outmin = float(7)
    inmax = float(100)
    inmin = float(0)
    A = float(outmax-outmin)
    B = float(inmax-inmin)
    C = float(x - inmin)
    D = float(outmin)
    return float(float(A/B)*C+D)

def check_float_test(val):
   # while True:
    try:
        float(val)
        return float(val)
       # break
    except ValueError:
        print("Not a float")

def printList(someList):
    for i in range(0,len(someList)):
        if i>0:
            check_float_test(someList[i])
            print(someList[i])

def checkList(someInput):
    lst = someInput.split(" ")
    print (lst)
    if lst[0] == 'm':
        print("Running motor at: " + lst[1])
        motor(lst[1])
    elif lst[0] == 's':
        print("Turning wheels to angle: " + lst[1])
        steer(lst[1])
    else:
        print("Not an acceptable command")

def steer(theta):
    theta = check_float_test(theta)
    if theta>=-30 and theta <=30:
        steerPin.ChangeDutyCycle(steerMap(theta))
    else:
        print("That angle isn't in range")
    
def motor(rev):
    rev = check_float_test(rev)
    if rev>0 and rev<=1000:
        motorPin.ChangeDutyCycle(motorMap(rev))
    elif rev == 0:
        motorPin.ChangeDutyCycle(5)
    else:
        print("That speed isn't in range")


print('Calibrating...')
for x in range(len(motor_cal)):
    motorPin.ChangeDutyCycle(motor_cal[x])
    time.sleep(3)

print('Finished Calibration')
#steer.ChangeDutyCycle(steerMap(-3))
motorPin.ChangeDutyCycle(0)
 
try:
    while True:
        checkList(raw_input())

except KeyboardInterrupt:
    motorPin.stop()
    steerPin.stop()
    GPIO.cleanup()
