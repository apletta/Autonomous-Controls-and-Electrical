import numpy as np
import cv2
from RCCommandSend import sendSteeringCommand, sendThrottleCommand, sendboth

face_cascade = cv2.CascadeClassifier('opencv_object_recognition_haarcascade_frontalface_alt.xml');

cap = cv2.VideoCapture(0)

goingforward = False  # stupid temp vars
forwardtime = 0

while True:
	# Capture frame-by-frame
	ret, frame = cap.read()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
	for (x, y, w, h) in faces:
		print(x, y, w, h)
		roi_gray = gray[y:y + h, x:x + w]
		
		color = (255, 0, 0)
		stroke = 2
		width = x + w
		height = y + h
		cv2.rectangle(frame, (x, y), (width, height), color, stroke)
		#cv2.rectangle(frame, (x + int(.5 * w), y + int(.5 * h)), (10, 10), color, 10)
		print("hello human")
		sendboth(100 + (640 - (x + int(.5 * w))), 110)
	
	# Display the resulting frame
	cv2.imshow('frame', frame)
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
