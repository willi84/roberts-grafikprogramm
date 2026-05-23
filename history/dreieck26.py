# Autor: Robert Willemelis
# Stand: 12.05.2006
# Version: 3.0
from Tkinter import *
from Canvas import *
from math import *
from string import *
from os import *
from tkMessageBox import *
from time import *
from threading import *
 

#globale threadVariable, Enter startet, getCursorPos stoppt und startet
#wenn auf infofeld gedrückt erscheint fenster
#drücken aktuellen punkt zeigen
#hilfestellungen
#icursor für namensänderungen, neuer name ist weiterer Tag: z.B. Original B7 -> #A1
#hervorheben bei infokästchen
#cursorvariablen neben cursor
#eingeben, versch optionen und bei berührung eingabe möglich
#try except bei tag-verwendung mit info es is halt nen kleiner laufzeitfehler aufgetreten
    
v={'p':[0,0],'aktuellesObjekt':[],'p1':[],'p2':[],'P1':[],'P2':[],'koord':[],
   'h':430, 'w':550,'ascii':65, 'ableitung':0,
   'k':1, 'n':0, 'winkel':0,'id':None,'info':None,'iP':None,'infoAct':False,
   'c':unichr(169), 'al':unichr(945), 'gr':unichr(186),
   'buttons':{'Punkt':False, 'Linie': False}}

v['xM']=(v['w']/2) #Koordinatenursprung
v['yM']=(v['h']/2)
v['x0']=v['xM']%50 
v['y0']=v['yM']%50
v['stX']=-(v['xM']-v['x0'])
v['stY']=  v['yM']-v['y0'] 

v['objekt']="?"+str(unichr(v['ascii'])) #enden

f={}; x={}; y={}; l={}; b={}; t={}; e={};m={}; cv={}
_=None


    


#------------------------------------------------



        
def getKoordSystem():
    global v
    #Achsen malen
    cLine(cv["1"],[v['xM'],0,v['xM'],v['h']],2,FIRST,_,[0,3,4],_)
    cText(cv["1"],v['xM']-7,5,"y",_,[0,3,5],_)
    cLine(cv["1"],[0,v['yM'],v['w'],v['yM']],2,LAST,_,[0,2,4],_)
    cText(cv["1"],v['w']-5,v['yM']+5,"x",_,[0,2,5],_)
    #x-Achsen-Markierung
    for i in range(0,v['w']+1,50):
        cLine(cv["1"],[v['x0']+i,v['yM']-3,v['x0']+i,v['yM']+3],1,_,_,[0,2,6],[str(v['stX']+i)])
        if v['stX']+i!=0:
            cText(cv["1"],v['x0']+i,v['yM']+9,str(v['stX']+i),("Arial",8),[0,2,7],[str(v['stX']+i)])   
        else:
            cText(cv["1"],v['x0']+i+5,v['yM']+9,str(v['stX']+i),("Arial",8),[0,2,7],[str(v['stX']+i)])        
    #y-Achsen-Markierung
    for i in range(0,v['h']+1,50):
        cLine(cv["1"],[v['xM']-3,v['y0']+i,v['xM']+3,v['y0']+i],1,_,_,[0,3,6],[str(v['stY']-i)])
        if v['stY']-i!=0:
            cText(cv["1"],v['xM']+15,v['y0']+i-1,str(v['stY']-i),("Arial",8),[0,3,7],[str(v['stY']-i)])
            

