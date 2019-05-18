import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
motor = GPIO.PWM(6,50)
steer = GPIO.PWM(4, 50)
theta = 0
rev = 0 #theta equivalent for motor
steer.start(theta)
motor.start(rev)
# Right Turn: 5
# Left Turn: 10
motor_cal = [15,7,4] #minimum voltage is 4.4V
#userInput = ''
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

print('Finished Calibration')
time.sleep(1)
 
timeDelay = .5
startSpeed = 7
newSpeed = 0
speedInc = .5
try:
    while True:
        
        newSpeed = startSpeed+speedInc

        motor.ChangeDutyCycle(newSpeed)
        
        time.sleep(timeDelay)
        
        steer.ChangeDutyCycle(pwmMap(30))
        
        time.sleep(timeDelay)
        
        newSpeed = newSpeed + speedInc

        motor.ChangeDutyCycle(newSpeed)
        
        time.sleep(timeDelay)
        
        steer.ChangeDutyCycle(pwmMap(0))
        
        time.sleep(timeDelay)
        
        newSpeed = newSpeed + speedInc

        motor.ChangeDutyCycle(newSpeed)

        time.sleep(timeDelay)

        steer.ChangeDutyCycle(pwmMap(-30))

        time.sleep(timeDelay)
        break
except KeyboardInterrupt:
    motor.stop()
    steer.stop()
    GPIO.cleanup()
