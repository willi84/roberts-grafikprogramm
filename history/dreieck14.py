# Autor: Robert Willemelis Stand: 12.05.2006 Version: 3.0
from Tkinter import *
from Canvas import *
from math import *
from string import *
from os import *
from tkMessageBox import *
from time import *


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
f={}; x={}; y={}; l={}; b={}; t={}; e={};m={}  #v=Variabeln

def window(name,nameWindow):
    global f
    f[name]=Tk()
    f[name].title(nameWindow)
def frame(name,root,border,relief,side,fill):
    global f
    f[name]=Frame(root,relief=relief,border=border)
    f[name].pack(side=side,fill=fill)
def label(name,root,text,side,fill):
    global l
    l[name]=Label(root,text=text)
    l[name].pack(side=side,fill=fill)
def button(name,root,border,relief,image,text,bg,command,side,fill):
    global b
    b[name]=Button(root,image=image,text=text,bg=bg,command=command,relief=relief, border=border)
    b[name].pack(side=side,fill=fill)
def text(name,root,width,height,side,fill):
    global t
    t[name]=Text(root,width=width,height=height)
    t[name].pack(side=side,fill=fill)
def entry(name,root,width,side,fill):
    global e
    e[name]=Entry(root,width=width)
    e[name].pack(side=side,fill=fill)
def normalform(zahl):
    return rstrip(lstrip(replace(zahl.get(),",", ".")))
def delEntry(entry):
    for i in entry:
        i.delete(0,len(i.get()))
def menu(name,root,id,commands):
    m[name]=Menu(root)
    if id==1:
        root.add_cascade(menu=m[name], label=name)
    if commands!=None:
        for i in commands:
            if len(i)==0:
                m[name].add_separator()
            else:
                m[name].add_command(label=i[0],command=i[1])
def aktion(obj,evt):
    for i in evt:
        obj.bind(i[0],i[1])
def nKE(fr,num):
        frame('NEingabe'+num,fr,None,None,None,X)
        label('x'+num,f['NEingabe'+num],'x',LEFT,None)
        entry('x'+num,f['NEingabe'+num],7,LEFT,None)
        label('y'+num,f['NEingabe'+num],'y',LEFT,None)
        entry('y'+num,f['NEingabe'+num],7,LEFT,None)
#für alle Eingaben kompatibel machen, 1 bis 2 punkte mit übergebenen tags
#[name,laenge usw,]
                
def cLine(obj,koord,d,s,f,tK1,tK2):
    tags(obj,tagKS(tK1,tK2),obj.create_line(koord,width=d,arrow=s,fill=f))
def cText(obj,pX,pY,t,f,tK1,tK2):
    tags(obj,tagKS(tK1,tK2),obj.create_text(pX,pY,text=t,font=f))
def cOval(obj,x1,y1,x2,y2,fi,tK1,tK2):
    tags(obj,tagKS(tK1,tK2),obj.create_oval(x1,y1,x2,y2,fill=fi))
    
def xyInfo(koordArt1, koordArt2, pktArt):
    listeKoordArt1=["Spiegelpunkteingabe","Koordinateneingabe"]
    listeKoordArt2=["Spiegelpunkt ","Ein Punkt ","Punkt "]
    showinfo(listeKoordArt1[koordArt1],listeKoordArt2[koordArt2]+\
             "konnte nicht eingegeben werden, da das "+pktArt+" fehlt!")
def tagKS(tID,tLi):
    global objekt; tListe=[]
    liste=["KS",objekt,
           "x-Achse","y-Achse",
           "Achse","Achsenbeschriftung",
           "Markierung","Markierungsbeschriftung",
           "punkt","spiegelpunkt","drehpunkt","textDrehpunkt",
           "linie","spiegellinie",
           "text"]
    if tID !=None:
        for i in tID:
            tListe.append(liste[i])
    if tLi !=None:
        for i in tLi:
            tListe.append(i)
    return tListe
 
def objektliste(objekt):
    global aktuellesObjekt
    if objekt not in aktuellesObjekt:
        aktuellesObjekt.append(objekt)
def tags(objekt,tagListe,objNr):
    for i in tagListe:
        objekt.addtag_withtag(i, objNr)
