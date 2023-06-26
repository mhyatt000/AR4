from exc import commands 
from gui.base import EntryField

def runProg():

    def threadProg():

        global rowinproc
        global stopQueue
        global splineActive

        stopQueue = "0"
        splineActive = "0"
        try:
            curRow = tab1.progView.curselection()[0]
            if curRow == 0:
                curRow = 1
        except:
            curRow = 1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(curRow)

        tab1.runTrue = 1
        while tab1.runTrue == 1:
            if tab1.runTrue == 0:
                almStatusLab.config(text="PROGRAM STOPPED", style="Alarm.TLabel")
                almStatusLab2.config(text="PROGRAM STOPPED", style="Alarm.TLabel")
            else:
                almStatusLab.config(text="PROGRAM RUNNING", style="OK.TLabel")
                almStatusLab2.config(text="PROGRAM RUNNING", style="OK.TLabel")

            rowinproc = 1
            executeRow()
            while rowinproc == 1:
                time.sleep(0.01)

            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index("end")

            for row in range(0, selRow):
                tab1.progView.itemconfig(row, {"fg": "dodger blue"})
            tab1.progView.itemconfig(selRow, {"fg": "blue2"})
            for row in range(selRow + 1, last):
                tab1.progView.itemconfig(row, {"fg": "black"})

            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            time.sleep(0.01)

            try:
                selRow = tab1.progView.curselection()[0]
                curRowEntryField.delete(0, "end")
                curRowEntryField.insert(0, selRow)
            except:
                curRowEntryField.delete(0, "end")
                curRowEntryField.insert(0, "---")
                tab1.runTrue = 0
                almStatusLab.config(text="PROGRAM STOPPED", style="Alarm.TLabel")
                almStatusLab2.config(text="PROGRAM STOPPED", style="Alarm.TLabel")

    t = threading.Thread(target=threadProg)
    t.start()

def alm_ready():
    """docstring"""

    almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
    almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")


def step(colors, val):
    """docstring"""

    alm_ready()
    executeRow()

    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index("end")

    for row in range(0, selRow):
        tab1.progView.itemconfig(row, {"fg": colors[0]})
    tab1.progView.itemconfig(selRow, {"fg":colors[1]})
    for row in range(selRow + 1, last):
        tab1.progView.itemconfig(row, {"fg":colors[2]})

    tab1.progView.selection_clear(0, END)
    selRow += val
    tab1.progView.select_set(selRow)
    try:
        selRow = tab1.progView.curselection()[0]
        curRowEntryField.delete(0, "end")
        curRowEntryField.insert(0, selRow)
    except:
        curRowEntryField.delete(0, "end")
        curRowEntryField.insert(0, "---")



def stepFwd():
    colors = [ "dodger blue", "blue2", "black" ]
    step(colors,1)


def stepRev():
    colors = [ "black", "red", "tomato2" ]
    step(colors,-1)

def stopProg():
    cmdType, splineActive, stopQueue = None,None,None

    lastProg = ""
    tab1.runTrue = 0
    almStatusLab.config(text="PROGRAM STOPPED", style="Alarm.TLabel")
    almStatusLab2.config(text="PROGRAM STOPPED", style="Alarm.TLabel")


