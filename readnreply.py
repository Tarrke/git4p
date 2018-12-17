#!/data/data/com.termux/files/usr/bin/python
# coding: utf8
#author pgg
#ver	0.0
#start	16 dec 2018
#end	

from os import system
#from datetime import datetime
from subprocess import getoutput
from time import time,strptime,mktime,sleep


fmt="%Y-%m-%d %H:%M"
dones={}
pos=""
def send(msg,nb):
    system("termux-sms-send -n %s %s"%(nb,msg))

def decTo60(val,axis):
    if val<0:
        val=-val
        ax=axis[1]
    else:
        ax=axis[0]
    va,vb=divmod(val,1)
    vb,vc=divmod(vb,1)
    vc*=60
    return("%d°%d'%s\"%s"%(int(va),int(vb),str(vc)[:7],ax))

def buildMsg(n,pos):
    if " " in pos:
        lat,lon =pos.split(" ")
        url="https://www.google.com/maps/place/"
        pos=decTo60(float(lat),"NS")+"+"
        url+=pos+decTo60(float(lon),"EW")
        ns="N"
        if lat[0]=="-":
            ns="S"
            lat=lat[1:]
        ew="E"
        if lon[0]=="-":
            ew="W"
            lon=lon[1:]
        pos=lat+ns+" "+lon+ew
        print(pos)
        print(url)
    else:
        url="https://www.wikipedia.org/wiki/Uranus"
    return("Bonjour %s.\rPascal se trouve à la position: %s.\r %s"%(n,pos,url))

def readNetworkPos():
    lines=getoutput("termux-location -p network -r updates").split("\n")
    pos="inconnue"
    lat=lon=0
    for line in lines:
        if ":" in line:
            fil,val=line.split(":",1)
            fil=fil.strip()
            if "latitude" in fil:
                lat=val[1:-1]
            if "longitude" in fil:
                lon=val[1:-1]
    if lat and lon:
        pos=lat+" "+lon
    return(pos)

def isOkay(t,n,r,b):
    print("isok",t)
    if not (t and n and r and b):
        print("not ok 1")
        return(False)
    if t in dones and dones[t]+15*60>r:
        print("not ok 2")
        return(False)
    if r+15*60>time():
        print("ok")
        return(True)
    print("not ok 3")
    return(False)
    
def getNewSms():
    global dones
    name=ok=whok=nb=0
    pos=""
    lines=getoutput("termux-sms-list").split("\n")
    for line in lines:
        if ":" in line:
            fil,val=line.split(":",1)
            fil=fil.strip()
            if "sender" in fil:
                name=val[2:-2]
            if "body" in fil:
                ok=("téoù"==val[2:-1])
                #print(val)
            if "received" in fil:
                whok=mktime(strptime(val[2:-2],fmt))
            if "number" in fil:
                nb=val[2:-2]
        elif "}" in line:
            #print("sms blk over")
            if isOkay(nb,name,whok,ok):
                if not pos:
                    print("refresh pos")
                    pos=readNetworkPos()
                msg=buildMsg(name,pos)
                send(msg,nb)
                print("msg sent to "+name)
                dones[nb]=whok
            name=ok=whok=nb=0
    
while True:
    sl= getNewSms()
    print("-------")
    sleep(30)

assert(False)
lin=input(">")
while lin!="":
    msg+=("\r" if len(msg)>0 else "")+lin
    lin=input(">")


#for nb in ["0676951126"]:
for nb in ["0676951126","0616957660","0617464154"]:
    le=0
    