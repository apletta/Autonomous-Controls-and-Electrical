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
    outmax = float(8)
    outmin = float(7.5)
    inmax = float(10)
    inmin = float(0)
    A = float(outmax-outmin)
    B = float(inmax-inmin)
    C = float(x - inmin)
    D = float(outmin)
    return float(float(A/B)*C+D)


print('Calibrating...')
for x in range(len(motor_cal)):
    motor.ChangeDutyCycle(motor_cal[x])
    time.sleep(3)

print('Finished Calibration')
time.sleep(1)

#steer.ChangeDutyCycle(steerMap(-3))
motor.ChangeDutyCycle(0)
#ALL OF THE STATEMENTS AND STUFF DOWN BELOW DON'T WORK YET, IF YOU CAN TRY AND FIX IT GO FOR IT SO WE HAVE LESS REPETITION AND MORE CONTROL ABILITY, OTHERWISE USE motorAndSteering file 
try:
    while True:
        print("Type motor or steer")
        userInput = raw_input()
        if userInput == "steer":
            print("Type the desired angle (-30 to 30)")                  
            while True:
                x = raw_input()
                try:
                    float(x)
                    break
                except ValueError:
                    print("Not a float")
                    print("Type the desired angle (-30 to 30)")
            theta = float(x)
            if theta>=-30 and theta <=30:
                steer.ChangeDutyCycle(steerMap(theta))  # turn towards desired angle theta
            else:
                print("That is not an acceptable angle, type -30 to 30")
            
        elif userInput == "motor":
            print("Type the desired speed (0 to 10)")
            while True: 
                y = raw_input()
                try:
                    float(y)
                    break
                except ValueError:
                    print("Not a float")
                    print("Type the desired speed (0 to 10)")
            rev = float(y)
            if rev>0 and rev<=10:
                motor.ChangeDutyCycle(motorMap(rev))
            elif rev == 0:
                motor.ChangeDutyCycle(5)
            else:
                print("That is not a speed in range... enter 0 to 10")
        else:
            print("That is not a recognizable command. Please input 'steer' or 'motor'")
    #    while rev < 7 or rev > 15:
     #       print('Speed is out of range, please try again:')
      #      rev = float(input())
       # while theta <-30 or theta>30:
        #    print('Angle is out of range, please try again:')
         #   theta = float(input())
except KeyboardInterrupt:
    motor.stop()
    steer.stop()
    GPIO.cleanup()
