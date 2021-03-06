import datetime
import os
from time import sleep
import time
from random import randint
from Tkinter import *
from pyowm import OWM

#sudo apt-get install espeak
#sudo pip install pyowm
#sudo apt-get install python-pygame


root = Tk()
backgroundColor = "lightgrey"
foregroundColor = "dodgerblue"
root.config(background=backgroundColor)
clockField = Label(root,font=("times",65,"bold"), text = "Welcome",bg=backgroundColor, fg=foregroundColor)
weatherField = Label(root,font=("times",30,"bold"),bg=backgroundColor, fg=foregroundColor ,text = "Sunny")
tempField = Label(root,font=("times",20,"bold") ,bg=backgroundColor , fg=foregroundColor, text = "this")

setup = {}
weatherconditions = []
actionData = []
reportPhrases = ["I thought I should let you know that", "I would like to remind you that", "Remember that, I am your gaurdian to your family,, that is why I must remind you, that", "I will always assist you, that is why, i must tell you ."]
alarmPhrases = ["I know you don't want to get up, but think of the possibilities", "I know today is going to be a great day so wake up.", "Ok listen we are both tired, but hey you've got work to do.", "You know what they say waking up early is good for something ha ha", "Good Morning and dont forget to be expectional today", "Life is like a nuclear appocolapse  you never know what is going to happen, so why don't you start your day"]
tests = [""] * 10
assignments = [""] * 10
blocker = 0

def settime():
    global setup
    H = datetime.datetime.now().hour
    setup["M"] = datetime.datetime.now().minute
    setup["S"] = datetime.datetime.now().second
    setup["h"] = H
    minute = str(setup["M"])
    second = str(setup["S"])
    if(len(minute) != 2):
        minute = "0" + minute
        setup["M"] = minute
    if(len(second) != 2):
       second = "0" + second
       setup["S"] = second
    if(H >12):
        H = H - 12
        setup["H"] = H
        setup["period"] = "p.m."
    if(H < 12):
       setup["H"] = H
       setup["period"] = "a.m."
    if(H == 0):
        setup["H"] = "12"
    return setup

def checkTransitionTimes():
    global setup
    global clockField
    global weatherField
    global tempField
    if((int(setup["h"]) >= int(setup["sunrise"])) and (setup["morning"] == "off")):
        backgroundColor = "lightgrey"
        foregroundColor = "dodgerblue"
        clockField.config(bg=backgroundColor, fg=foregroundColor)
        weatherField.config(bg=backgroundColor, fg=foregroundColor)
        tempField.config(bg=backgroundColor, fg=foregroundColor)
        root.config(background = backgroundColor)
        callAveraButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
        MusicPlayerButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
    if( int(setup["h"]) >= 9 ):
        backgroundColor = "lawngreen"
        foregroundColor = "green"
        clockField.config(bg=backgroundColor, fg=foregroundColor)
        weatherField.config(bg=backgroundColor, fg=foregroundColor)
        tempField.config(bg=backgroundColor, fg=foregroundColor)
        root.config(background = backgroundColor)
        callAveraButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
        MusicPlayerButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
    if((int(setup["h"]) >= int(setup["sunset"])) and (setup["afternoon"] == "off")):
        backgroundColor = "dodgerblue2"
        foregroundColor = "blue2"
        clockField.config(bg=backgroundColor, fg=foregroundColor)
        weatherField.config(bg=backgroundColor, fg=foregroundColor)
        tempField.config(bg=backgroundColor, fg=foregroundColor)
        root.config(background = backgroundColor)
        callAveraButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
        MusicPlayerButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
    if((int(setup["h"]) >= int(setup["bedTimeHour"])) and (setup["sleep"] == "off")):
        backgroundColor = "black"
        foregroundColor = "red2"
        clockField.config(bg=backgroundColor, fg=foregroundColor)
        weatherField.config(bg=backgroundColor, fg=foregroundColor)
        tempField.config(bg=backgroundColor, fg=foregroundColor)
        root.config(background = backgroundColor)
        callAveraButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
        MusicPlayerButton.config(bg=backgroundColor, fg=foregroundColor, activeforeground=foregroundColor,activebackground=backgroundColor)
        
def assignTimeValues():
    global setup
    settime()
    H = setup["H"]
    M = setup["M"]
    S = setup["S"]
    time = str(H) + ":" + str(M) + ":" + str(S)
    return time

