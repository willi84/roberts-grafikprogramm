#Autor   : Robert Willemelis
#Stand   : 29.05.2007
#Version : 4.0
#Zeitraum: 26.04.2006 - 30.05.2007

from Tkinter import *
from Canvas import *
from math import *
from string import *
from os import *
from tkMessageBox import *
from time import *
from threading import *
import tkFileDialog

_=None
v={'p':[0,0,_],'aktuellesObjekt':[],'p1':[],'p2':[],'id':0,
   'h':430, 'w':550,'ascii':65, 'ableitung':0,'Cur':[_,_],
   'k':1, 'n':0, 'winkel':0,'thread':_,'thread2':_,'info':_,'info2':_,'idObj':_,'infoArt':[_,_,_],
   'c':unichr(169), 'al':unichr(945), 'gr':unichr(186),
   'buttons':{'Punkt':False, 'Linie': False}}
v['xM']=(v['w']/2) #Koordinatenursprung
v['yM']=(v['h']/2)
v['x0']=v['xM']%50 
v['y0']=v['yM']%50
v['stX']=-(v['xM']-v['x0'])
v['stY']=  v['yM']-v['y0'] 
v['objekt']="?"+str(unichr(v['ascii'])) 

f={}; x={}; y={}; l={}; b={}; t={}; e={};m={}; cv={}
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
            v['n']+=1;id1=v['id']+1;id2=v['id']+2;v['id']+=2
            t=[str(unichr(v['ascii']))+str(v['n'])+"("+v['al']+")",str(unichr(v['ascii']))+str(v['n'])]
            #v1=0 (DP/DPT),=1 (P/T)
            i=[['black',[1,10,15],[1,11,15]],
               ['red'  ,[1,8,15 ],[1,14,15]]]
            cOval(cv["1"],x-2+v['xM'],  -(y-2)+v['yM'],x+2+v['xM'],-(y+2)+v['yM'],i[v1][0],i[v1][1],["*"+str(v['n']),[x,y],"%"+t[v1],'@'+str(id1),'^'+str([id1,id2])])
            cText(cv["1"],x-2+v['xM']+1,-(y-2+13)+v['yM'],t[v1],("Arial",8,"bold"),i[v1][2]        ,["*"+str(v['n']),[x,y],"%"+t[v1],'@'+str(id2),'g'+str([id1,id2])])
            if kontroll=="SP":
                v['p']=[x,y,str(id1)]
            if kontroll in ["P","KE"]:
                objektliste(v['objekt'])
    if kontroll in ["W","K"]:
        delEntry([e[kontroll]])
    if kontroll in ["SP","KE"]:
        delEntry([e['x'+kontroll],e['y'+kontroll]])
        
def spiegeln(farbe, art):
    global v
    def getSpiegelung(art,i,coord):
        spKoord=spp=[]
        for j in coord:
            if art=="x": spKoord.extend([j[0],-j[1]])
            if art=="y": spKoord.extend([-j[0],j[1]])
            if art=="n": spKoord.extend([j[0]*_cos(i[0])+j[1]*(-_sin(i[0])), j[0]*_sin(i[0])+j[1]*_cos(i[0])])
            if art=="p":
                for k in cvTags('@'+i[1]):
                    if k[0]=="[":
                        spp=listing(k[1:],1)
                spKoord.extend([((j[0]-spp[0])*_cos(i[0]) +(j[1]-spp[1])*(-_sin(i[0])))+spp[0],
                                         ((j[0]-spp[0])*_sin(i[0]) +(j[1]-spp[1])*_cos(i[0])) +spp[1]])
            if art=="z": spKoord.extend([i[0]*j[0], i[0]*j[1]])
        return spKoord
    spPunkt=[]
    listeArt={'x':[], 'y':[], 'n':[v['winkel']], 'p':[v['winkel'], v['p'][2]], 'z':[v['k']]}
    v['ableitung']+=1;
    figur=v['objekt']+v['ableitung']*"'"
    origFigur="§"+v['objekt'][1:]
    spiegelung="!"+art+str(listeArt[art])
    for i in cvWith(v['objekt']):
        koord=[]
        for j in cvTags(i):
            if j[0]=="[":
                koord=listing(j,1)
        if i in cvWith("T"):
            #Spiegelpunkte
            name="%"+cv["1"].itemcget(i, 'text')+v['ableitung']*"'"
            listeKoord=getSpiegelung(art,listeArt[art],[[koord[0],koord[1]]])
            x=float(listeKoord[0])
            y=float(listeKoord[1])
            punkt=ablIdii=""
            
            for j in cvTags(i):
                if j[0]=="*":
                    punkt=j
                if j[0]=="@":
                    ablIdii="~["+j[1:]+"]"
            id1=v['id']+1;id2=v['id']+2;v['id']+=2
            cOval(cv["1"],x-2+v['xM'],-(y-2)+v['yM'],x+2+v['xM'],-(y+2)+v['yM'],farbe,[9,15] ,[ablIdii,figur,origFigur,name,"&"+str(v['ableitung']),punkt,[x,y],spiegelung,'@'+str(id1),'^'+str([id1,id2])])
            cText(cv["1"],x-2+v['xM']+1,-(y-2+13)+v['yM'],name[1:],("Arial",8,"bold"),[14,15],[ablIdii,figur,origFigur,name,"&"+str(v['ableitung']),punkt,[x,y],spiegelung,'@'+str(id2),'^'+str([id1,id2])])
        if i in cvWith("L"):
            #Spiegellinie
            listeKoord=getSpiegelung(art,listeArt[art],[[koord[0],koord[1]],[koord[2],koord[3]]])
            x1=float(listeKoord[0])
            y1=float(listeKoord[1])
            x2=float(listeKoord[2])
            y2=float(listeKoord[3])
            ablIdii=origLinie=""; linie=[]
            for j in cvTags(i):
                if j[0]=="@": # ID der Originallinie wird Ableitungslinie
                    ablIdii="~["+j[1:]+"]"
                if j[0]=="=": # ID der Punkte der Linie ermitteln
                    origLinie=listing(j[1:],0)
                    line=[]
                    for k in origLinie: # 1.Ermitteln der Punkte(*) der Originallinie
                        x=0
                        for l in cvTags(cvWith('@'+str(k))):
                            if l[0]=="*":
                                line.append(l[1:])
                                
                    for k in line: # 2. Ermitteln der ID der Spiegelpunkte
                        for l in cvWith(figur): # alle Objekte der Figur
                            bools=False;id1=""
                            for m in cvTags(l):
                                if m[0]=="@":
                                    id1=m[1:]
                                if k==m[1:]: # wenn Originalpunkt mit Spiegelpunkt übereinstimmt...
                                    bools=True
                            if ('SP' in cvTags(l)) and (id1 not in linie):
                                linie.append(id1) # ...wird dessen ID der PunkteIDs der Linie zugefügt.
            linie="=["+linie[0]+","+linie[1]+"]"
            v['id']+=1
            cLine(cv["1"],linieAnpassen(v['xM']+x1,v['yM']-y1,v['xM']+x2,v['yM']-y2),_,_,farbe,[13,15],
                       [ablIdii,figur,origFigur,"&"+str(v['ableitung']),linie,[x1,y1,x2,y2],spiegelung,'@'+str(v['id'])])
    objektliste(figur)

