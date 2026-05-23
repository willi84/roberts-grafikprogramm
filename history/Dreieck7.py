# Autor: Robert Willemelis
# Stand: 12.05.2006
# Version: 3.0

from Tkinter import *
from Canvas import *
from math import *
from string import *
from tkMessageBox import *
from os import *

p=[0,0]  # winkel: Drehwinkel, p: Spiegelungspunkt
h=430;    w=550 ; ascii=65; k=i=1        # h: Hoehe      , w: Weite 
ableitung=n=winkel=0 
xM=(w/2);     yM=(h/2)  #  xM:  Mittelpunk der x-Achse (x=0),        yM: ... der y-Achse (y=0)
x0=xM%50;     y0=yM%50  #  x0:  erste Markierung auf der x-Achse,    y0: ... auf der y-Achse
stX=-(xM-x0); stY=yM-y0 # stX: erster Markierungswert auf x-Achse,  stY: ... auf der y-Achse

c=unichr(169); al=unichr(945); gr=unichr(186) #Sonderzeichen = c: Copyright, al: Alpha, gr: Grad 
objekt="Figur"+str(unichr(ascii))
zustand1=zustand2=False
aktuellesObjekt=position=p1=p2=[]

def neueFigur():
    global ascii, n, objekt, ableitung
    ascii+=1
    objekt="Figur"+str(str(unichr(ascii)))
    n=ableitung=0
def neu():
    global ableitung, n, ascii, objekt, winkel, p, k
    ableitung=n=winkel=0; ascii=65; objekt="Figur"+str(unichr(ascii)); p=[0,0]; k=1
    listeAlles=canvas.find_all()
    listeKS=canvas.find_withtag("KS")
    for i in listeAlles:
        if i not in listeKS:
            canvas.delete(i)
        
    

def getKoordSystem():
    ''' Das Grundgerüst des Koordinatensystems zeichen. '''
    global xM, yM, x0, y0, stX, stY
    #Achsen malen
    obj=canvas.create_line(xM,0,xM,h,width=2, arrow=FIRST)
    canvas.addtag_withtag("KS", obj)
    canvas.addtag_withtag("y-Achse", obj)
    canvas.addtag_withtag("Achse", obj)
    obj=canvas.create_text(xM-7,5,text="y")
    canvas.addtag_withtag("KS", obj)
    canvas.addtag_withtag("y-Achse", obj)
    canvas.addtag_withtag("Achsenbeschriftung", obj)

    obj=canvas.create_line(0,yM,w,yM,width=2, arrow=LAST)
    canvas.addtag_withtag("KS", obj)
    canvas.addtag_withtag("x-Achse", obj)
    canvas.addtag_withtag("Achse", obj)
    obj=canvas.create_text(w-5,yM+5,text="x")
    canvas.addtag_withtag("KS", obj)
    canvas.addtag_withtag("x-Achse", obj)
    canvas.addtag_withtag("Achsenbeschriftung", obj)

    #x-Achsen-Markierung
    for i in range(0,w+1,50):
        t=canvas.create_line(x0+i, yM-3, x0+i, yM+3, width=1)
        canvas.addtag_withtag("KS", t)
        canvas.addtag_withtag("x-Achse", t)
        canvas.addtag_withtag("Markierung", t)
        canvas.addtag_withtag(str(stX+i), t)
        if stX+i!=0:
            t=canvas.create_text(x0+i, yM+9, text=str(stX+i), font=("Arial",8))
            canvas.addtag_withtag("KS", t)
            canvas.addtag_withtag("x-Achse", t)
            canvas.addtag_withtag("Markierungsbeschriftung", t)
            canvas.addtag_withtag(str(stX+i), t)           
        else:
            t=canvas.create_text(x0+i+5, yM+9, text=str(stX+i), font=("Arial",8))
            canvas.addtag_withtag("KS", t)
            canvas.addtag_withtag("x-Achse", t)
            canvas.addtag_withtag("Markierungsbeschriftung", t)
            canvas.addtag_withtag(str(stX+i), t)            
            
    #y-Achsen-Markierung
    for i in range(0,h+1,50):
        t=canvas.create_line(xM-3, y0+i, xM+3, y0+i, width=1)
        canvas.addtag_withtag("KS", t)
        canvas.addtag_withtag("y-Achse", t)
        canvas.addtag_withtag("Markierung", t)
        canvas.addtag_withtag(str(stY-i), t)
        if stY-i!=0:
            t=canvas.create_text(xM+15, y0+i-1, text=str(stY-i), font=("Arial",8))
            canvas.addtag_withtag("KS", t)
            canvas.addtag_withtag("y-Achse", t)
            canvas.addtag_withtag("Markierungsbeschriftung", t)
            canvas.addtag_withtag(str(stY-i), t)
            
