from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
from ZEDStereoCam import ZED
import pyzed.sl as sl
import matplotlib.pyplot as plt

init = sl.InitParameters()

init.camera_resolution = sl.RESOLUTION.RESOLUTION_HD1080
init.depth_mode = sl.DEPTH_MODE.DEPTH_MODE_PERFORMANCE
init.coordinate_units = sl.UNIT.UNIT_METER
init.camera_fps = 30

zed = sl.Camera()


err = zed.open(init)
if err != sl.ERROR_CODE.SUCCESS:
    print(repr(err))
    zed.close()
    exit(1)


runtime = sl.RuntimeParameters()
runtime.sensing_mode = sl.SENSING_MODE.SENSING_MODE_STANDARD
zed.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_CONTRAST, 6)
zed.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_SATURATION, 6)
#zed.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_BRIGHTNESS, 6)
zed.set_camera_settings(sl.CAMERA_SETTINGS.CAMERA_SETTINGS_EXPOSURE, -1, True)
left_image_zed = sl.Mat()
#right_image_zed = sl.Mat()
#depth_image_zed = sl.Mat()
point_cloud_zed = sl.Mat()

frame = None


width = 1920
height = 1080

netMain = None
metaMain = None
altNames = None

# Converts yolo's bounding box format to opencv's
# Yolo returns x and y as the center of the bounding box
# OpenCV functions require x and y be the top left corner
# Network returns bounding boxes for resized input image, function also converts bounding boxes to original image size
def convertBoxes(x, y, w, h):
    xmin = int(round((x - (w / 2))*(width/darknet.network_width(netMain))))
    xmax = int(round((x + (w / 2))*(width/darknet.network_width(netMain))))
    ymin = int(round((y - (h / 2))*(height/darknet.network_height(netMain))))
    ymax = int(round((y + (h / 2))*(height/darknet.network_height(netMain))))

    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0],\
            detection[2][1],\
            detection[2][2],\
            detection[2][3]
        xmin, ymin, xmax, ymax = convertBoxes(
            float(x), float(y), float(w), float(h))
        upperLeft = (xmin, ymin)
        lowerRight = (xmax, ymax)
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_measure(point_cloud_zed, sl.MEASURE.MEASURE_XYZRGBA)
        # Y and X axis are switched for ZED's point cloud data
        #angleToCone = round((x - (608.0 / 2)) / 608.0) * 87, 2)
        depthX = x*(width/darknet.network_width(netMain))
        depthY = y*(height/darknet.network_height(netMain))
        point3D = point_cloud_zed.get_value(round(depthX),round(depthY))
        #print(point3D[1])
        distanceToCone = round(math.sqrt(point3D[1][0]*point3D[1][0] + point3D[1][1]*point3D[1][1] + point3D[1][2]*point3D[1][2]),2)
        #distanceToCone = 1
        confidence = round(detection[1] * 100,1)


        if detection[0].decode() == 'yellow':
            cv2.rectangle(img, upperLeft, lowerRight, (255, 255, 0), 2)
            cv2.putText(img,
                    detection[0].decode() + " " + str(confidence) + '% ' + str(distanceToCone) + ' m',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,[255, 255, 0])

        elif detection[0].decode() == 'blue':
            cv2.rectangle(img, upperLeft, lowerRight, (0, 0, 255), 2)
            cv2.putText(img,
                    detection[0].decode() + " " + str(confidence) + '% ' + str(distanceToCone) + ' m',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,[0, 0, 255])
        elif detection[0].decode() == 'orange':
            cv2.rectangle(img, upperLeft, lowerRight, (255, 150, 0), 2)
            cv2.putText(img,
                    detection[0].decode() + " " + str(confidence) + '% ' + str(distanceToCone) + ' m',(upperLeft[0], upperLeft[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6,[255, 150, 0])
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

        angleToCone = round((((xmin + (w / 2)) - (scaled_width / 2)) / scaled_width) * 87,6)
        angleToCone = math.radians(angleToCone)
        depthX = x*(width/darknet.network_width(netMain))
        depthY = y*(height/darknet.network_height(netMain))
        distanceToCone = depth_data_zed.get_value(round(depthY),round(depthX))
        distanceToCone = round(distanceToCone[1],2)
        
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
    configPath = "/home/masonberres/Documents/darknet-master/cfg/yolov3-cones-colab.cfg"
    weightPath = "/home/masonberres/Documents/darknet-master/weights/yolov3-cones-colab_best.weights"
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

    darknet_image = darknet.make_image(darknet.network_width(netMain),darknet.network_height(netMain), 3)

    #cap = cv2.VideoCapture("IMG_4400.m4v")
    #zed = ZED("720p", quality=0, fill=True)
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect

    while True:
        prev_time = time.time()

        #ret,frame = cap.read()
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(left_image_zed, sl.VIEW.VIEW_LEFT)
        frame = left_image_zed.get_data()
        #frame = zed.getLeftImage()
        #print(frame)
        #cv2.imshow('zed',frame)
        #cv2.waitKey(0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame,(darknet.network_width(netMain),darknet.network_height(netMain)),interpolation=cv2.INTER_LINEAR)
        #print(frame_resized.shape)
        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())
        #print("detection")
        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.5)
        #print("passed")
        frame = cvDrawBoxes(detections, frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Post processing for FPS and center line
        #cv2.line(frame, (round(width / 2), 0), (round(width / 2), height), (0, 0, 255), 1)
        cv2.putText(frame, 'FPS {:.1f}'.format(1 / (time.time() - prev_time)), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255))
        #frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)

        #print(1/(time.time()-prev_time))
        cv2.imshow('Cone Detection', frame)
        cv2.waitKey(1)


if __name__ == "__main__":
    YOLO()