def executeRow():

    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur

    global calStat
    global rowinproc
    global LineDist
    global Xv
    global Yv
    global Zv
    global commandCalc
    global moveInProc
    global splineActive
    global stopQueue

    startTime = time.time()
    selRow = tab1.progView.curselection()[0]
    tab1.progView.see(selRow + 2)
    data = list(map(int, tab1.progView.curselection()))
    command = tab1.progView.get(data[0])
    cmdType = command[:6]

    ##Call Program##
    if cmdType == "Call P":
        commands.call_prog()

    ##Return Program##
    if cmdType == "Return":
        commands.return_prog()

    ##Set Encoders 1000
    if cmdType == "Set En":
        if moveInProc == 1:
            moveInProc == 2
        command = "SE\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.05)
        time.sleep(0.2)
        ser.read()

    ##Read Encoders
    if cmdType == "Read E":
        read_encoders()

    ##Test Limit Switches
    if cmdType == "Test L":
        test_limit_switch()


    ##Servo Command##
    if cmdType == "Servo ":
        if moveInProc == 1:
            moveInProc == 2
        servoIndex = command.find("number ")
        posIndex = command.find("position: ")
        servoNum = str(command[servoIndex + 7 : posIndex - 4])
        servoPos = str(command[posIndex + 10 :])
        command = "SV" + servoNum + "P" + servoPos + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(0.2)
        ser2.read()

    ##If Input On Jump to Tab IO Board##
    if cmdType == "If On ":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("Input-")
        tabIndex = command.find("Tab-")
        inputNum = str(command[inputIndex + 6 : tabIndex - 9])
        tabNum = str(command[tabIndex + 4 :])
        command = "JFX" + inputNum + "T" + tabNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(0.2)
        response = str(ser2.readline().strip(), "utf-8")
        if response == "T":
            index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
            index = index - 1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    ##If Input Off Jump to Tab IO Board##
    if cmdType == "If Off":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("Input-")
        tabIndex = command.find("Tab-")
        inputNum = str(command[inputIndex + 6 : tabIndex - 9])
        tabNum = str(command[tabIndex + 4 :])
        command = "JFX" + inputNum + "T" + tabNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(0.2)
        response = str(ser2.readline().strip(), "utf-8")
        if response == "F":
            index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
            index = index - 1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    ##If Input On Jump to Tab Teensy##
    if cmdType == "TifOn ":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("Input-")
        tabIndex = command.find("Tab-")
        inputNum = str(command[inputIndex + 6 : tabIndex - 9])
        tabNum = str(command[tabIndex + 4 :])
        command = "JFX" + inputNum + "T" + tabNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response == "T":
            index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
            index = index - 1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    ##If Input Off Jump to Tab Teensy##
    if cmdType == "TifOff":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("Input-")
        tabIndex = command.find("Tab-")
        inputNum = str(command[inputIndex + 6 : tabIndex - 9])
        tabNum = str(command[tabIndex + 4 :])
        command = "JFX" + inputNum + "T" + tabNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response == "F":
            index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
            index = index - 1
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    ##Jump to Row##
    if cmdType == "Jump T":
        if moveInProc == 1:
            moveInProc == 2
        tabIndex = command.find("Tab-")
        tabNum = str(command[tabIndex + 4 :])
        index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(index)

    ##Set Output ON Command IO Board##
    if cmdType == "Out On":
        if moveInProc == 1:
            moveInProc == 2
        outputIndex = command.find("Out On = ")
        outputNum = str(command[outputIndex + 9 :])
        command = "ONX" + outputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(0.2)
        ser2.read()

    ##Set Output OFF Command IO Board##
    if cmdType == "Out Of":
        if moveInProc == 1:
            moveInProc == 2
        outputIndex = command.find("Out Off = ")
        outputNum = str(command[outputIndex + 10 :])
        command = "OFX" + outputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(0.2)
        ser2.read()

    ##Set Output ON Command Teensy##
    if cmdType == "ToutOn":
        if moveInProc == 1:
            moveInProc == 2
        outputIndex = command.find("outOn = ")
        outputNum = str(command[outputIndex + 8 :])
        command = "ONX" + outputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.read()

    ##Set Output OFF Command Teensy##
    if cmdType == "ToutOf":
        if moveInProc == 1:
            moveInProc == 2
        outputIndex = command.find("outOff = ")
        outputNum = str(command[outputIndex + 9 :])
        command = "OFX" + outputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.read()

    ##Wait Input ON Command IO Board##
    if cmdType == "Wait I":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("Wait Input On = ")
        inputNum = str(command[inputIndex + 16 :])
        command = "WIN" + inputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(0.2)
        ser2.read()

    ##Wait Input OFF Command IO Board##
    if cmdType == "Wait O":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("Wait Off Input = ")
        inputNum = str(command[inputIndex + 17 :])
        command = "WON" + inputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(0.2)
        ser2.read()

    ##Wait Input ON Command Teensy##
    if cmdType == "TwaitI":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("TwaitInput On = ")
        inputNum = str(command[inputIndex + 16 :])
        command = "WIN" + inputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.read()

    ##Wait Input OFF Command Teensy##
    if cmdType == "TwaitO":
        if moveInProc == 1:
            moveInProc == 2
        inputIndex = command.find("TwaitOff Input = ")
        inputNum = str(command[inputIndex + 16 :])
        command = "WON" + inputNum + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.read()

    ##Wait Time Command##
    if cmdType == "Wait T":
        if moveInProc == 1:
            moveInProc == 2
        timeIndex = command.find("Wait Time = ")
        timeSeconds = str(command[timeIndex + 12 :])
        command = "WTS" + timeSeconds + "\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.read()

    ##Set Register##
    if cmdType == "Regist":
        if moveInProc == 1:
            moveInProc == 2
        regNumIndex = command.find("Register ")
        regEqIndex = command.find(" = ")
        regNumVal = str(command[regNumIndex + 9 : regEqIndex])
        regEntry = "R" + regNumVal + "EntryField"
        testOper = str(command[regEqIndex + 3 : regEqIndex + 5])
        if testOper == "++":
            regCEqVal = str(command[regEqIndex + 5 :])
            curRegVal = eval(regEntry).get()
            regEqVal = str(int(regCEqVal) + int(curRegVal))
        elif testOper == "--":
            regCEqVal = str(command[regEqIndex + 5 :])
            curRegVal = eval(regEntry).get()
            regEqVal = str(int(curRegVal) - int(regCEqVal))
        else:
            regEqVal = str(command[regEqIndex + 3 :])
        eval(regEntry).delete(0, "end")
        eval(regEntry).insert(0, regEqVal)

    ##Set Position Register##
    if cmdType == "Positi":
        if moveInProc == 1:
            moveInProc == 2
        regNumIndex = command.find("Position Register ")
        regElIndex = command.find("Element")
        regEqIndex = command.find(" = ")
        regNumVal = str(command[regNumIndex + 18 : regElIndex - 1])
        regNumEl = str(command[regElIndex + 8 : regEqIndex])
        regEntry = "SP_" + regNumVal + "_E" + regNumEl + "_EntryField"
        testOper = str(command[regEqIndex + 3 : regEqIndex + 5])
        if testOper == "++":
            regCEqVal = str(command[regEqIndex + 4 :])
            curRegVal = eval(regEntry).get()
            regEqVal = str(float(regCEqVal) + float(curRegVal))
        elif testOper == "--":
            regCEqVal = str(command[regEqIndex + 5 :])
            curRegVal = eval(regEntry).get()
            regEqVal = str(float(curRegVal) - float(regCEqVal))
        else:
            regEqVal = str(command[regEqIndex + 3 :])
        eval(regEntry).delete(0, "end")
        eval(regEntry).insert(0, regEqVal)

    ##If Register Jump to Row##
    if cmdType == "If Reg":
        if moveInProc == 1:
            moveInProc == 2
        regIndex = command.find("If Register ")
        regEqIndex = command.find(" = ")
        regJmpIndex = command.find(" Jump to Tab ")
        regNum = str(command[regIndex + 12 : regEqIndex])
        regEq = str(command[regEqIndex + 3 : regJmpIndex])
        tabNum = str(command[regJmpIndex + 13 :])
        regEntry = "R" + regNum + "EntryField"
        curRegVal = eval(regEntry).get()
        if curRegVal == regEq:
            index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    ##Calibrate Command##
    if cmdType == "Calibr":
        if moveInProc == 1:
            moveInProc == 2
        calRobotAll()
        if calStat == 0:
            stopProg()

    ##Set tool##
    if cmdType == "Tool S":
        if moveInProc == 1:
            moveInProc == 2
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        xIndex = command.find(" X ")
        yIndex = command.find(" Y ")
        zIndex = command.find(" Z ")
        rzIndex = command.find(" Rz ")
        ryIndex = command.find(" Ry ")
        rxIndex = command.find(" Rx ")
        xVal = command[xIndex + 3 : yIndex]
        yVal = command[yIndex + 3 : zIndex]
        zVal = command[zIndex + 3 : rzIndex]
        rzVal = command[rzIndex + 4 : ryIndex]
        ryVal = command[ryIndex + 4 : rxIndex]
        rxVal = command[rxIndex + 4 :]
        TFxEntryField.delete(0, "end")
        TFyEntryField.delete(0, "end")
        TFzEntryField.delete(0, "end")
        TFrzEntryField.delete(0, "end")
        TFryEntryField.delete(0, "end")
        TFrxEntryField.delete(0, "end")
        TFxEntryField.insert(0, str(xVal))
        TFyEntryField.insert(0, str(yVal))
        TFzEntryField.insert(0, str(zVal))
        TFrzEntryField.insert(0, str(rzVal))
        TFryEntryField.insert(0, str(ryVal))
        TFrxEntryField.insert(0, str(rxVal))
        command = (
            "TF"
            + "A"
            + xVal
            + "B"
            + yVal
            + "C"
            + zVal
            + "D"
            + rzVal
            + "E"
            + ryVal
            + "F"
            + rxVal
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.read()

    ##Move J Command##
    if cmdType == "Move J":
        if moveInProc == 0:
            moveInProc == 1
        xIndex = command.find(" X ")
        yIndex = command.find(" Y ")
        zIndex = command.find(" Z ")
        rzIndex = command.find(" Rz ")
        ryIndex = command.find(" Ry ")
        rxIndex = command.find(" Rx ")
        J7Index = command.find(" J7 ")
        J8Index = command.find(" J8 ")
        J9Index = command.find(" J9 ")
        SpeedIndex = command.find(" S")
        ACCspdIndex = command.find(" Ac ")
        DECspdIndex = command.find(" Dc ")
        ACCrampIndex = command.find(" Rm ")
        WristConfIndex = command.find(" $")
        xVal = command[xIndex + 3 : yIndex]
        yVal = command[yIndex + 3 : zIndex]
        zVal = command[zIndex + 3 : rzIndex]
        rzVal = command[rzIndex + 4 : ryIndex]
        ryVal = command[ryIndex + 4 : rxIndex]
        rxVal = command[rxIndex + 4 : J7Index]
        J7Val = command[J7Index + 4 : J8Index]
        J8Val = command[J8Index + 4 : J9Index]
        J9Val = command[J9Index + 4 : SpeedIndex]
        speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
        Speed = command[SpeedIndex + 4 : ACCspdIndex]
        ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
        DECspd = command[DECspdIndex + 4 : ACCrampIndex]
        ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
        WC = command[WristConfIndex + 3 :]
        LoopMode = (
            str(J1OpenLoopStat.get())
            + str(J2OpenLoopStat.get())
            + str(J3OpenLoopStat.get())
            + str(J4OpenLoopStat.get())
            + str(J5OpenLoopStat.get())
            + str(J6OpenLoopStat.get())
        )
        command = (
            "MJ"
            + "X"
            + xVal
            + "Y"
            + yVal
            + "Z"
            + zVal
            + "Rz"
            + rzVal
            + "Ry"
            + ryVal
            + "Rx"
            + rxVal
            + "J7"
            + J7Val
            + "J8"
            + J8Val
            + "J9"
            + J9Val
            + speedPrefix
            + Speed
            + "Ac"
            + ACCspd
            + "Dc"
            + DECspd
            + "Rm"
            + ACCramp
            + "W"
            + WC
            + "Lm"
            + LoopMode
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        # ser.read()
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##Offs J Command##
    if cmdType == "OFF J ":
        if moveInProc == 0:
            moveInProc == 1
        SPnewInex = command.find("[ PR: ")
        SPendInex = command.find(" ] [")
        xIndex = command.find(" X ")
        yIndex = command.find(" Y ")
        zIndex = command.find(" Z ")
        rzIndex = command.find(" Rz ")
        ryIndex = command.find(" Ry ")
        rxIndex = command.find(" Rx ")
        J7Index = command.find(" J7 ")
        J8Index = command.find(" J8 ")
        J9Index = command.find(" J9 ")
        SpeedIndex = command.find(" S")
        ACCspdIndex = command.find(" Ac ")
        DECspdIndex = command.find(" Dc ")
        ACCrampIndex = command.find(" Rm ")
        WristConfIndex = command.find(" $")
        SP = str(command[SPnewInex + 6 : SPendInex])
        cx = eval("SP_" + SP + "_E1_EntryField").get()
        cy = eval("SP_" + SP + "_E2_EntryField").get()
        cz = eval("SP_" + SP + "_E3_EntryField").get()
        crz = eval("SP_" + SP + "_E4_EntryField").get()
        cry = eval("SP_" + SP + "_E5_EntryField").get()
        crx = eval("SP_" + SP + "_E6_EntryField").get()
        xVal = str(float(cx) + float(command[xIndex + 3 : yIndex]))
        yVal = str(float(cy) + float(command[yIndex + 3 : zIndex]))
        zVal = str(float(cz) + float(command[zIndex + 3 : rzIndex]))
        rzVal = str(float(crz) + float(command[rzIndex + 4 : ryIndex]))
        ryVal = str(float(cry) + float(command[ryIndex + 4 : rxIndex]))
        rxVal = str(float(crx) + float(command[rxIndex + 4 : J7Index]))
        J7Val = command[J7Index + 4 : J8Index]
        J8Val = command[J8Index + 4 : J9Index]
        J9Val = command[J9Index + 4 : SpeedIndex]
        speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
        Speed = command[SpeedIndex + 4 : ACCspdIndex]
        ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
        DECspd = command[DECspdIndex + 4 : ACCrampIndex]
        ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
        WC = command[WristConfIndex + 3 :]
        LoopMode = (
            str(J1OpenLoopStat.get())
            + str(J2OpenLoopStat.get())
            + str(J3OpenLoopStat.get())
            + str(J4OpenLoopStat.get())
            + str(J5OpenLoopStat.get())
            + str(J6OpenLoopStat.get())
        )
        command = (
            "MJ"
            + "X"
            + xVal
            + "Y"
            + yVal
            + "Z"
            + zVal
            + "Rz"
            + rzVal
            + "Ry"
            + ryVal
            + "Rx"
            + rxVal
            + "J7"
            + J7Val
            + "J8"
            + J8Val
            + "J9"
            + J9Val
            + speedPrefix
            + Speed
            + "Ac"
            + ACCspd
            + "Dc"
            + DECspd
            + "Rm"
            + ACCramp
            + "W"
            + WC
            + "Lm"
            + LoopMode
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##Move Vis Command##
    if cmdType == "Move V":
        if moveInProc == 0:
            moveInProc == 1
        SPnewInex = command.find("[ PR: ")
        SPendInex = command.find(" ] [")
        xIndex = command.find(" X ")
        yIndex = command.find(" Y ")
        zIndex = command.find(" Z ")
        rzIndex = command.find(" Rz ")
        ryIndex = command.find(" Ry ")
        rxIndex = command.find(" Rx ")
        J7Index = command.find(" J7 ")
        J8Index = command.find(" J8 ")
        J9Index = command.find(" J9 ")
        SpeedIndex = command.find(" S")
        ACCspdIndex = command.find(" Ac ")
        DECspdIndex = command.find(" Dc ")
        ACCrampIndex = command.find(" Rm ")
        WristConfIndex = command.find(" $")
        SP = str(command[SPnewInex + 6 : SPendInex])
        cx = eval("SP_" + SP + "_E1_EntryField").get()
        cy = eval("SP_" + SP + "_E2_EntryField").get()
        cz = eval("SP_" + SP + "_E3_EntryField").get()
        crz = eval("SP_" + SP + "_E4_EntryField").get()
        cry = eval("SP_" + SP + "_E5_EntryField").get()
        crx = eval("SP_" + SP + "_E6_EntryField").get()
        xVal = str(float(cx) + float(VisRetXrobEntryField.get()))
        yVal = str(float(cy) + float(VisRetYrobEntryField.get()))
        zVal = str(float(cz) + float(command[zIndex + 3 : rzIndex]))
        rzVal = str(float(crz) + float(command[rzIndex + 4 : ryIndex]))
        ryVal = str(float(cry) + float(command[ryIndex + 4 : rxIndex]))
        rxVal = str(float(crx) + float(command[rxIndex + 4 : J7Index]))
        J7Val = command[J7Index + 4 : J8Index]
        J8Val = command[J8Index + 4 : J9Index]
        J9Val = command[J9Index + 4 : SpeedIndex]
        speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
        Speed = command[SpeedIndex + 4 : ACCspdIndex]
        ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
        DECspd = command[DECspdIndex + 4 : ACCrampIndex]
        ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
        WC = command[WristConfIndex + 3 :]
        visRot = VisRetAngleEntryField.get()
        LoopMode = (
            str(J1OpenLoopStat.get())
            + str(J2OpenLoopStat.get())
            + str(J3OpenLoopStat.get())
            + str(J4OpenLoopStat.get())
            + str(J5OpenLoopStat.get())
            + str(J6OpenLoopStat.get())
        )
        command = (
            "MV"
            + "X"
            + xVal
            + "Y"
            + yVal
            + "Z"
            + zVal
            + "Rz"
            + rzVal
            + "Ry"
            + ryVal
            + "Rx"
            + rxVal
            + "J7"
            + J7Val
            + "J8"
            + J8Val
            + "J9"
            + J9Val
            + speedPrefix
            + Speed
            + "Ac"
            + ACCspd
            + "Dc"
            + DECspd
            + "Rm"
            + ACCramp
            + "W"
            + WC
            + "Vr"
            + visRot
            + "Lm"
            + LoopMode
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##Move PR Command##
    if cmdType == "Move P":
        if moveInProc == 0:
            moveInProc == 1
        SPnewInex = command.find("[ PR: ")
        SPendInex = command.find(" ] [")
        J7Index = command.find(" J7 ")
        J8Index = command.find(" J8 ")
        J9Index = command.find(" J9 ")
        SpeedIndex = command.find(" S")
        ACCspdIndex = command.find(" Ac ")
        DECspdIndex = command.find(" Dc ")
        ACCrampIndex = command.find(" Rm ")
        WristConfIndex = command.find(" $")
        SP = str(command[SPnewInex + 6 : SPendInex])
        cx = eval("SP_" + SP + "_E1_EntryField").get()
        cy = eval("SP_" + SP + "_E2_EntryField").get()
        cz = eval("SP_" + SP + "_E3_EntryField").get()
        crz = eval("SP_" + SP + "_E4_EntryField").get()
        cry = eval("SP_" + SP + "_E5_EntryField").get()
        crx = eval("SP_" + SP + "_E6_EntryField").get()
        xVal = str(float(cx))
        yVal = str(float(cy))
        zVal = str(float(cz))
        rzVal = str(float(crz))
        ryVal = str(float(cry))
        rxVal = str(float(crx))
        J7Val = command[J7Index + 4 : J8Index]
        J8Val = command[J8Index + 4 : J9Index]
        J9Val = command[J9Index + 4 : SpeedIndex]
        speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
        Speed = command[SpeedIndex + 4 : ACCspdIndex]
        ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
        DECspd = command[DECspdIndex + 4 : ACCrampIndex]
        ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
        WC = command[WristConfIndex + 3 :]
        LoopMode = (
            str(J1OpenLoopStat.get())
            + str(J2OpenLoopStat.get())
            + str(J3OpenLoopStat.get())
            + str(J4OpenLoopStat.get())
            + str(J5OpenLoopStat.get())
            + str(J6OpenLoopStat.get())
        )
        command = (
            "MJ"
            + "X"
            + xVal
            + "Y"
            + yVal
            + "Z"
            + zVal
            + "Rz"
            + rzVal
            + "Ry"
            + ryVal
            + "Rx"
            + rxVal
            + "J7"
            + J7Val
            + "J8"
            + J8Val
            + "J9"
            + J9Val
            + speedPrefix
            + Speed
            + "Ac"
            + ACCspd
            + "Dc"
            + DECspd
            + "Rm"
            + ACCramp
            + "W"
            + WC
            + "Lm"
            + LoopMode
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##OFFS PR Command##
    if cmdType == "OFF PR":
        if moveInProc == 0:
            moveInProc == 1
        SPnewInex = command.find("[ PR: ")
        SPendInex = command.find(" ] offs")
        SP2newInex = command.find("[ *PR: ")
        SP2endInex = command.find(" ]  [")
        J7Index = command.find(" J7 ")
        J8Index = command.find(" J8 ")
        J9Index = command.find(" J9 ")
        SpeedIndex = command.find(" S")
        ACCspdIndex = command.find(" Ac ")
        DECspdIndex = command.find(" Dc ")
        ACCrampIndex = command.find(" Rm ")
        WristConfIndex = command.find(" $")
        SP = str(command[SPnewInex + 6 : SPendInex])
        SP2 = str(command[SP2newInex + 7 : SP2endInex])
        xVal = str(
            float(eval("SP_" + SP + "_E1_EntryField").get())
            + float(eval("SP_" + SP2 + "_E1_EntryField").get())
        )
        yVal = str(
            float(eval("SP_" + SP + "_E2_EntryField").get())
            + float(eval("SP_" + SP2 + "_E2_EntryField").get())
        )
        zVal = str(
            float(eval("SP_" + SP + "_E3_EntryField").get())
            + float(eval("SP_" + SP2 + "_E3_EntryField").get())
        )
        rzVal = str(
            float(eval("SP_" + SP + "_E4_EntryField").get())
            + float(eval("SP_" + SP2 + "_E4_EntryField").get())
        )
        ryVal = str(
            float(eval("SP_" + SP + "_E5_EntryField").get())
            + float(eval("SP_" + SP2 + "_E5_EntryField").get())
        )
        rxVal = str(
            float(eval("SP_" + SP + "_E6_EntryField").get())
            + float(eval("SP_" + SP2 + "_E6_EntryField").get())
        )
        J7Val = command[J7Index + 4 : J8Index]
        J8Val = command[J8Index + 4 : J9Index]
        J9Val = command[J9Index + 4 : SpeedIndex]
        speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
        Speed = command[SpeedIndex + 4 : ACCspdIndex]
        ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
        DECspd = command[DECspdIndex + 4 : ACCrampIndex]
        ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
        WC = command[WristConfIndex + 3 :]
        LoopMode = (
            str(J1OpenLoopStat.get())
            + str(J2OpenLoopStat.get())
            + str(J3OpenLoopStat.get())
            + str(J4OpenLoopStat.get())
            + str(J5OpenLoopStat.get())
            + str(J6OpenLoopStat.get())
        )
        command = (
            "MJ"
            + "X"
            + xVal
            + "Y"
            + yVal
            + "Z"
            + zVal
            + "Rz"
            + rzVal
            + "Ry"
            + ryVal
            + "Rx"
            + rxVal
            + "J7"
            + J7Val
            + "J8"
            + J8Val
            + "J9"
            + J9Val
            + speedPrefix
            + Speed
            + "Ac"
            + ACCspd
            + "Dc"
            + DECspd
            + "Rm"
            + ACCramp
            + "W"
            + WC
            + "Lm"
            + LoopMode
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##Move L Command##
    if cmdType == "Move L":
        if moveInProc == 0:
            moveInProc == 1
        xIndex = command.find(" X ")
        yIndex = command.find(" Y ")
        zIndex = command.find(" Z ")
        rzIndex = command.find(" Rz ")
        ryIndex = command.find(" Ry ")
        rxIndex = command.find(" Rx ")
        J7Index = command.find(" J7 ")
        J8Index = command.find(" J8 ")
        J9Index = command.find(" J9 ")
        SpeedIndex = command.find(" S")
        ACCspdIndex = command.find(" Ac ")
        DECspdIndex = command.find(" Dc ")
        ACCrampIndex = command.find(" Rm ")
        RoundingIndex = command.find(" Rnd ")
        WristConfIndex = command.find(" $")
        xVal = command[xIndex + 3 : yIndex]
        yVal = command[yIndex + 3 : zIndex]
        zVal = command[zIndex + 3 : rzIndex]
        rzVal = command[rzIndex + 4 : ryIndex]
        if np.sign(float(rzVal)) != np.sign(float(RzcurPos)):
            rzVal = str(float(rzVal) * -1)
        ryVal = command[ryIndex + 4 : rxIndex]
        rxVal = command[rxIndex + 4 : J7Index]
        J7Val = command[J7Index + 4 : J8Index]
        J8Val = command[J8Index + 4 : J9Index]
        J9Val = command[J9Index + 4 : SpeedIndex]
        speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
        Speed = command[SpeedIndex + 4 : ACCspdIndex]
        ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
        DECspd = command[DECspdIndex + 4 : ACCrampIndex]
        ACCramp = command[ACCrampIndex + 4 : RoundingIndex]
        Rounding = command[RoundingIndex + 5 : WristConfIndex]
        WC = command[WristConfIndex + 3 :]
        LoopMode = (
            str(J1OpenLoopStat.get())
            + str(J2OpenLoopStat.get())
            + str(J3OpenLoopStat.get())
            + str(J4OpenLoopStat.get())
            + str(J5OpenLoopStat.get())
            + str(J6OpenLoopStat.get())
        )
        command = (
            "ML"
            + "X"
            + xVal
            + "Y"
            + yVal
            + "Z"
            + zVal
            + "Rz"
            + rzVal
            + "Ry"
            + ryVal
            + "Rx"
            + rxVal
            + "J7"
            + J7Val
            + "J8"
            + J8Val
            + "J9"
            + J9Val
            + speedPrefix
            + Speed
            + "Ac"
            + ACCspd
            + "Dc"
            + DECspd
            + "Rm"
            + ACCramp
            + "Rnd"
            + Rounding
            + "W"
            + WC
            + "Lm"
            + LoopMode
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##Move R Command##
    if cmdType == "Move R":
        if moveInProc == 0:
            moveInProc == 1
        J1Index = command.find(" J1 ")
        J2Index = command.find(" J2 ")
        J3Index = command.find(" J3 ")
        J4Index = command.find(" J4 ")
        J5Index = command.find(" J5 ")
        J6Index = command.find(" J6 ")
        J7Index = command.find(" J7 ")
        J8Index = command.find(" J8 ")
        J9Index = command.find(" J9 ")
        SpeedIndex = command.find(" S")
        ACCspdIndex = command.find(" Ac ")
        DECspdIndex = command.find(" Dc ")
        ACCrampIndex = command.find(" Rm ")
        WristConfIndex = command.find(" $")
        J1Val = command[J1Index + 4 : J2Index]
        J2Val = command[J2Index + 4 : J3Index]
        J3Val = command[J3Index + 4 : J4Index]
        J4Val = command[J4Index + 4 : J5Index]
        J5Val = command[J5Index + 4 : J6Index]
        J6Val = command[J6Index + 4 : J7Index]
        J7Val = command[J7Index + 4 : J8Index]
        J8Val = command[J8Index + 4 : J9Index]
        J9Val = command[J9Index + 4 : SpeedIndex]
        speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
        Speed = command[SpeedIndex + 4 : ACCspdIndex]
        ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
        DECspd = command[DECspdIndex + 4 : ACCrampIndex]
        ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
        WC = command[WristConfIndex + 3 :]
        LoopMode = (
            str(J1OpenLoopStat.get())
            + str(J2OpenLoopStat.get())
            + str(J3OpenLoopStat.get())
            + str(J4OpenLoopStat.get())
            + str(J5OpenLoopStat.get())
            + str(J6OpenLoopStat.get())
        )
        command = (
            "RJ"
            + "A"
            + J1Val
            + "B"
            + J2Val
            + "C"
            + J3Val
            + "D"
            + J4Val
            + "E"
            + J5Val
            + "F"
            + J6Val
            + "J7"
            + J7Val
            + "J8"
            + J8Val
            + "J9"
            + J9Val
            + speedPrefix
            + Speed
            + "Ac"
            + ACCspd
            + "Dc"
            + DECspd
            + "Rm"
            + ACCramp
            + "W"
            + WC
            + "Lm"
            + LoopMode
            + "\n"
        )
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##Move A Command##
    if cmdType == "Move A":
        if moveInProc == 0:
            moveInProc == 1
        subCmd = command[:10]
        if subCmd == "Move A End":
            almStatusLab.config(
                text="Move A must start with a Mid followed by End",
                style="Alarm.TLabel",
            )
            almStatusLab2.config(
                text="Move A must start with a Mid followed by End",
                style="Alarm.TLabel",
            )
        else:
            xIndex = command.find(" X ")
            yIndex = command.find(" Y ")
            zIndex = command.find(" Z ")
            rzIndex = command.find(" Rz ")
            ryIndex = command.find(" Ry ")
            rxIndex = command.find(" Rx ")
            trIndex = command.find(" Tr ")
            SpeedIndex = command.find(" S")
            ACCspdIndex = command.find(" Ac ")
            DECspdIndex = command.find(" Dc ")
            ACCrampIndex = command.find(" Rm ")
            WristConfIndex = command.find(" $")
            xVal = command[xIndex + 3 : yIndex]
            yVal = command[yIndex + 3 : zIndex]
            zVal = command[zIndex + 3 : rzIndex]
            rzVal = command[rzIndex + 4 : ryIndex]
            ryVal = command[ryIndex + 4 : rxIndex]
            rxVal = command[rxIndex + 4 : trIndex]
            trVal = command[trIndex + 4 : SpeedIndex]
            speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
            Speed = command[SpeedIndex + 4 : ACCspdIndex]
            ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
            DECspd = command[DECspdIndex + 4 : ACCrampIndex]
            ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
            WC = command[WristConfIndex + 3 :]
            TCX = 0
            TCY = 0
            TCZ = 0
            TCRx = 0
            TCRy = 0
            TCRz = 0
            ##read next row for End position
            curRow = tab1.progView.curselection()[0]
            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index("end")
            for row in range(0, selRow):
                tab1.progView.itemconfig(row, {"fg": "dodger blue"})
            tab1.progView.itemconfig(selRow, {"fg": "blue2"})
            for row in range(selRow + 1, last):
                tab1.progView.itemconfig(row, {"fg": "black"})
            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            selRow = tab1.progView.curselection()[0]
            tab1.progView.see(selRow + 2)
            data = list(map(int, tab1.progView.curselection()))
            command = tab1.progView.get(data[0])
            xIndex = command.find(" X ")
            yIndex = command.find(" Y ")
            zIndex = command.find(" Z ")
            rzIndex = command.find(" Rz ")
            ryIndex = command.find(" Ry ")
            rxIndex = command.find(" Rx ")
            trIndex = command.find(" Tr ")
            SpeedIndex = command.find(" S")
            ACCspdIndex = command.find(" Ac ")
            DECspdIndex = command.find(" Dc ")
            ACCrampIndex = command.find(" Rm ")
            WristConfIndex = command.find(" $")
            Xend = command[xIndex + 3 : yIndex]
            Yend = command[yIndex + 3 : zIndex]
            Zend = command[zIndex + 3 : rzIndex]
            rzVal = command[rzIndex + 4 : ryIndex]
            ryVal = command[ryIndex + 4 : rxIndex]
            rxVal = command[rxIndex + 4 : trIndex]
            trVal = command[trIndex + 4 : SpeedIndex]
            speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
            Speed = command[SpeedIndex + 4 : ACCspdIndex]
            ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
            DECspd = command[DECspdIndex + 4 : ACCrampIndex]
            ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
            WC = command[WristConfIndex + 3 :]
            TCX = 0
            TCY = 0
            TCZ = 0
            TCRx = 0
            TCRy = 0
            TCRz = 0
            # move arc command
            LoopMode = (
                str(J1OpenLoopStat.get())
                + str(J2OpenLoopStat.get())
                + str(J3OpenLoopStat.get())
                + str(J4OpenLoopStat.get())
                + str(J5OpenLoopStat.get())
                + str(J6OpenLoopStat.get())
            )
            command = (
                "MA"
                + "X"
                + xVal
                + "Y"
                + yVal
                + "Z"
                + zVal
                + "Rz"
                + rzVal
                + "Ry"
                + ryVal
                + "Rx"
                + rxVal
                + "Ex"
                + Xend
                + "Ey"
                + Yend
                + "Ez"
                + Zend
                + "Tr"
                + trVal
                + speedPrefix
                + Speed
                + "Ac"
                + ACCspd
                + "Dc"
                + DECspd
                + "Rm"
                + ACCramp
                + "W"
                + WC
                + "Lm"
                + LoopMode
                + "\n"
            )
            cmdSentEntryField.delete(0, "end")
            cmdSentEntryField.insert(0, command)
            ser.write(command.encode())
            ser.flushInput()
            time.sleep(0.2)
            response = str(ser.readline().strip(), "utf-8")
            if response[:1] == "E":
                handle_error(response)
            else:
                display_position(response)

    ##Move C Command##
    if cmdType == "Move C":
        if moveInProc == 0:
            moveInProc == 1
        subCmd = command[:10]
        if subCmd == "Move C Sta" or subCmd == "Move C Pla":
            almStatusLab.config(
                text="Move C must start with a Center followed by Start & Plane",
                style="Alarm.TLabel",
            )
            almStatusLab2.config(
                text="Move C must start with a Center followed by Start & Plane",
                style="Alarm.TLabel",
            )
        else:
            xIndex = command.find(" X ")
            yIndex = command.find(" Y ")
            zIndex = command.find(" Z ")
            rzIndex = command.find(" Rz ")
            ryIndex = command.find(" Ry ")
            rxIndex = command.find(" Rx ")
            trIndex = command.find(" Tr ")
            SpeedIndex = command.find(" S")
            ACCspdIndex = command.find(" Ac ")
            DECspdIndex = command.find(" Dc ")
            ACCrampIndex = command.find(" Rm ")
            WristConfIndex = command.find(" $")
            xVal = command[xIndex + 3 : yIndex]
            yVal = command[yIndex + 3 : zIndex]
            zVal = command[zIndex + 3 : rzIndex]
            rzVal = command[rzIndex + 4 : ryIndex]
            ryVal = command[ryIndex + 4 : rxIndex]
            rxVal = command[rxIndex + 4 : trIndex]
            trVal = command[trIndex + 4 : SpeedIndex]
            speedPrefix = command[SpeedIndex + 1 : SpeedIndex + 3]
            Speed = command[SpeedIndex + 4 : ACCspdIndex]
            ACCspd = command[ACCspdIndex + 4 : DECspdIndex]
            DECspd = command[DECspdIndex + 4 : ACCrampIndex]
            ACCramp = command[ACCrampIndex + 4 : WristConfIndex]
            WC = command[WristConfIndex + 3 :]
            TCX = 0
            TCY = 0
            TCZ = 0
            TCRx = 0
            TCRy = 0
            TCRz = 0
            ##read next row for Mid position
            curRow = tab1.progView.curselection()[0]
            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index("end")
            for row in range(0, selRow):
                tab1.progView.itemconfig(row, {"fg": "dodger blue"})
            tab1.progView.itemconfig(selRow, {"fg": "blue2"})
            for row in range(selRow + 1, last):
                tab1.progView.itemconfig(row, {"fg": "black"})
            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            selRow = tab1.progView.curselection()[0]
            tab1.progView.see(selRow + 2)
            data = list(map(int, tab1.progView.curselection()))
            command = tab1.progView.get(data[0])
            xIndex = command.find(" X ")
            yIndex = command.find(" Y ")
            zIndex = command.find(" Z ")
            Xmid = command[xIndex + 3 : yIndex]
            Ymid = command[yIndex + 3 : zIndex]
            Zmid = command[zIndex + 3 : rzIndex]
            ##read next row for End position
            curRow = tab1.progView.curselection()[0]
            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index("end")
            for row in range(0, selRow):
                tab1.progView.itemconfig(row, {"fg": "dodger blue"})
            tab1.progView.itemconfig(selRow, {"fg": "blue2"})
            for row in range(selRow + 1, last):
                tab1.progView.itemconfig(row, {"fg": "black"})
            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            selRow = tab1.progView.curselection()[0]
            tab1.progView.see(selRow + 2)
            data = list(map(int, tab1.progView.curselection()))
            command = tab1.progView.get(data[0])
            xIndex = command.find(" X ")
            yIndex = command.find(" Y ")
            zIndex = command.find(" Z ")
            Xend = command[xIndex + 3 : yIndex]
            Yend = command[yIndex + 3 : zIndex]
            Zend = command[zIndex + 3 : rzIndex]
            # move j to the beginning (second or mid point is start of circle)
            LoopMode = (
                str(J1OpenLoopStat.get())
                + str(J2OpenLoopStat.get())
                + str(J3OpenLoopStat.get())
                + str(J4OpenLoopStat.get())
                + str(J5OpenLoopStat.get())
                + str(J6OpenLoopStat.get())
            )
            command = (
                "MJ"
                + "X"
                + Xmid
                + "Y"
                + Ymid
                + "Z"
                + Zmid
                + "Rz"
                + rzVal
                + "Ry"
                + ryVal
                + "Rx"
                + rxVal
                + "Tr"
                + trVal
                + speedPrefix
                + Speed
                + "Ac"
                + ACCspd
                + "Dc"
                + DECspd
                + "Rm"
                + ACCramp
                + "W"
                + WC
                + "Lm"
                + LoopMode
                + "\n"
            )
            ser.write(command.encode())
            ser.flushInput()
            time.sleep(0.2)
            response = str(ser.readline().strip(), "utf-8")
            # move circle command
            LoopMode = (
                str(J1OpenLoopStat.get())
                + str(J2OpenLoopStat.get())
                + str(J3OpenLoopStat.get())
                + str(J4OpenLoopStat.get())
                + str(J5OpenLoopStat.get())
                + str(J6OpenLoopStat.get())
            )
            command = (
                "MC"
                + "Cx"
                + xVal
                + "Cy"
                + yVal
                + "Cz"
                + zVal
                + "Rz"
                + rzVal
                + "Ry"
                + ryVal
                + "Rx"
                + rxVal
                + "Bx"
                + Xmid
                + "By"
                + Ymid
                + "Bz"
                + Zmid
                + "Px"
                + Xend
                + "Py"
                + Yend
                + "Pz"
                + Zend
                + "Tr"
                + trVal
                + speedPrefix
                + Speed
                + "Ac"
                + ACCspd
                + "Dc"
                + DECspd
                + "Rm"
                + ACCramp
                + "W"
                + WC
                + "Lm"
                + LoopMode
                + "\n"
            )
            cmdSentEntryField.delete(0, "end")
            cmdSentEntryField.insert(0, command)
            ser.write(command.encode())
            ser.flushInput()
            time.sleep(0.1)
            response = str(ser.readline().strip(), "utf-8")
            if response[:1] == "E":
                handle_error(response)
            else:
                display_position(response)

    ##Start Spline
    if cmdType == "Start ":
        splineActive = "1"
        if moveInProc == 1:
            moveInProc == 2
        command = "SL\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        ser.read()

    ##End Spline
    if cmdType == "End Sp":
        splineActive = "0"
        if stopQueue == "1":
            stopQueue = "0"
            stop()
        if moveInProc == 1:
            moveInProc == 2
        command = "SS\n"
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            handle_error(response)
        else:
            display_position(response)

    ##Camera On
    if cmdType == "Cam On":
        if moveInProc == 1:
            moveInProc == 2
        start_vid()

    ##Camera Off
    if cmdType == "Cam Of":
        if moveInProc == 1:
            moveInProc == 2
        stop_vid()

    ##Vision Find
    if cmdType == "Vis Fi":
        # if (moveInProc == 1):
        # moveInProc == 2
        templateIndex = command.find("Vis Find - ")
        bgColorIndex = command.find(" - BGcolor ")
        scoreIndex = command.find(" Score ")
        passIndex = command.find(" Pass ")
        failIndex = command.find(" Fail ")
        template = command[templateIndex + 11 : bgColorIndex]
        checkBG = command[bgColorIndex + 11 : scoreIndex]
        if checkBG == "(Auto)":
            background = "Auto"
        else:
            background = eval(command[bgColorIndex + 11 : scoreIndex])
        min_score = float(command[scoreIndex + 7 : passIndex]) * 0.01
        passtab = command[passIndex + 6 : failIndex]
        failtab = command[failIndex + 6 :]
        take_pic()
        status = visFind(template, min_score, background)
        if status == "pass":
            tabIndex = command.find("Tab-")
            index = tab1.progView.get(0, "end").index("Tab Number " + passtab)
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)
        elif status == "fail":
            tabIndex = command.find("Tab-")
            index = tab1.progView.get(0, "end").index("Tab Number " + failtab)
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)

    rowinproc = 0