def setVar(variablen,kontroll,i1,i2):
    global v
    info=["Spiegelpunkteingabe","Koordinateneingabe","Winkeleingabe","Streckungsfaktor"]
    infoText=["Ein Punkt", "Der Punkt", "Der Spiegelpunkt"]
    weiter=True
    # keine oder mangelnden Eingaben
    if "" in variablen:
        weiter=False
        if variablen != ["",""]:
            if len(variablen)==1: showinfo(info[i1],"Sie haben keinen "+infoText[i2]+" eingegeben!")
            if len(variablen)==2:
                if variablen[0]=="": showinfo(info[i1],infoText[i2]+" konnte nicht eingegeben werden, da das x fehlte!")
                if variablen[1]=="": showinfo(info[i1],infoText[i2]+" konnte nicht eingegeben werden, da das y fehlte!")     
    if weiter==True and "" not in variablen:
        j=-1
        zulaessig=["0","1","2","3","4","5","6","7","8","9","."]
        for i in variablen:
            if weiter==True:
                j+=1
                variablen[j]=rstrip(lstrip(replace(variablen[j].get(),",", "."))) #normalform
                if variablen[j].count(".")>1:
                    showinfo(info[i1], "Bitte geben Sie bei Dezimalzahlen bitte nur ein Kommata ein!")
                    weiter=False
                else: 
                    for k in variablen[j]:
                        if k not in zulaessig:
                            if k==variablen[j][0] and k=="-":
                                pass
                            else:
                                showinfo(info[i1], "Bitte geben Sie wirklich nur Zahlen ein!")
                                weiter=False
    if weiter==True and "" not in variablen:
        if kontroll=="W":
            v['winkel']=float(variablen[j])
        if kontroll=="K":
            v['k']     =float(variablen[j])
        if kontroll in ["SP","P","KE"]:
            if kontroll in ["P","KE"]: v1=1
            else: v1=0
            
            x=float(variablen[0])
            y=float(variablen[1])
            v['n']+=1
            f=str(unichr(v['ascii']))
            tt=str(unichr(v['ascii']))+str(v['n'])
            tt1=str(unichr(v['ascii']))+str(v['n'])
            tt2=str(unichr(v['ascii']))+str(v['n'])+"("+v['al']+")"
            #v1=0 (DP/DPT),=1 (P/T)
            ll=[["black",[1,10],["°"+str(v['n']),[x,y],"%"+tt2,"^"+str(v['winkel'])],tt2,[1,11]],
                ["red"  ,[1,8] ,["*"+str(v['n']),[x,y],"%"+tt1                     ],tt1,[1,14]]]
            cOval(cv["1"],x-2+v['xM'],  -(y-2)+v['yM'],x+2+v['xM'],-(y+2)+v['yM'],ll[v1][0],ll[v1][1],ll[v1][2])
            cText(cv["1"],x-2+v['xM']+1,-(y-2+13)+v['yM'],ll[v1][3],("Arial",8,"bold"),ll[v1][4],ll[v1][2])
            if kontroll=="SP":
                v['p']=[x,y]
            if kontroll in ["P","KE"]:
                objektliste(v['objekt'])
    if kontroll in ["W","K"]:
        delEntry([e[kontroll]])
    if kontroll in ["SP","KE"]:
        delEntry([e['x'+kontroll],e['y'+kontroll]])

    
#------------------------------------------------------------------------------
        #spieglbild und tags abgleichen
