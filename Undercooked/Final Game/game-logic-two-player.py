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
import random

# Global Constants
numberOfGesturesUntilCooked = 10

# Globals
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.settimeout(10)

currentPlayerOneGesture = Gesture.NONE
currentPlayerTwoGesture = Gesture.NONE
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
        ingredient(Ingredient.RICE, IngredientStatus.COOKED, numberOfGesturesUntilCooked), 
        ingredient(Ingredient.FISH, IngredientStatus.COOKED, numberOfGesturesUntilCooked), 
        ingredient(Ingredient.SEAWEED, IngredientStatus.COOKED, numberOfGesturesUntilCooked)
    ],
    MenuItem.SALAD: [
        ingredient(Ingredient.LETTUCE, IngredientStatus.COOKED, numberOfGesturesUntilCooked), 
        ingredient(Ingredient.TOMATO, IngredientStatus.COOKED, numberOfGesturesUntilCooked)
    ]
    MenuItem.GRILLEDCHICKEN: [
        ingredient(Ingredient.CHICKEN, IngredientStatus.COOKED, numberOfGesturesUntilCooked),
        ingredient(Ingredient.RICE, IngredientStatus.COOKED, numberOfGesturesUntilCooked)
    ]
}

location_to_current_ingredient = {
    Location.CUTTINGBOARD: None,
    Location.STOVE: None,
}

ingredient_to_valid_location = {
    Ingredient.RICE: Location.STOVE,
    Ingredient.FISH: Location.CUTTINGBOARD,
    Ingredient.SEAWEED: Location.STOVE,
    Ingredient.LETTUCE: Location.CUTTINGBOARD,
    Ingredient.TOMATO: Location.CUTTINGBOARD,
    Ingredient.CHICKEN: Location.STOVE,
}

location_to_valid_ingredient = {
    Location.CUTTINGBOARD: {Ingredient.FISH, Ingredient.LETTUCE, Ingredient.TOMATO},
    Location.STOVE: {Ingredient.RICE, Ingredient.SEAWEED, Ingredient.CHICKEN}
}

