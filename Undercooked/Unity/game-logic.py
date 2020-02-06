import numpy as np
import time
import signal
from enum import Enum
from game-enums import *

# CuttingBoard, Stove, Station, Player, Plate, Points, Orders

# Input: voice to create fish and know location
# Input: gesture recognition to indicate that an ingredient has changed from raw to cooked state

# Globals
clientIP = ""
currentGesture = ""
currentLocation = ""
currentOrder = ""
currentRecipe = list()
points = ""

class ingredient():
    def __init__(self, name, status):
        self.name = name
        self.status = status

menu_to_recipe = {
    MenuItem.SUSHI: [Ingredient.RICE, Ingredient.FISH, Ingredient.SEAWEED],
    MenuItem.SALAD: [Ingredient.LETTUCE, Ingredient.TOMATO]
}

class TimeoutException(Exception):   # Custom exception class
    pass
def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException

def SetupGame():
    global currentOrder = MenuItem.SUSHI
    global currentRecipe = menu_to_recipe[currentOrder]

def RunGame():
    ip = get_ip_address('wlan0') #'172.20.10.5'
    print(ip)
    serv.bind((ip, 8080))

    # connect to the gesture rpi
    establishClientConnection()

    # create threads
    t1 = threading.Thread(target=imageRecognition, args=()) 
    t2 = threading.Thread(target=gestureProcessing, args=())
    t3 = threading.Thread(target=gameLogic, args=())
    t4 = threading.Thread(target=voiceRecognition, args=())
    
    # starting threads 
    t1.start() 
    t2.start()
    t3.start()
    t4.start()

    # wait until threads are completely executed 
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    
    # both threads completely executed 
    print("Done!")


def establishClientConnection():
    global clientIP

    while True:
        try:
            data, _ = serv.recvfrom(4096) #Sets up try/except block to ensure wait time isn't too long (cycles every 10 seconds)
        except socket.timeout:
            print("Timeout from establishing connection with a Client")
            continue
        if not data: continue
        clientIP = data.decode()
        return

def gestureProcessing():


def imageRecognition():
    #TODO: Mark put your stuff here

def voiceRecognition():
    #TODO: Wendy put your stuff here

if __name__ == "__main__":
    signal.alarm(120)
    try:
        RunGame()
    except TimeoutException:
        print("Game Over")