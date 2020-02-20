#Base code found on https://github.com/Mjrovai/OpenCV-Object-Face-Tracking/blob/master/ball_tracking.py

'''
Object detection ("Ball tracking") with OpenCV
    Adapted from the original code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
Developed by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import math
from gameenums import Location

global vs
global frame

global colorLower
global colorUpper
global maxIter

global x
global y
global radius
global center

global pixelConstant
global ballRadius

global name
global playerDistancesOne
global playerDistancesTwo
global isPlayerOneCloseEnough
global isPlayerTwoCloseEnough
global currentPlayerOneLocation
global currentPlayerTwoLocation
global minDistance

global colors

def initializeGlobals():
    global colorLower
    global colorUpper
    global maxIter
    global x
    global y
    global radius
    global center
    global pixelConstant
    global ballRadius
    global name
    global playerDistancesOne
    global playerDistancesTwo
    global isPlayerOneCloseEnough
    global isPlayerTwoCloseEnough
    global currentPlayerOneLocation
    global currentPlayerTwoLocation
    global minDistance
    global colors

    #Colors go [Yellow (BAD), Blue (GOOD), Orange(BAD), Purple (UNSTABLE), Green (UNSTABLE)]
    colorLower = [(20,150,150),(94,80,2),(5,100,100),(127,10,10),(40,52,72)]
    colorUpper = [(40,255,255),(126,255,255),(15,255,255),(170,255,255),(102,255,255)]
    maxIter = len(colorLower)
    x = [0.0,0.0,0.0,0.0,0.0]
    y = [0.0,0.0,0.0,0.0,0.0]
    radius = [0.0,0.0,0.0,0.0,0.0]
    center = [None,None,None,None,None]
    pixelConstant = 0
    ballRadius = 1.5 #Inches
    name = ["Cutting Board","Stove","Turn-it-in Counter"]
    playerDistancesOne = [0.0,0.0,0.0,0.0,0.0]
    playerDistancesTwo = [0.0,0.0,0.0,0.0,0.0]
    isPlayerOneCloseEnough = [False, False, False, False, False]
    isPlayerTwoCloseEnough = [False, False, False, False, False]
    currentPlayerOneLocation = Location.NONE
    currentPlayerTwoLocation = Location.NONE
    minDistance = 6 #Inches
    colors = [(0,255,255),(255,0,0),(0,165,255),(139,0,139),(0,255,0)] #BGR rather than RGB

def findACamera():
    global vs

    cams_test = 500
    findCamera = False
    i = 0
    count = 0
    while(i < cams_test and (not(findCamera))):
        vs = cv2.VideoCapture(i)
        test, _ = vs.read()
        if (test):
            print("i = ", str(i), " /// result: ", str(test))
            if(count == 0): #Determines attached camera or local camera
                findCamera = True
            count = count + 1
        i = i + 1


# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space

def drawCircle(cnts,iter):
    global frame
    global x
    global y
    global radius
    global center
    global pixelConstant
    global ballRadius
    global colors

    c = max(cnts, key=cv2.contourArea)
    ((x[iter], y[iter]), radius[iter]) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center[iter] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
    if radius[iter] > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(x[iter]), int(y[iter])), int(radius[iter]),
            colors[iter], 2)
        cv2.circle(frame, center[iter], 5, colors[iter], -1)
    
    pixelConstant = ballRadius/radius[iter]

def measureDistances():
    global playerDistancesOne
    global playerDistancesTwo
    global pixelConstant
    global x, y
    global maxIter
    
    playerOnePos = maxIter - 2
    playerTwoPos = maxIter - 1

    for i in range(maxIter):
        distanceOne = math.sqrt((x[playerOnePos]-x[i])*(x[playerOnePos]-x[i]) + (y[playerOnePos]-y[i])*(y[playerOnePos]-y[i]))
        playerDistancesOne[i] = math.fabs(distanceOne)*pixelConstant
        distanceTwo = math.sqrt((x[playerTwoPos]-x[i])*(x[playerTwoPos]-x[i]) + (y[playerTwoPos]-y[i])*(y[playerTwoPos]-y[i]))
        playerDistancesTwo[i] = math.fabs(distanceTwo)*pixelConstant

def checkDistances():
    global playerDistancesOne
    global playerDistancesTwo
    global x, y
    global maxIter
    global minDistance
    global name
    global isPlayerOneCloseEnough
    global isPlayerTwoCloseEnough

    measureDistances()

    for iter in range (maxIter):
        if(playerDistancesOne[iter] <= minDistance):
            isPlayerOneCloseEnough[iter] = True
        else:
            isPlayerOneCloseEnough[iter] = False

        if(playerDistancesTwo[iter] <= minDistance):
            isPlayerTwoCloseEnough[iter] = True
        else:
            isPlayerTwoCloseEnough[iter] = False

def updateLocation():
    global currentPlayerOneLocation
    global currentPlayerTwoLocation
    global isPlayerOneCloseEnough
    global isPlayerTwoCloseEnough

    checkDistances()

    if(isPlayerOneCloseEnough[0]):
        currentPlayerOneLocation = Location.CUTTINGBOARD
    elif(isPlayerOneCloseEnough[1]):
        currentPlayerOneLocation = Location.STOVE
        print("One at Stove")
    elif(isPlayerOneCloseEnough[2]):
        currentPlayerOneLocation = Location.SUBMITSTATION
    else:
        currentPlayerOneLocation = Location.NONE

    if(isPlayerTwoCloseEnough[0]):
        currentPlayerTwoLocation = Location.CUTTINGBOARD
    elif(isPlayerTwoCloseEnough[1]):
        currentPlayerTwoLocation = Location.STOVE
        print("Two at Stove")
    elif(isPlayerTwoCloseEnough[2]):
        currentPlayerTwoLocation = Location.SUBMITSTATION
    else:
        currentPlayerTwoLocation = Location.NONE

def runTracker():
    global frame
    global colorLower
    global colorUpper

    # keep looping
    while True:
        # grab the current frame
        (_, frame) = vs.read()
    
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
    
        # resize the frame
        # blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        for iter in range (maxIter):
            mask = cv2.inRange(hsv, colorLower[iter], colorUpper[iter])
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
        
            # find contours in the mask and initialize the current
            # (x, y) center of the ball
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]
            center[iter] = None
    
            # only proceed if at least one contour was found
            if len(cnts) > 0:
                drawCircle(cnts,iter)

        updateLocation()

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
    
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
    
    # cleanup the camera and close any open windows
    vs.release()
    cv2.destroyAllWindows()

def StartTracker():
    initializeGlobals()
    findACamera()
    runTracker()

if __name__ == "__main__":
    StartTracker()