def readNotificaions():
    global weatherconditions
    global reportPhrases
    global setup
    averaSpeach(reportPhrases[randint(0,(len(reportPhrases))-1)])
    for alert in range(4, 16):
        averaSpeach(actionData[alert])
    referenceTime = int(setup["WeatherConditionsStartTime"])
    averaSpeach("Current weather conditions are ")
    currentDay = " Today,,"
    for weatherAlert in range(0, 5):
        averaSpeach(weatherconditions[weatherAlert] + ",,")
        referenceTimeFix = ""
        if(referenceTime > 24):
            currentDay = " Tomorrow,, "
            referenceTime = referenceTime - 24
        if(24 > referenceTime > 12):
            referenceTimeFix = str(referenceTime - 12)
            averaSpeach(" at " + str(referenceTimeFix) + " O Clock, P.M. ," + currentDay)
        if(referenceTime == 24):
            averaSpeach(" at 12, A.M., " + currentDay)
        if(referenceTime < 12):
            averaSpeach(" at " + str(referenceTime) + " O Clock, A.M., " + currentDay)
        if(referenceTime == 12):
            averaSpeach(" at 12 O Clock, P.M., " + currentDay)

        referenceTime += 3
        if(weatherAlert != 4):
            averaSpeach(" ,and ")
        sleep(.1)
    alertOfTests()
    alertOfAssignments()

def call():
    readCSVDataFromFile()
    readAssignmentData()
    readTestData()
    readNotificaions()
     
callAveraButton = Button(root,activebackground=backgroundColor, activeforeground=foregroundColor, font=("times",25,"bold"),highlightthickness=0,bd = 0,text = "CALL",bg=backgroundColor, fg=foregroundColor, command=call)

def runMusicPlayer():
    os.system("python MusicPlayer.py")

MusicPlayerButton = Button(root,activebackground=backgroundColor, activeforeground=foregroundColor, font=("times",25,"bold"),highlightthickness=0,bd = 0,text = "Music",bg=backgroundColor, fg=foregroundColor, command=runMusicPlayer)

def alertOfTests():
    global tests
    if(len(tests) != 0):
        averaSpeach("Your current tests you need to prepare for are: ")
        for test in tests:
            averaSpeach(test)
            
def alertOfAssignments():
    global assignments
    if(len(assignments) != 0):
        averaSpeach("Your current assignments you need to do are: ")
        for assignment in assignments:
            averaSpeach(assignment)

def itsBedTime():
    goodNightStatements = ["If you would like to perform your best, I would reccommend that you go to bed now.", "I here to inform you, that it would be wise, to head to bed."]
    averaSpeach(goodNightStatements[randint(0,(len(goodNightStatements)-1))])
    activateBlocker()
    
def setBedTimeHour():
    global actionData
    bedTime = actionData[21]
    bedTimeHour, garbage = bedTime.split(":")
    setup["bedTimeHour"] = bedTimeHour
    
def checkAlarms(time):
    global alarmPhrases
    time = (str(setup["h"]) + ":" + str(setup["M"]))
    for alarmSection in range(0, 4):
        if ((actionData[alarmSection]) == (time)):
            averaSpeach(alarmPhrases[randint(0,(len(alarmPhrases) - 1))])
            print("ring")
            readNotificaions()
            activateBlocker()
    if(actionData[21] == time):
        itsBedTime()
            
def checkReportTimes(time):
    global reportPhrases
    for reportSection in range(16,21):
        if ((actionData[reportSection]+":00") == (time)):
            averaSpeach(reportPhrases[randint(0,(len(reportPhrases)))])
            print("ring")
            readNotificaions()
            activateBlocker()

def activateBlocker():
    global blocker
    blocker = 0

def initWeather():
    API_key = '5b5693677ce916aeb8ce810029baf174'
    owm = OWM(API_key)
    obs = owm.weather_at_place("US, Anniston")
    w = obs.get_weather()
    setTemp(w)
    setWeatherConditions(w)
    setSunriseAndSunsetTimes(w)
    initFutureWeatherChanges(owm)
    checkTransitionTimes()

def refreshWeather():
    API_key = '5b5693677ce916aeb8ce810029baf174'
    owm = OWM(API_key)
    obs = owm.weather_at_place("US, Anniston")
    w = obs.get_weather()
    setTemp(w)
    setWeatherConditions(w)
    setSunriseAndSunsetTimes(w)
    updateFutureWeatherChanges(owm)
    checkTransitionTimes()
    
