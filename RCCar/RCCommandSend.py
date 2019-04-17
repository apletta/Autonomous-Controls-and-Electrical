import serial
import time

minthrottle = 0
defthrottle = 90
maxthrottle = 180

minsteering = 70
defsteering = 100
maxsteering = 130

ser = serial.Serial('/dev/cu.usbmodem1421', 9600)

print(ser.readline())

throttle = defthrottle
steering = defsteering


def sendThrottleCommand(throttle):
	if throttle < minthrottle:  # these are supposed to be just last failsafes. Do actual throttle calcs in pathing code
		throttle = minthrottle
	elif throttle > maxthrottle:
		throttle = maxthrottle
	if len(str(throttle)) < 3:
		if len(str(throttle)) == 1:
			throttle = "00" + str(throttle)
		elif len(str(throttle)) == 2:
			throttle = "0" + str(throttle)
	
	ser.write(bytes(("<T" + str(throttle) + ">"), 'utf-8'))


def sendSteeringCommand(steering):
	if steering < minsteering:
		steering = minsteering
	elif steering > maxsteering:
		steering = maxsteering
	if len(str(steering)) < 3:
		steering = "0" + str(steering)
	
	ser.write(bytes(("<S" + str(steering) + ">"), 'utf-8'))
	
def sendboth(steering, throttle):
	sendSteeringCommand(steering)
	time.sleep(.1)
	sendThrottleCommand(throttle)

sendThrottleCommand(throttle)
sendSteeringCommand(steering)
