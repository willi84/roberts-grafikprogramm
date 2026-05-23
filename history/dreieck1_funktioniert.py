from Tkinter import *
from Canvas import *
from time import *

def spiegelY(p1):
    maSpY={(0,0):-1,(0,1):0, (0,2):0,
           (1,0):0, (1,1):1, (1,2):0,
           (2,0):0, (2,1):0, (2,2):1}
    x=p1[0]*maSpY[(0,0)]+ p1[1]*maSpY[(0,1)]+p1[2]*maSpY[(0,2)]
    y=p1[0]*maSpY[(1,0)]+ p1[1]*maSpY[(1,1)]+p1[2]*maSpY[(1,2)]
    e=p1[0]*maSpY[(2,0)]+ p1[1]*maSpY[(2,1)]+p1[2]*maSpY[(2,2)]
    return {(0):x, (1):y, (2):e}
def spiegelX(p1):
    maSpX={(0,0):1, (0,1):0, (0,2):0,
           (1,0):0, (1,1):-1,(1,2):0,
           (2,0):0, (2,1):0, (2,2):1}
    x=p1[0]*maSpX[(0,0)]+ p1[1]*maSpX[(0,1)]+p1[2]*maSpX[(0,2)]
    y=p1[0]*maSpX[(1,0)]+ p1[1]*maSpX[(1,1)]+p1[2]*maSpX[(1,2)]
    e=p1[0]*maSpX[(2,0)]+ p1[1]*maSpX[(2,1)]+p1[2]*maSpX[(2,2)]
    return {(0):x, (1):y, (2):e}



h=200
w=320

#Original    
a1={(0):10.2, (1):10.7, (2):1}
a2={(0):20.2, (1):20.7, (2):1}
a3={(0):30.2, (1):10.7, (2):1}

'''#Bild
a1[1]-=2*a1[1]
a2[1]-=2*a2[1]
a3[1]-=2*a3[1]'''


#an y-Achse gespiegelt
y1=spiegelY(a1)
y2=spiegelY(a2)
y3=spiegelY(a3)

#an x-Achse gespiegelt
x1=spiegelX(a1)
x2=spiegelX(a2)
x3=spiegelX(a3)


root=Tk()
canvas=Canvas(root, width=w, height=h, bg="white")
canvas.grid()

canvas.create_line(160,0,160,200,width=2, arrow="first") #1
canvas.create_line(0,100,320,100,width=2, arrow="last")  #2
CanvasText(canvas,315,105,text="x") #3
CanvasText(canvas,153,5,  text="y") #4
"""
a1=(160,100)
a2=(180,100)
a3=(170,80)
"""

canvas.create_polygon((a1[0],-a1[1]),
                      (a2[0],-a2[1]),
                      (a3[0],-a3[1]),
                       outline="black", fill="white") #5
canvas.move(5,160,100)

canvas.create_polygon((y1[0],-y1[1]),
                      (y2[0],-y2[1]),
                      (y3[0],-y3[1]),
                       outline="black",fill="white" ) #6
canvas.move(6,160,100)

canvas.create_polygon((x1[0],-x1[1]),
                      (x2[0],-x2[1]),
                      (x3[0],-x3[1]),
                       outline="black", fill="white") #7
canvas.move(7,160,100)

root.mainloop()


