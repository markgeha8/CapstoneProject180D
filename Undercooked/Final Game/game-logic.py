import socket
import threading
import numpy as np
import time
import signal
from enum import Enum
from gameenums import Gesture, Location, VoiceCommand, MenuItem, Ingredient, IngredientStatus
import localization 
import voiceRecog

# Globals
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
currentGesture = Gesture.NONE
currentOrder = ""
currentVoice = VoiceCommand.NONE
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
    serv.bind(('172.20.10.6', 8080))

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
    global currentOrder
    global currentVoice
    global currentPlate
    global points

    while True:
        if(voiceRecog.newVoice):
            currentVoice = voiceRecog.currentVoice
            voiceRecog.setVoice(False)
            print(str(currentVoice))

        if(False):
            if(localization.currentPlayerLocation == Location.CUTTINGBOARD):
                print("Cutting board")
            elif(localization.currentPlayerLocation == Location.STOVE):
                print("Stove")
            elif(localization.currentPlayerLocation == Location.SUBMITSTATION):
                print("Submit Station")

        if(True):
            if(currentVoice == VoiceCommand.PLATE):
                print("Commanding plate")
            elif(currentVoice == VoiceCommand.SUBMIT):
                print("Commanding submit")
            elif(currentVoice == VoiceCommand.TRASH):
                print("Commanding trash")
            elif(currentVoice == Ingredient.RICE):
                print("Ordering rice")
            elif(currentVoice == Ingredient.FISH):
                print("Ordering fish")
            elif(currentVoice == Ingredient.SEAWEED):
                print("Ordering seaweed")
            elif(currentVoice == Ingredient.LETTUCE):
                print("Ordering lettuce")
            elif(currentVoice == Ingredient.TOMATO):
                print("Ordering tomato")

        if ingredient_to_valid_location.get(currentVoice, Location.NONE) == Location.STOVE:
            # Put the Ingredient into the pot to be cooked if valid Ingredient and the player is in proximity to the location
            if (localization.currentPlayerLocation == Location.STOVE):
                location_to_current_ingredient[Location.STOVE] = ingredient(currentVoice, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("Sorry you cannot do that")

        elif ingredient_to_valid_location.get(currentVoice, Location.NONE) == Location.CUTTINGBOARD:
            # Put the Ingredient onto the cutting board to be chopped if valid Ingredient
            if (localization.currentPlayerLocation == Location.CUTTINGBOARD):
                location_to_current_ingredient[Location.CUTTINGBOARD] = ingredient(currentVoice, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("Sorry you cannot do that")

        elif (currentVoice == VoiceCommand.PLATE):
            # Check if the ingredient exists and is cooked before allowing it to be plated
            if (
                location_to_current_ingredient.get(localization.currentPlayerLocation, Location.NONE) != Location.NONE
                and location_to_current_ingredient[localization.currentPlayerLocation].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                currentPlate.append(location_to_current_ingredient[localization.currentPlayerLocation])
                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[localization.currentPlayerLocation] = None

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("Sorry you cannot do that")

        elif (currentVoice == VoiceCommand.SUBMIT):
                # Check that the currentLocation of player is SUBMITSTATION
                if localization.currentPlayerLocation == Location.SUBMITSTATION:
                    # Check currentPlate for matching with recipt of currentOrder, make sure all Ingredients are cooked and present
                    if currentPlate == menu_to_recipe[currentOrder]:
                        points += 10    #TODO(Charlotte): make number of points awarded based on time to complete
                    elif currentPlate != menu_to_recipe[currentOrder]:
                        points -= 2

                    # clear the currentPlate and update new currentOrder
                    currentPlate.clear()
                    currentOrder = MenuItem.SUSHI #TODO(Charlotte): randomly choose a MenuItem

        elif (currentVoice == VoiceCommand.TRASH):
            # Throw out everything on the current plate
            currentPlate.clear()

        if (
            (currentGesture == Gesture.CHOP and localization.currentPlayerLocation == Location.CUTTINGBOARD)
            or (currentGesture == Gesture.COOK and localization.currentPlayerLocation == Location.STOVE)
        ):
            if (
                location_to_current_ingredient[localization.currentPlayerLocation] != None
                and location_to_current_ingredient[localization.currentPlayerLocation].Status == IngredientStatus.RAW
            ):
                location_to_current_ingredient[localization.currentPlayerLocation].progress += 1

                if (location_to_current_ingredient[localization.currentPlayerLocation].progress >= 10):
                    location_to_current_ingredient[localization.currentPlayerLocation].status = IngredientStatus.COOKED

        currentVoice = VoiceCommand.NONE
        #print(points)

def gestureProcessing():
    #TODO(Bennett): use the game-enums.py file to grab the gesture enum to send to me.
    global currentGesture
    tempGesture = ""
    while True:
        try:
            data, _ = serv.recvfrom(4096)
        except socket.timeout:
            continue
        if not data:
            currentGesture = Gesture.NONE
            continue
        tempGesture = data.decode()

        if(tempGesture == "chop"):
            currentGesture = Gesture.CHOP
        elif(tempGesture == "cook"):
            currentGesture = Gesture.CHOP
        else:
            currentGesture = Gesture.NONE

def imageRecognition():
    localization.RunTracker()

def voiceRecognition():
    voiceRecog.RunVoice()

if __name__ == "__main__":
    #signal.alarm(120)
    try:
        RunGame()
    except TimeoutException:
        print("Game Over")