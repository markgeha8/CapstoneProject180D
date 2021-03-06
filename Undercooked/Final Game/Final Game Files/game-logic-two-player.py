import socket
import threading
import numpy as np
from enum import Enum
from gameenums import *
import localization 
import colorDetect
import voiceRecog
import os
import time
from datetime import datetime
from threading import Timer
import random
from playsound import playsound
from tkinter import *  
from PIL import ImageTk,Image

# Global Constants
numberOfGesturesUntilCooked = 10

# Socket Globals
serv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serv.settimeout(10)
ipadd = '192.168.1.105'

# Graphics Globals
window = Tk()
line1txt = StringVar()
line2txt = StringVar()
line3txt = StringVar()
line4txt = StringVar()

# Game State Globals
currentPlayerOneGesture = Gesture.NONE
currentPlayerTwoGesture = Gesture.NONE
currentOrder = ""
currentVoice = VoiceCommand.NONE
currentPlate = list()
points = 0

# Ingredient class
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
    def __lt__(self,other):
        return self.name.value < other.name.value

# Dictionaries for maintaining game state
menu_to_recipe = {
    MenuItem.SUSHI: [
        ingredient(Ingredient.RICE, IngredientStatus.COOKED, numberOfGesturesUntilCooked), 
        ingredient(Ingredient.FISH, IngredientStatus.COOKED, numberOfGesturesUntilCooked), 
        ingredient(Ingredient.SEAWEED, IngredientStatus.COOKED, numberOfGesturesUntilCooked)
    ],
    MenuItem.SALAD: [
        ingredient(Ingredient.LETTUCE, IngredientStatus.COOKED, numberOfGesturesUntilCooked), 
        ingredient(Ingredient.TOMATO, IngredientStatus.COOKED, numberOfGesturesUntilCooked)
    ],
    MenuItem.GRILLEDCHICKEN: [
        ingredient(Ingredient.CHICKEN, IngredientStatus.COOKED, numberOfGesturesUntilCooked),
        ingredient(Ingredient.RICE, IngredientStatus.COOKED, numberOfGesturesUntilCooked)
    ]
}

