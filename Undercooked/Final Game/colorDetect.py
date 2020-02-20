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
global playerDistances
global isPlayerCloseEnough
global minDistance

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
    global playerDistances
    global isPlayerCloseEnough
    global minDistance

    #Colors go [Yellow]
    colorLower = [(20,100,100)]
    colorUpper = [(30,255,255)]
    maxIter = len(colorLower)
    x = [0.0,0.0,0.0]
    y = [0.0,0.0,0.0]
    radius = [0.0,0.0,0.0]
    center = [None,None,None]
    pixelConstant = 0
    ballRadius = 1.5 #Inches
    name = ["Cutting Board","Stove","Turn-it-in Counter"]
    playerDistances = [0.0,0.0,0.0]
    isPlayerCloseEnough = [False, False, False]
    minDistance = 4 #Inches

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

    c = max(cnts, key=cv2.contourArea)
    ((x[iter], y[iter]), radius[iter]) = cv2.minEnclosingCircle(c)
    M = cv2.moments(c)
    center[iter] = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
    if radius[iter] > 10:
        # draw the circle and centroid on the frame,
        # then update the list of tracked points
        cv2.circle(frame, (int(x[iter]), int(y[iter])), int(radius[iter]),
            (0, 255, 255), 2)
        cv2.circle(frame, center[iter], 5, (0, 0, 255), -1)
    
    pixelConstant = ballRadius/radius[iter]

def measureDistances():
    global playerDistances
    global pixelConstant
    global x, y
    global maxIter

    for i in range (maxIter):
    	distance = math.sqrt((x[maxIter - 1]-x[i])*(x[maxIter - 1]-x[i]) + (y[maxIter - 1]-y[i])*(y[maxIter - 1]-y[i]))
    	playerDistances[i] = math.fabs(distance)*pixelConstant

def checkDistances():
    global playerDistances
    global x, y
    global maxIter
    global minDistance
    global name

    measureDistances()
    for iter in range (maxIter):
    	if(playerDistances[iter] <= minDistance):
    		#print("Player is close enough to ", name[iter])
    		isPlayerCloseEnough[iter] = True
    	else:
    		isPlayerCloseEnough[iter] = False

def updateLocation():
	global currentPlayerLocation
	global isPlayerCloseEnough 

	checkDistances()

	if(isPlayerCloseEnough[0]):
	    #print("Yes")
	    currentPlayerLocation = Location.CUTTINGBOARD
	#elif(isPlayerCloseEnough[1]):
	#	currentPlayerLocation = Location.STOVE
	#elif(isPlayerCloseEnough[2]):
	#	currentPlayerLocation = Location.SUBMITSTATION
	else:
	    #print("No")
	    currentPlayerLocation = Location.NONE

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

def startTracker():
    initializeGlobals()
    findACamera()
    runTracker()

if __name__ == "__main__":
    startTracker()