def neueFigur():
    global ascii, n, objekt, ableitung
    ascii+=1
    objekt="Figur"+str(unichr(ascii))
    n=ableitung=0
def neu():
    global ableitung, n, ascii, objekt, winkel, p, k
    ableitung=n=winkel=0; ascii=65; objekt="Figur"+str(unichr(ascii)); p=[0,0]; k=1
    listeAlles=cvAll(); listeKS=cvWith("KS")
    for i in listeAlles:
        if i not in listeKS: cv.delete(i)
        
def getKoordSystem():
    global xM, yM, x0, y0, stX, stY
    #Achsen malen
    cLine(cv,[xM,0,xM,h],2,FIRST,None,[0,3,4],None)
    cText(cv,xM-7,5,"y",None,[0,3,5],None)
    cLine(cv,[0,yM,w,yM],2,LAST,None,[0,2,4],None)
    cText(cv,w-5,yM+5,"x",None,[0,2,5],None)
    #x-Achsen-Markierung
    for i in range(0,w+1,50):
        cLine(cv,[x0+i,yM-3,x0+i,yM+3],1,None,None,[0,2,6],[str(stX+i)])
        if stX+i!=0:
            cText(cv,x0+i,yM+9,str(stX+i),("Arial",8),[0,2,7],[str(stX+i)])   
        else:
            cText(cv,x0+i+5,yM+9,str(stX+i),("Arial",8),[0,2,7],[str(stX+i)])        
    #y-Achsen-Markierung
    for i in range(0,h+1,50):
        cLine(cv,[xM-3,y0+i,xM+3,y0+i],1,None,None,[0,3,6],[str(stY-i)])
        if stY-i!=0:
            cText(cv,xM+15,y0+i-1,str(stY-i),("Arial",8),[0,3,7],[str(stY-i)])
            
def setKoordinaten():
    global objekt
    punktMalen(entryX,entryY,2)
    delEntry([entryX,entryY])
    objektliste(objekt)

def nKoordEingeben():
    var=5  #Anzahl der moeglichen Eingaben
    window('nKoordRoot',"Eingabe mehrerer Punkte")
    label('mpe',f['nKoordRoot'],"Mehrere Punkte eingeben",None,X)
    frame('mainFrame',f['nKoordRoot'],None,None,None,None)
    '''def nKE(fr,num):
        frame('NEingabe'+str(i),f['mainFrame'],None,None,None,X)
        label('x'+num,f['NEingabe'+num],'x',LEFT,None)
        entry('x'+num,f['NEingabe'+num],7,LEFT,None)
        label('y'+num,f['NEingabe'+num],'y',LEFT,None)
        entry('y'+num,f['NEingabe'+num],7,LEFT,None)'''
    for i in range(var):
        nKE(f['mainFrame'],str(i))
    objektliste(objekt)
    def setNKoordinaten():
        for i in range(var):
            punktMalen(e['x'+str(i)],e['y'+str(i)],1)
        f['nKoordRoot'].destroy()
    button('buttonNKoord',f['nKoordRoot'],None,None,None,"eingeben",None,setNKoordinaten,None,None)
    f['nKoordRoot'].mainloop()
    
def punktMalen(eingabe1,eingabe2,kontroll):
    global n, ascii, objekt
    # Vorbereitung für float: Kommata in Punkte, Entfernung von Leerzeichen
    kX=normalform(eingabe1); kY=normalform(eingabe2)
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if kX and kY != "":
        weiter=wertlisteKoord(kX, 0)
        if weiter==True:
            weiter=wertlisteKoord(kY, 0) #kX mit kY ersetzt
            if weiter==True:
                x=float(kX)
                y=float(kY)
                n+=1
                malePunkt(x, y, "red", objekt, str(unichr(ascii))+str(n),"punkt")
    if kX=="" and kY !="": xyInfo(1,kontroll,"x")
    if kY=="" and kX !="": xyInfo(1,kontroll,"y")
