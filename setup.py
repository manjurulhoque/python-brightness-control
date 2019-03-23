from tkinter import Tk
from Gui import *

root = Tk()
app = Gui(root)  # Initialize our GUI

w = 400  # width for the window
h = 100  # height for the window

# get screen width and height
ws = app.master.winfo_screenwidth()  # width of the screen
hs = app.master.winfo_screenheight()  # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)

# set the dimensions of the screen
app.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
app.master.mainloop()
