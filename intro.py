import datetime
import os
from time import sleep
from random import randint
from pyowm import OWM
import Tkinter as Tk
import time

runs = 0
actionData = []
root = Tk.Tk()
statusField = Tk.Label(root,font=("times",10,"bold"), text = "Checking Systems", fg="black")
background_image=Tk.PhotoImage(file="brown2.gif")

def averaSpeach(text):
    os.system("espeak -v female3 '" + text + "' -s 140")

def getDay():
    day = time.strftime("%d")
    return day

def getMonth():
    month = time.strftime("%m")
    return month

def loadIntoStorage(dataCollection):
    global actionData
    actionData = dataCollection.split(',')

def readCSVDataFromFile():
    dayCounter = 1
    collection = []
    month = getMonth()
    day = getDay()
    year = "2016"
    infile = open(year + "-" + month +".csv")
    line = infile.readline().strip()
    while(len(line)>0):
        if(dayCounter == int(day)):
            loadIntoStorage(line)
        dayCounter = dayCounter + 1
        line = infile.readline().strip()
    infile.close()

def checkIfFileInfoCanBeFound():
    global root
    changeStatusTo("CHECKING FOR NECESSARY FILES", "black")
    averaSpeach("Checking system for necessary files. Please standby.")
    sleep(2)
    try:
        readCSVDataFromFile()
        changeStatusTo("ALL SYSTEMS ARE A GO! \nCODE: GREEN", "green")
        averaSpeach("All Systems are a go.")
        sleep(5)
        os.system("python pyclock.py &")
    except:
        changeStatusTo("MISSING ESSENTIAL FILES \nCODE: RED", "red")
        averaSpeach("Alert! Critical Files are missing.")
        sleep(5)
    
def checkIfAllSystemsAreAGO():
    global root
    global runs
    if(runs == 0):
        averaSpeach("Performing System Checks. Please Standby")
        sleep(3)
    if(runs != 0):
        try:
            if(runs == 1):
                averaSpeach("Attempting to establish link with weather service")
            API_key = "5b5693677ce916aeb8ce810029baf174"
            owm = OWM(API_key)
            state = owm.is_API_online()
            if(state == True):
                changeStatusTo("OPEN WEATHER SERVICE IS ONLINE \nCONDITION: GREEN", "green")
                averaSpeach("Link Has Been Established. Please Standby")
                sleep(2)
                checkIfFileInfoCanBeFound()
                root.destroy()
        except:
            changeStatusTo("ATTEMPT " + str(runs)+" TO CONTACT WEATHER SERVICE HAS FAILED \nCONDITION: ORANGE", "orange")
    if(runs == 60):
        changeStatusTo("ALL ATTEMPTS TO CONTACT THE WEATHER SERVICE HAS FAILED\nCONDITION: RED", "red")
        averaSpeach("All, attempts to contact the weather service, has failed.")
        sleep(6)
        root.destroy()
    runs += 1
    statusField.after(2000, checkIfAllSystemsAreAGO)

def changeStatusTo(textData ,color):
    statusField.configure(text = textData, fg= color,font=("times",8))
    root.update()

def main():
    global root
    global statusField
    background_label = Tk.Label(root, image=background_image)
    background_label.pack()
    statusField.pack(side = "bottom")
    root.wm_geometry("500x300+10+10")
    root.title('intro')
    checkIfAllSystemsAreAGO()
    root.mainloop()
main()
