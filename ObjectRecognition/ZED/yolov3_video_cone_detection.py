from ctypes import *
import os
import math
import cv2
import numpy as np
import time
import darknet
from ZEDStereoCam import ZED
import matplotlib.pyplot as plt

frame = None

# Frame scaling for making detection window visible on high resolution screens
frame_scaling_factor = 1

scaled_width = None
scaled_height = None

netMain = None
metaMain = None
altNames = None


fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.show(block=False)

lower_white = np.array([0,0,245])
upper_white = np.array([255,30,255])

#Hmin-44,Hmax-71;Smin-54,Smax-255,Vmin-63,Vmax-255
lower_black = np.array([0, 0, 0])
upper_black = np.array([255, 255, 30])


# Converts YOLO's bounding box format to OpenCV's
# YOLO returns x and y as the center of the bounding box
# OpenCV functions require x and y be the top left corner of the bounding box
# Darknet returns bounding boxes for network image size (416x416), function also converts bounding boxes to original (scaled) image size
def convertBoxes(x, y, w, h):
    xmin = int(round((x - (w / 2))*(scaled_width/darknet.network_width(netMain))))
    xmax = int(round((x + (w / 2))*(scaled_width/darknet.network_width(netMain))))
    ymin = int(round((y - (h / 2))*(scaled_height/darknet.network_height(netMain))))
    ymax = int(round((y + (h / 2))*(scaled_height/darknet.network_height(netMain))))

    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    print(len(detections))
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBoxes(
            float(x), float(y), float(w), float(h))
        upperLeft = (xmin, ymin)
        lowerRight = (xmax, ymax)
    
        #cropped = img[ymin:ymax,xmin:xmax]
        #cv2.imshow("cropped",cropped)
        #black_mask = cv2.inRange(cropped, lower_black, upper_black)
        #white_mask = cv2.inRange(cropped, lower_white, upper_white)
        #cv2.imshow("cropped",black_mask)
        #where = np.array(np.where(black_mask))

        #x1, y1 = np.amin(where, axis=1)
        #x2, y2 = np.amax(where, axis=1)
        #cv2.rectangle(img, (x1,y1), (x2,y2), (255, 255, 0), 1)
        
        angleToCone = round((((xmin + (w / 2)) - (scaled_width / 2)) / scaled_width) * 87, 2)
        distanceToCone = round(12 * 30 / h, 2)
        confidence = round(detection[1] * 100,1)


        # Print just class name
        #cv2.putText(img,detection[0].decode(),(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,[r, g, b])
        # Print confidence and distance
        #cv2.putText(img, detection[0].decode() + " " + str(confidence) + '% ' + str(distanceToCone) + ' deg',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,[r, g, b])
        
        if detection[0].decode() == 'yellow':
            cv2.rectangle(img, upperLeft, lowerRight, (255, 255, 0), 1)
            # Print distance and angle
            cv2.putText(img, detection[0].decode() + " " + str(distanceToCone) + 'ft ' + str(angleToCone) + ' deg',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,[255, 255, 0])
        elif detection[0].decode() == 'blue':
            cv2.rectangle(img, upperLeft, lowerRight, (0, 200, 255), 1)
            # Print distance and angle
            cv2.putText(img, detection[0].decode() + " " + str(distanceToCone) + 'ft ' + str(angleToCone) + ' deg',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,[0, 200, 255])
        elif detection[0].decode() == 'orange':
            cv2.rectangle(img, upperLeft, lowerRight, (255, 190, 0), 1)
            # Print distance and angle
            cv2.putText(img, detection[0].decode() + " " + str(distanceToCone) + 'ft ' + str(angleToCone) + ' deg',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,[255, 190, 0])
        elif detection[0].decode() == 'orange-big':
            cv2.rectangle(img, upperLeft, lowerRight, (255, 190, 0), 1)
            # Print distance and angle
            cv2.putText(img, detection[0].decode() + " " + str(distanceToCone) + 'ft ' + str(angleToCone) + ' deg',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,[255, 190, 0])
    return img


def plotCones(detections):
    ax1.clear()
    yellowConesX = []
    yellowConesY = []
    blueConesX = []
    blueConesY = []
    for detection in detections:
        x, y, w, h = detection[2][0], \
                 detection[2][1], \
                 detection[2][2], \
                 detection[2][3]
        xmin, ymin, xmax, ymax = convertBoxes(
            float(x), float(y), float(w), float(h))
        upperLeft = (xmin, ymin)
        lowerRight = (xmax, ymax)

        angleToCone = round((((xmin + (w / 2)) - (scaled_width / 2)) / scaled_width) * 73,6)
        angleToCone = math.radians(angleToCone)
        distanceToCone = round(12 * 30 / h, 6)

        distX = distanceToCone*math.tan(angleToCone)
        distY = distanceToCone

        if detection[0].decode() == 'yellow':
            if -10 <= distX <= 40 and distY <= 50:
                yellowConesX.append(distX)
                yellowConesY.append(distY)

        elif detection[0].decode() == 'blue':
            if -10 <= distX <= 40 and distY <= 50:
                blueConesX.append(distX)
                blueConesY.append(distY)
    
    #print(yellowConesX,yellowConesY)
    ax1.plot(yellowConesX, yellowConesY, 'yo')
    ax1.plot(blueConesX,blueConesY,'bo')
    plt.xlim([-10,40])
    plt.ylim([0,50])
    plt.draw()
    plt.pause(0.01)
    
    

def YOLO():

    global metaMain, netMain, altNames
    global scaled_height, scaled_width, height, width

    configPath = "/home/masonberres/Documents/darknet-master/cfg/yolov3-cones-colab.cfg"
    weightPath = "/home/masonberres/Documents/darknet-master/weights/prune.weights"
    metaPath = "/home/masonberres/Documents/darknet-master/cfg/cones.data"
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath)+"`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath)+"`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath)+"`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass


    cap = cv2.VideoCapture("IMG_4400.m4v")
    #cap = cv2.VideoCapture(0)
    # Set start frame to 0
    #cap.set(1,250)

    scaled_height = cap.get(4)*frame_scaling_factor
    scaled_width = cap.get(3)*frame_scaling_factor

    print(scaled_width,scaled_height)


    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                    darknet.network_height(netMain),3)
    while True:
        prev_time = time.time()
        ret, frame = cap.read()
        #frame = cv2.imread("cone_images/cones-8.jpg")
        #scaled_height = round(np.size(frame,0)*frame_scaling_factor,0)
        #scaled_width = round(np.size(frame,1)*frame_scaling_factor,0)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame,(darknet.network_width(netMain),darknet.network_height(netMain)),interpolation=cv2.INTER_LINEAR)
        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())

        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.5)
        postTime = time.time()
        frame = cv2.resize(frame, None, fx=frame_scaling_factor, fy=frame_scaling_factor, interpolation=cv2.INTER_NEAREST)
        frame = cvDrawBoxes(detections, frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        # Post processing for FPS and center line
        #cv2.line(frame, (round(width / 2), 0), (round(width / 2), height), (0, 0, 255), 1)
        cv2.putText(frame, 'FPS {:.1f}'.format(1 / (time.time() - prev_time)), (10, 30),cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 255))
        cv2.putText(frame, 'Render '+str(round((time.time()-postTime)*1000,2))+' ms', (10, 50),cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255))

        #print(1/(time.time()-prev_time))
        cv2.imshow('Cone Detection', frame)
        #plotCones(detections)
        #while(cv2.waitKey(1) != 13): pass
        cv2.waitKey(1)


if __name__ == "__main__":
    YOLO()
