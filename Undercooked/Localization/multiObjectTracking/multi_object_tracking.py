#Base code found on https://www.pyimagesearch.com/2018/08/06/tracking-multiple-objects-with-opencv/ 
#and https://gist.github.com/keithweaver/5bd13f27e2cc4c4b32f9c618fe0a7ee5
#Updated for our own game usage.

# USAGE
# python multi_object_tracking.py --video videos/soccer_01.mp4 --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import numpy as np
import math

x = [0,0,0,0]
y = [0,0,0,0]
w = [0,0,0,0]
h = [0,0,0,0]
min_distance = 4 #Inches
playerDistances = [0.0,0.0,0.0]
name = ["Cutting Board","Stove","Turn-it-in Counter"]
pixel_size = 0
isPlayerCloseEnough = [False, False, False]

def measureDistances():
	for i in range (3):
		distance = math.sqrt((x[3]+w[3]/2 - (x[i]+w[i]/2))*(x[3]+w[3]/2 - (x[i]+w[i]/2)) + (y[3]+h[3]/2 - (y[i]+h[i]/2))*(y[3]+h[3]/2 - (y[i]+h[i]/2)))
		playerDistances[i] = math.fabs(distance)*pixel_size

def checkDistances():
	measureDistances()
	for i in range (3):
		if(playerDistances[i] <= min_distance):
			print("Player is close enough to ", name[i])
			isPlayerCloseEnough[i] = True
		else:
			isPlayerCloseEnough[i] = False


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
ap.add_argument("-s", "--size", type=float, required=True,
	help="size of the balls")
args = vars(ap.parse_args())

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
OPENCV_OBJECT_TRACKERS = {
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create
}

ball_size = args["size"]

# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()

# if a video path was not supplied, grab the reference to the web cam
print("[INFO] starting video stream...")

vs = cv2.VideoCapture(0)

currentFrame = 0

init = True
while(True):
    # Capture frame-by-frame
    ret, frame = vs.read()

    # Handles the mirroring of the current frame
    frame = cv2.flip(frame,1)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)

    # To stop duplicate images
    currentFrame += 1

    # check to see if we have reached the end of the stream
    if frame is None:
	    break

    # resize the frame (so we can process it faster)
    frame = imutils.resize(frame, width=600)

	# grab the updated bounding box coordinates (if any) for each
	# object that is being tracked
    (success, boxes) = trackers.update(frame)

    i = 0
    # loop over the bounding boxes and draw then on the frame
    for box in boxes:
	    (xTemp, yTemp, wTemp, hTemp) = [int(v) for v in box]
	    x[i] = xTemp
	    y[i] = yTemp
	    w[i] = wTemp
	    h[i] = hTemp
	    cv2.rectangle(frame, (x[i], y[i]), (x[i] + w[i], y[i] + h[i]), (0, 255, 0), 2)
	    #w and h are the dimensions of the box (associate w/h with ball_size)
	    pixel_size_w = ball_size/w[i] 	#Creates the conversion for inches/pixels to find the total inches distance between objects
	    pixel_size_h = ball_size/h[i]
	    pixel_size = (pixel_size_h+pixel_size_w)/2
	    i = i+1

    if not (init):
	    checkDistances()

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):
    	if(init): #Set all four main locations at the beginning
    		print("Please select the cutting board.")
    		box = cv2.selectROI("Frame", frame, fromCenter=False,
    			showCrosshair=True)

    		# create a new object tracker for the bounding box and add it
    		# to our multi-object tracker
    		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
    		trackers.add(tracker, frame, box)
    		print("Cutting board is set.")  

    		print("Please select the stove top.")
    		box = cv2.selectROI("Frame", frame, fromCenter=False,
    			showCrosshair=True)

    		# create a new object tracker for the bounding box and add it
    		# to our multi-object tracker
    		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
    		trackers.add(tracker, frame, box)
    		print("Stove is set.")

    		print("Please select the turn-it-in counter.")
    		box = cv2.selectROI("Frame", frame, fromCenter=False,
    			showCrosshair=True)

    		# create a new object tracker for the bounding box and add it
    		# to our multi-object tracker
    		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
    		trackers.add(tracker, frame, box)
    		print("Turn-it-in Counter is set.")

    		print("Please select the player.")
    		box = cv2.selectROI("Frame", frame, fromCenter=False,
    			showCrosshair=True)

    		# create a new object tracker for the bounding box and add it
    		# to our multi-object tracker
    		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
    		trackers.add(tracker, frame, box)
    		print("Player is set.")

    	init = False

    if key == ord("r"):
    	init = True
    	trackers.clear()
    	trackers = cv2.MultiTracker_create()
    	print("Trackers reset.")

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
    	break

# When everything done, release the capture
vs.release()
cv2.destroyAllWindows()