def showInfo():
    global v
    if v['infoArt']!=[_,_,_]:
        v['info2']=Label(f['Hauptfenster'],text=v['infoArt'][0],bg='#FFFFCC')
        v['info2'].place(x=v['Cur'][0]+v['infoArt'][1]-25, y=v['Cur'][1]+v['infoArt'][2])
def infobox():
    global v,cv
    x=v['Cur'][0]; y=v['Cur'][1]
    liste={'P': 'Punkt', 'T': 'Punkt','SP': 'Spiegelpunkt','DP': 'Drehpunkt','DPT': 'Drehpunkt','L': 'Linie','SL': 'Spiegellinie'}
    info={};
    if v['idObj']!=_:
        figur=punkt=name=""; info['Ableitung']=0
        art=list(set(['P','DP','SP','T','DPT','L','SL'])& set(cvTags(v['idObj'])))[0]
        if art in ['P','T','L']: info['Bild']="f"
        if art in ['DP','DPT'] : info['Bild']="d"
        info['art']=liste[art]
        info['origPunkt']=info['origLinie']=info['winkel']=info['k']=info['p']=""; info['pKoord']=[_,_]
        for i in cvTags(v['idObj']):
            if i[0]=="?":
                info['figur']=i[1:]
                figur=i[1:].replace("'","")
            if i[0]=="*":
                punkt=i[1:]
            if i[0]=="%":
                info['name']=i[1:] 
            if i[0]=="[":
                info['koord']=rd(listing(i,1))
            if i[0]=="&":
                info['Ableitung']=int(i[1:])
            if i[0]=="~":
                for j in cvTags(cvWith('@'+listing(i[1:],0)[0])):
                    if j[0]=="%":
                        info['origPunkt']=j[1:]
                    if j[0]=="=":
                        linie=[]
                        for k in listing(j[1:],0):
                            for l in cvTags(cvWith('@'+str(k))):
                                if l[0]=="%":
                                    linie.append(l[1:])
                        info['origLinie']=linie[0]+"-"+linie[1]
            if i[0]=="=":
                linie2=[]
                for j in listing(i[1:],0):
                    for k in cvTags(cvWith('@'+j)):
                        if k[0]=="%":
                            linie2.append(k[1:])
                info['Linie']=linie2[0]+"-"+linie2[1]   
            if i[0]=="!":
                info['Bild']=i[1]
                liste=listing(i[2:],0)
                if i[1]=="n" or i[1]=="p":
                    info['winkel']=str(rd([float(liste[0])])[0])
                if i[1]=="p":
                    for j in cvTags(cvWith('@'+str((liste[1].replace("'","")).replace('"','')))):
                        if j[0]=="^":
                            info['p']=cv["1"].itemcget(cvWith('@'+listing(j[1:],0)[1]), 'text')
                        if j[0]=="[":
                            info['pKoord']=rd(listing(j,1))
                if i[1]=="z":
                    info['k']=str(rd([float(liste[0])])[0])
        info['punkt']=figur+punkt+info['Ableitung']*"'"
    if (art=='T') and (info['Bild'] in ['x','y','p','n','z']):
        info['art']='Spiegelpunkt'
    if info!={}:
        w=150;h=200
        point=line="";spArt=spiegelung={}
        if info['art'] in ['Punkt','Spiegelpunkt','Drehpunkt']: 
            point=('Figur: '+info['figur']+'\n'+
                  'Punkt: '+info['punkt']+" ("+str(info['koord'][0])+"/"+str(info['koord'][1])+")")
        if info['art'] in ['Linie','Spiegellinie']:
            line=('Figur: '+info['figur']+'\n'+
                 'Linie: '+linie2[0]+" ("+str(info['koord'][0])+"/"+str(info['koord'][1])+")\n"
                 '         '+linie2[1]+" ("+str(info['koord'][2])+"/"+str(info['koord'][3])+")")
        i={'Punkt':point,'Linie':line,'Drehpunkt':point}
        if info['art'] in ['Spiegelpunkt','Spiegellinie']:
            spArt['Spiegelpunkt']="des\nPunktes "+info['origPunkt']+" "
            spArt['Spiegellinie']="der\nLinie ("   +info['origLinie']+") "
            spiegelung['f']=spiegelung['d']=""
            spiegelung['x']='Spiegelung '+spArt[info['art']]+'\nan der x-Achse.'
            spiegelung['y']='Spiegelung '+spArt[info['art']]+'\nan der y-Achse.'
            spiegelung['n']=('Spiegelung '+spArt[info['art']]+' am\nKoordinatenursprung\num den Winkel '+
                            v['al']+"="+info['winkel']+v['gr']+".")
            spiegelung['p']=('Spiegelung '+spArt[info['art']]+'\nam Punkt '+info['p']+" ("+
                            str(info['pKoord'][0])+"/"+str(info['pKoord'][1])+')\num den Winkel '+v['al']+"="+info['winkel']+v['gr']+".")
            spiegelung['z']='Zentrische Streckung '+spArt[info['art']]+'\num k='+info['k']+"."
            i['Spiegelpunkt']=point+'\n\n'+spiegelung[info['Bild']]
            i['Spiegellinie']=line +'\n\n'+spiegelung[info['Bild']]
        p="";pKoord=leng=[]
        if info['art'] in ['Punkt','Spiegelpunkt','Drehpunkt']:
            p=info['art']+' ('+info['name']+')'
        if info['art'] in ['Linie','Spiegellinie']:
            p=info['art']+' ('+info['Linie']+')'
        v['info']=Canvas(v['info'],bg='#FFFFCC',width=w, height=h)
        headImage=v['info'].create_image(16,10,image=img[info['Bild']])
        headName=v['info'].create_text(33,13,text=p,font=('Arial','9','bold'))
        mainInfo=v['info'].create_text(5,30,text=i[info['art']])
        headKoord= v['info'].bbox(headName)
        mainKoord= v['info'].bbox(mainInfo)
        v['info'].move(headName,33-headKoord[0],0)
        v['info'].move(mainInfo,10-mainKoord[0],30-mainKoord[1])
        headKoord2= v['info'].bbox(headName)
        mainKoord2= v['info'].bbox(mainInfo)
        leng.append(33+(headKoord2[2]-headKoord2[0]))
        leng.append(mainKoord2[2])
        breite=max(leng)
        hoehe=mainKoord2[3]
        v['info'].configure(width=breite)
        v['info'].configure(height=hoehe)
        v['info'].create_line(0,23,v['info'].cget('width'),23)
        x=x+15
        if (x+breite+10)>=v['w']:
            x=x-30-breite
        if (y+hoehe+10)>=v['h']:
            y=v['h']-10-hoehe
        v['info'].place(x=x,y=y)

