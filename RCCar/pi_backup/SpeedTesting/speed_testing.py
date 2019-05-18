import RPi.GPIO as GPIO
import time
import csv
from utilities import *

def main():
    motor_pin, steer_pin = initialize_car()
    try:
        while True:
            speed = input('Motor speed:\t')
            try:
                print(speed)
                print(map_motor(float(speed)))
                motor_to(map_motor(float(speed)),motor_pin)
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        motor_pin.stop()
        steer_pin.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()


