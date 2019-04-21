import RPi.GPIO as GPIO
import time
import csv
from utilities import *

def initialize():

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

def main():
    initialze()

    vel = []
    delta = []
    dt = .1

    print('Reading Data')
    time.sleep(3)
    with open('data/straight.csv',newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                vel.append(float(row[3]))
                delta.append(float(row[2]))

    print('Running Motors')
    time.sleep(3)
    for i in range(len(vel)):
        print('Motor:\t' + str(map_motor(vel[i])))
        print('Steer:\t' + str(map_steer(delta[i])))
        motor_to(map_motor(vel[i]))
        steer_to(map_steer(delta[i]))
        time.sleep(dt)

if __name__ == '__main__':
    main()
