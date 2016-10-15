def readInAssignment():
    assignmentData = []
    infile = open("assignments.csv")
    line = infile.readline().strip()
    count = 0
    while(count != 10):
        if(line != ","):
            assignmentInfo, date = line.split(",")
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
    choice = input("What is the assignment that you have completed: ")
    assignmentData[int(choice) - 1] = " "
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
            testInfo, date = line.split(",")
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
    choice = input("What is the test you have completed: ")
    testData[int(choice) - 1] = " "
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

def main():
    print "What would you like to do:\n1. Mark Test as Completed\n2. Mark Assignment as Completed\n"
    choice = input("I would like to: ")
    if(choice == 1):
        testData = readInTests()
        displayTests(testData)
        testData = editTestInfo(testData)
        writeTestInformation(testData)
    elif(choice == 2):
        assignmentData = readInAssignment()
        displayAssignment(assignmentData)
        assignmentData = editAssignmentInfo(assignmentData)
        writeAssignmentInformation(assignmentData)
main()
