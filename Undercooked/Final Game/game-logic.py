import socket
import threading
import numpy as np
from enum import Enum
from gameenums import Gesture, Location, VoiceCommand, MenuItem, Ingredient, IngredientStatus
import localization 
import colorDetect
import voiceRecog
import os
import time
from datetime import datetime
from threading import Timer


# Globals
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.settimeout(10)

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
        if (not(other == None)):
            return ((self.name == other.name) and (self.status == other.status) and (self.progress == other.progress))
        else:
            return False

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

def SetupGame():
    global currentOrder
    currentOrder = MenuItem.SUSHI

def RunGame():
    SetupGame()

    global serv

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

        if(False): #Debugging Localization
            if(colorDetect.currentPlayerOneLocation == Location.CUTTINGBOARD):
                print("Player One is at the Cutting Board")
            elif(colorDetect.currentPlayerOneLocation == Location.STOVE):
                print("Player One is at the Stove")
            elif(colorDetect.currentPlayerOneLocation == Location.SUBMITSTATION):
                print("Player One is at the Submit Station")

            if(colorDetect.currentPlayerTwoLocation == Location.CUTTINGBOARD):
                print("Player Two is at the Cutting Board")
            elif(colorDetect.currentPlayerTwoLocation == Location.STOVE):
                print("Player Two is at the Stove")
            elif(colorDetect.currentPlayerTwoLocation == Location.SUBMITSTATION):
                print("Player Two is at the Submit Station")

        if(False): #Debugging Voice
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

        if(False): #Debugging Gesture
            if(currentGesture == Gesture.CHOP):
                print("Chopping")
            elif(currentGesture == Gesture.COOK):
                print("Cooking")

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
            print(not(location_to_current_ingredient.get(localization.currentPlayerLocation, None) == None))
            if (
                not(location_to_current_ingredient.get(localization.currentPlayerLocation, None) == None)
                and location_to_current_ingredient[localization.currentPlayerLocation].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                currentPlate.append(location_to_current_ingredient[localization.currentPlayerLocation])
                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[localization.currentPlayerLocation] = None
                print("Plated")

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("Plate: Sorry you cannot do that")

        elif (currentVoice == VoiceCommand.SUBMIT):
                # Check that the currentLocation of player is SUBMITSTATION
                if localization.currentPlayerLocation == Location.SUBMITSTATION:
                    # Check currentPlate for matching with recipt of currentOrder, make sure all Ingredients are cooked and present
                    if currentPlate == menu_to_recipe[currentOrder]:
                        points += 10    #TODO(Charlotte): make number of points awarded based on time to complete
                    elif not(currentPlate == menu_to_recipe[currentOrder]):
                        points -= 2
                    print(points)
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
                not(location_to_current_ingredient[localization.currentPlayerLocation] == Ingredient.NONE)
                and location_to_current_ingredient[localization.currentPlayerLocation].status == IngredientStatus.RAW
            ):
                location_to_current_ingredient[localization.currentPlayerLocation].progress += 1

                if (location_to_current_ingredient[localization.currentPlayerLocation].progress >= 10):
                    location_to_current_ingredient[localization.currentPlayerLocation].status = IngredientStatus.COOKED
                    print("Item is cooked")

        currentVoice = VoiceCommand.NONE

#Incoming string ""

def gestureProcessing():
    #TODO(Bennett): use the game-enums.py file to grab the gesture enum to send to me.
    global currentGesture
    while True:
        tempGesture = ""
        try:
            data, _ = serv.recvfrom(4096)
        except socket.timeout:
            print("Timeout without connecting to Client")
            continue
        if not data:
            currentGesture = Gesture.NONE
            continue
        tempGesture = data.decode()

        if(tempGesture == "chop"):
            print("Chop")
            currentGesture = Gesture.CHOP
        elif(tempGesture == "cook"):
            print("Cook")
            currentGesture = Gesture.COOK
        else:
            currentGesture = Gesture.NONE

def imageRecognition():
    localization.RunTracker()
    colorDetect.StartTracker()

def voiceRecognition():
    voiceRecog.RunVoice()

def exitfunc():
    print ("Game Over")
    print ("Score: ", points)
    os._exit(1)

if __name__ == "__main__":
    serv.bind(('131.179.4.10', 8080))
    Timer(10, exitfunc).start() # exit in 2 minutes
    RunGame()