def spiegeln(farbe, art):
    '''Verwaltung der zu spiegelnden Objekte.'''
    global v
    def spiegel(art,i,coord):
        spKoord=[]
        for j in coord:
            print j
            if art=="x": spKoord.extend([j[0],-j[1]])
            if art=="y": spKoord.extend([-j[0],j[1]])
            if art=="n": spKoord.extend([j[0]*_cos(i[0])+j[1]*(-_sin(i[0])), j[0]*_sin(i[0])+j[1]*_cos(i[0])])
            if art=="p": spKoord.extend([((j[0]-i[1][0])*_cos(i[0]) +(j[1]-i[1][1])*(-_sin(i[0])))+i[1][0],
                                         ((j[0]-i[1][0])*_sin(i[0]) +(j[1]-i[1][1])*_cos(i[0])) +i[1][1]])
            if art=="z": spKoord.extend([i[0]*j[0], i[0]*j[1]])
        return spKoord
    listeArt={'x':[], 'y':[], 'n':[v['winkel']], 'p':[v['winkel'], v['p']], 'z':[v['k']]}
    v['ableitung']+=1;
    figur=v['objekt']+v['ableitung']*"'"
    origFigur="§"+v['objekt'][1:]
    spiegelung="!"+art+str(listeArt[art])
    for i in cvWith(v['objekt']):
        koord=[]
        for j in cvTags(i):
            if j[0]=="[":
                koord=listing(j)
        if i in cvWith("T"):
            name="%"+cv["1"].itemcget(i, 'text')+v['ableitung']*"'"
            listeKoord=spiegel(art,listeArt[art],[[koord[0],koord[1]]])
            x=float(listeKoord[0])
            y=float(listeKoord[1])
            punkt=""
            for j in cvTags(i):
                if j[0]=="*":
                    punkt=j
            cOval(cv["1"],x-2+v['xM'],-(y-2)+v['yM'],x+2+v['xM'],-(y+2)+v['yM'],farbe,[9] ,[figur,origFigur,name,"&"+str(v['ableitung']),punkt,[x,y],spiegelung])
            cText(cv["1"],x-2+v['xM']+1,-(y-2+13)+v['yM'],name[1:],("Arial",8,"bold"),[14],[figur,origFigur,name,"&"+str(v['ableitung']),punkt,[x,y],spiegelung])
        if i in cvWith("L"):
            listeKoord=spiegel(art,listeArt[art],[[koord[0],koord[1]],[koord[2],koord[3]]])
            x1=float(listeKoord[0])
            y1=float(listeKoord[1])
            x2=float(listeKoord[2])
            y2=float(listeKoord[3])
            linie=""
            for j in cvTags(i):
                if j[0]=="~":
                    linie=j
            cLine(cv["1"],linieAnpassen(v['xM']+x1,v['yM']-y1,v['xM']+x2,v['yM']-y2),_,_,farbe,[13],[figur,origFigur,"&"+str(v['ableitung']),linie,[x1,y1,x2,y2],spiegelung])  
    objektliste(figur)
    

    

