# import djitellopy as tello
import KeyPressModule as kp
import numpy as np
import cv2
import time
import math

#######################################
# Tello Drone Code
#me = tello.Tello()
#me.connect()
#print(me.get_battery())

#me.streamon()
#me.takeoff()
#me.send_rc_control(0, 0, 25, 0)
#time.sleep(2.2)

#######################################

w, h = 360, 240
fbRange = [6200, 6800]
# proportional, integral, and derivative
pid = [0.4, 0.4, 0]
pError = 0


cap = cv2.VideoCapture(0)

def findFace(img):
    faceCascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(img, 1.2, 8) # tweaking the second two parameters will give you the ability
                                                    # to improve the detection capabilities of this method

    myFaceListC = []
    myFaceListArea = []

    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 8)
        cx = x + w // 2         # Center X
        cy = y + h // 2         # Center y
        area = w*h
        cv2.circle(img, (cx,cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0,0], 0]

def trackFace(info, w, pid, pError):

    
    area = info[1]

    x,y = info[0]

    fb = 0

    # x is the object, and w/2 is the center of the image
    # this calculation is used to find the diviation between them
    # telling us how far away the detected face/object is
    error = x - w//2 
    speed = pid[0] * error + pid[1] * (error - pError)

    # this keeps the speed within -100 and 100 so that it does
    # not issue values lower or higher then those.
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20


    print(speed, fb)

    if x == 0:
        speed = 0
        error = 0

    # sends command to the drone
    #me.send_rc_control(0, fb, 0, speed)
    return error



while True:
    _, img  = cap.read()
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)
    
    # The center values will be used to rotate
    # The area values will be used to go forward or backwards
    #print("Center", info[0],"Area", info[1]) 
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #me.land()
        break