from Tkinter import *
from Canvas import *



root=Tk()
canvas=Canvas(root, width=320, height=200, bg="white")
canvas.grid()

canvas.create_oval(159,99,161,101, fill="black")
CanvasText(canvas,160,90,text="A")
canvas.move(1,-100,-20)
canvas.move(2,-100,-20)

canvas.create_oval(159,99,161,101, fill="black")
CanvasText(canvas,160,110,text="B")
canvas.move(3,100,20)
canvas.move(4,100,20)

canvas.create_line(160,0,160,200,width=2)
canvas.create_line(0,100,320,100,width=2)



root.mainloop()