#----------------------------------------------------
#Events
def getCursorPos(event):


    #sorgen dass auch wirklich box verschwindet mittels try
    global v,cv
    x=event.x
    y=event.y
    t['Pos'].delete("0.0",END)
    t['Pos'].insert("0.0","("+str(x-v['xM'])+"/"+str(-(y-v['yM']))+")")
    if v['iP']!=_:
        # wenn Cursor außerhalb Punktbereich (+/- 2).
        if (x<(v['iP'][0]-2) or x>(v['iP'][0]+2)) or (y<(v['iP'][1]-2) or y>(v['iP'][1]+2)):
            cv["1"].delete(v['info'])
            v['iP']=v['info']=_
    cv["1"].after_cancel(v['id'])

    #Koordinate als string
    def test2():
        
        liste={'P': 'Punkt', 'SP': 'Spiegelpunkt', 'DP': 'Drehpunkt','L': 'Linie','SL': 'Spiegellinie'}
        texten="Leere"
        global cv
        xD=15
        yD=-20
        idii=cvClose(float(x),float(y))
        close=cvBB(idii)
        '''if (x >= close[0] or x <= close[2]) or (y >= close[1] or y <= close[3]):'''
        idiiTags=cvTags(idii)
        art=""
        if not 'KS' in idiiTags:
            koord=name=figur=[]; punkt={}
            
            if 'P' in idiiTags:
                art='P'
                for i in cvTags(idii):
                    if i[0]=="[":
                        koord=listing(i)
                    if i[0]=="%":
                        name=i[1:]
                    if i[0]=="?":
                        punkt['?']=i
                        figur="Figur "+i[1:]
                    if i[0]=="*":
                        punkt['*']=i
                punkt=punkt['?'][1:]+str(punkt['*'][1:])
                texten= str(koord)+"\n"+figur+"\n"+punkt+"\n"+name
                
            if 'SP' in idiiTags:
                art='SP'
                for i in cvTags(idii):
                    if i[0]=="[":
                        koord=listing(i)
                    if i[0]=="%":
                        name=i[1:]
                    if i[0]=="?":
                        punkt['?']=i
                        figur="Figur "+i[1:]
                    if i[0]=="*":
                        punkt['*']=i
                texten= 'spiegelpunkt'
            if 'DP' in idiiTags:
                art='DP'
                texten= 'drehpunkt'
            if 'L' in idiiTags:
                art='L'
                
                coo=""
                for i in cvTags(idii):
                    if i[0]=="[":
                        coo=listing(i)
                texten=("Linie\n"+"x1: "+str(coo[0])+"\n"+"y1: "+str(coo[1])+"\n"+"x2: "+str(coo[2])+"\n"+"y2: "+str(coo[3]))
                
                
            if 'SL' in idiiTags:
                art='SL'
                texten= 'spiegellinie'
            if 'DPT' in idiiTags:
                art='DP'
                texten= 'textDrehpunkt'
            if 'T' in idiiTags:
                art='P'
                for i in cvTags(idii):
                    if i[0]=="[":
                        koord=listing(i)
                    if i[0]=="%":
                        name=i[1:]
                    if i[0]=="?":
                        punkt['?']=i
                        figur="Figur "+i[1:]
                    if i[0]=="*":
                        punkt['*']=i
                punkt=punkt['?'][1:]+str(punkt['*'][1:])
                texten= str(koord)+"\n"+figur+"\n"+punkt+"\n"+name
        
        ##hier auch nen cancel nach so und so viel sekunden
        #objektArt=liste[art]
        '''photo={'P': ['rd_pin.gif','Punkt'],
               'SP':['yl_pin.gif','Spiegelpunkt'],
               'L' :['bl_pin.gif','Linie'],
               'SL':['gr_pin.gif','Spiegellinie']}'''
        #fra=Frame(bg='#FFFFCC')
        #fra.pack()
        #fr=Frame(fra,bg='#FFFFCC')
        #fr.pack(fill=X)
        '''froh=Frame()
        froh.pack()
        pin=PhotoImage(file=photo[art][0]) #photo[art][0]
        pinLa=Button(froh,image=pin)
        pinLa.pack()'''
        #arrt=Label(fr,text=photo[art][1],font=('Arial','10','bold'),bg='#FFFFCC')
        #arrt.pack()
        #frr=Frame(fra,relief=RIDGE,bd=2,bg='#FFFFCC')
        #frr.pack(fill=X)
        #laba=Label(frr, text="Punkt [100,50]", font=('Arial','10'),bg='#FFFFCC')
        #laba.pack(fill=X)
        #labs=Label(frr, text="A1", font=('Arial','10'),bg='#FFFFCC')
        #l#abs.pack(fill=X)
        f['infoWi']=Frame(bd=1)
        f['infoWi'].pack()
        
        bb1=Label(bg='#FFFFBB', text='Das ist ein Test!')
        bb1.pack()
        
        
        #i#mg_test = PhotoImage(file="linie_verbinden.gif")
        
        #label=Label(fr1, text="ich")
        #label.pack()
        if x > v['w']-50: xD=-53 
        if y < 50: yD=5
        #x+xD, y+yD
        v['info']=cv["1"].create_window(x+xD,y+yD,anchor=NW,window=f['infoWi'])
        v['iP']=[x,y]  #cvBB(idii) idii als Tag oder id
    v['id']=cv["1"].after(2000,test2)
    



def setNull(event):
    global v
    t['Pos'].delete("0.0",END)
    cv["1"].after_cancel(v['id'])
        
def punktZeichnen(event):
    global v
    objektliste(v['objekt']) 
    x=float(event.x-v['xM'])
    y=float(-(event.y-v['yM']))
    v['n']+=1
    name="%"+str(unichr(v['ascii']))+str(v['n'])
    cOval(cv["1"],x-2+v['xM'],-(y-2)+v['yM'],x+2+v['xM'],-(y+2)+v['yM'],"red",[1,8] ,[name, "*"+str(v['n']),[x,y]])
    cText(cv["1"],x-2+v['xM']+1,-(y-2+13)+v['yM'],name[1:],("Arial",8,"bold"),[1,14],[name, "*"+str(v['n']),[x,y]])
    
