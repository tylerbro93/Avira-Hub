import datetime
import os
from time import sleep
import time
from random import randint
from Tkinter import *
from pyowm import OWM

#sudo apt-get install espeak
#sudo pip install pyowm

API_key = '8a74e5d89485c26ec225fd3c27d1379d'
owm = OWM(API_key)
obs = owm.weather_at_place("US, Anniston")
w = obs.get_weather()
root = Tk()
backgroundColor = "lightgrey"
foregroundColor = "dodgerblue"
root.config(background=backgroundColor)
clockField = Label(root,font=("times",60,"bold"), text = "Welcome",bg=backgroundColor, fg=foregroundColor)
weatherField = Label(root,font=("times",20,"bold"),bg=backgroundColor, fg=foregroundColor ,text = "Sunny")
tempField = Label(root,font=("times",20,"bold") ,bg=backgroundColor , fg=foregroundColor, text = "this")

setup = {}
actionData = []
reportPhrases = ["I thought I should let you know that", "I would like to remind you that", "Remember that I am your gaurdian to your family that is why I must remind you that", "I will always assist you that is why i must tell you ."]
alarmPhrases = ["I know you don't want to get up, but think of the possibilities", "I know today is goingto be a great day so wake up.", "Ok listen we are both tired, but hey you've got work to do.", "You know what they say waking up early is good for something ha ha", "Good Morning and dont forget to be expectional today", "Life is like a nuclear appocolapse  you never know what is going to happen, so why don't you start your day"]


def settime():
    global setup
    H = datetime.datetime.now().hour
    setup["M"] = datetime.datetime.now().minute
    setup["S"] = datetime.datetime.now().second
    setup["h"] = H
    if(H >12):
        H = H - 12
        setup["H"] = H
        setup["period"] = "p.m."
    else:
       setup["H"] = H
       setup["period"] = "a.m."
    return setup

def setTransitionTimes():
    global setup
    global clockField
    global weatherField
    global tempField
    
    if(((setup["h"]) >= (setup["sunrise"])) and (setup["morning"] == "off")):
        backgroundColor = "yellow"
        foregroundColor = "dodgerblue"
        clockField.config(bg=backgroundColor, fg=foregroundColor)
        weatherField.config(bg=backgroundColor, fg=foregroundColor)
        tempField.config(bg=backgroundColor, fg=foregroundColor)
        
def assignTimeValues():
    global setup
    settime()
    H = setup["H"]
    M = setup["M"]
    S = setup["S"]
    time = str(H) + ":" + str(M) + ":" + str(S)
    return time

def readNotificaions():
    global reportPhrases
    averaSpeach(reportPhrases[randint(0,(len(reportPhrases))-1)])
    for alert in range(4, 16):
        averaSpeach(actionData[alert])
        
callAveraButton = Button(root,activebackground=backgroundColor, activeforeground=foregroundColor, font=("times",20,"bold"),highlightthickness=0,bd = 0,text = "CALL",bg=backgroundColor, fg=foregroundColor, command=readNotificaions)
        
def checkAlarms(time):
    global alarmPhrases
    time = (str(setup["h"]) + ":" + str(setup["M"]))
    for alarmSection in range(0, 4):
        if ((actionData[alarmSection]) == (time)):
            averaSpeach(alarmPhrases[randint(0,(len(alarmPhrases) - 1))])
            print("ring")
            readNotificaions()
            
def checkReportTimes(time):
    global reportPhrases
    for reportSection in range(16,21):
        if ((actionData[reportSection]+":0") == (time)):
            averaSpeach(reportPhrases[randint(0,(len(reportPhrases)))])
            print("ring")
            readNotificaions()
            
def initializeWeather():
    setTemp()
    setWeatherConditions()
    setSunriseAndSunsetTimes()
    setTransitionTimes()
    
def weatherChanges():
    fc = owm.three_hours_forecast("US, Anniston")
    f = fc.get_forecast()
    lst = f.get_weathers()
    for weather in f:
        print (weather.get_reference_time('iso'),weather.get_status())
    
def setWeatherConditions():
    global weatherField
    weather =  w.get_detailed_status()
    weatherField.config(text = weather)

def setTemp():
    global tempField
    temp = w.get_temperature('fahrenheit')
    print temp
    tempField.config(text = str(temp['temp']))

def setSunriseAndSunsetTimes():
    global setup
    rawData = w.get_sunset_time('iso')
    garbage, timestamp = rawData.split(" ")
    hour, minute, second = timestamp.split(":")
    hour = str((int(hour)-5))
    sunset = hour
    setup["sunset"] = sunset
    rawData = w.get_sunrise_time('iso')
    garbage, timestamp = rawData.split(" ")
    hour, minute, second = timestamp.split(":")
    hour = str((int(hour)-5))
    sunrise = hour
    setup["sunrise"] = sunrise
    print setup["sunrise"]
            
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

def averaSpeach(text):
    os.system("espeak -v female3 '" + text + "'")
    
def welcomeMessage():
    global setup
    text = "Hello, I am AVIRA. It is my job to oversee the Brown Family"
    averaSpeach(text)
    #averaSpeach("It is always good to see you, Tyler. I will do my best to serve you, always.")
    setSunriseAndSunsetTimes()
    setup["morning"] = "off"
def runClock():
    global clockField
    time = assignTimeValues()
    checkAlarms(time)
    checkReportTimes(time)
    clockField.config(text = time)
    if((setup["M"]) == "30" or (setup["M"]) == "00" ):
        initializeWeather()
    clockField.after(1000, runClock)
    
def main():
    global root
    global clockField
    global backgroundColor
    global foregroundColor
    root.title("Avira by Tyler Brown")
    welcomeMessage()
    clockField.grid(row=1,column=1)
    weatherField.grid(row=2,column=1)
    tempField.grid(row=2,column=2)
    callAveraButton.grid(row=0, column=0)
    readCSVDataFromFile()
    runClock()
    initializeWeather()
    weatherChanges()
    setTransitionTimes()
    root.mainloop()

main()
