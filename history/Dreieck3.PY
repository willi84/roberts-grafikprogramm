# autor: Robert Willemelis
# datum: 28.04.2006
# was funktioniert: Eingabe mehrerer Koordinaten und eines Winkels, jedoch muss
# Programm nach einmal mal und einer darauffolgenden Spiegelanweisung noch neu
# gestartet werden

from Tkinter import *
from Canvas import *
from math import *
from string import *
from tkMessageBox import *
from os import *


original=[];   ySpiegelung=[];  xSpiegelung=[]   # Listen = original: Original, y: Spiegelung an y-Achse, x: ... an x-Achse 
zStreckung=[]; pSpiegelung=[];  nSpiegelung=[]   # Listen = v: zentrische Streckung, z: Drehung
winkel=0; p=[]; k=0           # winkel: Drehwinkel, p: Spiegelungspunkt
h=430;    w=550         #      h: Höhe      , w: Weite 
n=0; m=0
xM=(w/2);     yM=(h/2)  #  xM:  Mittelpunk der x-Achse (x=0),        yM: ... der y-Achse (y=0)
x0=xM%50;     y0=yM%50  #  x0:  erste Markierung auf der x-Achse,    y0: ... auf der y-Achse
stX=-(xM-x0); stY=yM-y0 # stX: erster Markierungswert auf x-Achse,  stY: ... auf der y-Achse

c=unichr(169); al=unichr(945); gr=unichr(186) #Sonderzeichen = c: Copyright, al: Alpha, gr: Grad 

position=[]; zustand1=0
listePunkte=["z"]
def getKoordSystem():
    ''' Das Grundgerüst des Koordinatensystems zeichen. '''
    global xM; global yM; global x0; global y0; global stX; global stY
    #Achsen malen
    canvas.create_line(xM,0,xM,h,width=2, arrow="first") # id=1
    canvas.addtag_closest("y-Achse",xM, 0, xM, h)
    print canvas.coords("y-Achse")
    canvas.create_line(0,yM,w,yM,width=2, arrow="last")  # id=2
    canvas.create_text(w-5,yM+5,text="x") # id=3
    canvas.create_text(xM-7,5,text="y") # id=4
    print canvas.find_withtag("y-Achse")[0]
    
    
    #x-Achsen-Markierung
    for i in range(0,w+1,50):
        canvas.create_line(x0+i, yM-3, x0+i, yM+3, width=1)
        if stX+i!=0:
            canvas.create_text(x0+i, yM+9, text=str(stX+i), font=("Arial",8))
        else:            
            canvas.create_text(x0+i+5, yM+9, text=str(stX+i), font=("Arial",8))
            
    #y-Achsen-Markierung
    for i in range(0,h+1,50):
        canvas.create_line(xM-3, y0+i, xM+3, y0+i, width=1)
        if stY-i!=0:
            canvas.create_text(xM+15, y0+i-1, text=str(stY-i), font=("Arial",8))
    