def getPunkt1(event): getPunkt('p1',event)
def getPunkt2(event): getPunkt('p2',event)
def getPunkt(p,event):
    global v
    v[p]=[]
    idii=cvClose(float(event.x),float(event.y))[0]
    if (idii in cvWith(v['objekt'])) and ((idii in cvWith("P")) or (idii in cvWith("T"))):
        for i in cvTags(idii):
            if i[0]=="[":
                v[p]=listing(i)
                v[p].append(idii)
    else:
        v[p]=[] 

def punkteVerbinden(event):
    global v
    objektliste(v['objekt'])
    getPunkt2(event)
    if v['p1'] != []:
        if v['p2'] != []:
            cLine(cv["1"],linieAnpassen(v['p1'][0]+v['xM'],v['yM']-v['p1'][1],v['p2'][0]+v['xM'],v['yM']-v['p2'][1]),_,_,"black",
                  [1,12],
                  ["~"+str([v['p1'][2],v['p2'][2]]),[float(v['p1'][0]),float(v['p1'][1]),float(v['p2'][0]),float(v['p2'][1])]])  
            objektliste(v['objekt'])
            
def buttons(button):
    global v
    liste={'Punkt':['NeueFigur',                                              
                    img['+malen'],img['-malen'],                                     
                    'red','black',                                            
                    [["<Button-1>", punktZeichnen]],[["<Button-1>", leer]]],  
           'Linie':['Figurdaten',                                             
                    img['+linie'],img['-linie'],                   
                    'blue','black',                                           
                    [["<Button-1>", getPunkt1],["<ButtonRelease-1>", punkteVerbinden]],[["<Button-1>", leer],["<ButtonRelease-1>", leer]]]}
    for i in v['buttons']:
        #alle Buttons außer dem Betätigten deaktivieren.
        if i !=button:  
            v['buttons'][i]=False
            b[liste[i][0]].config(image=liste[i][2],bg=liste[i][4])
            aktion(cv["1"],liste[i][6])
    #Zustand des aktivierten Buttons ändern.
    if v['buttons'][button]==False:
        v['buttons'][button]=True
        b[liste[button][0]].config(image=liste[button][1],bg=liste[button][3])
        aktion(cv["1"],liste[button][5])
    else:
        v['buttons'][button]=False
        b[liste[button][0]].config(image=liste[button][2],bg=liste[button][4])
        aktion(cv["1"],liste[button][6])
            
def checkButton_PunktZeichnen():   buttons('Punkt')
def checkButton_PunkteVerbinden(): buttons('Linie')


#----------------------------------------------------------------------------------
#Standardfunktionen

def window(name,nameWindow):
    global f
    f[name]=Tk()
    f[name].title(nameWindow)
def frame(name,root,border,relief,side,fill):
    global f     
    f[name]=Frame(f[root],relief=relief,border=border)
    f[name].pack(side=side,fill=fill)
def label(name,root,text,side,fill):
    global l
    l[name]=Label(f[root],text=text)
    l[name].pack(side=side,fill=fill)
def button(name,root,border,relief,image,text,bg,command,side,fill):
    global b
    b[name]=Button(f[root],image=image,text=text,bg=bg,command=command,relief=relief, border=border)
    b[name].pack(side=side,fill=fill)
def text(name,root,width,height,side,fill):
    global t
    t[name]=Text(f[root],width=width,height=height)
    t[name].pack(side=side,fill=fill)
def entry(name,root,width,side,fill):
    global e
    e[name]=Entry(f[root],width=width)
    e[name].pack(side=side,fill=fill)
def canvas(name,root,width,height,bg):
    global cv
    cv[name]=Canvas(f[root],width=width,height=height,bg=bg)
    cv[name].grid()
def menu(name,root,id,commands):
    global m
    m[name]=Menu(root)
    if id==1: root.add_cascade(menu=m[name], label=name)
    if commands!=_:
        for i in commands:
            if len(i)==0: m[name].add_separator()
            else:         m[name].add_command(label=i[0],command=i[1])

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

