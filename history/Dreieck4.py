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
winkel=0; p=[0,0]; k=0           # winkel: Drehwinkel, p: Spiegelungspunkt
h=430;    w=550         #      h: Hoehe      , w: Weite 
m=0;n=0; ascii=65
xM=(w/2);     yM=(h/2)  #  xM:  Mittelpunk der x-Achse (x=0),        yM: ... der y-Achse (y=0)
x0=xM%50;     y0=yM%50  #  x0:  erste Markierung auf der x-Achse,    y0: ... auf der y-Achse
stX=-(xM-x0); stY=yM-y0 # stX: erster Markierungswert auf x-Achse,  stY: ... auf der y-Achse

c=unichr(169); al=unichr(945); gr=unichr(186) #Sonderzeichen = c: Copyright, al: Alpha, gr: Grad 
idArt={}; objekt="Figur"+unichr(ascii)
position=[]; zustand=0


p1=[]; p2=[]

def getKoordSystem():
    ''' Das Grundgerüst des Koordinatensystems zeichen. '''
    global xM; global yM; global x0; global y0; global stX; global stY
    global idArt
    #Achsen malen
    idArt[canvas.create_line(xM,0,xM,h,width=2, arrow="first")]="line"
    canvas.addtag_overlapping("KS",xM,0,xM,h)
    idArt[canvas.create_line(0,yM,w,yM,width=2, arrow="last")]="line"
    canvas.addtag_overlapping("KS",0,yM,w,yM)
    idArt[canvas.create_text(w-5,yM+5,text="x")]="text"
    canvas.addtag_overlapping("KS",w-5,yM+5,w-5,yM+5)
    idArt[canvas.create_text(xM-7,5,text="y")]="text"
    canvas.addtag_overlapping("KS",xM-7,5,xM-7,5)
    
    #x-Achsen-Markierung
    for i in range(0,w+1,50):
        idArt[canvas.create_line(x0+i, yM-3, x0+i, yM+3, width=1)]="line"
        canvas.addtag_overlapping("KS",x0+i,yM-3,x0+i,yM+3)
        if stX+i!=0:
            idArt[canvas.create_text(x0+i, yM+9, text=str(stX+i), font=("Arial",8))]="text"
            canvas.addtag_overlapping("KS",x0+i,yM+9,x0+i,yM+9)
        else:            
            idArt[canvas.create_text(x0+i+5, yM+9, text=str(stX+i), font=("Arial",8))]="text"
            canvas.addtag_overlapping("KS",x0+i+5,yM+9,x0+i+5,yM+9)
            
    #y-Achsen-Markierung
    for i in range(0,h+1,50):
        idArt[canvas.create_line(xM-3, y0+i, xM+3, y0+i, width=1)]="line"
        canvas.addtag_overlapping("KS",xM-3,y0+i,xM+3,y0+i)
        if stY-i!=0:
            idArt[canvas.create_text(xM+15, y0+i-1, text=str(stY-i), font=("Arial",8))]="text"
            canvas.addtag_overlapping("KS",xM+15,y0+i-1,xM+15,y0+i-1)
    
def setKoordinaten():
    global n; global idArt; global ascii
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
                n+=1
                idArt[canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill="red")]="oval"
                canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM)
                idArt[canvas.create_text(x-2+xM+1,-(y-2+13)+yM,text=unichr(ascii)+str(n), font=("Arial",8,"bold"))]="text"
                canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM-5,x+2+xM,-(y+2)+yM-5)
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
    nKoordRoot.title("Eingabe mehrerer Punkte")
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
        global idArt; global n; global ascii
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
                    n+=1
                    idArt[canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill="red")]="oval"
                    canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM)
                    idArt[canvas.create_text(x-2+xM+1,-(y-2+13)+yM,text=unichr(ascii)+str(n), font=("Arial",8,"bold"))]="text"
                    canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM-5,x+2+xM,-(y+2)+yM-5)
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
        nKoordRoot.destroy()
    
    jkl=Button(nKoordRoot, text="eingeben", command=setNKoordinaten)
    jkl.pack()
    nKoordRoot.mainloop()