def RunGame():
    # Set the first order
    global currentOrder
    
    #TODO(Charlotte): make sure this works correctly
    currentOrder = random.choice(list(menu_to_recipe))
    currentRecipe = menu_to_recipe[currentOrder]
    print("The order is: ", currentOrder)
    print("The ingredients are: ")
    for i in range(len(currentRecipe)): 
        print currentRecipe[i].name

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
    global numberOfGesturesUntilCooked
    global currentPlayerOneGesture
    global currentPlayerTwoGesture
    global currentOrder
    global currentVoice
    global currentPlate
    global points

    # Debugigng Variables
    debugLocalization = False
    debugVoice = False
    debugGesture = False

    while True:
        if(voiceRecog.newVoice):
            currentVoice = voiceRecog.currentVoice
            voiceRecog.setVoice(False)
            print(str(currentVoice))

        if(debugLocalization): #Debugging Localization
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

        if(debugVoice): #Debugging Voice
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

        if(debugGesture): #Debugging Gesture
            if(currentPlayerOneGesture == Gesture.CHOP):
                print("Chopping")
            elif(currentPlayerOneGesture == Gesture.COOK):
                print("Cooking")

            if(currentPlayerTwoGesture == Gesture.CHOP):
                print("Chopping")
            elif(currentPlayerTwoGesture == Gesture.COOK):
                print("Cooking")

        if ingredient_to_valid_location.get(currentVoice, Location.NONE) == Location.STOVE:
            # Put the Ingredient into the pot to be cooked if valid Ingredient and the player is in proximity to the location
            if (
                colorDetect.currentPlayerOneLocation == Location.STOVE 
                or colorDetect.currentPlayerTwoLocation == Location.STOVE
            ):
                location_to_current_ingredient[Location.STOVE] = ingredient(currentVoice, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("Sorry you cannot do that")

        elif ingredient_to_valid_location.get(currentVoice, Location.NONE) == Location.CUTTINGBOARD:
            # Put the Ingredient onto the cutting board to be chopped if valid Ingredient
            if (
                colorDetect.currentPlayerOneLocation == Location.CUTTINGBOARD 
                or colorDetect.currentPlayerTwoLocation == Location.CUTTINGBOARD
            ):
                location_to_current_ingredient[Location.CUTTINGBOARD] = ingredient(currentVoice, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("Sorry you cannot do that")

        elif (currentVoice == VoiceCommand.PLATE):
            # Check if the ingredient exists and is cooked before allowing it to be plated

            # Player One
            if (
                not(location_to_current_ingredient.get(colorDetect.currentPlayerOneLocation, None) == None)
                and location_to_current_ingredient[colorDetect.currentPlayerOneLocation].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                currentPlate.append(location_to_current_ingredient[colorDetect.currentPlayerOneLocation])
                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[colorDetect.currentPlayerOneLocation] = None
                print("Plated", location_to_current_ingredient[colorDetect.currentPlayerOneLocation])
                print("Current items on plate: ")
                for i in range(len(currentPlate)): 
                    print currentPlate[i].name

            # Player Two
            elif (
                not(location_to_current_ingredient.get(colorDetect.currentPlayerTwoLocation, None) == None)
                and location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                currentPlate.append(location_to_current_ingredient[colorDetect.currentPlayerTwoLocation])
                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[colorDetect.currentPlayerTwoLocation] = None
                print("Plated", location_to_current_ingredient[colorDetect.currentPlayerTwoLocation])
                print("Current items on plate: ")
                for i in range(len(currentPlate)): 
                    print currentPlate[i].name

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
                print("Plate: Sorry you cannot do that")

        elif (currentVoice == VoiceCommand.SUBMIT):
                # Check that the currentLocation of player is SUBMITSTATION
                if (
                    colorDetect.currentPlayerOneLocation == Location.SUBMITSTATION
                    or colorDetect.currentPlayerTwoLocation == Location.SUBMITSTATION
                ):
                    # Check currentPlate for matching with recipt of currentOrder, make sure all Ingredients are cooked and present
                    if currentPlate == menu_to_recipe[currentOrder]:
                        points += 10    #TODO(Charlotte): make number of points awarded based on time to complete
                    elif not(currentPlate == menu_to_recipe[currentOrder]):
                        points -= 2
                    print("Current points: ", points)
                    # clear the currentPlate and update new currentOrder
                    currentPlate.clear()
    
                    #TODO(Charlotte): make sure this works correctly
                    currentOrder = random.choice(list(menu_to_recipe))
                    currentRecipe = menu_to_recipe[currentOrder]
                    print("The next order is: ", currentOrder)
                    print("The ingredients are: ")
                    for i in range(len(currentRecipe)): 
                        print currentRecipe[i].name

        elif (currentVoice == VoiceCommand.TRASH):
            # Throw out everything on the current plate
            currentPlate.clear()

        # Player One Gesture Recognition
        if (
            (currentPlayerOneGesture == Gesture.CHOP and colorDetect.currentPlayerOneLocation == Location.CUTTINGBOARD)
            or (currentPlayerOneGesture == Gesture.COOK and colorDetect.currentPlayerOneLocation == Location.STOVE)
        ):
            if (
                not(location_to_current_ingredient[colorDetect.currentPlayerOneLocation] == Ingredient.NONE)
                and location_to_current_ingredient[colorDetect.currentPlayerOneLocation].status == IngredientStatus.RAW
            ):
                location_to_current_ingredient[colorDetect.currentPlayerOneLocation].progress += 1

                if (location_to_current_ingredient[colorDetect.currentPlayerOneLocation].progress >= numberOfGesturesUntilCooked):
                    location_to_current_ingredient[colorDetect.currentPlayerOneLocation].status = IngredientStatus.COOKED
                    print("Item is cooked")

        # Player Two Gesture Recognition
        if (
            (currentPlayerTwoGesture == Gesture.CHOP and colorDetect.currentPlayerTwoLocation == Location.CUTTINGBOARD)
            or (currentPlayerTwoGesture == Gesture.COOK and colorDetect.currentPlayerTwoLocation == Location.STOVE)
        ):
            if (
                not(location_to_current_ingredient[colorDetect.currentPlayerTwoLocation] == Ingredient.NONE)
                and location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].status == IngredientStatus.RAW
            ):
                location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].progress += 1

                if (location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].progress >= numberOfGesturesUntilCooked):
                    location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].status = IngredientStatus.COOKED
                    print("Item is cooked")

        currentVoice = VoiceCommand.NONE

def gestureProcessing():
    global currentPlayerOneGesture
    global currentPlayerTwoGesture
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
        decodedData = data.decode().split(",")
        playerNumer = decodedData[0]
        tempGesture = decodedData[1]
        currentGesture = Gesture.NONE

        if(tempGesture == "chop"):
            print("Chop")
            currentGesture = Gesture.CHOP
        elif(tempGesture == "cook"):
            print("Cook")
            currentGesture = Gesture.COOK
        if(playerNumber == "1"):
            currentPlayerOneGesture = currentGesture
        elif(playerNumber == "2"):
            currentPlayerTwoGesture = currentGesture

        

def imageRecognition():
    localization.RunTracker()
    colorDetect.StartTracker()

def voiceRecognition():
    voiceRecog.RunVoice()

def exitfunc():
    print ("Game Over")
    print ("Score: ", points)
    os._exit(0)

if __name__ == "__main__":
    serv.bind(('172.20.10.6', 8080))
    Timer(120, exitfunc).start() # exit in 2 minutes
    RunGame()
