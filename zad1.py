#!/usr/bin/env python

import yaml
from tkinter import *
import socket
import sys

frame = None
pilot = None
UDP_ADDR = "255.255.255.255"
UDP_PORT = 2018
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)

def getRooms(yamlDict):  #funkcja zwraca liste pokoi
    rooms = []
    for i in yamlDict:
        for j in i.items():
            if j[1] == None:
                rooms.append(j[0])
    return rooms

def getVals(room,yamlDict): #funkcja zwraca liste tupli (klucz,wartosc) oprocz nazwy pokoju
    devs=[]
    for i in yamlDict:
        if i.get(room,0) != 0:
            j = i.items()
            for d in j:
                if d[1] != None:
                    devs.append(d)
    return devs

def turnOn(dev): #funkcja obslugi wlaczania urzadzenia, wysyla tresc wiadomosci na zadany adres
    send = "on " + dev
    sock.sendto(bytes(send,"utf-8"),(UDP_ADDR,UDP_PORT))

def turnOff(dev): #funkcja obslugi wylaczania urzadzenia, wysyla tresc wiadomosci na zadany adres
    send = "off " + dev
    sock.sendto(bytes(send,"utf-8"),(UDP_ADDR,UDP_PORT))

def roomPanel(vals): #funkcja obslugi nacisniecia przycisku z nazwa pokoju, wypisuje urzadzenia i przyciski ON/OFF
    global frame
    global pilot
    frame.destroy()
    frame = Frame(pilot,width=300,height=400)
    frame.pack()
    Label(frame,text="\n").pack()
    for val in vals:
        fm = Frame(frame,height=300,width=150)
        fm.pack(fill=BOTH,expand=1,anchor=NW)
        b = Button(fm,text="ON",highlightbackground='#3E4149',command = lambda x=val[0]:turnOn(x))
        b.pack(side=LEFT,anchor=N,expand=1,fill=BOTH)
        text = Label(fm,text = val[1]+'\n',relief=RAISED,width=20,bg='yellow')
        text.pack(expand=1,side=LEFT,anchor=W)
        c = Button(fm,text="OFF",highlightbackground='#3E4149',command = lambda y=val[0]:turnOff(y))
        c.pack(side=LEFT,anchor=N,expand=1,fill=BOTH)

def newWindowCreate(rooms,yamlDict): #funkcja tworzy okno pilota i przyciski z nazwami pokoi
    global frame
    global pilot
    pilot = Tk()
    pilot.title("Wirtualny Pilot")
    pilot.minsize(350,500)
    pilot.maxsize(500,650)
    mainFrame = Frame(pilot,width=300,height=500)
    mainFrame.pack(fill=BOTH,anchor=W)
    frame = Frame(pilot,width=300,height=400)
    frame.pack(side=BOTTOM,fill=BOTH)
    Label(mainFrame,text="\n").pack()
    for room in rooms:
        vals = getVals(room,yamlDict)
        b = Button(mainFrame, text = room, command = lambda arg=vals:roomPanel(arg))
        b.pack(side=LEFT,anchor=N,expand=1,fill=BOTH)
    pilot.mainloop()

def main(argv): #main wczytuje nazwe pliku z linii komend np. python3 zad1.py example.yaml
    yamlDict = {}
    name = argv[0] #"example.yaml"
    with open(name, 'r') as stream:
        try:
            yamlDict = yaml.load(stream)
        except yaml.YAMLError as exc:
            print("Plik ma niepoprawny format")
            return 1
    if yamlDict == None:
        print("Plik pusty")
        return 1
    rooms = getRooms(yamlDict)
    newWindowCreate(rooms,yamlDict)

if __name__ == "__main__":
   main(sys.argv[1:])