def setKoordinaten():
    global original
    # Vorbereitung für float: Kommata in Punkte, Entfernung von Leerzeichen
    kX=rstrip(lstrip(replace(entryX.get(),",", ".")))
    kY=rstrip(lstrip(replace(entryY.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if kX and kY != "":
        weiter=wertTest(kX, 0)
        if weiter==True:
            weiter=wertTest(kY, 0)
            if weiter==True:
                x=float(kX)
                y=float(kY)
                original.append([x,y,1])
    if kX=="":
        showinfo("Koordinateneingabe",
                 "Punkt konnte nicht eingegeben werden, da das x fehlt!")
    if kY=="":
        showinfo("Koordinateneingabe",
                 "Punkt konnte nicht eingegeben werden, da das y fehlt!")
    entryX.delete(0,len(entryX.get()))
    entryY.delete(0,len(entryY.get()))

def nKoordEingeben():
    nKoordRoot=Tk()
    Label(nKoordRoot, text="Mehrere Punkte eingeben").pack(fill=X)

    n1=Frame(nKoordRoot)
    n1.pack(fill=X)
    Label(n1,text="x=").pack(side=LEFT)
    n1_XEntry=Entry(n1,width=7)
    n1_XEntry.pack(side=LEFT)
    Label(n1,text="y=").pack(side=LEFT)
    n1_YEntry=Entry(n1,width=7)
    n1_YEntry.pack(side=LEFT)

    n2=Frame(nKoordRoot)
    n2.pack(fill=X)
    Label(n2,text="x=").pack(side=LEFT)
    n2_XEntry=Entry(n2,width=7)
    n2_XEntry.pack(side=LEFT)
    Label(n2,text="y=").pack(side=LEFT)
    n2_YEntry=Entry(n2,width=7)
    n2_YEntry.pack(side=LEFT)

    n3=Frame(nKoordRoot)
    n3.pack(fill=X)
    Label(n3,text="x=").pack(side=LEFT)
    n3_XEntry=Entry(n3,width=7)
    n3_XEntry.pack(side=LEFT)
    Label(n3,text="y=").pack(side=LEFT)
    n3_YEntry=Entry(n3,width=7)
    n3_YEntry.pack(side=LEFT)

    n4=Frame(nKoordRoot)
    n4.pack(fill=X)
    Label(n4,text="x=").pack(side=LEFT)
    n4_XEntry=Entry(n4,width=7)
    n4_XEntry.pack(side=LEFT)
    Label(n4,text="y=").pack(side=LEFT)
    n4_YEntry=Entry(n4,width=7)
    n4_YEntry.pack(side=LEFT)

    n5=Frame(nKoordRoot)
    n5.pack(fill=X)
    Label(n5,text="x=").pack(side=LEFT)
    n5_XEntry=Entry(n5,width=7)
    n5_XEntry.pack(side=LEFT)
    Label(n5,text="y=").pack(side=LEFT)
    n5_YEntry=Entry(n5,width=7)
    n5_YEntry.pack(side=LEFT)

    def getNKoordinaten(eingabeX, eingabeY):
        global original
        # Vorbereitung für float: Kommata in Punkte, Entfernung von Leerzeichen
        kX=rstrip(lstrip(replace(eingabeX.get(),",", ".")))
        kY=rstrip(lstrip(replace(eingabeY.get(),",", ".")))
        weiter=True
        # Zahlen mit nur 1 Koordinate werden nicht eingegeben
        if kX and kY != "":
            weiter=wertTest(kX, 0)
            if weiter==True:
                weiter=wertTest(kX, 0)
                if weiter==True:
                    x=float(kX)
                    y=float(kY)
                    original.append([x,y,1])
        if kX=="" and kY !="":
            showinfo("Koordinateneingabe",
                     "Ein Punkt konnte nicht eingegeben werden, da das x fehlte!")
        if kY=="" and kX !="":
            showinfo("Koordinateneingabe",
                     "Ein Punkt konnte nicht eingegeben werden, da das y fehlte!")
        
    
    def setNKoordinaten():
        getNKoordinaten(n1_XEntry,n1_YEntry)
        getNKoordinaten(n2_XEntry,n2_YEntry)
        getNKoordinaten(n3_XEntry,n3_YEntry)
        getNKoordinaten(n4_XEntry,n4_YEntry)
        getNKoordinaten(n5_XEntry,n5_YEntry)
        print original
        nKoordRoot.destroy()
    
    Button(nKoordRoot, text="eingeben", command=setNKoordinaten).pack()
    nKoordRoot.mainloop()

def setWinkel():
    global winkel
    winkel=rstrip(lstrip(replace(entryWinkel.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if winkel != "":
        weiter=wertTest(winkel, 2)
        if weiter==True:
            winkel=float(winkel)
    if winkel =="":
        showinfo("Winkeleingabe",
                 "Sie haben keinen Winkel eingegeben!")
    entryWinkel.delete(0,len(entryWinkel.get()))

def setK():
    global k
    k=rstrip(lstrip(replace(kEntry.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if k != "":
        weiter=wertTest(k, 3)
        if weiter==True:
            k=float(k)
    if k =="":
        showinfo("Streckungsfaktor",
                 "Sie haben keinen Streckungsfaktor k eingegeben!")
    kEntry.delete(0,len(kEntry.get()))

def setP():
    global p
    x=rstrip(lstrip(replace(entrySpPunktX.get(),",", ".")))
    y=rstrip(lstrip(replace(entrySpPunktY.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if x and y != "":
        weiter=wertTest(x, 1)
        if weiter==True:
            weiter=wertTest(y, 1)
            if weiter==True:
                x=float(x)
                y=float(y)
                p.append([x,y,1])
    if x=="":
        showinfo("Spiegelpunkteingabe",
                 "Spiegelpunkt konnte nicht eingegeben werden, da das x fehlt!")
    if x=="":
        showinfo("Spiegelpunkteingabe",
                 "Spiegelpunkt konnte nicht eingegeben werden, da das y fehlt!")
    entrySpPunktX.delete(0,len(entrySpPunktX.get()))
    entrySpPunktY.delete(0,len(entrySpPunktY.get()))

def originalliste():
    origListe=[]
    for i in original:
        origListe.extend(list(i))
    return origListe
        
def malen():
    print getcwd()
    global original
    global n; global xM; global yM
    n=max(canvas.find_all()); print n; n+=1
    original=getBildKoord(original)
    canvas.create_polygon(original,outline="black", fill="white")
    canvas.move(n, xM, yM)
    original=getOriginalKoord(original)
    #canvas.update()
def anYAchseSpiegeln():
    global original; global ySpiegelung
    global n; global xM; global yM
    ySpiegelung=spiegelY(original)
    ySpiegelung=getBildKoord(ySpiegelung)
    canvas.create_polygon(ySpiegelung,outline="black", fill="white"); n+=1
    canvas.move(n, xM, yM)
    ySpiegelung=getOriginalKoord(ySpiegelung)
def anXAchseSpiegeln():
    global original; global xSpiegelung
    global n; global xM; global yM
    xSpiegelung=spiegelX(original)
    xSpiegelung=getBildKoord(xSpiegelung)
    canvas.create_polygon(xSpiegelung,outline="black", fill="white"); n+=1
    canvas.move(n, xM, yM)
    xSpiegelung=getOriginalKoord(xSpiegelung)
    
def amUrsprungSpiegeln():
    global original; global nSpiegelung; global winkel
    global n; global xM; global yM
    nSpiegelung=spiegelNull(original, winkel)
    nSpiegelung=getBildKoord(nSpiegelung)
    canvas.create_polygon(nSpiegelung,outline="black", fill="white"); n+=1 #fill="white"
    canvas.move(n, xM, yM)
    nSpiegelung=getOriginalKoord(nSpiegelung)

def anPSpiegeln():
    global original; global pSpiegelung
    global n; global xM; global yM; global winkel; global p
    pSpiegelung=spiegelP(original, winkel, p)
    pSpiegelung=getBildKoord(pSpiegelung)
    canvas.create_polygon(pSpiegelung,outline="black", fill="white"); n+=1
    canvas.move(n, xM, yM)
    pSpiegelung=getOriginalKoord(pSpiegelung)

def zenStrecken():
    global original; global zStreckung
    global n; global xM; global yM; global k
    zStreckung=zentrischeStreckung(original,k)
    zStreckung=getBildKoord(zStreckung)
    canvas.create_polygon(zStreckung,outline="black", fill="white"); n+=1
    canvas.move(n, xM, yM)
    zStreckung=getOriginalKoord(zStreckung)
    
def spiegelY(koord):
    spKoord=[]
    for i in koord:
        maSpY={(0,0):-1,(0,1):0, (0,2):0, 
               (1,0):0 ,(1,1):1, (1,2):0, 
               (2,0):0 ,(2,1):0, (2,2):1 } 
        
        x=i[0]*maSpY[(0,0)]+ i[1]*maSpY[(0,1)]+1*maSpY[(0,2)]
        y=i[0]*maSpY[(1,0)]+ i[1]*maSpY[(1,1)]+1*maSpY[(1,2)]
        e=i[0]*maSpY[(2,0)]+ i[1]*maSpY[(2,1)]+1*maSpY[(2,2)]
        canvas.create_oval(x-1, y-1, x+1, y+1)
        spKoord.append([x,y,1])
    return spKoord
def spiegelX(koord):
    spKoord=[]
    for i in koord:
        maSpX={(0,0):1, (0,1):0, (0,2):0,
               (1,0):0, (1,1):-1,(1,2):0,
               (2,0):0, (2,1):0, (2,2):1 }
        x=i[0]*maSpX[(0,0)]+ i[1]*maSpX[(0,1)]+1*maSpX[(0,2)]
        y=i[0]*maSpX[(1,0)]+ i[1]*maSpX[(1,1)]+1*maSpX[(1,2)]
        e=i[0]*maSpX[(2,0)]+ i[1]*maSpX[(2,1)]+1*maSpX[(2,2)]
        spKoord.append([x,y,1])
    return spKoord

def spiegelNull(koord, alpha):
    spKoord=[]
    for i in koord:
        maSpN={(0,0):cos(radians(alpha)), (0,1):(-sin(radians(alpha))), (0,2):0,
               (1,0):sin(radians(alpha)), (1,1):cos(radians(alpha))   , (1,2):0,
               (2,0):0                  , (2,1):0                     , (2,2):1 }
        x=i[0]*maSpN[(0,0)]+ i[1]*maSpN[(0,1)]+1*maSpN[(0,2)]
        y=i[0]*maSpN[(1,0)]+ i[1]*maSpN[(1,1)]+1*maSpN[(1,2)]
        e=i[0]*maSpN[(2,0)]+ i[1]*maSpN[(2,1)]+1*maSpN[(2,2)]
        spKoord.append([x,y,1])
    return spKoord

def spiegelP(koord, alpha, pkt):
    spKoord=[]
    for i in koord:
        i[0]=float(i[0])
        i[1]=float(i[1])
        i[0]-=float(pkt[0])
        i[1]-=float(pkt[1])
        maSpN={(0,0):cos(radians(alpha)), (0,1):(-sin(radians(alpha))), (0,2):0,
               (1,0):sin(radians(alpha)), (1,1):cos(radians(alpha))   , (1,2):0,
               (2,0):0                  , (2,1):0                     , (2,2):1 }
        x=i[0]*maSpN[(0,0)]+ i[1]*maSpN[(0,1)]+1*maSpN[(0,2)]
        y=i[0]*maSpN[(1,0)]+ i[1]*maSpN[(1,1)]+1*maSpN[(1,2)]
        e=i[0]*maSpN[(2,0)]+ i[1]*maSpN[(2,1)]+1*maSpN[(2,2)]
        x+=float(pkt[0])
        y+=float(pkt[1])
        spKoord.append([x,y,1])
    return spKoord

def zentrischeStreckung(koord, k):
    spKoord=[]
    for i in koord:
        maSpN={(0,0):k, (0,1):0,(0,2):0,
               (1,0):0, (1,1):k,(1,2):0,
               (2,0):0, (2,1):0,(2,2):1 }
        x=i[0]*maSpN[(0,0)]+ i[1]*maSpN[(0,1)]+1*maSpN[(0,2)]
        y=i[0]*maSpN[(1,0)]+ i[1]*maSpN[(1,1)]+1*maSpN[(1,2)]
        e=i[0]*maSpN[(2,0)]+ i[1]*maSpN[(2,1)]+1*maSpN[(2,2)]
        spKoord.append([x,y,1])
    return spKoord
    
def getBildKoord(koord):
    bKoord=[]
    for i in koord:
        i.pop()
        i[1]=-i[1]
        bKoord.append(i)
    print bKoord
    return bKoord
def getOriginalKoord(bKoord):
    koord=[]
    for i in bKoord:
        i.append(1)
        i[1]=-i[1]
        koord.append(i)
    return koord

def wertTest(x, hX):
    head=["Koordinateneingabe", "Spiegelpunktseingabe",
          "Winkeleingabe", "Eingabe des Streckungsfaktors"]
    zulaessig=["0","1","2","3","4","5","6","7","8","9","."]
    wort=head[hX]
    richtig=True
    for i in x:
        if i not in zulaessig:
            if i==x[0] and i=="-":
                pass
            else:
                showinfo(wort,
                         "Bitte geben Sie wirklich nur Zahlen ein!")
                richtig=False
        if x.count(".")>1:
            showinfo(wort,
                     "Bei Dezimalzahlen gibt es nur ein Kommata!\n Viel Spass beim Klicken!")
            richtig=False
    return richtig

def getCursorPos(event):
    t="("+str(event.x-xM)+"/"+str(-(event.y-yM))+")"
    pos.delete("0.0",END)
    pos.insert("0.0",t)

def setNull(event):
    pos.delete("0.0",END)

def punktZeichnen(event):
    n=max(canvas.find_all())
    n=n+2; m+=1
    punkt=["P"+str(m),n-1,n,event.x,event.y,1]
    x #getBildKoord
    y #getBildKoord
    canvas.create_oval(punkt[4]-1, punkt[5]-1, punkt[4]+1,punkt[5]+1, outline=black)
    canvas.create_text(punt[4]-3, punkt[5]+3, text=punkt[0])
    canvas.move(n-1, xM, yM)
    canvas.move(n, xM, yM)
    
    

def punkteVerbinden():
    if zustand1.get==0:
        canvas.bind("<Button-1>", punktZeichenen)
    
    
    
    
    
    
    

    


#----1. Start des Masters ----------------------------------------------------------
root=Tk()
root.title("Roberts Grafikprogramm")


#-------


#----2. Beginn Menueoptionsleiste -------------------------

menueleiste=Menu(root)
aktionsmenue=Menu(menueleiste)
spiegelnmenue=Menu(menueleiste)
hilfemenue=Menu(menueleiste)

menueleiste.add_cascade(menu=aktionsmenue, label="Aktionen")
menueleiste.add_cascade(menu=spiegelnmenue, label="Spiegeln")
menueleiste.add_cascade(menu=hilfemenue, label="?")

aktionsmenue.add_command(label="Neu")
aktionsmenue.add_separator()
aktionsmenue.add_command(label="Malen")
aktionsmenue.add_separator()
aktionsmenue.add_command(label="Aktuelles Objekt löschen")
aktionsmenue.add_command(label="Bestimmtes Objekt löschen")
aktionsmenue.add_command(label="Alle Objekte löschen")
aktionsmenue.add_separator()
aktionsmenue.add_command(label="Liste aller Objekte")
aktionsmenue.add_command(label="Liste aller Koordinaten")
aktionsmenue.add_separator()
aktionsmenue.add_command(label="Programm beenden", command=root.destroy)

spiegelnmenue.add_command(label="... an der x-Achse", command=anXAchseSpiegeln)
spiegelnmenue.add_command(label="... an der y-Achse", command=anYAchseSpiegeln)
spiegelnmenue.add_separator()
spiegelnmenue.add_command(label="... am Ursprung", command=amUrsprungSpiegeln)
spiegelnmenue.add_command(label="... an einem bestimmten Punkt", command=anPSpiegeln)
spiegelnmenue.add_separator()
spiegelnmenue.add_command(label="Zentrische Streckung", command=zenStrecken)

hilfemenue.add_command(label="Programmbeschreibung")
hilfemenue.add_command(label="Impressum")

root.config(menu=menueleiste)

#----2. Ende Menueoptionsleiste ---------------------------


#----3. Beginn des Arbeitsbereiches ----------------------- 
arbeitsbereich=Frame(root, relief="groove", border=2)
arbeitsbereich.pack()
#Zeichenfläche mit Canvas-Widget
zeichenbrett=Frame(arbeitsbereich)
zeichenbrett.pack(side=LEFT)
canvas=Canvas(zeichenbrett, width=w, height=h, bg="white")
canvas.grid()
getKoordSystem()
canvas.bind("<Motion>", getCursorPos)
canvas.bind("<Leave>", setNull)

    
#Eingabebereich
eingabefenster=Frame(arbeitsbereich, border=2)
eingabefenster.pack(side=RIGHT, fill=BOTH)
#---
Label(eingabefenster, text="  ").pack()
buttons=Frame(eingabefenster)
buttons.pack()
buttonNeueFigur=Button(buttons, text="neue Figur")
buttonNeueFigur.pack(fill=X)
buttonPunkteVerbinden=Checkbutton(buttons,indicatoron=0,text="Punkte verbinden", variable=zustand1)
buttonPunkteVerbinden.pack(fill=X)
buttonFigurdaten=Button(buttons, text="Figurdaten")
buttonFigurdaten.pack(fill=X)
Label(eingabefenster, text="  ").pack()

koordinatenfenster=Frame(eingabefenster, relief="groove", border=2)
koordinatenfenster.pack(fill=X)
Label(koordinatenfenster, text="Koordinaten eines Punktes:").pack(fill=X)
koordEingabe=Frame(koordinatenfenster)
koordEingabe.pack(fill=X)
Label(koordEingabe, text="x=").pack(side=LEFT)
entryX=Entry(koordEingabe, width=4)
entryX.pack(side=LEFT)
Label(koordEingabe, text="y=").pack(side=LEFT)
entryY=Entry(koordEingabe, width=4)
entryY.pack(side=LEFT)
Label(koordEingabe, text="  ").pack(side=LEFT)
buttonKoordEingeben=Button(koordEingabe, text="eingeben")
buttonKoordEingeben.pack(side=LEFT)
Label(koordinatenfenster, text="  ").pack()
buttonNPunkteEingeben=Button(koordinatenfenster, text="mehrere Punkte eingeben")
buttonNPunkteEingeben.pack(fill=X)
Label(eingabefenster, text="  ").pack()

spiegelpunktfenster=Frame(eingabefenster, relief="groove", border=2)
spiegelpunktfenster.pack(fill=X)
Label(spiegelpunktfenster, text="Spiegelpunkt:").pack(fill=X)
spiegelpunktEingabe=Frame(spiegelpunktfenster)
spiegelpunktEingabe.pack(fill=X)
Label(spiegelpunktEingabe, text="x=").pack(side=LEFT)
entrySpPunktX=Entry(spiegelpunktEingabe, width=4)
entrySpPunktX.pack(side=LEFT)
Label(spiegelpunktEingabe, text="y=").pack(side=LEFT)
entrySpPunktY=Entry(spiegelpunktEingabe, width=4)
entrySpPunktY.pack(side=LEFT)
Label(spiegelpunktEingabe, text="  ").pack(side=LEFT)
buttonSpiegelpunktEingeben=Button(spiegelpunktEingabe, text="eingeben")
buttonSpiegelpunktEingeben.pack(side=LEFT)

drehwinkelfenster=Frame(eingabefenster, relief="groove", border=2)
drehwinkelfenster.pack(fill=X)
Label(drehwinkelfenster, text="Drehwinkel:").pack(fill=X)
winkelEingabe=Frame(drehwinkelfenster)
winkelEingabe.pack(fill=X)
Label(winkelEingabe, text=al+"=").pack(side=LEFT)
entryWinkel=Entry(winkelEingabe, width=4)
entryWinkel.pack(side=LEFT)
Label(winkelEingabe, text=gr).pack(side=LEFT)
buttonWinkelEingeben=Button(winkelEingabe, text="eingeben")
buttonWinkelEingeben.pack(side=RIGHT)


streckungsfenster=Frame(eingabefenster, relief="groove", border=2)
streckungsfenster.pack(fill=X)
Label(streckungsfenster, text="Streckungsfaktor:").pack(fill=X)
kEingabe=Frame(streckungsfenster)
kEingabe.pack(fill=X)
Label(kEingabe, text="k=").pack(side=LEFT)
entryK=Entry(kEingabe, width=4)
entryK.pack(side=LEFT)
buttonKEingeben=Button(kEingabe, text="eingeben")
buttonKEingeben.pack(side=RIGHT)

Label(eingabefenster, text=" ").pack()
Label(eingabefenster, text="Cursor: ").pack(side=LEFT)
pos=Text(eingabefenster, width=10, height=1)
pos.pack(side=LEFT)




'''koordFenster=Frame(eingabefenster,relief="groove", border=2)
koordFenster.pack(fill=X)
koordTitle=Frame(koordFenster)
koordTitle.pack(fill=X)
Label(koordTitle, text="Figur").pack()
Label(koordTitle, text="Koordinaten eines Punktes: ").pack(side=LEFT)
koord=Frame(koordFenster)
koord.pack(fill=X)
Label(koord, text="x=").pack(side=LEFT)
entryX=Entry(koord, width=7)
entryX.pack(side=LEFT)
Label(koord, text="y=").pack(side=LEFT)
entryY=Entry(koord, width=7)
entryY.pack(side=LEFT)
koordEingeben=Frame(koordFenster)
koordEingeben.pack(fill=X)
eingabebuttonKoord=Checkbutton(koordEingeben,indicatoron=0, width=8,
                               text="eingeben",command=setKoordinaten)
eingabebuttonKoord.pack()
#---
nKoord=Frame(eingabefenster,relief="groove", border=2)
nKoord.pack(fill=X)
Label(nKoord,text="Koordinaten mehrer Punkte:").pack()
eingabebuttonNKoord=Button(nKoord,text="eingeben", command=nKoordEingeben)
eingabebuttonNKoord.pack()
Label(eingabefenster, text=" ").pack()
male=Button(eingabefenster, text="   Figur malen   ", command=malen)
male.pack()
Label(eingabefenster, text=" ").pack()
#---
winkelFenster=Frame(eingabefenster,relief="groove", border=2)
winkelFenster.pack(fill=X)
winkelTitle=Frame(winkelFenster)
winkelTitle.pack(fill=X)
Label(winkelTitle, text="Drehwinkel: ").pack(side=LEFT)
winkelGet=Frame(winkelFenster)
winkelGet.pack(fill=X)
Label(winkelGet, text=al+"=").pack(side=LEFT)
entryWinkel=Entry(winkelGet, width=18)
entryWinkel.pack(side=LEFT)
Label(winkelGet, text=gr).pack(side=LEFT)
winkelEingeben=Frame(winkelFenster)
winkelEingeben.pack(fill=X)
Label(winkelEingeben, text=" ").pack()
eingabebuttonWinkel=Button(winkelEingeben,text="eingeben", command=setWinkel)
eingabebuttonWinkel.pack()
#---
spPunktFenster=Frame(eingabefenster,relief="groove", border=2)
spPunktFenster.pack(fill=X)
spPunktTitle=Frame(spPunktFenster)
spPunktTitle.pack(fill=X)
Label(spPunktTitle, text="Spiegelpunkt: P (x/y) ").pack(side=LEFT)
spPunktGet=Frame(spPunktFenster)
spPunktGet.pack(fill=X)
Label(spPunktGet, text="P (").pack(side=LEFT)
entrySpPunktX=Entry(spPunktGet, width=7)
entrySpPunktX.pack(side=LEFT)
Label(spPunktGet, text="/").pack(side=LEFT)
entrySpPunktY=Entry(spPunktGet, width=7)
entrySpPunktY.pack(side=LEFT)
Label(spPunktGet, text=")").pack(side=LEFT)
spPunktEingeben=Frame(spPunktFenster)
spPunktEingeben.pack(fill=X)
pos=Text(spPunktEingeben, width=10, height=1)
pos.pack()




eingabebuttonSpPunkt=Button(spPunktEingeben,text="eingeben", command=setP)
eingabebuttonSpPunkt.pack()
#---
zentrStrecken=Frame(eingabefenster,relief="groove", border=2)
zentrStrecken.pack(fill=X)
Label(zentrStrecken, text="Zentrische Streckung um:").pack()
streckung=Frame(zentrStrecken)
streckung.pack()
Label(streckung, text="k=").pack(side=LEFT)
kEntry=Entry(streckung, width=12)
kEntry.pack(side=LEFT)
eingabebuttonK=Button(zentrStrecken, text="eingeben", command=setK)
eingabebuttonK.pack()'''


#----3. Ende des Arbeitsbereiches -------------------------


#----4. Beginn der Abspannsleiste -------------------------
abspann=Frame(root)
abspann.pack()
info=Label(abspann, text=c+" 2006 Robert Willemelis ")
info.pack()
#----4. Ende der Abspannsleiste ---------------------------


#-------
root.mainloop()
#----1. Ende des Masters -----------------------------------------------------------