def neueFigur():
    global ascii; global n; global objekt
    ascii+=1
    objekt="Figur"+unichr(ascii)
    n=0
    

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
    k=rstrip(lstrip(replace(entryK.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if k != "":
        weiter=wertTest(k, 3)
        if weiter==True:
            k=float(k)
    if k =="":
        showinfo("Streckungsfaktor",
                 "Sie haben keinen Streckungsfaktor k eingegeben!")
    entryK.delete(0,len(entryK.get()))

def setP():
    global p; global n; global idArt; global ascii; global objekt
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
                p=[x,y]
                n+=1
                idArt[canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill="black")]="oval"
                canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM)
                idArt[canvas.create_text(x-2+xM+1,-(y-2+13)+yM,text=unichr(ascii)+str(n)+"("+al+")", font=("Arial",8,"bold"))]="text"
                canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM-5,x+2+xM,-(y+2)+yM-5)
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
        

def anYAchseSpiegeln():
    global objekt; global idArt; global m; m+=1; n=0
    listeElemente=[]
    listeElemente=canvas.find_withtag(objekt)
    print canvas.find_withtag("KS")
    print
    print objekt
    print listeElemente
    for i in listeElemente:
        print i
        print canvas.coords(i)
        koord=canvas.coords(i)
        if idArt[i]=="oval":
            x1=koord[0]+2-xM
            y1=-koord[1]-2+yM
            listeKoord=spiegelY([x1, y1])
            x=listeKoord[0]
            y=listeKoord[1]
            idArt[canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill="blue")]="oval"
            canvas.addtag_overlapping(objekt+"Spiegelbild",x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM)
        if idArt[i]=="text":
            t=canvas.itemcget(i, 'text')
            x1=koord[0]+2-xM-1
            y1=-(koord[1]+2-13)+yM
            listeKoord=spiegelY([x1, y1])
            x=listeKoord[0]
            y=listeKoord[1]
            idArt[canvas.create_text(x-2+xM+1,-(y-2-13)+yM,text=t+m*"'", font=("Arial",8,"bold"), fill="blue")]="text"
            canvas.addtag_overlapping(objekt+"Spiegelbild",x-2+xM+1,-(y-2-13)+yM,x-2+xM+1,-(y-2-13)+yM)
            
        if idArt[i]=="line":
            listeKoord1=koord[:2]
            listeKoord2=koord[2:]
            x1=koord[0]-xM
            y1=koord[1]-yM
            x2=koord[2]-xM
            y2=koord[3]-yM
            listeKoord1=spiegelY([x1, y1])
            listeKoord2=spiegelY([x2, y2])
            x1=xM+listeKoord1[0]
            y1=yM+listeKoord1[1]
            x2=xM+listeKoord2[0]
            y2=yM+listeKoord2[1]
            idArt[canvas.create_line(x1,y1,x2,y2, fill="blue")]="line"
            canvas.addtag_overlapping(objekt+"Spiegelbild",x1,y1,x2,y2)
            l="Du"
    canvas.itemconfigure(1, tags="E")
    print canvas.itemconfigure(1)
    
            
