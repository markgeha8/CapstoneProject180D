from tkinter import *

window = Tk()

window.title("Undercooked")
window.geometry('650x500')

line1 = Label(window, text="Current Recipe: Sushi", font=("Arial", 20))
line1.grid(column=0, row=0)

line2 = Label(window, text="Ingredients: Fish, Rice, Seaweed", font=("Arial", 20))
line2.grid(column=0, row=1)

line3 = Label(window, text="Plate: Fish", font=("Arial", 20))
line2.grid(column=0, row=2)

line4 = Label(window, text="Score: 10", font=("Arial", 20))
line4.grid(column=0, row=3)

window.mainloop()