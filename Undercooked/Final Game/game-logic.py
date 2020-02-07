import socket
import threading
import numpy as np
import time
import signal
from enum import Enum
from gameenums import *
from localization import *

# Globals
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
currentGesture = Gesture.NONE
currentPlayerLocation = Location.NONE
transcript = ""
currentOrder = ""
currentPlate = list()
points = 0

class ingredient():
    def __init__(self, name, status, progress):
        self.name = name
        self.status = status
        self.progress = progress
    def __eq__(self,other):
        return ((self.name == other.name) and (self.status == other.status) and (self.progress == other.progress))

menu_to_recipe = {
    MenuItem.SUSHI: [
        ingredient(Ingredient.RICE, IngredientStatus.COOKED, 10), 
        ingredient(Ingredient.FISH, IngredientStatus.COOKED, 10), 
        ingredient(Ingredient.SEAWEED, IngredientStatus.COOKED, 10)
    ],
    MenuItem.SALAD: [
        ingredient(Ingredient.LETTUCE, IngredientStatus.COOKED, 10), 
        ingredient(Ingredient.TOMATO, IngredientStatus.COOKED, 10)
    ]
}

location_to_current_ingredient = {
    Location.CUTTINGBOARD: None,
    Location.STOVE: None,
}

ingredient_to_valid_location = {
    Ingredient.RICE: Location.STOVE,
    Ingredient.FISH: Location.CUTTINGBOARD,
    Ingredient.SEAWEED: Location.CUTTINGBOARD,
    Ingredient.LETTUCE: Location.CUTTINGBOARD,
    Ingredient.TOMATO: Location.CUTTINGBOARD,
}

location_to_valid_ingredient = {
    Location.CUTTINGBOARD: {Ingredient.FISH, Ingredient.SEAWEED, Ingredient.LETTUCE, Ingredient.TOMATO},
    Location.STOVE: {Ingredient.RICE}
}

class TimeoutException(Exception):   # Custom exception class
    pass
def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException

def SetupGame():
    global currentOrder
    currentOrder = MenuItem.SUSHI

def RunGame():
    SetupGame()

    global serv 
    serv.bind(('172.20.10.12', 8080))

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
    global transcript
    global currentOrder
    global currentPlate
    global points

    while True:
        if ingredient_to_valid_location.get(transcript, Location.NONE) == Location.STOVE:
            # Put the Ingredient into the pot to be cooked if valid Ingredient and the player is in proximity to the location
            if (currentPlayerLocation == Location.STOVE):
                location_to_current_ingredient[Location.STOVE] = ingredient(transcript, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("sheet")

        elif ingredient_to_valid_location.get(transcript, Location.NONE) == Location.CUTTINGBOARD:
            # Put the Ingredient onto the cutting board to be chopped if valid Ingredient
            if (currentPlayerLocation == Location.CUTTINGBOARD):
                location_to_current_ingredient[Location.CUTTINGBOARD] = ingredient(transcript, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("sheet")

        elif (transcript == VoiceCommand.PLATE):
            # Check if the ingredient exists and is cooked before allowing it to be plated
            if (
                location_to_current_ingredient.get(currentPlayerLocation, Location.NONE) != Location.NONE
                and location_to_current_ingredient[currentPlayerLocation].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                currentPlate.append(location_to_current_ingredient[currentPlayerLocation])
                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[currentPlayerLocation] = None

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("sheet")

        elif (transcript == VoiceCommand.SUBMIT):
                # Check that the currentLocation of player is SUBMITSTATION
                if currentPlayerLocation == Location.SUBMITSTATION:
                    # Check currentPlate for matching with recipt of currentOrder, make sure all Ingredients are cooked and present
                    if currentPlate == menu_to_recipe[currentOrder]:
                        points += 10    #TODO(Charlotte): make number of points awarded based on time to complete
                    elif currentPlate != menu_to_recipe[currentOrder]:
                        points -= 2

                    # clear the currentPlate and update new currentOrder
                    currentPlate.clear()
                    currentOrder = MenuItem.SUSHI #TODO(Charlotte): randomly choose a MenuItem

        elif (transcript == VoiceCommand.TRASH):
            # Throw out everything on the current plate
            currentPlate.clear()

        if (
            (currentGesture == Gesture.CHOP and currentPlayerLocation == Location.CUTTINGBOARD)
            or (currentGesture == Gesture.COOK and currentPlayerLocation == Location.STOVE)
        ):
            if (
                location_to_current_ingredient[currentPlayerLocation] != None
                and location_to_current_ingredient[currentPlayerLocation].Status == IngredientStatus.RAW
            ):
                location_to_current_ingredient[currentPlayerLocation].progress += 1

                if (location_to_current_ingredient[currentPlayerLocation].progress >= 10):
                    location_to_current_ingredient[currentPlayerLocation].status = IngredientStatus.COOKED

        print(points)

def gestureProcessing():
    #TODO(Bennett): use the game-enums.py file to grab the gesture enum to send to me.
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
    global currentPlayerLocation
    runCode()

def voiceRecognition():
    #TODO(Wendy): Set the currentVoiceCommand global to something
    # For PLATE, SUBMIT, TRASH, and NONE this will just be VoiceCommand
    global transcript

if __name__ == "__main__":
    signal.alarm(120)
    try:
        RunGame()
    except TimeoutException:
        print("Game Over")