def leer():
    pass
def unfertig():
    pass
def _sin(a):
    return sin(radians(a))
def _cos(a):
    return cos(radians(a))
def pos(a):
    return float(str(a).replace('-',''))
def delEntry(entry):
    for i in entry:
        i.delete(0,len(i.get()))
def aktion(objekt,events):
    for i in events:
        objekt.bind(i[0],i[1])
def listing(string):
    liste=[]
    for i in (string.replace("[","")).replace("]","").split(","):
        liste.append(float(i))
    return liste
        

def cLine(objekt,koord,d,s,f,tK1,tK2):
    tags(objekt,tagKS(tK1,tK2),objekt.create_line(koord,width=d,arrow=s,fill=f))
def cText(objekt,pX,pY,t,f,tK1,tK2):
    tags(objekt,tagKS(tK1,tK2),objekt.create_text(pX,pY,text=t,font=f))
def cOval(objekt,x1,y1,x2,y2,fi,tK1,tK2):
    tags(objekt,tagKS(tK1,tK2),objekt.create_oval(x1,y1,x2,y2,fill=fi))
def malePunkt(x, y, farbe, figur, name, tagArt):
    cOval(cv["1"],x-2+v['xM'],-(y-2)+v['yM'],x+2+v['xM'],-(y+2)+v['yM'],farbe,_,[figur, name, tagArt])
    cText(cv["1"],x-2+v['xM']+1,-(y-2+13)+v['yM'],name,("Arial",8,"bold"),[14], [figur, name])
    objektliste(figur)

def maleLinie(x1, y1, x2, y2, farbe, figur, name, tagArt):
    cLine(cv["1"],linieAnpassen(x1, y1, x2, y2),_,_,farbe,_,[figur, name, tagArt])  
    objektliste(figur)
    
def tagKS(tagListe,tags):
    global v; tListe=[]
    liste=["KS",v['objekt'],"XA","YA","A","AT","M","MT","P","SP","DP","DPT","L","SL","T"]
    if tagListe !=_:
        for i in tagListe:
            tListe.append(liste[i])
    if tags !=_:
        for i in tags:
            tListe.append(i)
    return tListe
 
def objektliste(objekt):
    global v
    if objekt not in v['aktuellesObjekt']:
        v['aktuellesObjekt'].append(objekt)
def tags(objekt,tagListe,objektNr):
    for i in tagListe:
        objekt.addtag_withtag(i, objektNr)


#-------------------------------------------------------------------------------
#Buttons

#---Eingabe---
def setWinkel():
    setVar([e['W']],"W",2,_)
def setK():
    setVar([e['K']],"K",3,_)
def setP():
    setVar([e['xSP'],e['ySP']],"SP",0,2)
def setKoordinaten():
    setVar([e['xKE'],e['yKE']],'KE',1,1)
def nKoordEingeben():
    var=5  #Anzahl der moeglichen Eingaben
    window('nKoordRoot',"Eingabe mehrerer Punkte")
    label('mpe','nKoordRoot',"Mehrere Punkte eingeben",_,X)
    frame('mainFrame','nKoordRoot',_,_,_,_)
    for i in range(var):
        frame('NEingabe'+str(i),'mainFrame',_,_,_,X)
        label('x'+str(i),'NEingabe'+str(i),'x',LEFT,_); entry('x'+str(i),'NEingabe'+str(i),7,LEFT,_)
        label('y'+str(i),'NEingabe'+str(i),'y',LEFT,_); entry('y'+str(i),'NEingabe'+str(i),7,LEFT,_)
    def setNKoordinaten():
        for i in range(var):
            setVar([e['x'+str(i)],e['y'+str(i)]],"P",1,0)
        f['nKoordRoot'].destroy()
    button('buttonNKoord','nKoordRoot',_,_,_,"eingeben",_,setNKoordinaten,_,_)
    f['nKoordRoot'].mainloop()