def anXAchseSpiegeln():
    global objekt; global idArt; global m; m+=1; n=0
    listeElemente=[]
    listeElemente=canvas.find_withtag(objekt)
    for i in listeElemente:
        koord=canvas.coords(i)
        if idArt[i]=="oval":
            x1=koord[0]+2-xM
            y1=-koord[1]-2+yM
            listeKoord=spiegelX([x1, y1])
            x=listeKoord[0]
            y=listeKoord[1]
            idArt[canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill="blue")]="oval"
            canvas.addtag_overlapping(objekt+"Spiegelbild",x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM)
        if idArt[i]=="text":
            t=canvas.itemcget(i, 'text')
            x1=koord[0]+2-xM-1
            y1=-(koord[1]+2-13)+yM
            listeKoord=spiegelX([x1, y1])
            x=listeKoord[0]
            y=listeKoord[1]
            idArt[canvas.create_text(x-2+xM+1,-(y-2-13)+yM,text=t+m*"'", font=("Arial",8,"bold"), fill="blue")]="text"
            canvas.addtag_overlapping(objekt+"Spiegelbild",x-2+xM+1,-(y-2-13)+yM,x-2+xM+1,-(y-2-13)+yM)
            
        if idArt[i]=="line":
            listeKoord1=koord[:2]
            listeKoord2=koord[2:]
            x1=koord[0]-xM
            y1=koord[1]-yM
            x2=koord[2]-xM
            y2=koord[3]-yM
            listeKoord1=spiegelX([x1, y1])
            listeKoord2=spiegelX([x2, y2])
            x1=xM+listeKoord1[0]
            y1=yM+listeKoord1[1]
            x2=xM+listeKoord2[0]
            y2=yM+listeKoord2[1]
            idArt[canvas.create_line(x1,y1,x2,y2, fill="blue")]="line"
            canvas.addtag_overlapping(objekt+"Spiegelbild",x1,y1,x2,y2)
            
    
def amUrsprungSpiegeln():
    global objekt; global idArt; global m; m+=1; n=0; global winkel
    listeElemente=[]
    listeElemente=canvas.find_withtag(objekt)
    for i in listeElemente:
        koord=canvas.coords(i)
        if idArt[i]=="oval":
            listeKoord=[koord[0]+2-xM,koord[1]+2-yM] #Fehler ? (-)
            listeKoord=spiegelNull(listeKoord, winkel)
            listeKoord[0]-=2+xM
            listeKoord[1]=-(listeKoord-2)+yM
            idArt[canvas.create_oval(listeKoord[0]-2+xM,-(listeKoord[1]-2)+yM,listeKoord[0]+2+xM,-(listeKoord[1]+2)+yM, fill="magenta")]="oval"
            canvas.addtag_overlapping(objekt,listeKoord[0]-2+xM,-(listeKoord[1]-2)+yM,listeKoord[0]+2+xM,-(listeKoord[1]+2)+yM)
        if idArt[i]=="text":
            n+=1
            listeKoord=[koord[0]+2-xM,koord[1]+2-yM] #Fehler ? (-)
            listeKoord=spiegelNull(listeKoord, winkel)
            listeKoord[0]-=2+xM
            listeKoord[1]=-(listeKoord-2)+yM
            idArt[canvas.create_text(listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM,text=unichr(ascii)+m*"'"+str(n), font=("Arial",8,"bold"), fill="magenta")]="text"
            canvas.addtag_overlapping(objekt,listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM,listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM)
        if idArt[i]=="line":
            listeKoord1=koord[:2]
            listeKoord2=koord[2:]
            listeKoord1[0]-=xM; listeKoord1[1]-=xM
            listeKoord2[0]-=xM; listeKoord2[1]-=xM
            listeKoord1=spiegelNull(listeKoord1, winkel)
            listeKoord2=spiegelNull(listeKoord2, winkel)
            listeKoord1[0]+=xM; listeKoord1[1]+=xM
            listeKoord2[0]+=xM; listeKoord2[1]+=xM
            listeKoord=listeKoord1
            listeKoord.extend(listeKoord2)
            idArt[canvas.create_line(listeKoord)]="line"
            canvas.addtag_overlapping(objekt,listeKoord)