def setWinkel():
    global winkel
    winkel=normalform(entryWinkel)
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if winkel != "":
        weiter=wertlisteKoord(winkel, 2)
        if weiter==True:
            winkel=float(winkel)
    if winkel == "": showinfo("Winkeleingabe", "Sie haben keinen Winkel eingegeben!")  #in xyInfo-Standard
    delEntry([entryWinkel])

def setK():
    global k
    k=normalform(entryK)
    weiter=True
    # Zahlen mit nur 1 Koordinate werden nicht eingegeben
    if k != "":
        weiter=wertlisteKoord(k, 3)
        if weiter==True:
            k=float(k)
    if k == "": showinfo("Streckungsfaktor", "Sie haben keinen Streckungsfaktor k eingegeben!")
    delEntry([entryK])

def setP():
    global p, n, ascii, objekt
    x=normalform(entrySpPunktX); y=normalform(entrySpPunktY)
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
                cOval(cv,x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM,"black",[1,10],
                      [str(unichr(ascii))+str(n)+"("+al+")"])
                cText(cv,x-2+xM+1,-(y-2+13)+yM,str(unichr(ascii))+str(n)+"("+al+")",
                      ("Arial",8,"bold"),[1,11],[str(unichr(ascii))+str(n)+"("+al+")"])
                                
    if x=="": xyInfo(0,0,"x")
    if y=="": xyInfo(0,0,"y")
    delEntry([entrySpPunktX,entrySpPunktY])
#------------------------------------------------------------------------------    
def spiegeln(farbe, art):
    global objekt, ableitung, winkel, p, k
    ableitung+=1;
    listeElemente=[]
    listeElemente=cvWith(objekt)
    spiegelfigur=objekt+"Spiegelbild"+ableitung*"'"
    for i in listeElemente:
        koord=cvCoords(i)
        if i in cvWith("text"):
            t=cv.itemcget(i, 'text')
            x1=koord[0]+2-xM-1
            y1=-(koord[1]-2+13)+yM
            if art=="x": listeKoord=spiegelX([x1, y1])
            if art=="y": listeKoord=spiegelY([x1, y1])
            if art=="n": listeKoord=spiegelNull([x1, y1], winkel)
            if art=="p": listeKoord=spiegelP([x1, y1], winkel, p)
            if art=="z": listeKoord=zentrischeStreckung([x1, y1], k)
            x=listeKoord[0]
            y=listeKoord[1]
            malePunkt(x, y, farbe, spiegelfigur, t+ableitung*"'","spiegelpunkt")
        if i in cvWith("linie"):
            x1=koord[0]-xM
            y1=-koord[1]+yM
            x2=koord[2]-xM
            y2=-koord[3]+yM
            if art=="x":
                listeKoord1=spiegelX([x1, y1]); listeKoord2=spiegelX([x2, y2])
            if art=="y":
                listeKoord1=spiegelY([x1, y1]); listeKoord2=spiegelY([x2, y2])
            if art=="n":
                listeKoord1=spiegelNull([x1, y1], winkel)
                listeKoord2=spiegelNull([x2, y2], winkel)
            if art=="p":
                listeKoord1=spiegelP([x1, y1], winkel, p)
                listeKoord2=spiegelP([x2, y2], winkel, p)
            if art=="z":
                listeKoord1=zentrischeStreckung([x1, y1], k)
                listeKoord2=zentrischeStreckung([x2, y2], k)
            x1=xM+listeKoord1[0]
            y1=yM-listeKoord1[1]
            x2=xM+listeKoord2[0]
            y2=yM-listeKoord2[1]
            maleLinie(x1, y1, x2, y2, farbe, spiegelfigur,
                             "["+str(x1)+","+str(y1)+"] "+"["+str(x2)+","+str(y2)+"]","spiegellinie")
    objektliste(spiegelfigur)
    