#---Menue: Aktionen---
def neu():
    global v
    v['ableitung']=v['n']=v['winkel']=0
    v['ascii']=65
    v['objekt']="?"+str(unichr(v['ascii']))
    v['p']=[0,0]
    v['k']=1
    for i in cvAll():
        if i not in cvWith("KS"): cv["1"].delete(i)
def neueFigur():
    global v
    v['ascii']+=1
    v['objekt']="?"+str(unichr(v['ascii']))
    v['n']=v['ableitung']=0
def deleteAktuellesObjekt():
    global v
    #1) mindestens eine Figur
    if len(v['aktuellesObjekt'])>0:

        #1.1) Grundfigur A
        if len(v['aktuellesObjekt'])==1:    
            delObjekt=v['aktuellesObjekt'][0]
            v['n']=0
            for i in cvWith(delObjekt):
                cv["1"].delete(i)

        #1.2) mehrere Figuren
        if len(v['aktuellesObjekt'])>1:     
            delObjekt=v['aktuellesObjekt'].pop()
            aktuellesObjekt=v['aktuellesObjekt'][len(v['aktuellesObjekt'])-1]
            if "'" in delObjekt:
                v['ableitung']-=1     
            else:
                v['ascii']-=1
            for i in cvWith(delObjekt):
                cv["1"].delete(i)
            liste=cvWith(aktuellesObjekt)
            listeN=set()

            #Ermitteln von aktuellem n der jetzt aktuellen Figur.
            for i in liste:
                if ('T' in cv["1"].gettags(i)) or ('DPT' in cv["1"].gettags(i)):
                    for j in cv["1"].gettags(i):
                        if ('*' in j) or ('°' in j):
                            j=(j.replace("°",'')).replace("*","")
                            if j in '0123456789': #Kontrolle, ob nur Zahl noch ist.
                                listeN.add(int(j))
            v['n']= max(listeN)
            
            #wenn eine Figur geloescht, damit v['objekt'] wieder aktuell
            beenden=False
            while not beenden: 
                for i in v['aktuellesObjekt']:
                    if "'" not in i:
                        v['objekt']=i
                        beenden=True

#---Menue: Spiegeln---
def anXAchseSpiegeln():
    spiegeln("#3333ff", "x")
def anYAchseSpiegeln():
    spiegeln("#ff9900", "y")
def amUrsprungSpiegeln():
    spiegeln("#cc0099", "n")
def anPSpiegeln():
    spiegeln("#d2691e", "p")
def zenStrecken():
    spiegeln("#33cc00", "z") 

#--------------------------------------------------------------------------------------------
#Oberfläche
    
#----1. Start des Masters ----------------------------------------------------------
window('Hauptfenster',"Roberts Grafikprogramm 3.0")

#-------
img={'P' : PhotoImage(file="images/rd_pin.gif"),
     'L' : PhotoImage(file="images/bl_pin.gif"),
     'SP': PhotoImage(file="images/gr_pin.gif"),
     'SL': PhotoImage(file="images/yl_pin.gif"),
     '+malen': PhotoImage(file="images/malen.gif"),
     '-malen': PhotoImage(file="images/malen_in.gif"),
     '+linie': PhotoImage(file="images/linie_verbinden.gif"),
     '-linie': PhotoImage(file="images/linie_verbinden_in.gif"),
     '+KE': PhotoImage(file="images/liste.gif"),
     '-KE': PhotoImage(file="images/liste_in.gif")}
#----2. Beginn Menueoptionsleiste -------------------------
menu('menue',f['Hauptfenster'],0,_)
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
frame('Arbeitsbereich','Hauptfenster',2,"groove",_,_) 
#Zeichenfläche mit Canvas-Widget
frame('Zeichenbrett','Arbeitsbereich',_,_,LEFT,_)
canvas("1",'Zeichenbrett',v['w'],v['h'],"white")
v['id']=cv["1"].after(1,leer) #Start

