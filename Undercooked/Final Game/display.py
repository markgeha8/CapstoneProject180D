from tkinter import *

def setupDisplay(line1txt, line2txt, line3txt, line4txt):
    window.title("Undercooked")
    window.geometry('650x500')

    line1txt.set("Current Recipe: ")

    line2txt.set("Ingredients: ")

    line3txt.set("Plate: ")

    line4txt.set("Score: ")

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

    line9 = Label(window, text="Items chopped on cuttingboard:", font=("Arial", 20), justify=LEFT)
    line9.pack()

    line10 = Label(window, text="Fish, Tomato, Lettuce", font=("Arial", 20), justify=LEFT)
    line10.pack()



line1Str = "1"
line2Str = "2"
line3Str = "3"
line4Str = "4"

while True:
    line1txt.set("Current Recipe: " + line1Str)
    line2txt.set("Ingredients: " + line2Str)
    line3txt.set("Plate: " + line3Str)
    line4txt.set("Score: " + line4Str)

    window.update()
