import csv
import calendar
from datetime import date

data = [""] * 23
"""
    amountOfAlarms = 4 #0-3
    amountOfNotifications = 12 #4-15
    amountOfReportTimes = 5 #16-20
    amountOfTests = 6 #21-26
    amountOfAssignments = 6 # 27-32
    amountOfBedTimeAlert = 1 #21
"""
year = ""
displayData = []

def main():
    choice = actionPrompt()
    settings = getSettings()
    print(settings)
    global year
    year = settings["year"]
    print(settings["year"])
    runActionsFromChoice(choice)

def runActionsFromChoice(choice):
    if(choice == 1):
        month = getMonth()
        day = getDay(month)
        readCSVDataFromFile(month, day, 0, 3)
        alarms(month, day)
    elif(choice == 2):
        month = getMonth()
        day = getDay(month)
        readCSVDataFromFile(month, day, 4, 15)
        notifications(month, day)
    elif(choice == 3):
        month = getMonth()
        day = getDay(month)
        readCSVDataFromFile(month, day, 4, 15)
        reportTime(month, day)
    elif(choice == 4):
        testData = readInTests()
        displayTests(testData)
        testData = editTestInfo(testData)
        writeTestInformation(testData)
    elif(choice == 5):
        assignmentData = readInAssignment()
        displayAssignment(assignmentData)
        assignmentData = editAssignmentInfo(assignmentData)
        writeAssignmentInformation(assignmentData)

def readInAssignment():
    assignmentData = []
    infile = open("assignments.csv")
    line = infile.readline().strip()
    count = 0
    while(count != 10):
        if(line != ","):
            date, assignmentInfo = line.split(",")
            assignmentData.append(date + ": " + assignmentInfo)
        else:
            assignmentData.append(" ")
        count += 1
        line = infile.readline().strip()
    infile.close()
    return assignmentData

def displayAssignment(assignmentData):
    print("DATE:   Description")
    count = 1
    for i in range(0, 10):
        info = assignmentData[i]
        print(str(count) + ".) " + info)
        count += 1
        
def editAssignmentInfo(assignmentData):
    choice = input("What would you like to change: ")
    month = raw_input("what is the month that it is due: ")
    day = raw_input("what is the day that it is due: ")
    assignmentInfo = (raw_input("Please give a descrition or title for the assignment: "))
    assignmentData[int(choice) - 1] = (month + "-" + day + ": " + assignmentInfo)
    return assignmentData

def writeAssignmentInformation(assignmentData):
    infile = open("assignments.csv", "w")
    text = ""
    for i in range(0, 10):
        info = assignmentData[i]
        if(info != " "):
            date, assignmentInfo = info.split(": ")
            text = text + date+ "," + assignmentInfo + "\n"
        else:
            text = text + ",\n"
    infile.write(text)
    infile.close()
    
def readInTests():
    testData = []
    infile = open("tests.csv")
    line = infile.readline().strip()
    count = 0
    while(count != 10):
        if(line != ","):
            date, testInfo = line.split(",")
            testData.append(date + ": " + testInfo)
        else:
            testData.append(" ")
        count += 1
        line = infile.readline().strip()
    infile.close()
    return testData

def displayTests(testData):
    print("DATE:   Description")
    count = 1
    for i in range(0, 10):
        info = testData[i]
        print(str(count) + ".) " + info)
        count += 1
        
def editTestInfo(testData):
    choice = input("What would you like to change: ")
    month = raw_input("what is the month that it is due: ")
    day = raw_input("what is the day that it is due: ")
    testInfo = (raw_input("Please give a descrition or title for the test: "))
    testData[int(choice) - 1] = (month + "-" + day + ": " + testInfo)
    return testData

def writeTestInformation(testData):
    infile = open("tests.csv", "w")
    text = ""
    for i in range(0, 10):
        info = testData[i]
        if(info != " "):
            date, testInfo = info.split(": ")
            text = text + date+ "," + testInfo + "\n"
        else:
            text = text + ",\n"
    infile.write(text)
    infile.close()
    
def displayDataValues():
    global displayData
    number = 1
    for i in displayData:
       print(str(number) + ": " + i)
       number += 1
        
def readCSVDataFromFile(month, day, low, high):
    dayCounter = 1
    collection = []
    infile = open(year + "-" + str(month) +".csv")
    line = infile.readline().strip()
    while(len(line)>0):
        if(dayCounter == day):
            loadIntoStorage(line, low, high)
        dayCounter = dayCounter + 1
        line = infile.readline().strip()
    infile.close()

def loadIntoStorage(dataCollection, low, high):
    valuesHolder = []
    valuesHolder = dataCollection.split(',')
    getDisplayData(valuesHolder, low, high)

def getDisplayData(valuesHolder, low, high):
    global displayData
    for i in range(low, high+1):
        displayData.append(valuesHolder[i])
        print(displayData)

def reportTime(month, day):
    print("The current notification times are: ")
    displayDataValues()
    choice = input("Enter number of what you would like to modify: ")
    editTimes(choice)
    dataToBeWritten = buildWriteData(16, 20, month, day)
    writeData(dataToBeWritten, month)