def anPSpiegeln():
    global winkel; global p
    global objekt; global idArt; global m; m+=1; n=0; global winkel; global p
    listeElemente=[]
    listeElemente=canvas.find_withtag(objekt)
    for i in listeElemente:
        koord=canvas.coords(i)
        if idArt[i]=="oval":
            listeKoord=[koord[0]+2-xM,koord[1]+2-yM] #Fehler ? (-)
            listeKoord=spiegelP(listeKoord, winkel, p)
            listeKoord[0]-=2+xM
            listeKoord[1]=-(listeKoord-2)+yM
            idArt[canvas.create_oval(listeKoord[0]-2+xM,-(listeKoord[1]-2)+yM,listeKoord[0]+2+xM,-(listeKoord[1]+2)+yM, fill="yellow")]="oval"
            canvas.addtag_overlapping(objekt,listeKoord[0]-2+xM,-(listeKoord[1]-2)+yM,listeKoord[0]+2+xM,-(listeKoord[1]+2)+yM)
        if idArt[i]=="text":
            n+=1
            listeKoord=[koord[0]+2-xM,koord[1]+2-yM] #Fehler ? (-)
            listeKoord=spiegelP(listeKoord, winkel, p)
            listeKoord[0]-=2+xM
            listeKoord[1]=-(listeKoord-2)+yM
            idArt[canvas.create_text(listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM,text=unichr(ascii)+m*"'"+str(n), font=("Arial",8,"bold"), fill="yellow")]="text"
            canvas.addtag_overlapping(objekt,listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM,listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM)
        if idArt[i]=="line":
            listeKoord1=koord[:2]
            listeKoord2=koord[2:]
            listeKoord1[0]-=xM; listeKoord1[1]-=xM
            listeKoord2[0]-=xM; listeKoord2[1]-=xM
            listeKoord1=spiegelP(listeKoord, winkel, p)
            listeKoord2=spiegelP(listeKoord, winkel, p)
            listeKoord1[0]+=xM; listeKoord1[1]+=xM
            listeKoord2[0]+=xM; listeKoord2[1]+=xM
            listeKoord=listeKoord1
            listeKoord.extend(listeKoord2)
            idArt[canvas.create_line(listeKoord)]="line"
            canvas.addtag_overlapping(objekt,listeKoord)
    
    

def zenStrecken():
    global k
    global objekt; global idArt; global m; m+=1; n=0; global winkel; global p
    listeElemente=[]
    listeElemente=canvas.find_withtag(objekt)
    for i in listeElemente:
        koord=canvas.coords(i)
        if idArt[i]=="oval":
            listeKoord=[koord[0]+2-xM,koord[1]+2-yM] #Fehler ? (-)
            listeKoord=zentrischeStreckung(listeKoord, k)
            listeKoord[0]-=2+xM
            listeKoord[1]=-(listeKoord-2)+yM
            idArt[canvas.create_oval(listeKoord[0]-2+xM,-(listeKoord[1]-2)+yM,listeKoord[0]+2+xM,-(listeKoord[1]+2)+yM, fill="cyan")]="oval"
            canvas.addtag_overlapping(objekt,listeKoord[0]-2+xM,-(listeKoord[1]-2)+yM,listeKoord[0]+2+xM,-(listeKoord[1]+2)+yM)
        if idArt[i]=="text":
            n+=1
            listeKoord=[koord[0]+2-xM,koord[1]+2-yM] #Fehler ? (-)
            listeKoord=zentrischeStreckung(listeKoord, k)
            listeKoord[0]-=2+xM
            listeKoord[1]=-(listeKoord-2)+yM
            idArt[canvas.create_text(listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM,text=unichr(ascii)+m*"'"+str(n), font=("Arial",8,"bold"), fill="cyan")]="text"
            canvas.addtag_overlapping(objekt,listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM,listeKoord[0]-2+xM+1,-(listeKoord[1]-2+13)+yM)
        if idArt[i]=="line":
            listeKoord1=koord[:2]
            listeKoord2=koord[2:]
            listeKoord1[0]-=xM; listeKoord1[1]-=xM
            listeKoord2[0]-=xM; listeKoord2[1]-=xM
            listeKoord1=zentrischeStreckung(listeKoord, k)
            listeKoord2=zentrischeStreckung(listeKoord, k)
            listeKoord1[0]+=xM; listeKoord1[1]+=xM
            listeKoord2[0]+=xM; listeKoord2[1]+=xM
            listeKoord=listeKoord1
            listeKoord.extend(listeKoord2)
            idArt[canvas.create_line(listeKoord)]="line"
            canvas.addtag_overlapping(objekt,listeKoord)
    

