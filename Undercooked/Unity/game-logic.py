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
    MenuItem.SUSHI: {
        ingredient(Ingredient.RICE, IngredientStatus.COOKED, 10), 
        ingredient(Ingredient.FISH, IngredientStatus.COOKED, 10), 
        ingredient(Ingredient.SEAWEED, IngredientStatus.COOKED, 10)
    },
    MenuItem.SALAD: {
        ingredient(Ingredient.LETTUCE, IngredientStatus.COOKED, 10), 
        ingredient(Ingredient.TOMATO, IngredientStatus.COOKED, 10)
    }
}

location_to_current_ingredient = {
    Location.CUTTINGBOARD: None,
    Location.STOVE: None,
}

ingredient_to_valid_location = {
    RICE: Location.STOVE,
    FISH: Location.CUTTINGBOARD,
    SEAWEED: Location.NONE,
    LETTUCE: Location.CUTTINGBOARD,
    TOMATO: Location.CUTTINGBOARD,
}

action_to_valid_ingredient = {
    VoiceCommand.CHOP: {Ingredient.FISH, Ingredient.LETTUCE, Ingredient.TOMATO},
    VoiceCommand.COOK: {Ingredient.RICE}
}

class TimeoutException(Exception):   # Custom exception class
    pass
def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException

def SetupGame():
    global currentOrder = MenuItem.SUSHI

def RunGame():
    SetupGame()

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
    global currentPlate
    global points

    while true:
        if currentVoiceCommand == VoiceCommand.CHOP:
            # Put the Ingredient onto the cutting board to be chopped if valid Ingredient
            if (
                currentVoiceIngredient in action_to_valid_ingredient[VoiceCommand.CHOP] 
                and currentPlayerLocation == Location.CUTTINGBOARD
            ):
                location_to_current_ingredient[Location.CUTTINGBOARD] = ingredient(currentVoiceIngredient, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
        else if currentVoiceCommand == VoiceCommand.COOK:
            # Put the Ingredient into the pot to be cooked if valid Ingredient and the player is in proximity to the location
            if (
                currentVoiceIngredient in action_to_valid_ingredient[VoiceCommand.COOK] 
                and currentPlayerLocation == Location.STOVE
            ):
                location_to_current_ingredient[Location.STOVE] = ingredient(currentVoiceIngredient, IngredientStatus.RAW, 0)

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something
        else if (currentVoiceCommand == VoiceCommand.PLATE):
            # Check if the ingredient exists and is cooked before allowing it to be plated
            if (
                location_to_current_ingredient[ingredient_to_valid_location[currentVoiceIngredient]] != None 
                and location_to_current_ingredient[ingredient_to_valid_location[currentVoiceIngredient]].status == IngredientStatus.COOKED
            ):
                # Add the cooked ingredient to the plate
                currentPlate.add(location_to_current_ingredient[ingredient_to_valid_location[currentVoiceIngredient]])
                # Remove the cooked ingredient from the location it existed before
                location_to_current_ingredient[ingredient_to_valid_location[currentVoiceIngredient]] = None

            # This is an ingredient that doesn't need to be cooked beforehand and can be directly plated
            else if ingredient_to_valid_location[currentVoiceIngredient] == Location.NONE:
                # Create the ingredient and add it to the plate
                currentPlate.add(ingredient(currentVoiceIngredient, IngredientStatus.COOKED, 10))

            # Invalid action
            else:
                #TODO(Charlotte): Action is invalid, play farting noise or something

        else if currentVoiceCommand == VoiceCommand.SUBMIT:
                # Check that the currentLocation of player is SUBMITSTATION
                if currentPlayerLocation == Location.SUBMITSTATION:
                    # Check currentPlate for matching with recipt of currentOrder, make sure all Ingredients are cooked and present
                    if currentPlate == menu_to_recipe[currentOrder]:
                        points += 10    #TODO(Charlotte): make number of points awarded based on time to complete
                    else if currentPlate != menu_to_recipe[currentOrder]:
                        points -= 2

                    # clear the currentPlate and update new currentOrder
                    currentPlate.clear()
                    currentOrder = MenuItem.SUSHI #TODO(Charlotte): randomly choose a MenuItem

        else if currentVoiceCommand == VoiceCommand.TRASH:
            # Throw out everything on the current plate
            currentPlate.clear()

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
    #TODO(Mark): Set the currentPlayerLocation global to something
    global currentPlayerLocation

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