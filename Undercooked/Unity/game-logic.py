import numpy as np
import time
import signal

# CuttingBoard, Stove, Station, Player, Plate, Points, Orders


# Global Constants
SUSHI = 1
SALAD = 2

menu_to_recipe = {
    SUSHI: ["Rice", "Fish", "Seaweed"],
    SALAD: ["Lettuce", "Tomato"]
}

index_to_name = {
    SUSHI: "Sushi",
    SALAD: "Salad"
}

# Global Variables
currentOrder = list()
currentOrderWord = ""


class TimeoutException(Exception):   # Custom exception class
    pass
def timeout_handler(signum, frame):  # Custom signal handler
    raise TimeoutException

def SetupGame():
    global currentOrder = menu_to_recipe[SUSHI]
    global currentOrderWord = index_to_name[SUSHI]

def RunGame():
    
    while(true):



if __name__ == "__main__":
    signal.alarm(120)
    try:
        RunGame()
    except TimeoutException:
        print("Game Over")