#Dot-Notation vermeiden
#----
cvWith=cv["1"].find_withtag; cvAll=cv["1"].find_all;
cvClose=cv["1"].find_closest; cvCoords=cv["1"].coords;
cvTags=cv['1'].gettags
cvOpt=cv['1'].itemcget
cvBB=cv['1'].bbox
cvText=cv['1'].icursor
getKoordSystem()
aktion(cv["1"],[["<Motion>", getCursorPos],
                ["<Leave>", setNull]])
#["<Enter>",test]
#--------
    
#Eingabebereich
frame('Eingabe','Arbeitsbereich',2,_,RIGHT,BOTH)
#---
label('leerEingabe','Eingabe',"  ", _, _)
frame('Buttons','Eingabe',_,_,_,_)
frame('Buttons2','Eingabe',_,_,_,_)

button('NeueFigur','Buttons',_,FLAT,img['-malen'],_,"black",checkButton_PunktZeichnen,LEFT,_)



button('Figurdaten','Buttons',_,FLAT,img['-linie'],_,"black",checkButton_PunkteVerbinden,LEFT,_)


label('leerEingabe2','Eingabe',"  ", _, _)  #probieren nur leerEingabe

frame('Koordinaten', 'Eingabe',2,"groove",_,X)
label('KEP','Koordinaten',"Koordinaten eines Punktes:", _, X)

#Eingabe eines Punktes
frame('KoordEingabe','Koordinaten',_,_,_,X)
label('xKE','KoordEingabe',"x=",LEFT,_)
entry('xKE','KoordEingabe',4,LEFT,_)
label('yKE','KoordEingabe',"y=",LEFT,_)
entry('yKE','KoordEingabe',4,LEFT,_)
label('leerKE','KoordEingabe',"  ", LEFT,_)
button('KoordEingeben','KoordEingabe',_,_,_,"eingeben",_,setKoordinaten,LEFT,_)
      
         

label('leerK','Koordinaten',"  ", _, _)
button('NPunkteEingeben','Koordinaten',_,FLAT,img['+KE'],_,_,nKoordEingeben,_,_)#text="mehrere Punkte eingeben"
label('leerEingabe','Eingabe',"  ", _, _)

frame('SP', 'Eingabe',2,"groove",_,X)
label('SP','SP',"Spiegelpunkt:", _,X)
frame('SPE', 'SP',_,_,_,X)

label('xSPE','SPE',"x=", LEFT,_)##
entry('xSP','SPE',4,LEFT,_)
label('ySPE','SPE',"y=",LEFT,_)##
entry('ySP','SPE',4,LEFT,_)

label('leerSPE','SPE',"  ",LEFT,_) #eigenen Frame machen
button('SPE','SPE',_,_,_,"eingeben",_,setP,LEFT,_)

frame('W','Eingabe',2,"groove",_,X)
label('dWW','W',"Drehwinkel:",_,X)
frame('WE','W',_,_,_,X)

label('alpha','WE',v['al']+"=",LEFT,_)####
entry('W','WE',4,LEFT,_)

label('grad','WE',v['gr'],LEFT,_)
button('WE','WE',_,_,_,"eingeben",_,setWinkel,RIGHT,_)

frame('K','Eingabe',2,"groove",_,X)
label('KT','K',"Streckungsfaktor:",_,X)
frame('KE','K',_,_,_,X)

label('K','KE',"k=",LEFT,_)
entry('K','KE',4,LEFT,_)
button('KE','KE',_,_,_,"eingeben",_,setK,RIGHT,_)

label('leerE','Eingabe'," ",_,_)
label('Cursor','Eingabe',"Cursor: ",LEFT,_)
text('Pos','Eingabe',10,1,LEFT,_)

#----3. Ende des Arbeitsbereiches -------------------------

#----4. Beginn der Abspannsleiste -------------------------
frame('last','Hauptfenster',_,_,_,_)
label('info','last',v['c']+" 2007 Robert Willemelis ",_,_)

#----4. Ende der Abspannsleiste ---------------------------


#-------
f['Hauptfenster'].mainloop()
#----1. Ende des Masters -------------------------------------------------------
