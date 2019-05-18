import RPi.GPIO as GPIO
import time

def initialize_car():

    # Calibrates the motor
    def calibrate_motor():
        for dc in [15,7,4,0]:
            motor_pin.ChangeDutyCycle(dc)
            time.sleep(3)

    GPIO.setmode(GPIO.BCM)

    # Setup motor and steering pins
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)

    motor_pin = GPIO.PWM(13,50)
    steer_pin = GPIO.PWM(12,50)

    steer_pin.start(0)
    motor_pin.start(0)
    
    print('Calibrating...')
    calibrate_motor()
    print('Calibration Complete')

    return motor_pin, steer_pin


def map_steer(x,inmin=-30,inmax=30,outmin=10,outmax=5.,offset=-2.65): #maps input values of (inmin, inmax) for our understood range of angles to output values of(outmin, outmax) that are used for the ChangeDutyCycle
    x += offset
    A = outmax-outmin
    B = inmax-inmin
    C = x - inmin
    D = outmin
    return A/B*C+D

def map_motor(x,inmin=0.,inmax=1.,outmin=7.5,outmax=8.):
    if x < inmin:
        raise Exception('The minimum allowable value is {}, but a value of {} was inputted.'.format(inmin,x))
    elif x > inmax:
        raise Exception('The maximum allowable value is {}, but a value of {} was inputted.'.format(inmax,x))
    A = outmax-outmin
    B = inmax-inmin
    C = x - inmin
    D = outmin
    return A/B*C+D

def steer_to(theta,steerPin):
    if theta>=-30 and theta <=30:
        steerPin.ChangeDutyCycle(theta)
    else:
        print("That angle isn't in range")
    
def motor_to(rev,motorPin):
    if rev>0 and rev<=1000:
        motorPin.ChangeDutyCycle(rev)
    elif rev == 0:
        motorPin.ChangeDutyCycle(5)
    else:
        print("That speed isn't in range")