def anXAchseSpiegeln():   spiegeln("#3333ff", "x")
def anYAchseSpiegeln():   spiegeln("#ff9900", "y")
def amUrsprungSpiegeln(): spiegeln("#cc0099", "n")
def anPSpiegeln():        spiegeln("#d2691e", "p")
def zenStrecken():        spiegeln("#33cc00", "z")   
def _sin(a): return sin(radians(a))
def _cos(a): return cos(radians(a))
def spiegelX(i): return [ i[0],-i[1]]
def spiegelY(i): return [-i[0], i[1]]
def spiegelNull(i, a): return [i[0]*_cos(a)+i[1]*(-_sin(a)), i[0]*_sin(a)+i[1]*_cos(a)]
def spiegelP(i, a, p):
    return [((i[0]-p[0])*_cos(a) +(i[1]-p[1])*(-_sin(a)))+p[0],
            ((i[0]-p[0])*_sin(a) +(i[1]-p[1])*  _cos(a)) +p[1]]
def zentrischeStreckung(i, k): return [k*i[0], k*i[1]]


#----------------------------------------------------
#Events
def getCursorPos(event):
    x=event.x
    y=event.y
    pos.delete("0.0",END)
    pos.insert("0.0","("+str(x-xM)+"/"+str(-(y-yM))+")")
    return [x,y]

def setNull(event): pos.delete("0.0",END)
def punktZeichnen(event):
    global n, ascii, objekt
    objektliste(objekt)
    x=float(event.x-xM)
    y=float(-(event.y-yM))
    n+=1
    malePunkt(x, y, "red", objekt, str(unichr(ascii))+str(n),"punkt")

def deleteAktuellesObjekt():
    #sorgen, dass auch Grad der Spiegelung zurückgesetzt wird
    #Nummer des Buchstabens aktualisierern A12 (ascii)
    global aktuellesObjekt, n, ableitung, ascii
    #mind. 1 Eintrag
    test=False
    if len(aktuellesObjekt)>0:
        liste=cvWith(aktuellesObjekt.pop())
        #if ascii>65:
        #   ascii-=1
        allTag=""
        for i in liste:
            if 'text' in cv.gettags(i):
                for j in cv.gettags(i):
                    allTag+=j
            j=cv.gettags(i)
            cv.delete(i)
        if len(aktuellesObjekt)>0:
            liste=set(cvWith(aktuellesObjekt[len(aktuellesObjekt)-1]))
            listeP=set(cvWith("punkt"))
            listeSp=set(cvWith("spiegelpunkt"))
            if len(liste&listeP) ==0: n=0
            if len(liste&listeP) !=0: pass #leer ?funktion
            if len(liste&listeSp)!=0: pass
        else:
            n=0
    #kein Eintrag -> Ursprungszustand
    else:
        n=0
    if "'" in allTag:
        ableitung-=1
def getPunkt1(event):
    global objekt, p1
    idii=cvClose(float(event.x),float(event.y))[0]
    cvCoords(idii)
    if idii in cvWith(objekt):
        if idii in cvWith("punkt"):
            p1=cvCoords(idii)
        else:
            if idii in cvWith("text"):
                p1=cvCoords(idii)
                p1[0]-=1  #2-1-2
                p1[1]+=9  #13-2-2
    else:
        p1=[] 

def getPunkt2(event):
    global objekt, p2
    idii=cvClose(float(event.x),float(event.y))[0]
    if idii in cvWith(objekt):
        if idii in cvWith("punkt"):
            p2=cvCoords(idii)
        else:
            if idii in cvWith("text"):
                p2=cvCoords(idii)
                p2[0]-= 1 #2-1-2
                p2[1]+=9  #13-2-2
    else:
        p2=[]
    
def punkteVerbinden(event):
    global p1,p2, objekt, aktuellesObjekt
    objektliste(objekt)
    getPunkt2(event)
    print [p1[0]-xM,yM+p1[1]]
    print [p2[0]-xM,yM+p2[1]]
    if p1 != []:
        if p2 != []:
            maleLinie(p1[0]+2,p1[1]+2,p2[0]+2,p2[1]+2, "black", objekt, str(p1)+" "+str(p2),"linie")
          
def malePunkt(x, y, farbe, figur, name, tagArt):
    cOval(cv,x-2+xM,-(y-2)+yM,x+2+xM,-(y+2)+yM,farbe,None,[figur, name, tagArt])
    cText(cv,x-2+xM+1,-(y-2+13)+yM,name,("Arial",8,"bold"),[14],[figur, name])
    objektliste(figur)