def buttons(button):
    global v
    liste={'Punkt':['punktZeichnen',                                              
                    img['+malen'],img['-malen'],                                     
                    'red','black',                                            
                    [["<Button-1>", punktZeichnen]],[["<Button-1>", leer]]],  
           'Linie':['linieZeichnen',                                             
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
def checkButton_PunktZeichnen():
    buttons('Punkt')
def checkButton_PunkteVerbinden():
    buttons('Linie')           
#----------------------------------------------------
#Events
def getCursorPos(event):
    global v,cv
    x=event.x
    y=event.y
    t['Pos'].delete("0.0",END)
    t['Pos'].insert("0.0","("+str(x-v['xM'])+"/"+str(-(y-v['yM']))+")")
def setNull(event):
    global v
    t['Pos'].delete("0.0",END)
    
def getPunkt1(event):
    getPunkt('p1',event)
def getPunkt2(event):
    getPunkt('p2',event)
def getPunkt(p,event):
    global v
    v[p]=[_,_,_]
    idii=cvClose(float(event.x),float(event.y))[0]
    if (idii in cvWith(v['objekt'])) and ((idii in cvWith("P")) or (idii in cvWith("T"))):
        for i in cvTags(idii):
            if i[0]=="[":
                v[p][0]=listing(i,1)[0]
                v[p][1]=listing(i,1)[1]
            if i[0]=='^':
                v[p][2]=listing(i[1:],0)[0]       
    else:
        v[p]=[]

def punktZeichnen(event):
    global v
    objektliste(v['objekt']) 
    x=float(event.x-v['xM'])
    y=float(-(event.y-v['yM']))
    v['n']+=1
    name="%"+str(unichr(v['ascii']))+str(v['n'])
    id1=v['id']+1;id2=v['id']+2;v['id']+=2
    cOval(cv["1"],x-2+v['xM'],-(y-2)+v['yM'],x+2+v['xM'],-(y+2)+v['yM'],"red",[1,8,15] ,[name, "*"+str(v['n']),[x,y],'@'+str(id1),'^'+str([id1,id2])])
    cText(cv["1"],x-2+v['xM']+1,-(y-2+13)+v['yM'],name[1:],("Arial",8,"bold"),[1,14,15],[name, "*"+str(v['n']),[x,y],'@'+str(id2),'^'+str([id1,id2])])
def punkteVerbinden(event):
    global v
    objektliste(v['objekt'])
    getPunkt2(event)
    if v['p1'] != []:
        if v['p2'] != []:
            linie="="+"["+v['p1'][2]+","+v['p2'][2]+"]"
            v['id']+=1
            cLine(cv["1"],linieAnpassen(v['p1'][0]+v['xM'],v['yM']-v['p1'][1],v['p2'][0]+v['xM'],v['yM']-v['p2'][1]),_,_,"black",
                  [1,12,15],[linie,[float(v['p1'][0]),float(v['p1'][1]),float(v['p2'][0]),float(v['p2'][1])],'@'+str(v['id'])])
            objektliste(v['objekt'])

def leer(event):
    pass           

#Infoboxen
def setIDObj(event):
    global v
    v['idObj']=cvClose(event.x,event.y)
    v['Cur']=[event.x,event.y]
    v['thread']=cv["1"].after(2000,infobox)
def delIDObj(event):
    global v
    v['idObj']=_
    cv["1"].after_cancel(v['thread'])
    v['Cur']=[_,_]
    if v['info']!=_:
        v['info'].destroy()
    v['info']=_

def btnPunktZeichnen(event):
    global v
    v['infoArt']=["Einen Punkt freihand zeichnen!",596-40,50]
def btnLinieZeichnen(event):
    global v
    v['infoArt']=["Zwei Punkte zu einer Linie verbinden!",633-90,50]
def btnNKoordinaten(event):
    global v
    v['infoArt']=["Mehrere Punkte eingeben!",613-50,170]
def delInfoArt(event):
    global v
    v['infoArt']=[_,_,_]
def infoZeichnen(event):
    global v
    f['Hauptfenster'].after_cancel(v['thread2'])
    if v['info2']!=_: v['info2'].destroy()
    v['info2']=v['Cur']=_
    v['thread2']=f['Hauptfenster'].after(2000,showInfo)
    v['Cur']=[event.x,event.y]
    
#Schnellwahltasten
def sw_speichern(event):
    speichern()
def sw_laden(event):
    laden()
def sw_neu(event):
    neu()
def sw_quit(event):
    f['Hauptfenster'].destroy()
def sw_xSp(event):
    anXAchseSpiegeln()
def sw_ySp(event):
    anYAchseSpiegeln()
def sw_nSp(event):
    amUrsprungSpiegeln()
def sw_pSp(event):
    anPSpiegeln()
def sw_zSp(event):
    zenStrecken()
#Enter
def winkelEnter(event):
    setWinkel()
#----------------------------------------------------------------------------------
#Standardfunktionen

def window(name,nameWindow,root):
    global f
    f[name]=Tk()
    f[name].title(nameWindow)
    if root!=_:
        f[name].wm_iconbitmap(root)
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

def rd(num):
    #runden
    liste=[]
    for i in num:
        zahl=round(i,1)
        if int(zahl)==zahl:
            liste.append(int(zahl))
        else:
            liste.append(zahl)
    return liste
def _sin(a):
    return sin(radians(a))
def _cos(a):
    return cos(radians(a))
def delEntry(entry):
    for i in entry:
        i.delete(0,len(i.get()))
def aktion(objekt,events):
    for i in events:
        objekt.bind(i[0],i[1])
def listing(string,var):
    liste=[]
    if var in [0,1]:
        for i in ((string.replace("[","")).replace("]","").replace(" ","")).split(","):
            if var==0:
                liste.append(i)
            if var==1:
                liste.append(float(i))
    if var==2:
        for i in string.split('|'):
            liste.append(i)
    return liste
def objektliste(objekt):
    global v
    if objekt not in v['aktuellesObjekt']:
        v['aktuellesObjekt'].append(objekt)
        
def cLine(objekt,koord,d,s,f,tK1,tK2):
    return tags(objekt,tagKS(tK1,tK2),objekt.create_line(koord,width=d,arrow=s,fill=f))
def cText(objekt,pX,pY,t,f,tK1,tK2):
    return tags(objekt,tagKS(tK1,tK2),objekt.create_text(pX,pY,text=t,font=f))
def cOval(objekt,x1,y1,x2,y2,fi,tK1,tK2):
    return tags(objekt,tagKS(tK1,tK2),objekt.create_oval(x1,y1,x2,y2,fill=fi))

def tagKS(tagListe,tags):
    global v; tListe=[]
    liste=["KS",v['objekt'],"XA","YA","A","AT","M","MT","P","SP","DP","DPT","L","SL","T","B"]
    if tagListe !=_:
        for i in tagListe:
            tListe.append(liste[i])
    if tags !=_:
        for i in tags:
            tListe.append(i)
    return tListe
def tags(objekt,tagListe,objektNr):
    for i in tagListe:
        objekt.addtag_withtag(i, objektNr)
    return objektNr
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
    window('nKoordRoot',"Eingabe mehrerer Punkte",'images/head.ico')
    label('mpe','nKoordRoot',"Mehrere Punkte eingeben",_,X)
    frame('mainFrame','nKoordRoot',_,_,_,_)
    for i in range(var):
        frame('NEingabe'+str(i),'mainFrame',_,_,_,X)
        label('x'+str(i),'NEingabe'+str(i),'x'+str(i+1)+"=",LEFT,_); entry('x'+str(i),'NEingabe'+str(i),7,LEFT,_)
        label('y'+str(i),'NEingabe'+str(i),'y'+str(i+1)+"=",LEFT,_); entry('y'+str(i),'NEingabe'+str(i),7,LEFT,_)
    def setNKoordinaten():
        for i in range(var):
            setVar([e['x'+str(i)],e['y'+str(i)]],"P",1,0)
        f['nKoordRoot'].destroy()
    button('buttonNKoord','nKoordRoot',_,_,_,"eingeben",_,setNKoordinaten,_,_)
    f['nKoordRoot'].mainloop()


#---Menue: Aktionen---
def neu():
    global v
    v['ableitung']=v['n']=v['winkel']=v['id']=0
    v['ascii']=65
    v['objekt']="?"+str(unichr(v['ascii']))
    v['p']=[0,0,_]
    v['k']=1
    v['Cur']=[_,_]
    if v['info']!=_:
        v['info'].destroy()
    v['info']=v['idObj']=_
    
    for i in cvAll():
        if i not in cvWith("KS"): cv["1"].delete(i)
def neueFigur():
    global v
    v['ascii']+=1
    v['objekt']="?"+str(unichr(v['ascii']))
    v['n']=v['ableitung']=0
def laden():
    global v,cv
    datei=tkFileDialog.askopenfile()
    if datei:
        #Kontrolle, ob es die richtige Datei ist.
        if datei.readline()=='Roberts Grafikprogramm\n':
            for i in cvWith('B'):
                cv["1"].delete(i)
            n=0
            for i in datei.readlines():
                n+=1
                if n==1:
                    #Liste der Objekte erstellen
                    v['aktuellesObjekt']=listing(i.replace('\n',''),0)
                if n==2:
                    #Variablen erstellen
                    liste=listing(i.replace('\n',''),0)
                    v['p'][0]=float(liste[0])
                    v['p'][1]=float(liste[1])
                    if liste[2]=='None':
                        v['p'][2]=_
                    else:
                        v['p'][2]=liste[2]
                    v['id']=int(liste[3])
                    v['h']=int(liste[4])
                    v['w']=int(liste[5])
                    v['ascii']=int(liste[6])
                    v['ableitung']=int(liste[7])
                    v['k']=float(liste[8])
                    v['n']=int(liste[9])
                    v['winkel']=float(liste[10])
                    v['p1']=v['p2']=[]
                    v['Cur']=[_,_]
                    v['thread']=v['info']=v['idObj']=_
                    v['buttons']['Punkt']=v['buttons']['Linie']=False
                    v['xM']=(v['w']/2); v['yM']=(v['h']/2)
                    v['x0']=v['xM']%50; v['y0']=v['yM']%50
                    v['stX']=-(v['xM']-v['x0'])
                    v['stY']=  v['yM']-v['y0']
                    v['objekt']="?"+str(unichr(v['ascii']))
                if n>=3:
                    #alle grafischen Elemente aus deren Tags erstellen
                    liste=listing(i.replace('\n',''),2)
                    koord=name=farbe=_
                    color={'x':"#3333ff",'y':"#ff9900",'n':"#cc0099",'p':"#d2691e",'z':"#33cc00",'P':'red','DP':'black','L':'black',None:""}
                    for j in liste:
                        if j[0]=="[":
                            koord=listing(j[1:],1)
                        if j[0]=="%":
                            name=j[1:]
                        if j[0]=="!":
                            farbe=j[1]
                    if list(set(['P','DP','L'])&set(liste))!=[]:
                        farbe=list(set(['P','DP','L'])&set(liste))[0]
                    farbe=color[farbe]
                    if list(set(['P','DP','SP'])&set(liste))!=[]:
                        cOval(cv["1"],koord[0]-2+v['xM'],-(koord[1]-2)+v['yM'],koord[0]+2+v['xM'],-(koord[1]+2)+v['yM'],farbe,_,liste)
                    if list(set(['T','DPT'])&set(liste))!=[]:
                        cText(cv["1"],koord[0]-2+v['xM']+1,-(koord[1]-2+13)+v['yM'],name,("Arial",8,"bold"),_,liste)
                    if list(set(['L','SL'])&set(liste))!=[]:
                        cLine(cv["1"],linieAnpassen(koord[0]+v['xM'],v['yM']-koord[1],koord[2]+v['xM'],v['yM']-koord[3]),_,_,farbe,_,liste)
        else:
            showinfo('Öffnen einer bestehenden Grafik','Die Grafik konnte nicht geladen werden, da die Datei keine Grafik für dieses Programm ist.')
def speichern():
    global v,cv
    beginn='Roberts Grafikprogramm\n'
    var=str([v['p'][0],v['p'][1],v['p'][2],v['id'],v['h'],v['w'],v['ascii'],v['ableitung'],v['k'],v['n'],v['winkel']])+'\n'
    aktuellesObjekt="["
    for i in v['aktuellesObjekt']:
        aktuellesObjekt+=i+","
    aktuellesObjekt=aktuellesObjekt.rstrip(',')+']\n'
    objekte=""
    for i in cvWith('B'):
        liste=""
        for j in cvTags(i):
            liste+=(j+'|')
        liste=liste.rstrip('|')
        objekte+=(liste+'\n')
    datei=tkFileDialog.asksaveasfile()
    if datei:
        datei.truncate(0) #Sicherstellen, dass Datei korrekt überschrieben wird
        datei.writelines(beginn+aktuellesObjekt+var+objekte)
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
                        if '*' in j:
                            j=j.replace("*","")
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
def setNamePunkt():
    window('changePoint',"Name eines Punktes ändern",'images/head.ico')
    frame('headCP','changePoint',_,_,_,_)
    frame('oldPoint','changePoint',_,_,_,_)
    frame('newPoint','changePoint',_,_,_,_)
    frame('buttonCP','changePoint',_,_,_,_)
    label('headCP','headCP','Bitte geben Sie den alten und neuen Namen ein.\nDer neue Name darf nicht länger als 10 Zeichen sein.',LEFT,_)
    label('oldPoint','oldPoint','Alter Name: ',LEFT,_)
    entry('oldPoint','oldPoint',10,LEFT,_)
    label('newPoint','newPoint','Neuer Name: ',LEFT,_)
    entry('newPoint','newPoint',10,LEFT,_)
    button('buttonCP','buttonCP',_,_,_,"Name ändern",_,setName,_,_)
def setName():
    global v
    x=len(cvWith('%'+e['oldPoint'].get()))
    y=len(e['oldPoint'].get())
    z=len(e['newPoint'].get())
    listeP=cvWith('%'+e['oldPoint'].get())
    tagNewP='%'+e['newPoint'].get()
    newP=e['newPoint'].get()
    f['changePoint'].destroy()
    if x>0:
        if y==0:
            showinfo('Alter Name',"Sie haben vergessen den alten Namen einzugeben!")
        else:
            if z==0:
                showinfo('Neuer Name',"Sie haben vergessen einen neuen Namen einzugeben!")
            else:
                if z>10:
                    showinfo('Neuer Name',"Ihr eingegebener neuer Name ist zu lang!")
                else:
                    if '|' in newP:
                        showinfo('Ungültiges Zeichen','Das Zeichen "|" kann aus programmtechnischen Gründen nicht verwendet werden!')
                    else:
                        for i in listeP:
                            for j in cvTags(i):
                                if j[0]=='%':
                                    cv['1'].dtag(i,j)
                                    if len(set(['T','DPT'])&set(cvTags(i)))!=0:
                                        cv['1'].itemconfigure(i,text=newP)
                                    tags(cv['1'],[tagNewP],i)
    else:
       showinfo('Alter Name',"Ihr eingegebener alter Name existiert nicht!") 
    
#---Menue: Spiegeln---
def anXAchseSpiegeln():
    if cvWith('B')!=():
        spiegeln("#3333ff", "x")
def anYAchseSpiegeln():
    if cvWith('B')!=():
        spiegeln("#ff9900", "y")
def amUrsprungSpiegeln():
    if cvWith('B')!=():
        spiegeln("#cc0099", "n")
def anPSpiegeln():
    if cvWith('B')!=() and cvWith('DP')!=():
        spiegeln("#d2691e", "p")
def zenStrecken():
    if cvWith('B')!=():
        spiegeln("#33cc00", "z")

#---Menue: Aktionen---
def programmbeschreibung():
    showinfo('Programmbeschreibung',
             'Allgemeines\n'+
             '--------------\n'+
             'Mit diesem Programm können Sie Punkte und Linien zeichnen und diese dann auf die verschiedensten Weisen spiegeln.\n'+
             'Die entstehenden Figuren können an der x- und an der y-Achse,sowie am Koordinatenursprung bzw. an einem bestimmten\n'+
             'Punkt gespiegelt werden. Überdies ist es möglich die Figur zentrisch zu strecken.\n\n'
             'Einen Punkt zeichnen\n'+
             '-------------------------\n'+
             'Einen Punkt können Sie durch Eingabe in der rechten Toolbar oder durch direktes setzen im Koordinatensystem nach\n'+
             'der Aktivierung des linken oberen Checkbuttons zeichnen. Mehrere Punkte können Sie durch das Drücken des unteren\n'+
             'Buttons eingeben.\n\n'+
             'Zwei Punkte zu einer Linie verbinden\n'+
             '-------------------------------------------\n'
             'Zwei Punkte können Sie zu einer Linie verbinden, indem Sie den rechten oberen Checkbutton aktivieren, den ersten\n'+
             'Punkt anklicken und gedrückt halten, dann zum 2. Punkt den Cursor ziehen und dort loslassen. Voraussetzung ist, dass\n'+
             'beide Punkte zur gleichen Figur gehören.\n\n'+
             'Spiegeln\n'+
             '----------\n'+
             "Die verschiedenen Formen des Spiegelns können Sie im Menü 'Spiegeln' abrufen oder durch die Schnellwahltasten, die in\n"+
             'diesem Menü angegeben sind, tätigen\n'+
             'Wenn Sie am Ursprung spiegeln, müssen Sie zuvor einen Winkel eingegeben (voreingestellt ist der Winkel 0). Bei einer\n'+
             'Spiegelung an einem Spiegelpunkt müssen Sie zuvor einen Spiegelpunkt eingeben, sowie einen Winkel. Bei der zentrischen\n'+
             "Streckung müssen Sie zuvor den Streckungsfaktor 'k' eingeben.\n\n"+
             'Figuren und Punkte editieren\n'+
             '-----------------------------------\n'+
             'Jedes Spiegelobjekt ist eine Figur. Es ist möglich neue Figuren zu erstellen bzw. alte zu löschen. Das kann man mit den ent-\n'+
             'sprechenden Menüunterpunkten bewerkstelligen. Bei jedem Punkt im Koordinatensystem ist es möglich dessen Namen zu ändern.\n\n'+
             'Infoboxen\n'+
             '-------------\n'+
             'Bei jedem Punkt bzw. jeder Linie öffnet sich nach 2 Sekunden, bei Stillstand des Cursors, eine Infobox mit den wichtigsten Daten.\n\n'+
             'Öffnen und Speichern\n'+
             '---------------------------\n'+
             'Ihre Zeichnung kann in jeder Dateitypform gespeichert werden. Die Dateien sind dann auch per Texteditor einsehbar. Geöffnet werden\n'+
             'können nur diese Dateien, die die entsprechende Kennung für dieses Programm besitzen.')
def impressum():
    showinfo('Impressum','Dieses Programm wurde erstellt durch\n\n'+'Robert Willemelis\n'+'Handjerystr. 36\n'+
             'D-12489 Berlin\n\n'+'Tel.:   +49 30-67 70 25 2\n'+'Mobil: +49 162-73 95 059\n\n'+
             "im Zeitraum vom 26.04.2006 bis 30.05.2007\n"+'als Bewerbungsprogramm.\n\n'+v['c']+' 2007')
#--------------------------------------------------------------------------------------------
#Oberfläche
    
#----1. Start des Masters ----------------------------------------------------------
window('Hauptfenster',"Roberts Grafikprogramm 4.0",'images/head.ico')
v['thread2']=f['Hauptfenster'].after(2000,showInfo)
#-------
img={'f': PhotoImage(file="images/rd_pin.gif"),
     'd': PhotoImage(file="images/bk_pin.gif"),
     'x': PhotoImage(file="images/bl_pin.gif"),
     'y': PhotoImage(file="images/yl_pin.gif"),
     'p': PhotoImage(file="images/or_pin.gif"),
     'n': PhotoImage(file="images/pi_pin.gif"),
     'z': PhotoImage(file="images/gr_pin.gif"),
     '+malen': PhotoImage(file="images/malen.gif"),
     '-malen': PhotoImage(file="images/malen_in.gif"),
     '+linie': PhotoImage(file="images/linie_verbinden.gif"),
     '-linie': PhotoImage(file="images/linie_verbinden_in.gif"),
     '+KE': PhotoImage(file="images/liste.gif"),
     '-KE': PhotoImage(file="images/liste_in.gif")}
#----2. Beginn Menueoptionsleiste -------------------------
menu('menue',f['Hauptfenster'],0,_)
menu('Aktionen',m['menue'],1,[["Neu                                                Strg+N",neu],[],
                              ["Neue Figur",neueFigur],[],
                              ["Öffnen                                           Strg+O",laden],
                              ["Speichern                                       Strg+S",speichern],[],
                              ["Aktuelles Objekt löschen",deleteAktuellesObjekt],
                              ["Name eines Punktes ändern",setNamePunkt],[],
                              ["Programm beenden                        Strg+Q",f['Hauptfenster'].destroy]])
menu('Spiegeln',m['menue'],1,[["... an der x-Achse                       Strg+X",anXAchseSpiegeln],
                              ["... an der y-Achse                       Strg+Y",anYAchseSpiegeln],[],
                              ["... am Ursprung                           Strg+U",amUrsprungSpiegeln],
                              ["... an einem bestimmten Punkt    Strg+P",anPSpiegeln],[],
                              ["Zentrische Streckung                   Strg+Z",zenStrecken]])
menu('?',m['menue'],1,[["Programmbeschreibung",programmbeschreibung],
                       ["Impressum",impressum]])
f['Hauptfenster'].config(menu=m['menue'])

#----2. Ende Menueoptionsleiste ---------------------------
#----3. Beginn des Arbeitsbereiches -----------------------
frame('Arbeitsbereich','Hauptfenster',2,"groove",_,_) 
#Zeichenfläche mit Canvas-Widget
frame('Zeichenbrett','Arbeitsbereich',_,_,LEFT,_)
canvas("1",'Zeichenbrett',v['w'],v['h'],'white')

#Dot-Notation vermeiden
cvWith=cv["1"].find_withtag; cvAll=cv["1"].find_all;
cvClose=cv["1"].find_closest; cvCoords=cv["1"].coords;
cvTags=cv['1'].gettags
cvOpt=cv['1'].itemcget
cvBB=cv['1'].bbox
cvText=cv['1'].icursor

#Koordinatensystem zeichnen
getKoordSystem()

#Aktionen
aktion(cv["1"],[["<Motion>", getCursorPos],["<Leave>", setNull]])
aktion(f['Hauptfenster'],[["<Control-KeyPress-s>",sw_speichern],["<Control-KeyPress-o>",sw_laden],
                          ["<Control-KeyPress-n>",sw_neu      ],["<Control-KeyPress-q>",sw_quit],
                          ["<Control-KeyPress-x>",sw_xSp       ],["<Control-KeyPress-y>",sw_ySp],
                          ["<Control-KeyPress-u>",sw_nSp       ],["<Control-KeyPress-p>",sw_pSp],
                          ["<Control-KeyPress-z>",sw_zSp]])
cv['1'].tag_bind('B','<Enter>',setIDObj)
cv['1'].tag_bind('B','<Leave>',delIDObj)
#--------
#Eingabebereich
frame('Eingabe','Arbeitsbereich',2,_,RIGHT,BOTH)
#---
label('leerEingabe','Eingabe',"  ", _, _)
frame('Buttons','Eingabe',_,_,_,_)
frame('Buttons2','Eingabe',_,_,_,_)
button('punktZeichnen','Buttons',_,FLAT,img['-malen'],_,"black",checkButton_PunktZeichnen,LEFT,_)
#-
b['punktZeichnen'].configure(activebackground='red')
b['punktZeichnen'].bind('<Enter>',btnPunktZeichnen)
b['punktZeichnen'].bind('<Leave>',delInfoArt)
f['Hauptfenster' ].bind('<Motion>',infoZeichnen)
#-
button('linieZeichnen','Buttons',_,FLAT,img['-linie'],_,"black",checkButton_PunkteVerbinden,LEFT,_)
#-
b['linieZeichnen'].configure(activebackground='blue')
b['linieZeichnen'].bind('<Enter>',btnLinieZeichnen)
b['linieZeichnen'].bind('<Leave>',delInfoArt)
#-
label('leerEingabe2','Eingabe',"  ", _, _)  
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
label('leerK','Koordinaten',"Koordinaten mehrerer Punkte:", _, _)
#Eingabe mehrerer Punkte
button('NPunkteEingeben','Koordinaten',_,FLAT,img['+KE'],_,_,nKoordEingeben,_,_)
b['NPunkteEingeben'].bind('<Enter>',btnNKoordinaten)
b['NPunkteEingeben'].bind('<Leave>',delInfoArt)
label('leerEingabe','Eingabe',"  ", _, _)
#Eingabe eines Spiegelpunktes
frame('SP', 'Eingabe',2,"groove",_,X)
label('SP','SP',"Spiegelpunkt:", _,X)
frame('SPE', 'SP',_,_,_,X)
label('xSPE','SPE',"x=", LEFT,_)
entry('xSP','SPE',4,LEFT,_)
label('ySPE','SPE',"y=",LEFT,_)
entry('ySP','SPE',4,LEFT,_)
label('leerSPE','SPE',"  ",LEFT,_) 
button('SPE','SPE',_,_,_,"eingeben",_,setP,LEFT,_)
#Winkel eingeben
frame('W','Eingabe',2,"groove",_,X)
label('dWW','W',"Drehwinkel:",_,X)
frame('WE','W',_,_,_,X)
label('alpha','WE',v['al']+"=",LEFT,_)
entry('W','WE',4,LEFT,_)
label('grad','WE',v['gr'],LEFT,_)
button('WE','WE',_,_,_,"eingeben",_,setWinkel,RIGHT,_)
#Streckungsfaktor eingeben
frame('K','Eingabe',2,"groove",_,X)
label('KT','K',"Streckungsfaktor:",_,X)
frame('KE','K',_,_,_,X)
label('K','KE',"k=",LEFT,_)
entry('K','KE',4,LEFT,_)
button('KE','KE',_,_,_,"eingeben",_,setK,RIGHT,_)
label('leerE','Eingabe'," ",_,_)
#Cursorposition
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
