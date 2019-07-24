import serial
from pynput import keyboard


minthrottle = 0
defthrottle = 90
maxthrottle = 180

minsteering = 70
defsteering = 100
maxsteering = 130

ser = serial.Serial('/dev/cu.usbmodem143101', 9600)

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

sendThrottleCommand(throttle)
sendSteeringCommand(steering)
for i in range(0, 4):
	print(ser.readline())

def on_press(key):
	try:
		print('alphanumeric key {0} pressed'.format(key.char))
	except AttributeError:
		pressed = 'special key {0} pressed'.format(key)
		# print('special key {0} pressed'.format(key))
	if pressed == "special key Key.shift_r pressed":
		print("TURBO")
		sendThrottleCommand(maxthrottle)
	elif pressed == "special key Key.alt_r pressed":
		print("FORWARD")
		sendThrottleCommand(120)
	elif pressed == "special key Key.cmd_r pressed":
		print("TURN RIGHT")
		sendSteeringCommand(maxsteering)
	elif pressed == "special key Key.cmd pressed":
		print("TURN LEFT")
		sendSteeringCommand(minsteering)
	elif pressed == "special key Key.alt pressed":
		print("SLOW DOWN")
		sendThrottleCommand(defthrottle)
	elif pressed == "special key Key.shift pressed":
		print("STOP")
		sendThrottleCommand(minthrottle)
	
	print(ser.readline())
	print(ser.readline())

# Collect events until released
with keyboard.Listener(on_press=on_press) as listener:listener.join()

while True:

	state = "h"
	print(state)
	#ser.write(bytes(("<" + state + ">"), 'utf-8'))

#for i in range(0, 2):
#print(ser.readline())
