import numpy as np
import time
import signal
from enum import Enum
from game-enums import *

# Globals
currentGesture = Gesture.NONE
currentPlayerLocation = Location.NONE
currentVoiceCommand = VoiceCommand.NONE
currentVoiceIngredient = Ingredient.NONE
currentOrder = ""
currentRecipe = list()
currentPlate = list()
points = 0

class ingredient():
    def __init__(self, name, status, progress):
        self.name = name
        self.status = status
        self.progress = progress

menu_to_recipe = {
    MenuItem.SUSHI: [Ingredient.RICE, Ingredient.FISH, Ingredient.SEAWEED],
    MenuItem.SALAD: [Ingredient.LETTUCE, Ingredient.TOMATO]
}

location_to_current_item = {
    Location.CUTTINGBOARD: None,
    Location.STOVE: None,
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

def gameLogic():
    global currentGesture
    global currentPlayerLocation
    global currentVoiceCommand
    global currentVoiceIngredient
    global currentOrder
    global currentRecipe
    global currentPlate
    global points

    while true:
        
        switch (currentVoiceCommand) {
            case VoiceCommand.CHOP:
                # Put the Ingredient onto the cutting board to be chopped
                # Update location_to_current_item
            case VoiceCommand.COOK:
                # Put the Ingredient into the pot to be cooked
                # Update location_to_current_item
            case VoiceCommand.PLATE:
                # Put the Ingredient that is in proximity onto the plate
                # update currentPlate
            case VoiceCommand.TURNIN:
                # Check currentPlate for matching with currentOrder, make sure all Ingredients are cooked and present
                # And that the currentLocation of player is TURNINSTATION
                # and determine points to be awarded
                # update new currentOrder and currentRecipe
            case VoiceCommand.TRASH:
                # Throw out everything on the current plate
                currentPlate.clear()
        }

        switch (currentGesture) {
            case Gesture.CHOP:
                # Check if there is an ingredient to be chopped (location_to_current_item)
                # And if the location of the player is at CUTTINGBOARD
                # Update status of item in location_to_current_item
            case Gesture.COOK:
                # Check if there is an ingredient to be cooked (location_to_current_item)
                # And if the location of the player is at STOVE
                # Update status of item in location_to_current_item
        }

def gestureProcessing():
    #TODO: Bennett, use the game-enums.py file to grab the gesture enum to send to me.
    global currentGesture
    
    while True:
        try:
            data, _ = serv.recvfrom(4096)
        except socket.timeout:
            continue
        if not data:
            currentGesture = Gesture.NONE
            continue
        currentGesture = data.decode()

def imageRecognition():
    #TODO: Mark put your stuff here. Set the currentPlayerLocation global to something
    global currentPlayerLocation

def voiceRecognition():
    #TODO: Wendy put your stuff here. Set the currentVoiceCommand global to something
    # For CHOP, COOK, and PLATE this will be VoiceCommand + Ingredient
    # For TURNIN, TRASH, and NONE this will just be VoiceCommand
    global currentVoiceCommand
    global currentVoiceIngredient

if __name__ == "__main__":
    signal.alarm(120)
    try:
        RunGame()
    except TimeoutException:
        print("Game Over")