location_to_current_ingredient = {
    Location.CUTTINGBOARD: None,
    Location.STOVE: None,
    Location.NONE: None,
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
    
    currentOrder = random.choice(list(menu_to_recipe))

    setupDisplay()

    global serv

    # Create threads
    t1 = threading.Thread(target=imageRecognition, args=()) 
    t2 = threading.Thread(target=gestureProcessing, args=())
    t3 = threading.Thread(target=voiceRecognition, args=())
    
    # Start up threads, game logic should run in main thread
    t1.start() 
    t2.start()
    t3.start()
    gameLogic()

    # Wait until threads have exited
    t1.join()
    t2.join()
    t3.join()
    
    # All threads executed 
    print("Done!")

def gameLogic():
    global numberOfGesturesUntilCooked
    global currentPlayerOneGesture
    global currentPlayerTwoGesture
    global currentOrder
    global currentVoice
    global currentPlate
    global points

    # Debugging Variables
    debugLocalization = False
    debugVoice = False
    debugGesture = False

    while True:

        # Update global voice variable if a new voice command has been sent by voice file
        if(voiceRecog.newVoice):
            currentVoice = voiceRecog.currentVoice
            voiceRecog.setVoice(False)

        # Debugging Localization
        if(debugLocalization):
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

        # Debugging Voice
        if(debugVoice):
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
            elif(currentVoice == Ingredient.CHICKEN):
                print("Ordering chimkin")

        # Debugging Gesture
        if(debugGesture):
            if(currentPlayerOneGesture == Gesture.CHOP):
                print("Chopping")
            elif(currentPlayerOneGesture == Gesture.COOK):
                print("Cooking")

            if(currentPlayerTwoGesture == Gesture.CHOP):
                print("Chopping")
            elif(currentPlayerTwoGesture == Gesture.COOK):
                print("Cooking")

        # Voice command is an ingredient that should be put on a stove
        if ingredient_to_valid_location.get(currentVoice, Location.NONE) == Location.STOVE:
            # Put the Ingredient into the pot to be cooked if valid Ingredient and the player is in proximity to the location
            if (
                colorDetect.currentPlayerOneLocation == Location.STOVE 
                or colorDetect.currentPlayerTwoLocation == Location.STOVE
            ):
                location_to_current_ingredient[Location.STOVE] = ingredient(currentVoice, IngredientStatus.RAW, 0)
                playsound('placeItem.mp3')

            # Invalid action
            else:
                playsound('negative.mp3')

        # Voice command is an ingredient that should be put on a cutting board
        elif ingredient_to_valid_location.get(currentVoice, Location.NONE) == Location.CUTTINGBOARD:
            # Put the Ingredient onto the cutting board to be chopped if valid Ingredient
            if (
                colorDetect.currentPlayerOneLocation == Location.CUTTINGBOARD 
                or colorDetect.currentPlayerTwoLocation == Location.CUTTINGBOARD
            ):
                location_to_current_ingredient[Location.CUTTINGBOARD] = ingredient(currentVoice, IngredientStatus.RAW, 0)
                playsound('placeItem.mp3')

            # Invalid action
            else:
                playsound('negative.mp3')

        # Voice command is plate
        elif (currentVoice == VoiceCommand.PLATE):
            # Check if the ingredient exists and is cooked before allowing it to be plated

            # Player One
            currentPlayerOneLocation = colorDetect.currentPlayerOneLocation
            currentPlayerTwoLocation = colorDetect.currentPlayerTwoLocation
            if (
                not(currentPlayerOneLocation == Location.NONE)
                and not(location_to_current_ingredient.get(currentPlayerOneLocation, None) == None)
                and location_to_current_ingredient[currentPlayerOneLocation].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                playsound('placeItem.mp3')
                currentPlate.append(location_to_current_ingredient[currentPlayerOneLocation])

                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[currentPlayerOneLocation] = None
                updateDisplay()

            # Player Two
            elif (
                not(currentPlayerTwoLocation == Location.NONE)
                and not(location_to_current_ingredient.get(currentPlayerTwoLocation, None) == None)
                and location_to_current_ingredient[currentPlayerTwoLocation].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                playsound('placeItem.mp3')
                currentPlate.append(location_to_current_ingredient[currentPlayerTwoLocation])

                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[currentPlayerTwoLocation] = None
                updateDisplay()

            # Invalid action
            else:
                playsound('negative.mp3')

        # Voice command is submit
        elif (currentVoice == VoiceCommand.SUBMIT):
            # Check that the currentLocation of player is SUBMITSTATION
            if (
                colorDetect.currentPlayerOneLocation == Location.SUBMITSTATION
                or colorDetect.currentPlayerTwoLocation == Location.SUBMITSTATION
            ):
                # Check currentPlate for matching with recipt of currentOrder, make sure all Ingredients are cooked and present
                recipe = menu_to_recipe[currentOrder].copy()
                isPlateCorrect = False

                if len(currentPlate) == len(recipe):
                    counter = 0
                    for i in range(len(currentPlate)):
                        tempi = i - counter
                        for j in range(len(recipe)):
                            tempj = j
                            if currentPlate[tempi].name == recipe[tempj].name:
                                currentPlate.pop(tempi)
                                recipe.pop(tempj)
                                counter = counter + 1
                                break
                    
                    if len(recipe) == 0 and len(currentPlate) == 0:
                        isPlateCorrect = True

                if isPlateCorrect:
                    points += 10
                    playsound('positive.mp3')
                else:
                    points -= 2
                    playsound('negative.mp3')
                
                # Clear the plate and choose a new current order
                currentPlate.clear()
                currentOrder = random.choice(list(menu_to_recipe))
                updateDisplay()

            else:
                playsound('negative.mp3')

        elif (currentVoice == VoiceCommand.TRASH):
            # Throw out everything on the current plate
            playsound('placeItem.mp3')
            currentPlate.clear()
            updateDisplay()

        # Player One Gesture Recognition
        if (
            (currentPlayerOneGesture == Gesture.CHOP and colorDetect.currentPlayerOneLocation == Location.CUTTINGBOARD)
            or (currentPlayerOneGesture == Gesture.COOK and colorDetect.currentPlayerOneLocation == Location.STOVE)
        ):
            # if the player is in a location with a raw ingredient and doing the correct gesture, increase progress of ingredient
            if (
                not(location_to_current_ingredient[colorDetect.currentPlayerOneLocation] == None)
                and location_to_current_ingredient[colorDetect.currentPlayerOneLocation].status == IngredientStatus.RAW
            ):
                location_to_current_ingredient[colorDetect.currentPlayerOneLocation].progress += 1
                
                # update the ingredient to be in a cooked state
                if (location_to_current_ingredient[colorDetect.currentPlayerOneLocation].progress >= numberOfGesturesUntilCooked):
                    location_to_current_ingredient[colorDetect.currentPlayerOneLocation].status = IngredientStatus.COOKED
                    print(location_to_current_ingredient[colorDetect.currentPlayerOneLocation].name, " is cooked")
                    playsound('positive.mp3')

        # Player Two Gesture Recognition
        if (
            (currentPlayerTwoGesture == Gesture.CHOP and colorDetect.currentPlayerTwoLocation == Location.CUTTINGBOARD)
            or (currentPlayerTwoGesture == Gesture.COOK and colorDetect.currentPlayerTwoLocation == Location.STOVE)
        ):
            # if the player is in a location with a raw ingredient and doing the correct gesture, increase progress of ingredient
            if (
                not(location_to_current_ingredient[colorDetect.currentPlayerTwoLocation] == None)
                and location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].status == IngredientStatus.RAW
            ):
                location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].progress += 1

                # update the ingredient to be in a cooked state
                if (location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].progress >= numberOfGesturesUntilCooked):
                    location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].status = IngredientStatus.COOKED
                    print(location_to_current_ingredient[colorDetect.currentPlayerTwoLocation].name, " is cooked")
                    playsound('positive.mp3')

        # set the voice command back to none until updated with a new command again
        currentVoice = VoiceCommand.NONE

