from tkinter import *

window = Tk()

window.title("Undercooked")
window.geometry('650x500')

line1 = "1"
line2 = "2"
line3 = "3"
line4 = "4"

line1txt = StringVar()
line1txt.set("Current Recipe: ")

line2txt = StringVar()
line2txt.set("Ingredients: ")

line3txt = StringVar()
line3txt.set("Plate: ")

line4txt = StringVar()
line4txt.set("Score: ")

line1 = Label(window, textvariable=line1txt, font=("Arial", 20), justify=LEFT)
line1.pack()

line2 = Label(window, textvariable=line2txt, font=("Arial", 20), justify=LEFT)
line2.pack()

line3 = Label(window, textvariable=line3txt, font=("Arial", 20), justify=LEFT)
line3.pack()

line4 = Label(window, textvariable=line4txt, font=("Arial", 20), justify=LEFT)
line4.pack()

while True:
    sleep(1) # Need this to slow the changes down
    line1txt.set("Current Recipe: " + line1)
    line2txt.set("Ingredients: " + line2)
    line3txt.set("Plate: " + line3)
    line4txt.set("Score: " + line4)

    root.update_idletasks()
