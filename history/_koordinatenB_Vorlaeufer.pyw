from Tkinter import *
from Canvas import *
from time import *



root=Tk()
canvas=Canvas(root, width=320, height=200, bg="white")
canvas.grid()

canvas.create_line(160,0,160,200,width=2)
canvas.create_line(0,100,320,100,width=2)

canvas.create_polygon((185,25),(235,25),(235,75),(185,75), outline="black", fill="white")
CanvasText(canvas,210,50,text="Original")
canvas.create_polygon((185,25),(235,25),(235,75),(185,75), outline="black", fill="white")
CanvasText(canvas,210,50,text="Spiegelbild")
canvas.move(5,-100,100)
canvas.move(6,-100,100)
root.mainloop()