'''def spiegelY(i):
    spKoord=[]
    maSpY={(0,0):-1,(0,1):0, (0,2):0, 
           (1,0):0 ,(1,1):1, (1,2):0, 
           (2,0):0 ,(2,1):0, (2,2):1 } 
        
    x=i[0]*maSpY[(0,0)]+ i[1]*maSpY[(0,1)]+1*maSpY[(0,2)]
    y=i[0]*maSpY[(1,0)]+ i[1]*maSpY[(1,1)]+1*maSpY[(1,2)]
    e=i[0]*maSpY[(2,0)]+ i[1]*maSpY[(2,1)]+1*maSpY[(2,2)]
    spKoord=[x,y]
    return spKoord'''

def spiegelY(i):
    return [-1*i[0], 1*i[1]]

def spiegelX(i):
    spKoord=[]
    maSpX={(0,0):1, (0,1):0, (0,2):0,
           (1,0):0, (1,1):-1,(1,2):0,
           (2,0):0, (2,1):0, (2,2):1 }
    x=i[0]*maSpX[(0,0)]+ i[1]*maSpX[(0,1)]+1*maSpX[(0,2)]
    y=i[0]*maSpX[(1,0)]+ i[1]*maSpX[(1,1)]+1*maSpX[(1,2)]
    e=i[0]*maSpX[(2,0)]+ i[1]*maSpX[(2,1)]+1*maSpX[(2,2)]
    spKoord=[x,y]
    return spKoord

def spiegelNull(i, alpha):
    spKoord=[]
    maSpN={(0,0):cos(radians(alpha)), (0,1):(-sin(radians(alpha))), (0,2):0,
           (1,0):sin(radians(alpha)), (1,1):cos(radians(alpha))   , (1,2):0,
           (2,0):0                  , (2,1):0                     , (2,2):1 }
    x=i[0]*maSpN[(0,0)]+ i[1]*maSpN[(0,1)]+1*maSpN[(0,2)]
    y=i[0]*maSpN[(1,0)]+ i[1]*maSpN[(1,1)]+1*maSpN[(1,2)]
    e=i[0]*maSpN[(2,0)]+ i[1]*maSpN[(2,1)]+1*maSpN[(2,2)]
    spKoord=[x,y]
    return spKoord

def spiegelP(i, alpha, pkt):
    spKoord=[]
    i[0]=float(i[0])
    i[1]=float(i[1]) #?? '-'
    i[0]-=float(pkt[0]+2-xM)
    i[1]-=float(-pkt[1]+2-yM)#?? '-'
    maSpN={(0,0):cos(radians(alpha)), (0,1):(-sin(radians(alpha))), (0,2):0,
           (1,0):sin(radians(alpha)), (1,1):cos(radians(alpha))   , (1,2):0,
           (2,0):0                  , (2,1):0                     , (2,2):1 }
    x=i[0]*maSpN[(0,0)]+ i[1]*maSpN[(0,1)]+1*maSpN[(0,2)]
    y=i[0]*maSpN[(1,0)]+ i[1]*maSpN[(1,1)]+1*maSpN[(1,2)]
    e=i[0]*maSpN[(2,0)]+ i[1]*maSpN[(2,1)]+1*maSpN[(2,2)]
    x+=float(pkt[0]-2+xM)
    y+=float(-(pkt[1]-2)+yM)
    spKoord=[x,y]
    return spKoord

def zentrischeStreckung(i, k):
    spKoord=[]
    maSpN={(0,0):k, (0,1):0,(0,2):0,
           (1,0):0, (1,1):k,(1,2):0,
           (2,0):0, (2,1):0,(2,2):1 }
    x=i[0]*maSpN[(0,0)]+ i[1]*maSpN[(0,1)]+1*maSpN[(0,2)]
    y=i[0]*maSpN[(1,0)]+ i[1]*maSpN[(1,1)]+1*maSpN[(1,2)]
    e=i[0]*maSpN[(2,0)]+ i[1]*maSpN[(2,1)]+1*maSpN[(2,2)]
    spKoord=[x,y]
    return spKoord
    