def maleLinie(x1, y1, x2, y2, farbe, figur, name, tagArt):
    koord=linieAnpassen(x1, y1, x2, y2)
    cLine(cv,koord,None,None,farbe,None,[figur, name, tagArt])  
    objektliste(figur)
    
#wichtig: verschiedenste Stellungen regeln, z.B. wenn beide gedrückt -> überspringen
def checkButton_PunktZeichnen():
    global zustand1
    if zustand1==False: zustand1=True
    else: zustand1=False
    if zustand1==True:
        b['NeueFigur'].config(image=malen_aktiv,bg="red")
        aktion(cv,[["<Button-1>", punktZeichnen]])
    else:
        b['NeueFigur'].config(image=malen_in,bg="black")
        aktion(cv,[["<Button-1>", leer]])
def checkButton_PunkteVerbinden():
    global zustand2
    if zustand2==False: zustand2=True
    else: zustand2=False
    if zustand2==True:
        b['Figurdaten'].config(image=linieVerbinden_aktiv,bg="blue")
        aktion(cv,[["<Button-1>", getPunkt1],["<ButtonRelease-1>", punkteVerbinden]])
    else:
        b['Figurdaten'].config(image=linieVerbinden_in,bg="black")
        aktion(cv,[["<Button-1>", leer],["<ButtonRelease-1>", leer]])
#----------------------------------------------------------------------------------
#Standardfunktionen

def leer(): pass

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

def wertlisteKoord(x, hX): 
    head=["Koordinateneingabe", "Spiegelpunktseingabe",
          "Winkeleingabe", "Eingabe des Streckungsfaktors"]
    zulaessig=["0","1","2","3","4","5","6","7","8","9","."]
    wort=head[hX]
    richtig=True
    if x.count(".")>1:
        showinfo(wort, "Bei Dezimalzahlen gibt es nur ein Kommata!\n Viel Spass beim Klicken!")
        richtig=False
    else:
        for i in x:
            if i not in zulaessig:
                if i==x[0] and i=="-":
                    pass
                else:
                    showinfo(wort, "Bitte geben Sie wirklich nur Zahlen ein!")
                    richtig=False
    return richtig
def unfertig():
    pass
#--------------------------------------------------------------------------------------------
#Oberfläche
    
#----1. Start des Masters ----------------------------------------------------------
window('Hauptfenster',"Roberts Grafikprogramm 3.0")
#-------
malen_in=PhotoImage(file="malen_in.gif")
malen_aktiv=PhotoImage(file="malen.gif")
linieVerbinden_in=PhotoImage(file="linie_verbinden_in.gif")
linieVerbinden_aktiv=PhotoImage(file="linie_verbinden.gif")
listeKoord=PhotoImage(file="liste.gif")

#----2. Beginn Menueoptionsleiste -------------------------
menu('menue',f['Hauptfenster'],0,None)
menu('Aktionen',m['menue'],1,[["Neu",neu],[],
                              ["Neue Figur",neueFigur],[],
                              ["Aktuelles Objekt löschen",deleteAktuellesObjekt],
                              ["Bestimmtes Objekt löschen",unfertig],[],
                              ["Liste aller Objekte",unfertig],
                              ["Liste aller Koordinaten",unfertig],[],
                              ["Programm beenden",f['Hauptfenster'].destroy]])
menu('Spiegeln',m['menue'],1,[["... an der x-Achse",anXAchseSpiegeln],
                              ["... an der y-Achse",anYAchseSpiegeln],[],
                              ["... am Ursprung",amUrsprungSpiegeln],
                              ["... an einem bestimmten Punkt",anPSpiegeln],[],
                              ["Zentrische Streckung",zenStrecken]])
menu('?',m['menue'],1,[["Programmbeschreibung",unfertig],["Impressum",unfertig]])
f['Hauptfenster'].config(menu=m['menue'])

#----2. Ende Menueoptionsleiste ---------------------------


#----3. Beginn des Arbeitsbereiches -----------------------
frame('Arbeitsbereich',f['Hauptfenster'],2,"groove",None,None) 
#Zeichenfläche mit Canvas-Widget
frame('Zeichenbrett',f['Arbeitsbereich'],None,None,LEFT,None)
cv=Canvas(f['Zeichenbrett'], width=w, height=h, bg="white")#nur optimieren wenn nötig
cv.grid()