def initFutureWeatherChanges(owm):
    global setup
    global weatherconditions
    fc = owm.three_hours_forecast("US, Anniston")
    f = fc.get_forecast()
    lst = f.get_weathers()
    g = lst[0]
    count = 0
    isoData = g.get_reference_time('iso')
    garbage, timeStamp = isoData.split(" ")
    hour, minute, second = timeStamp.split(":")
    hour = int(hour) - 5
    if(hour < 0):
        hour = hour + 24
    setup["WeatherConditionsStartTime"] = str(hour)
    for weather in f:
        if(count < 5):
            text = weather.get_status()
            weatherconditions.append(str(text)) 
        count += 1
        
def updateFutureWeatherChanges(owm):
    global setup
    global weatherconditions
    fc = owm.three_hours_forecast("US, Anniston")
    f = fc.get_forecast()
    lst = f.get_weathers()
    g = lst[0]
    count = 0
    isoData = g.get_reference_time('iso')
    garbage, timeStamp = isoData.split(" ")
    hour, minute, second = timeStamp.split(":")
    hour = int(hour) - 5
    if(hour < 0):
        hour = hour + 24
    setup["WeatherConditionsStartTime"] = str(hour)
    for weather in f:
        if(count < 5):
            text = weather.get_status()
            weatherconditions[count] = (str(text)) 
        count += 1
        
def setWeatherConditions(w):
    global weatherField
    weather =  w.get_detailed_status()
    weatherField.config(text = weather)

def setTemp(w):
    global tempField
    temp = w.get_temperature('fahrenheit')
    tempField.config(text = (" " + str(temp['temp'])))
    return temp

def setSunriseAndSunsetTimes(w):
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
    
def readTestData():
    global tests
    limit = 0
    position = 0
    monthlist = ["January", "February", "March", "April", "May", "June", "July", "August","September", "October", "November", "December"] 
    infile = open("tests.csv")
    line = infile.readline().strip()
    while(len(line)>0):
        if(line != "," and limit < 10):
            date, info = line.split(",")
            monthnum, day = date.split("-")
            month = monthlist[int(monthnum) - 1]
            text = info + " on,,,, " + month + ",,, " + day
            tests[position] = text
            position += 1
        line = infile.readline().strip()
        limit += 1
    infile.close()

def readAssignmentData():
    global assignments
    limit = 0
    position = 0
    monthlist = ["January", "February", "March", "April", "May", "June", "July", "August","September", "October", "November", "December"] 
    infile = open("assignments.csv")
    line = infile.readline().strip()
    while(len(line)>0):
        if(line != "," and limit < 10):
            date, info = line.split(",")
            monthnum, day = date.split("-")
            month = monthlist[int(monthnum) - 1]
            text = info + " on " + month + ", " + day
            assignments[position] = text
            position += 1
        line = infile.readline().strip()
        limit += 1
    infile.close()
    
def averaSpeach(text):
    os.system("espeak -v female3 '" + text + "' -s 140")

def averaSpeachNoWait(text):
    os.system("espeak -v female3 '" + text + "' -s 140 &")
    
def welcomeMessage():
    global setup
    text = "Hello, I am AVIRA. It is my job to oversee the Brown Family"
    averaSpeachNoWait(text)
    #averaSpeach("It is always good to see you, Tyler. I will do my best to serve you, always.")
    setup["morning"] = "off"
    setup["afternoon"] = "off"
    setup["sleep"] = "off"
    
def runClock():
    global clockField
    global blocker
    time = assignTimeValues()
    if(blocker == 60):
        checkAlarms(time)
        checkReportTimes(time)
    else:
        blocker += 1
    clockField.config(text = time)
    if((setup["M"]) == "30" or (setup["M"]) == "00" ):
        refreshWeather()
        readCSVDataFromFile()
        readAssignmentData()
        readTestData()
    clockField.after(1000, runClock)
    
def main():
    global root
    global clockField
    global backgroundColor
    global foregroundColor
    root.title("Avira by tylerbro93")
    welcomeMessage()
    clockField.grid(row=1,column=1)
    weatherField.grid(row=2,column=1)
    tempField.grid(row=2,column=2)
    callAveraButton.grid(row=0, column=0)
    MusicPlayerButton.grid(row=0, column =2)
    readCSVDataFromFile()
    readTestData()
    setBedTimeHour()
    runClock()
    initWeather()
    #root.geometry("500x300")
    root.mainloop()

main()