# Gesture recognition
def gestureProcessing():
    global currentPlayerOneGesture
    global currentPlayerTwoGesture
    while True:
        tempGesture = ""
        playerNumber = ""
        try:
            data, _ = serv.recvfrom(4096)
        except socket.timeout:
            continue
        if not data:
            currentGesture = Gesture.NONE
            continue
        decodedData = data.decode().split(",")
        if(len(decodedData) == 2):
            playerNumber = decodedData[0]
            tempGesture = decodedData[1]
        currentGesture = Gesture.NONE

        if(tempGesture == "chop"):
            currentGesture = Gesture.CHOP
        elif(tempGesture == "cook"):
            currentGesture = Gesture.COOK
        if(playerNumber == "1"):
            currentPlayerOneGesture = currentGesture
        elif(playerNumber == "2"):
            currentPlayerTwoGesture = currentGesture

def setupDisplay():
    global window
    global line1txt
    global line2txt
    global line3txt
    global line4txt

    global currentOrder
    global points

    currentRecipe = menu_to_recipe[currentOrder]
    
    currentRecipeString = ""
    for i in range(len(currentRecipe)): 
        currentRecipeString += ingredient_enum_to_name[currentRecipe[i].name] + ", "

    currentRecipeString = currentRecipeString[:len(currentRecipeString)-2]

    window.title("Undercooked")
    window.geometry('650x500')

    line1txt.set("Order: " + menuItem_enum_to_name[currentOrder])

    line2txt.set("Recipe: " + currentRecipeString)

    line3txt.set("Plate: ")

    line4txt.set("Score: " + str(points))

    line1 = Label(window, textvariable=line1txt, font=("Arial", 20), justify=LEFT)
    line1.pack()

    line2 = Label(window, textvariable=line2txt, font=("Arial", 20), justify=LEFT)
    line2.pack()

    line3 = Label(window, textvariable=line3txt, font=("Arial", 20), justify=LEFT)
    line3.pack()

    line4 = Label(window, textvariable=line4txt, font=("Arial", 20), justify=LEFT)
    line4.pack()

    line5 = Label(window, text="________________________________", font=("Arial", 20), justify=LEFT)
    line5.pack()

    line6 = Label(window, text="Items cooked on stove:", font=("Arial", 20), justify=LEFT)
    line6.pack()

    line7 = Label(window, text="Chicken, Rice, Seaweed", font=("Arial", 20), justify=LEFT)
    line7.pack()

    line8 = Label(window, text="________________________________", font=("Arial", 20), justify=LEFT)
    line8.pack()

    line9 = Label(window, text="Items chopped on cutting board:", font=("Arial", 20), justify=LEFT)
    line9.pack()

    line10 = Label(window, text="Fish, Tomato, Lettuce", font=("Arial", 20), justify=LEFT)
    line10.pack()

    line11 = Label(window, text="________________________________", font=("Arial", 20), justify=LEFT)
    line11.pack()

    line12 = Label(window, text="Voice Commands:", font=("Arial", 20), justify=LEFT)
    line12.pack()

    line13 = Label(window, text="Ingredients, Plate/Set, Trash, Submit", font=("Arial", 20), justify=LEFT)
    line13.pack()
    
    window.update()

def updateDisplay():
    global currentOrder
    global currentPlate
    global points
    global line1txt
    global line2txt
    global line3txt
    global line4txt
    global window

    currentRecipe = menu_to_recipe[currentOrder]

    currentRecipeString = ""
    for i in range(len(currentRecipe)): 
        currentRecipeString += ingredient_enum_to_name[currentRecipe[i].name] + ", "

    currentRecipeString = currentRecipeString[:len(currentRecipeString)-2]

    currentPlateString = ""
    for i in range(len(currentPlate)): 
        currentPlateString += ingredient_enum_to_name[currentPlate[i].name] + ", "
    
    currentPlateString = currentPlateString[:len(currentPlateString)-2]

    line1txt.set("Order: " + menuItem_enum_to_name[currentOrder])
    line2txt.set("Recipe: " + currentRecipeString)
    line3txt.set("Plate: " + currentPlateString)
    line4txt.set("Score: " + str(points))

    window.update()       

def imageRecognition():
    colorDetect.StartTracker()

def voiceRecognition():
    voiceRecog.RunVoice()

def exitfunc():
    print ("Game Over")
    print ("Score: ", points)
    os._exit(0)

if __name__ == "__main__":
    serv.bind((ipadd, 8080))
    Timer(180, exitfunc).start() # exit in 3 minutes
    RunGame()