def getBildKoord(koord):
    bKoord=[]
    for i in koord:
        i.pop()
        i[1]=-i[1]
        bKoord.append(i)
    
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
    global n; global idArt; global ascii
    x=float(event.x-xM)
    y=float(-(event.y-yM))
    n+=1
    idArt[canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill="red")]="oval"
    canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM)
    idArt[canvas.create_text(x-2+xM+1,-(y-2+13)+yM,text=unichr(ascii)+str(n), font=("Arial",8,"bold"))]="text"
    canvas.addtag_overlapping(objekt,x-2+xM,-(y-2)+yM-5,x+2+xM,-(y+2)+yM-5)
    

def getPunkt1(event):
    global idArt; global objekt; global p1
    idii=canvas.find_closest(float(event.x),float(event.y))[0]
    canvas.coords(idii)
    if idii in canvas.find_withtag(objekt):
        if idArt[idii]=="oval":
            p1=canvas.coords(idii)
        else:
            if idii in canvas.find_withtag(objekt):
                idii-=1
                if idArt[idii]=="oval":
                    p1=canvas.coords(idii)
                else:
                    p1=[]
    else:
        p1=[]
        

def getPunkt2(event):
    global idArt; global objekt; global p2
    idii=canvas.find_closest(float(event.x),float(event.y))[0]
    if idii in canvas.find_withtag(objekt):
        if idArt[idii]=="oval":
            p2=canvas.coords(idii)
        else:
            if idii in canvas.find_withtag(objekt):
                idii-=1
                if idArt[idii]=="oval":
                    p2=canvas.coords(idii)
                else:
                    p2=[]
    else:
        p2=[]
        
    

def punkteVerbinden(event):
    global p1; global p2; global idArt
    getPunkt2(event)
    if p1 != []:
        if p2 != []:
            idArt[canvas.create_line(p1[0]+2,p1[1]+2,p2[0]+2,p2[1]+2)]="line"
            canvas.addtag_overlapping(objekt,p1[0]+2,p1[1]+2,p2[0]+2,p2[1]+2)
            print p1[0]-xM
            print -p1[1]+yM
            print p2[0]-xM
            print -p2[1]+yM

            
    
    
    
    
    
    
    

    


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

aktionsmenue.add_command(label="Neu", command=neueFigur)
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
canvas.bind("<Button-1>", punktZeichnen)
canvas.bind("<Button-3>", getPunkt1)
canvas.bind("<ButtonRelease-3>", punkteVerbinden)

    
#Eingabebereich
eingabefenster=Frame(arbeitsbereich, border=2)
eingabefenster.pack(side=RIGHT, fill=BOTH)
#---
Label(eingabefenster, text="  ").pack()
buttons=Frame(eingabefenster)
buttons.pack()
buttonNeueFigur=Button(buttons, text="neue Figur", command=neueFigur)
buttonNeueFigur.pack(fill=X)
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
buttonKoordEingeben=Button(koordEingabe, text="eingeben", command=setKoordinaten)
buttonKoordEingeben.pack(side=LEFT)
Label(koordinatenfenster, text="  ").pack()
buttonNPunkteEingeben=Button(koordinatenfenster, text="mehrere Punkte eingeben", command=nKoordEingeben)
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
buttonSpiegelpunktEingeben=Button(spiegelpunktEingabe, text="eingeben", command=setP)
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
buttonWinkelEingeben=Button(winkelEingabe, text="eingeben", command=setWinkel)
buttonWinkelEingeben.pack(side=RIGHT)


streckungsfenster=Frame(eingabefenster, relief="groove", border=2)
streckungsfenster.pack(fill=X)
Label(streckungsfenster, text="Streckungsfaktor:").pack(fill=X)
kEingabe=Frame(streckungsfenster)
kEingabe.pack(fill=X)
Label(kEingabe, text="k=").pack(side=LEFT)
entryK=Entry(kEingabe, width=4)
entryK.pack(side=LEFT)
buttonKEingeben=Button(kEingabe, text="eingeben", command=setK)
buttonKEingeben.pack(side=RIGHT)

Label(eingabefenster, text=" ").pack()
Label(eingabefenster, text="Cursor: ").pack(side=LEFT)
pos=Text(eingabefenster, width=10, height=1)
pos.pack(side=LEFT)


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
