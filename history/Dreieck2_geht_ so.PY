# autor: Robert Willemelis
# datum: 28.04.2006
# was funktioniert: Eingabe mehrerer Koordinaten und eines Winkels, jedoch muss
# Programm nach einmal mal und einer darauffolgenden Spiegelanweisung noch neu
# gestartet werden

from Tkinter import *
from Canvas import *
from math import *

a=[];y=[];x=[];z=[];n=0;h=200;w=320; winkel=0;winkel=0
def setKoordinaten():
    x=int(entryX.get())
    y=int(entryY.get())
    a.append([x,y,1])
    entryX.delete(0,len(entryX.get()))
    entryY.delete(0,len(entryY.get()))
    print a
def originalliste():
    origListe=[]
    for i in a:
        origListe.extend(list(i))
    return origListe
        
    
    

def malen():
    global x
    global y
    global z
    global a
    y=spiegelY(a)
    x=spiegelX(a)
    z=spiegelNull(a,winkel)
    b=getBildKoord(a)
    print "aa:",a
    canvas.create_polygon(a,outline="black", fill="white")
    canvas.move(5, w/2, h/2)
    koordOriginal(a)
    
    #canvas.update()
def anYAchseSpiegeln():
    #aCopy=a[:]
    #print a
    #print "aCopy:",aCopy
    global y
    y=getBildKoord(y)
    print y
    print y
    canvas.create_polygon(y,outline="black", fill="white")
    canvas.move(6+n, w/2, h/2)
    koordOriginal(y)
def anXAchseSpiegeln():
    #aCopy=a[:]
    global x
    x=getBildKoord(x)
    canvas.create_polygon(x,outline="black", fill="white")
    canvas.move(6+n, w/2, h/2)
    koordOriginal(x)
def setWinkel():
    global winkel
    winkel=int(entryWinkel.get())
    entryWinkel.delete(0,len(entryWinkel.get()))
    
def amUrsprungSpiegeln():
    #aCopy=a[:]
    global z
    global winkel
    
    z=getBildKoord(z)
    canvas.create_polygon(z,outline="black", fill="white")
    canvas.move(6+n, w/2, h/2)
    koordOriginal(z)
    
def spiegelY(koord):
    spKoord=[]
    print "koord:",koord
    for i in koord:
        print i
        maSpY={(0,0):-1,(0,1):0, (0,2):0,
               (1,0):0, (1,1):1, (1,2):0,
               (2,0):0, (2,1):0, (2,2):1}
        x=i[0]*maSpY[(0,0)]+ i[1]*maSpY[(0,1)]+i[2]*maSpY[(0,2)]
        y=i[0]*maSpY[(1,0)]+ i[1]*maSpY[(1,1)]+i[2]*maSpY[(1,2)]
        e=i[0]*maSpY[(2,0)]+ i[1]*maSpY[(2,1)]+i[2]*maSpY[(2,2)]
        spKoord.append([x,y,1])
    return spKoord
def spiegelX(koord):
    spKoord=[]
    for i in koord:
        maSpX={(0,0):1, (0,1):0, (0,2):0,
               (1,0):0, (1,1):-1,(1,2):0,
               (2,0):0, (2,1):0, (2,2):1}
        x=i[0]*maSpX[(0,0)]+ i[1]*maSpX[(0,1)]+i[2]*maSpX[(0,2)]
        y=i[0]*maSpX[(1,0)]+ i[1]*maSpX[(1,1)]+i[2]*maSpX[(1,2)]
        e=i[0]*maSpX[(2,0)]+ i[1]*maSpX[(2,1)]+i[2]*maSpX[(2,2)]
        spKoord.append([x,y,1])
    return spKoord

def spiegelNull(koord,alpha):
    spKoord=[]
    for i in koord:
        maSpN={(0,0):cos(radians(alpha)), (0,1):(-sin(radians(alpha))), (0,2):0,
               (1,0):sin(radians(alpha)), (1,1):cos(radians(alpha))   , (1,2):0,
               (2,0):0,          (2,1):0            , (2,2):1}
        x=i[0]*maSpN[(0,0)]+ i[1]*maSpN[(0,1)]+i[2]*maSpN[(0,2)]
        y=i[0]*maSpN[(1,0)]+ i[1]*maSpN[(1,1)]+i[2]*maSpN[(1,2)]
        e=i[0]*maSpN[(2,0)]+ i[1]*maSpN[(2,1)]+i[2]*maSpN[(2,2)]
        spKoord.append([x,y,1])
    return spKoord

def getBildKoord(koord):
    bKoord=[]
    for i in koord:
        i.pop()
        i[1]=-i[1]
        bKoord.append(i)
    return bKoord
def koordOriginal(j):
    jKoord=[]
    for i in j:
        i.append(1)
        i[1]=-i[1]
        jKoord.append(i)
    return jKoord

'''def male_polygon(objekt,nr,koord,farbeLinie, farbeInnen, weite, hoehe):
    koord=getBildKoord(koord)
    objekt.create_polygon(koord,outline=farbeLinie, fill=farbeInnen)
    objekt.move(nr, weite/2, hoehe/2)'''

root=Tk()

frame1=Frame(root)
frame1.grid(row=0)
canvas=Canvas(frame1, width=w, height=h, bg="white")
canvas.grid(sticky=N)

frame2=Frame(root)
frame2.grid(row=1)
label=Label(frame2,text="Spiegeln:\n")
label.grid(sticky=N,column=0, row=0)

frame3=Frame(root)
frame3.grid(row=2)
button=Button(frame3,text="an y-Achse", command=anYAchseSpiegeln)
button.grid(column=0, row=0)
button=Button(frame3,text="an x-Achse", command=anXAchseSpiegeln)
button.grid(column=1, row=0)
button=Button(frame3,text="am Ursprung", command=amUrsprungSpiegeln)
button.grid(column=2, row=0)

frame4=Frame(root)
frame4.grid(row=3)
Label(frame4, text="").grid(row=3,column=0)
Label(frame4, text="x=").grid(row=4,column=0)
entryX=Entry(frame4)
entryX.grid(row=4, column=1)
Label(frame4, text="y=").grid(row=4, column=2)
entryY=Entry(frame4)
entryY.grid(row=4, column=3)
button=Button(frame4,text="eingeben", command=setKoordinaten)
button.grid(row=4, column=4)

frame5=Frame(root)
frame5.grid(row=5)
Label(frame5, text="Winkel in Grad:").grid(row=5, column=0)
entryWinkel=Entry(frame5)
entryWinkel.grid(row=5, column=1)
button=Button(frame5,text="eingeben", command=setWinkel)
button.grid(row=5, column=2)

frame6=Frame(root)
frame6.grid(row=6)
button=Button(frame6,text="malen", command=malen)
button.grid(row=6)

frame7=Frame(root)
frame7.grid(row=7)
button=Button(frame7,text="beenden", command=root.destroy)
button.grid(column=0)

canvas.create_line(160,0,160,200,width=2, arrow="first") #1
canvas.create_line(0,100,320,100,width=2, arrow="last")  #2
canvas.create_text(315,105,text="x") #3
canvas.create_text(153,5,text="y") #4


'''male_polygon(canvas,5,a,"black", "white",w,h)
male_polygon(canvas,6,x,"black", "white",w,h)
male_polygon(canvas,7,y,"black", "white",w,h)
male_polygon(canvas,8,z,"black", "white",w,h)'''
    


root.mainloop()