#Dot-Notation vermeiden
#----
cvLine=cv.create_line; cvText=cv.create_text; cvOval=cv.create_oval
cvWith=cv.find_withtag; cvAll=cv.find_all; cvClose=cv.find_closest
cvCoords=cv.coords
getKoordSystem()
aktion(cv,[["<Motion>", getCursorPos],["<Leave>", setNull]])
#--------
    
#Eingabebereich
f['Eingabe']=Frame(f['Arbeitsbereich'], border=2)
f['Eingabe'].pack(side=RIGHT, fill=BOTH)
#---
Label(f['Eingabe'], text="  ").pack()
f['Buttons']=Frame(f['Eingabe'])
f['Buttons'].pack()
f['Buttons2']=Frame(f['Eingabe'])
f['Buttons2'].pack()
    

b['NeueFigur']=Button(f['Buttons'], image=malen_in,bg="black",relief=FLAT,command=checkButton_PunktZeichnen) #command=neueFigur
b['NeueFigur'].pack(side=LEFT)
b['Figurdaten']=Button(f['Buttons'], image=linieVerbinden_in, relief=FLAT, bg="black", command=checkButton_PunkteVerbinden)
b['Figurdaten'].pack(side=LEFT)
Label(f['Eingabe'], text="  ").pack()

f['Koordinaten']=Frame(f['Eingabe'], relief="groove", border=2)
f['Koordinaten'].pack(fill=X)
Label(f['Koordinaten'], text="Koordinaten eines Punktes:").pack(fill=X)
f['KoordEingabe']=Frame(f['Koordinaten'])
f['KoordEingabe'].pack(fill=X)
Label(f['KoordEingabe'], text="x=").pack(side=LEFT)
entryX=Entry(f['KoordEingabe'], width=4)
entryX.pack(side=LEFT)
Label(f['KoordEingabe'], text="y=").pack(side=LEFT)
entryY=Entry(f['KoordEingabe'], width=4)
entryY.pack(side=LEFT)
Label(f['KoordEingabe'], text="  ").pack(side=LEFT)
buttonKoordEingeben=Button(f['KoordEingabe'], text="eingeben", command=setKoordinaten)
buttonKoordEingeben.pack(side=LEFT)
Label(f['Koordinaten'], text="  ").pack()
buttonNPunkteEingeben=Button(f['Koordinaten'], relief=FLAT,image=listeKoord, command=nKoordEingeben)
buttonNPunkteEingeben.pack() #text="mehrere Punkte eingeben"
Label(f['Eingabe'], text="  ").pack()

spiegelpunktfenster=Frame(f['Eingabe'], relief="groove", border=2)
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

drehwinkelfenster=Frame(f['Eingabe'], relief="groove", border=2)
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


streckungsfenster=Frame(f['Eingabe'], relief="groove", border=2)
streckungsfenster.pack(fill=X)
Label(streckungsfenster, text="Streckungsfaktor:").pack(fill=X)
kEingabe=Frame(streckungsfenster)
kEingabe.pack(fill=X)
Label(kEingabe, text="k=").pack(side=LEFT)
entryK=Entry(kEingabe, width=4)
entryK.pack(side=LEFT)
buttonKEingeben=Button(kEingabe, text="eingeben", command=setK)
buttonKEingeben.pack(side=RIGHT)

Label(f['Eingabe'], text=" ").pack()
Label(f['Eingabe'], text="Cursor: ").pack(side=LEFT)
pos=Text(f['Eingabe'], width=10, height=1)
pos.pack(side=LEFT)


#----3. Ende des Arbeitsbereiches -------------------------

#sleep(20)
#----4. Beginn der Abspannsleiste -------------------------
abspann=Frame(f['Hauptfenster'])
abspann.pack()
info=Label(abspann, text=c+" 2006 Robert Willemelis ")
info.pack()
#----4. Ende der Abspannsleiste ---------------------------


#-------
f['Hauptfenster'].mainloop()
#----1. Ende des Masters -----------------------------------------------------------