def notifications(month, day):
    print("The current notifications that are assigned are: ")
    displayDataValues()
    choice = input("Enter number of what you would like to modify: ")
    editText(choice)
    dataToBeWritten = buildWriteData(4, 15, month, day)
    writeData(dataToBeWritten, month)
    
def alarms(month, day):
    print("The current alarms are: ")
    displayDataValues()
    choice = input("Enter number of what you would like to modify: ")
    editTimes(choice)
    dataToBeWritten = buildWriteData(0, 3, month, day)
    writeData(dataToBeWritten, month)

def writeData(dataToBeWritten, month):
    infile = open(year + "-" + str(month) +".csv", "w")
    infile.write(dataToBeWritten)
    infile.close()
    
def buildWriteData(low, high, month, day):
    global displayData
    dayCounter = 1
    valuesHolder = []
    dataToBeWritten = ""
    modifiedData = ""
    infile = open(year + "-" + str(month) +".csv")
    line = infile.readline().strip()
    while(len(line)>0):
        if(dayCounter == day):
            valuesHolder = line.split(',')
            for i in range(low, high+1):
                valuesHolder[i] = displayData[i - low]
            for i in range(0,22):
                if(i != 0):
                    modifiedData += ","
                modifiedData = modifiedData + valuesHolder[i]
            dataToBeWritten = dataToBeWritten + modifiedData + "\n"
        else:
            dataToBeWritten = dataToBeWritten + line + "\n"
        dayCounter = dayCounter + 1
        line = infile.readline().strip()
    print dataToBeWritten
    infile.close()
    return dataToBeWritten

def editText(i):
    global displayData
    text = raw_input("What would you like to be reminded about: ")
    displayData[i-1] = text

def editTimes(i):
    global displayData
    hour = raw_input("hour of alarm: ")
    minute = raw_input("Minute of alarm: ")
    time = (str(hour) + ":" + str(minute))
    displayData[i-1] = time

def actionPrompt():
    print("WELCOME TYLER!\n1. alarms\n2. notification")
    print("3. Report Times\n4. Set test info\n5. set assignment info\n6. Set Defualt times\n7. settings")
    choice = input("What would like to do: ")
    print(50 * "\n")
    return choice

def getMonth():
    print("1: JAN\t2: FEB\n3: MAR\t4: APR\n5: MAY\t6: JUN\n7: JUL\t8: AUG")
    print("9: SEP\t10: OCT\n11: NOV\t12: DEC")
    month = input("Which month: ")
    doesFileExist(month)
    return month

def doesFileExist(month):
    filesInExistance = []
    state = False
    infile = open("2016-filesConstructed.txt")
    line = infile.readline()
    while len(line) > 0:
        filesInExistance.append(line)
        line = infile.readline()
    infile.close()
    fileSize = len(filesInExistance)
    for i in filesInExistance:
        if( i == ("2016-" + str(month) + ".csv")):
            state = True
    if (state != True):
        createFile(month)
        makeNoteThatFileExist(month)
        
def makeNoteThatFileExist(month):
    file = open("2016-filesConstructed.txt", "a")
    file.write("2016-" + str(month) + ".csv\n")
    file.close()

def createFile(month):
    c = (open("2016-" + str(month) + ".csv", "w"))
    c.close()
    default = getDefaultValues()
    writeStartData(default, month)

def getDefaultValues():
    default = {}
    infile = open("defaultValues.txt")
    line = infile.readline().strip()
    
    while(len(line)>0):
        weekDay, listOfValues = line.split("=")
        valuesHolder = listOfValues.split(',')
        line = infile.readline().strip()
        default[weekDay] = valuesHolder
        
    infile.close()
    return default

def writeStartData(default, month):
    file = open("2016-" + str(month) + ".csv", "a")
    monthLength = getMonthLength(month)
    for dateNum in range(0, monthLength):
        weekday = getWeekday(dateNum, month)
        section = default[weekday]
        completeSection = ""
        for i in range(0, 21):
            if(i == 0):
                completeSection = completeSection + section[0]
            elif(i == 16):
                completeSection = completeSection + section[2]
            elif(i == 17):
                completeSection = completeSection + section[3]
            
            completeSection = completeSection + ","
        completeSection = completeSection + section[1]
        file.write(completeSection + "\n")

def getMonthLength(month):
    ml = calendar.monthrange(2016, month)
    monthLength = ml[1]
    return monthLength

def getDay(month):
    monthLength = getMonthLength(month)
    print("possible values are 1 - " + str(monthLength))
    day = input("what day would you like to access: ")
    day = checkIfDayIsValid(month, day, monthLength)
    return day
    
def checkIfDayIsValid(month, day, monthLength):
    if( 0 < day <= monthLength):
        return day
    else:
        print("day choosen is invalid")
        day = getDay(month)
        return day
        
def getWeekday(dateNum, month):
    weekDaysList = [ "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    dateNum = dateNum + 1
    dateInput = [year, month, dateNum] 
    dayOfTheWeek = date(2016, month, dateNum).weekday()
    return weekDaysList[dayOfTheWeek]

def getSettings():
    infile = open("settings.txt")
    line = infile.readline().strip()
    settings = {}
    while(len(line)>0):
        valueName, value = line.split("=")
        settings[valueName] = value
        line = infile.readline().strip()
    infile.close()
    return settings

main()
