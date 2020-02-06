from enum import Enum

# This makes enums return their name instead of number
class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

# Actions
class Gestures(AutoName):
    CHOP = auto()
    COOK = auto()
    TRASH = auto()
    NONE = auto()

# Menu Items
class MenuItem(AutoName):
    SUSHI = auto()
    SALAD = auto()

# Ingredients
class Ingredient(AutoName):
    RICE = auto()
    FISH = auto()
    SEAWEED = auto()
    LETTUCE = auto()
    TOMATO = auto()

# Ingredient Status
class IngredientStatus(AutoName):
    RAW = auto()
    COOKED = auto()
    PLATED = auto()

# Locations
class Locations(AutoName):
    CUTTINGBOARD = auto()
    STOVE = auto()
    TURNINSTATION = auto()
    PLAYER = auto()

# Actions
class Actions(AutoName):
    CHOP = auto()
    COOK = auto()
    PLATE = auto()
    TURNIN = auto()
    TRASH = auto()