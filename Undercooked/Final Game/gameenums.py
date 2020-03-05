from enum import Enum, auto

# This makes enums return their name instead of number
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

# Gestures
class Gesture(AutoName):
    CHOP = auto()
    COOK = auto()
    NONE = auto()

# Menu Items
class MenuItem(AutoName):
    SUSHI = auto()
    SALAD = auto()
    GRILLEDCHICKEN = auto()

# Ingredients
class Ingredient(AutoName):
    RICE = auto()
    FISH = auto()
    SEAWEED = auto()
    LETTUCE = auto()
    TOMATO = auto()
    CHICKEN = auto()
    NONE = auto()

# Ingredient Status
class IngredientStatus(AutoName):
    RAW = auto()
    COOKED = auto()

# Locations
class Location(AutoName):
    CUTTINGBOARD = auto()
    STOVE = auto()
    SUBMITSTATION = auto()
    NONE = auto()

# Voice Commands
class VoiceCommand(AutoName):
    PLATE = auto()
    SUBMIT = auto()
    TRASH = auto()
    NONE = auto()