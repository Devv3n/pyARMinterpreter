programCounter = 0;
code = []
labels = {}
memory, registers = {}, {}
compareValueEquals = 0 # 0NE - 1EQ 
compareValueDifference = 0 # 0EQ - 1GT - 2LT


# init
with open("code.txt", "r") as codeFile:
    for lineNum,line in enumerate(codeFile):
        if line[0:2] == "//": continue
        
        lineCode = line.strip("\n").split(" ")
        for i,v in enumerate(lineCode):
            lineCode[i] = v.strip(",")

        code.append(line.strip("\n"))
        if len(lineCode) == 1 and (lineCode[0] == "" or lineCode[0][0] == ":"):
            labels[lineCode[0][1:]] = lineNum
        
with open("memory.txt", "r") as memoryFile:
    for line in memoryFile:
        if line[0:2] == "//": continue
        
        memoryLine = line.strip("\n").split(" ")
        memory[memoryLine[0]] = int(memoryLine[1])



# functions
def getMemory(address):
    try: return memory[address]
    except:
        print(f"Invalid memory address {address}") 
        return 0

def setMemory(address, data):
    memory[address] = data

def getRegister(address):
    try: return registers[address]
    except: 
        print(f"Invalid register address {address}")
        return 0

def setRegister(address, data):
    registers[address] = data

def compareValues(val1, val2):
    global compareValueEquals, compareValueDifference
    if val1 == val2:
        compareValueEquals = 1
        compareValueDifference = 0
    
    else:
        compareValueEquals = 0
        if val1 > val2:
            compareValueDifference = 1
        elif val1 < val2:
            compareValueDifference = 2

def jumpToLabel(label):
    global programCounter
    if label in labels:
        programCounter = labels[label]



# main loop
while True:
    if programCounter >= len(code):
        break

    executing = code[programCounter].split(" ")
    lenExecuting = len(executing)
    for i,v in enumerate(executing):
        executing[i] = v.strip(",")

    orgProgramCounter = programCounter + 1
    programCounter += 1

    if lenExecuting == 1 and (executing[0] == "" or executing[0][0] == ":"):
        continue
            
    match (executing[0]):
        case "LDR":
            if lenExecuting == 3:
                if executing[2][0] == "#":
                    setRegister(executing[1][1:], int((executing[2][1:])))
                else:
                    setRegister(executing[1][1:], getMemory(executing[2]))

        case "STR":
            if lenExecuting == 3:
                if executing[1][0] == "#":
                    setMemory(executing[2], executing[1][1:])
                elif executing[1][0] == "R":
                    setMemory(executing[2], getRegister(executing[1][1:]))

        case "ADD":
            if lenExecuting == 4 and executing[1][0] == "R" and executing[2][0] == "R":
                if executing[3][0] == "#":
                    setRegister(executing[1][1:], getRegister(executing[2][1:])+int(executing[3][1:]))
                elif executing[3][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:])+getRegister(executing[3][1:]))

        case "SUB":
            if lenExecuting == 4 and executing[1][0] == "R" and executing[2][0] == "R":
                if executing[3][0] == "#":
                    setRegister(executing[1][1:], getRegister(executing[2][1:])-int(executing[3][1:]))
                elif executing[3][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:])-getRegister(executing[3][1:]))

        case "MOV":
            if lenExecuting == 3 and executing[1][0] == "R":
                if executing[2][0] == "#":
                    setRegister(executing[1][1:], int(executing[2][1:]))
                elif executing[2][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]))

        case "CMP":
            if lenExecuting == 3 and executing[1][0] == "R":
                if executing[2][0] == "#":
                    compareValues(getRegister(executing[1][1:]), int(executing[2][1:]))
                elif executing[2][0] == "R":
                    compareValues(getRegister(executing[1][1:]), getRegister(executing[2][1:]))
                
        case "B":
            if lenExecuting == 2:
                jumpToLabel(executing[1])

        case "BEQ":
            if lenExecuting == 2 and compareValueEquals == 1 and compareValueDifference == 0:
                jumpToLabel(executing[1])

        case "BNE":
            if lenExecuting == 2 and compareValueEquals == 0:
                jumpToLabel(executing[1])

        case "BGT":
            if lenExecuting == 2 and compareValueEquals == 0 and compareValueDifference == 1:
                jumpToLabel(executing[1])

        case "BLT":
            if lenExecuting == 2 and compareValueEquals == 0 and compareValueDifference == 2:
                jumpToLabel(executing[1])

        case "AND":
            if lenExecuting == 4 and executing[1][0] == "R" and executing[2][0] == "R":
                if executing[3][0] == "#":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) & int(executing[3][1:]))
                elif executing[3][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) & getRegister(executing[3][1:]))

        case "ORR":
            if lenExecuting == 4 and executing[1][0] == "R" and executing[2][0] == "R":
                if executing[3][0] == "#":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) | int(executing[3][1:]))
                elif executing[3][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) | getRegister(executing[3][1:]))

        case "EOR":
            if lenExecuting == 4 and executing[1][0] == "R" and executing[2][0] == "R":
                if executing[3][0] == "#":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) ^ int(executing[3][1:]))
                elif executing[3][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) ^ getRegister(executing[3][1:]))

        case "MVN":
            if lenExecuting == 3 and executing[1][0] == "R":
                if executing[2][0] == "#":
                    setRegister(executing[1][1:], ~int(executing[2][1:]))
                elif executing[2][0] == "R":
                    setRegister(executing[1][1:], ~getRegister(executing[2][1:]))

        case "LSL":
            if lenExecuting == 4 and executing[1][0] == "R" and executing[2][0] == "R":
                if executing[3][0] == "#":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) << int(executing[3][1:]))
                elif executing[3][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) << getRegister(executing[3][1:]))

        case "LSR":
            if lenExecuting == 4 and executing[1][0] == "R" and executing[2][0] == "R":
                if executing[3][0] == "#":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) >> int(executing[3][1:]))
                elif executing[3][0] == "R":
                    setRegister(executing[1][1:], getRegister(executing[2][1:]) >> getRegister(executing[3][1:]))

        case "HALT":
            print(f"Line {orgProgramCounter} calls halt.")
            break

        case _:
            print(f"Line {orgProgramCounter} is shit.")
        

    print(f"Line {orgProgramCounter}\n - Registers:{registers}\n - Memory:{memory}\n - Executing:{executing}\n")