def setKoordinaten():
    global n, ascii, objekt, aktuellesObjekt
    # Vorbereitung für float: Kommata in Punkte, Entfernung von Leerzeichen
    kX=rstrip(lstrip(replace(entryX.get(),",", ".")))
    kY=rstrip(lstrip(replace(entryY.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if kX and kY != "":
        weiter=wertlisteKoord(kX, 0)
        if weiter==True:
            weiter=wertlisteKoord(kY, 0)
            if weiter==True:
                x=float(kX)
                y=float(kY)
                n+=1
                malePunkt(x, y, "red", objekt, str(unichr(ascii))+str(n))
    if kX=="":
        showinfo("Koordinateneingabe",
                 "Punkt konnte nicht eingegeben werden, da das x fehlt!")
    if kY=="":
        showinfo("Koordinateneingabe",
                 "Punkt konnte nicht eingegeben werden, da das y fehlt!")
    entryX.delete(0,len(entryX.get()))
    entryY.delete(0,len(entryY.get()))
    if objekt not in aktuellesObjekt:
        aktuellesObjekt.append(objekt)
    print 'setKoordinaten:', aktuellesObjekt, aktuellesObjekt[0]

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
        global n, ascii, objekt, aktuellesObjekt
        # Vorbereitung für float: Kommata in Punkte, Entfernung von Leerzeichen
        kX=rstrip(lstrip(replace(eingabeX.get(),",", ".")))
        kY=rstrip(lstrip(replace(eingabeY.get(),",", ".")))
        weiter=True
        # Zahlen mit nur 1 Koordinate werden nicht eingegeben
        if kX and kY != "":
            weiter=wertlisteKoord(kX, 0)
            if weiter==True:
                weiter=wertlisteKoord(kX, 0)
                if weiter==True:
                    x=float(kX)
                    y=float(kY)
                    n+=1
                    malePunkt(x, y, "red", objekt, str(unichr(ascii))+str(n))
        if kX=="" and kY !="":
            showinfo("Koordinateneingabe",
                     "Ein Punkt konnte nicht eingegeben werden, da das x fehlte!")
        if kY=="" and kX !="":
            showinfo("Koordinateneingabe",
                     "Ein Punkt konnte nicht eingegeben werden, da das y fehlte!")
    if objekt not in aktuellesObjekt:
        aktuellesObjekt.append(objekt)
    print 'getNKoordinaten: ', aktuellesObjekt, aktuellesObjekt[0]
           
    def setNKoordinaten():
        getNKoordinaten(n1_XEntry,n1_YEntry)
        getNKoordinaten(n2_XEntry,n2_YEntry)
        getNKoordinaten(n3_XEntry,n3_YEntry)
        getNKoordinaten(n4_XEntry,n4_YEntry)
        getNKoordinaten(n5_XEntry,n5_YEntry)
        nKoordRoot.destroy()
    
    buttonNKoord=Button(nKoordRoot, text="eingeben", command=setNKoordinaten)
    buttonNKoord.pack()
    nKoordRoot.mainloop()
    
def setWinkel():
    global winkel
    winkel=rstrip(lstrip(replace(entryWinkel.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if winkel != "":
        weiter=wertlisteKoord(winkel, 2)
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
        weiter=wertlisteKoord(k, 3)
        if weiter==True:
            k=float(k)
    if k =="":
        showinfo("Streckungsfaktor",
                 "Sie haben keinen Streckungsfaktor k eingegeben!")
    entryK.delete(0,len(entryK.get()))

def setP():
    global p, n, ascii, objekt
    x=rstrip(lstrip(replace(entrySpPunktX.get(),",", ".")))
    y=rstrip(lstrip(replace(entrySpPunktY.get(),",", ".")))
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if x and y != "":
        weiter=wertlisteKoord(x, 1)
        if weiter==True:
            weiter=wertlisteKoord(y, 1)
            if weiter==True:
                x=float(x)
                y=float(y)
                p=[x,y]
                n+=1
                obj=canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill="black")
                canvas.addtag_withtag(objekt, obj)
                canvas.addtag_withtag(str(unichr(ascii))+str(n)+"("+al+")", obj)
                canvas.addtag_withtag("drehpunkt", obj)
                obj=canvas.create_text(x-2+xM+1,-(y-2+13)+yM,text=str(unichr(ascii))+str(n)+"("+al+")", font=("Arial",8,"bold"))
                canvas.addtag_withtag(objekt, obj)
                canvas.addtag_withtag(str(unichr(ascii))+str(n)+"("+al+")", obj)
                canvas.addtag_withtag("textDrehpunkt", obj)
    if x=="":
        showinfo("Spiegelpunkteingabe",
                 "Spiegelpunkt konnte nicht eingegeben werden, da das x fehlt!")
    if x=="":
        showinfo("Spiegelpunkteingabe",
                 "Spiegelpunkt konnte nicht eingegeben werden, da das y fehlt!")
    entrySpPunktX.delete(0,len(entrySpPunktX.get()))
    entrySpPunktY.delete(0,len(entrySpPunktY.get()))
def spiegeln(farbe, art):
    global objekt, ableitung, winkel, p, k
    ableitung+=1;
    listeElemente=[]
    listeElemente=canvas.find_withtag(objekt)
    spiegelfigur=objekt+"Spiegelbild"+ableitung*"'"
    for i in listeElemente:
        koord=canvas.coords(i)
        if i in canvas.find_withtag("text"):
            t=canvas.itemcget(i, 'text')
            x1=koord[0]+2-xM-1
            y1=-(koord[1]-2+13)+yM
            if art=="x":
                listeKoord=spiegelX([x1, y1])
            if art=="y":
                listeKoord=spiegelY([x1, y1])
            if art=="null":
                listeKoord=spiegelNull([x1, y1], winkel)
            if art=="p":
                listeKoord=spiegelP([x1, y1], winkel, p)
            if art=="zentr":
                listeKoord=zentrischeStreckung([x1, y1], k)
            x=listeKoord[0]
            y=listeKoord[1]
            maleSpiegelPunkt(x, y, farbe, spiegelfigur, t+ableitung*"'")
        if i in canvas.find_withtag("linie"):
            x1=koord[0]-xM
            y1=-koord[1]+yM
            x2=koord[2]-xM
            y2=-koord[3]+yM
            if art=="x":
                listeKoord1=spiegelX([x1, y1])
                listeKoord2=spiegelX([x2, y2])
            if art=="y":
                listeKoord1=spiegelY([x1, y1])
                listeKoord2=spiegelY([x2, y2])
            if art=="null":
                listeKoord1=spiegelNull([x1, y1], winkel)
                listeKoord2=spiegelNull([x2, y2], winkel)
            if art=="p":
                listeKoord1=spiegelP([x1, y1], winkel, p)
                listeKoord2=spiegelP([x2, y2], winkel, p)
            if art=="zentr":
                listeKoord1=zentrischeStreckung([x1, y1], k)
                listeKoord2=zentrischeStreckung([x2, y2], k)
            x1=xM+listeKoord1[0]
            y1=yM-listeKoord1[1]
            x2=xM+listeKoord2[0]
            y2=yM-listeKoord2[1]
            maleSpiegelLinie(x1, y1, x2, y2, farbe, spiegelfigur,
                             "["+str(x1)+","+str(y1)+"] "+"["+str(x2)+","+str(y2)+"]")
    if spiegelfigur not in aktuellesObjekt:
        aktuellesObjekt.append(spiegelfigur)
    print 'spiegeln: ', aktuellesObjekt, aktuellesObjekt[0]
    
def anXAchseSpiegeln():
    spiegeln("#3333ff", "x")
def anYAchseSpiegeln():
    spiegeln("#ff9900", "y")
def amUrsprungSpiegeln():
    spiegeln("#cc0099", "null")
def anPSpiegeln():
    spiegeln("#d2691e", "p")
def zenStrecken():
    spiegeln("#33cc00","zentr")
    
def spiegelY(i):
    return [-1*i[0], 1*i[1]]
def spiegelX(i):
    return [1*i[0], -1*i[1]]

def spiegelNull(i, alpha):
    return [i[0]*cos(radians(alpha))+i[1]*(-sin(radians(alpha))),
            i[0]*sin(radians(alpha))+i[1]*cos(radians(alpha))]

def spiegelP(i, alpha, pkt):
    return [((i[0]-pkt[0])*cos(radians(alpha)) \
                   +(i[1]-pkt[1])*(-sin(radians(alpha))))+pkt[0],
                    ((i[0]-pkt[0])*sin(radians(alpha)) \
                   +(i[1]-pkt[1])*cos(radians(alpha)))+pkt[1]]

def zentrischeStreckung(i, k):
    return [k*i[0], k*i[1]]

def wertlisteKoord(x, hX):
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
    pos.delete("0.0",END)
    pos.insert("0.0","("+str(event.x-xM)+"/"+str(-(event.y-yM))+")")

def setNull(event):
    pos.delete("0.0",END)

def punktZeichnen(event):
    global n, ascii, objekt, aktuellesObjekt
    if objekt not in aktuellesObjekt:
        aktuellesObjekt.append(objekt)
    print 'punktZeichnen: ', aktuellesObjekt, aktuellesObjekt[0]
    x=float(event.x-xM)
    y=float(-(event.y-yM))
    n+=1
    malePunkt(x, y, "red", objekt, str(unichr(ascii))+str(n))

def deleteAktuellesObjekt():
    global aktuellesObjekt, n, ableitung, ascii
    #mind. 1 Eintrag
    if len(aktuellesObjekt)>0:
        liste=canvas.find_withtag(aktuellesObjekt.pop())
        #if ascii>65:
        #   ascii-=1
        for i in liste:
            canvas.delete(i)
        if len(aktuellesObjekt)>0:
            liste=set(canvas.find_withtag(aktuellesObjekt[len(aktuellesObjekt)-1]))
            listeP=set(canvas.find_withtag("punkt"))
            listeSp=set(canvas.find_withtag("spiegelpunkt"))
            print liste
            print listeP
            if len(liste&listeP)==0:
                n=0
            if len(liste&listeP)!=0:
                pass
            if len(liste&listeSp)!=0:
                pass
        else:
            n=0
    #kein Eintrag -> Ursprungszustand
    else:
        n=0
            
    print 'deleteAktuellesObjekt: ', aktuellesObjekt, aktuellesObjekt[0]
    
def getPunkt1(event):
    global objekt, p1
    idii=canvas.find_closest(float(event.x),float(event.y))[0]
    canvas.coords(idii)
    if idii in canvas.find_withtag(objekt):
        if idii in canvas.find_withtag("punkt"):
            p1=canvas.coords(idii)
        else:
            if idii in canvas.find_withtag("text"):
                p1=canvas.coords(idii)
                p1[0]-=1  #2-1-2
                p1[1]+=9  #13-2-2
    else:
        p1=[]

def getPunkt2(event):
    global objekt, p2
    idii=canvas.find_closest(float(event.x),float(event.y))[0]
    if idii in canvas.find_withtag(objekt):
        if idii in canvas.find_withtag("punkt"):
            p2=canvas.coords(idii)
        else:
            if idii in canvas.find_withtag("text"):
                p2=canvas.coords(idii)
                p2[0]-= 1 #2-1-2
                p2[1]+=9  #13-2-2
    else:
        p2=[]
    
def punkteVerbinden(event):
    global p1, p2, objekt, aktuellesObjekt
    if objekt not in aktuellesObjekt:
        aktuellesObjekt.append(objekt)
    print 'punkteVerbinden: ', aktuellesObjekt, aktuellesObjekt[0]
    getPunkt2(event)
    if p1 != []:
        if p2 != []:
            maleLinie(p1[0]+2,p1[1]+2,p2[0]+2,p2[1]+2, "black", objekt, str(p1)+" "+str(p2))
          
def malePunkt(x, y, farbe, figur, name):
    i=canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill=farbe)
    canvas.addtag_withtag(figur, i)
    canvas.addtag_withtag(name, i)
    canvas.addtag_withtag("punkt", i)
    i=canvas.create_text(x-2+xM+1,-(y-2+13)+yM,text=name, font=("Arial",8,"bold"))
    canvas.addtag_withtag(figur, i)
    canvas.addtag_withtag(name, i)
    canvas.addtag_withtag("text", i)
    if figur not in aktuellesObjekt:
        aktuellesObjekt.append(figur)
    print 'malePunkt: ', aktuellesObjekt, aktuellesObjekt[0]
def maleSpiegelPunkt(x, y, farbe, figur, name):
    global aktuellesObjekt
    i=canvas.create_oval(x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM, fill=farbe)
    canvas.addtag_withtag(figur, i)
    canvas.addtag_withtag(name, i)
    canvas.addtag_withtag("spiegelpunkt", i)
    i=canvas.create_text(x-2+xM+1,-(y-2+13)+yM,text=name, font=("Arial",8,"bold"), fill=farbe)
    canvas.addtag_withtag(figur, i)
    canvas.addtag_withtag(name, i)
    canvas.addtag_withtag("text", i)
    if figur not in aktuellesObjekt:
        aktuellesObjekt.append(figur)
    print 'maleSpiegelPunkt: ', aktuellesObjekt, aktuellesObjekt[0]

def maleLinie(x1, y1, x2, y2, farbe, figur, name):
    global i
    koord=linieAnpassen(x1, y1, x2, y2)
    i=canvas.create_line(koord, fill=farbe)
    canvas.addtag_withtag(figur, i)
    canvas.addtag_withtag(name, i)
    canvas.addtag_withtag("linie", i)
    if figur not in aktuellesObjekt:
        aktuellesObjekt.append(figur)
    print 'maleLinie: ', aktuellesObjekt, aktuellesObjekt[0]
def maleSpiegelLinie(x1, y1, x2, y2, farbe, figur, name):
    koord=linieAnpassen(x1, y1, x2, y2)
    i=canvas.create_line(koord, fill=farbe)
    canvas.addtag_withtag(figur, i)
    canvas.addtag_withtag(name, i)
    canvas.addtag_withtag("spiegellinie", i)
    if figur not in aktuellesObjekt:
        aktuellesObjekt.append(figur)
    print 'maleSpiegelLinie: ', aktuellesObjekt, aktuellesObjekt[0]
def linieAnpassen(x1, y1, x2, y2):
    # senkrechte Linie
    if x1==x2 and y1<y2: y1+=2; y2-=2 
    if x1==x2 and y1>y2: y1-=2; y2+=2 
    # waagerechte Linie
    if x1>x2 and y1==y2: x1-=2; x2+=2; 
    if x1<x2 and y1==y2: x1+=2; x2-=2; 
    # schraege Linie
    if x1<x2 and y1>y2: x1+=1; x2-=1; y1-=1; y2+=1
    if x1>x2 and y1<y2: x1-=1; x2+=1; y1+=1; y2-=1
    if x1<x2 and y1<y2: x1+=1; x2-=1; y1+=1; y2-=1
    if x1>x2 and y1>y2: x1-=1; x2+=1; y1-=1; y2+=1
    return [x1, y1, x2, y2]

    
#----1. Start des Masters ----------------------------------------------------------
root=Tk()
root.title("Roberts Grafikprogramm 3.0")


#-------
malen_in=PhotoImage(file="malen_in.gif")
malen_aktiv=PhotoImage(file="malen.gif")
linieVerbinden_in=PhotoImage(file="linie_verbinden_in.gif")
linieVerbinden_aktiv=PhotoImage(file="linie_verbinden.gif")
listeKoord=PhotoImage(file="liste.gif")

#----2. Beginn Menueoptionsleiste -------------------------

menueleiste=Menu(root)
aktionsmenue=Menu(menueleiste)
spiegelnmenue=Menu(menueleiste)
hilfemenue=Menu(menueleiste)

menueleiste.add_cascade(menu=aktionsmenue, label="Aktionen")
menueleiste.add_cascade(menu=spiegelnmenue, label="Spiegeln")
menueleiste.add_cascade(menu=hilfemenue, label="?")

aktionsmenue.add_command(label="Neu", command=neu)
aktionsmenue.add_separator()
aktionsmenue.add_command(label="Neue Figur", command=neueFigur)
aktionsmenue.add_separator()
aktionsmenue.add_command(label="Aktuelles Objekt löschen", command=deleteAktuellesObjekt)
aktionsmenue.add_command(label="Bestimmtes Objekt löschen")
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
buttons2=Frame(eingabefenster)
buttons2.pack()
    
def schalten4():
    pass
def schalten1():
    global zustand1
    if zustand1==False: zustand1=True
    else: zustand1=False
    if zustand1==True:
        buttonNeueFigur.config(image=malen_aktiv)
        buttonNeueFigur.config(bg="red")
        canvas.bind("<Button-1>", punktZeichnen)
    else:
        buttonNeueFigur.config(image=malen_in)
        buttonNeueFigur.config(bg="black")
        canvas.bind("<Button-1>", schalten4)
def schalten2():
    global zustand2
    if zustand2==False: zustand2=True
    else: zustand2=False
    if zustand2==True:
        buttonFigurdaten.config(image=linieVerbinden_aktiv)
        buttonFigurdaten.config(bg="blue")
        canvas.bind("<Button-1>", getPunkt1)
        canvas.bind("<ButtonRelease-1>", punkteVerbinden)
    else:
        buttonFigurdaten.config(image=linieVerbinden_in)
        buttonFigurdaten.config(bg="black")
        canvas.bind("<Button-1>", schalten4)
        canvas.bind("<ButtonRelease-1>", schalten4)
buttonNeueFigur=Button(buttons, image=malen_in,bg="black",
                            relief=FLAT,command=schalten1) #command=neueFigur
buttonNeueFigur.pack(side=LEFT)
buttonFigurdaten=Button(buttons, image=linieVerbinden_in, relief=FLAT, bg="black", command=schalten2)
buttonFigurdaten.pack(side=LEFT)
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
buttonNPunkteEingeben=Button(koordinatenfenster, relief=FLAT,image=listeKoord, command=nKoordEingeben)
buttonNPunkteEingeben.pack() #text="mehrere Punkte eingeben"
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
