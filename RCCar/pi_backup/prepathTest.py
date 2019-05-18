import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
motor = GPIO.PWM(13,50)
steer = GPIO.PWM(12, 50)
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


def myControl():
    print("type motor or steer")
    userInput = raw_input()
    if userInput == "steer":
        print("type the desired angle (-30 to 30)")
        theta = float(input())
        steer.ChangeDutyCycle(pwmMap(theta))
    elif userInput == "motor":
        print("Type the desired speed (7 to 15)")
        rev = float(input())
        motor.ChangeDutyCycle(rev)
    else:
        print("That is not a recognizable command. Please input 'steer' or 'motor'")

def circle(sped, angl):
    motor.ChangeDutyCycle(sped)
    steer.ChangeDutyCycle(pwmMap(angl))


def figureEight(sped, rotFac): #rotFac = rotationalFactor = how fast the angle changes (how small figure 8 is)
    motor.ChangeDutyCycle(sped)
    while True:
       for a in range(-3,3):
           steer.ChangeDutyCycle(pwmMap(a*rotFac))
           time.sleep(timeDelay)
        #   print("Angle = "+ str(a))



print('Calibrating...')
for x in range(len(motor_cal)):
    motor.ChangeDutyCycle(motor_cal[x])
    time.sleep(5)

print('Finished Calibration')
time.sleep(1)
 
timeDelay = 0.05
startSpeed = 7
try:
    while True:
        inComm = raw_input()
        if inComm == 'myControl':
            myControl()
        elif inComm == 'circle':
            s, a = 0,0
            print("type speed: ")
            s = input()
            print("type angle: ")
            a = input()
            circle(s, a)
        elif  inComm == "figureEight":
            sp, an = 0,0
            print("type speed: ")
            sp = input()
            print ("type angular factor ")
            an = input()
            figureEight(sp, an)
        else: 
            print("That is not a defined function, please try again")


except KeyboardInterrupt:
    motor.stop()
    steer.stop()
    GPIO.cleanup()
