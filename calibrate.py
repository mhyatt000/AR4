""" NOTE
dont use black yet... 
the command expands 20+ lines
"""

def calRobotAll():

    ##### STAGE 1 ########
    command = ( "LL" + "A" + str(J1CalStatVal) + "B" + str(J2CalStatVal) + "C" + str(J3CalStatVal) + "D" + str(J4CalStatVal) + "E" + str(J5CalStatVal) + "F"
        + str(J6CalStatVal) + "G0H0I0" + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff) + "M" + str(J4calOff) + "N" + str(J5calOff)
        + "O" + str(J6calOff) + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff) + "\n")

    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    response = str(ser.readline().strip(), "utf-8")

    if response[:1] == "A":
        displayPosition(response)
        message = "Auto Calibration Stage 1 Successful"
        almStatusLab.config(text=message, style="OK.TLabel")
        almStatusLab2.config(text=message, style="OK.TLabel")
    else:
        message = "Auto Calibration Stage 1 Failed"
        almStatusLab.config(text=message, style="Alarm.TLabel")
        almStatusLab2.config(text=message, style="Alarm.TLabel")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime + " - " + message)
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))
    ##### STAGE 2 ########
    CalStatVal2 = (
        int(J1CalStatVal2)
        + int(J2CalStatVal2)
        + int(J3CalStatVal2)
        + int(J4CalStatVal2)
        + int(J5CalStatVal2)
        + int(J6CalStatVal2)
    )

    if CalStatVal2 > 0:
        command = (
            "LL"
            + "A"
            + str(J1CalStatVal2)
            + "B"
            + str(J2CalStatVal2)
            + "C"
            + str(J3CalStatVal2)
            + "D"
            + str(J4CalStatVal2)
            + "E"
            + str(J5CalStatVal2)
            + "F"
            + str(J6CalStatVal2)
            + "G0H0I0"
            + "J"
            + str(J1calOff)
            + "K"
            + str(J2calOff)
            + "L"
            + str(J3calOff)
            + "M"
            + str(J4calOff)
            + "N"
            + str(J5calOff)
            + "O"
            + str(J6calOff)
            + "P"
            + str(J7calOff)
            + "Q"
            + str(J8calOff)
            + "R"
            + str(J9calOff)
            + "\n"
        )
        ser.write(command.encode())
        cmdSentEntryField.delete(0, "end")
        cmdSentEntryField.insert(0, command)
        ser.flushInput()
        response = str(ser.readline().strip(), "utf-8")

        if response[:1] == "A":
            displayPosition(response)
            message = "Auto Calibration Stage 2 Successful"
            almStatusLab.config(text=message, style="OK.TLabel")
            almStatusLab2.config(text=message, style="OK.TLabel")
        else:
            message = "Auto Calibration Stage 2 Failed"
            almStatusLab.config(text=message, style="Alarm.TLabel")
            almStatusLab2.config(text=message, style="Alarm.TLabel")
        Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
        tab6.ElogView.insert(END, Curtime + " - " + message)
        value = tab6.ElogView.get(0, END)
        pickle.dump(value, open("ErrorLog", "wb"))


def cal(joint, command):
    """basic calibrate"""

    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    response = str(ser.readline().strip(), "utf-8")

    if response[:1] == "A":
        displayPosition(response)
        message = f"{joint.name} Calibrated Successfully"
        style="OK.TLabel"
    else:
        message = f"{joint.name} Calibrated Failed"
        style="Alarm.TLabel"

    almStatusLab.config(text=message, style="Alarm.TLabel")
    almStatusLab2.config(text=message, style="Alarm.TLabel")

    now = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, f"{now} - {message}")
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))


def calRobotJ1():
    command = (
        "LLA1B0C0D0E0F0G0H0I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(1, command)

def calRobotJ2():
    command = (
        "LLA0B1C0D0E0F0G0H0I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(2, command)

def calRobotJ3():
    command = (
        "LLA0B0C1D0E0F0G0H0I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(3, command)

def calRobotJ4():
    command = (
        "LLA0B0C0D1E0F0G0H0I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(4, command)

def calRobotJ5():
    command = (
        "LLA0B0C0D0E1F0G0H0I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(5, command)

def calRobotJ6():
    command = (
        "LLA0B0C0D0E0F1G0H0I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(6, command)


def calRobotJ7():
    command = (
        "LLA0B0C0D0E0F0G1H0I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(7, command)

def calRobotJ8():
    command = (
        "LLA0B0C0D0E0F0G0H1I0"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(8, command)

def calRobotJ9():
    command = (
        "LLA0B0C0D0E0F0G0H0I1"
        + "J" + str(J1calOff) + "K" + str(J2calOff) + "L" + str(J3calOff)
        + "M" + str(J4calOff) + "N" + str(J5calOff) + "O" + str(J6calOff)
        + "P" + str(J7calOff) + "Q" + str(J8calOff) + "R" + str(J9calOff)
        + "\n")

    cal(9, command)

def calRobotMid():
    print("foo")
    # add mid command


def correctPos():
    command = "CP\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    displayPosition(response)


def requestPos():
    command = "RP\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    displayPosition(response)


def toolFrame():
    TFx = TFxEntryField.get()
    TFy = TFyEntryField.get()
    TFz = TFzEntryField.get()
    TFrz = TFrzEntryField.get()
    TFry = TFryEntryField.get()
    TFrx = TFrxEntryField.get()
    command = "TF" + "A" + TFx + "B" + TFy + "C" + TFz + "D" + TFrz + "E" + TFry + "F" + TFrx + "\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = ser.read()


def calExtAxis():
    J7axisLimNeg = 0
    J8axisLimNeg = 0
    J9axisLimNeg = 0

    J7axisLimPos = float(axis7lengthEntryField.get())
    J8axisLimPos = float(axis8lengthEntryField.get())
    J9axisLimPos = float(axis9lengthEntryField.get())

    J7negLimLab.config(text=str(-J7axisLimNeg), style="Jointlim.TLabel")
    J8negLimLab.config(text=str(-J8axisLimNeg), style="Jointlim.TLabel")
    J9negLimLab.config(text=str(-J9axisLimNeg), style="Jointlim.TLabel")

    J7posLimLab.config(text=str(J7axisLimPos), style="Jointlim.TLabel")
    J8posLimLab.config(text=str(J8axisLimPos), style="Jointlim.TLabel")
    J9posLimLab.config(text=str(J9axisLimPos), style="Jointlim.TLabel")

    J7jogslide.config(
        from_=-J7axisLimNeg,
        to=J7axisLimPos,
        length=125,
        orient=HORIZONTAL,
        command=J7sliderUpdate,
    )
    J8jogslide.config(
        from_=-J8axisLimNeg,
        to=J8axisLimPos,
        length=125,
        orient=HORIZONTAL,
        command=J8sliderUpdate,
    )
    J9jogslide.config(
        from_=-J9axisLimNeg,
        to=J9axisLimPos,
        length=125,
        orient=HORIZONTAL,
        command=J9sliderUpdate,
    )

    command = ( "CE" + "A" + str(J7axisLimPos) + "B" + str(J7rotation)
        + "C" + str(J7steps) + "D" + str(J8axisLimPos) + "E" + str(J8rotation)
        + "F" + str(J8steps) + "G" + str(J9axisLimPos) + "H" + str(J9rotation)
        + "I" + str(J9steps) + "\n")

    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = ser.read()

def zero():
    """basic zero axis"""

    pass

def zeroAxis7():
    command = "Z7" + "\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    almStatusLab.config(text="J7 Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="J7 Calibration Forced to Zero", style="Warn.TLabel")
    message = "J7 Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime + " - " + message)
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))
    response = str(ser.readline().strip(), "utf-8")
    displayPosition(response)


def zeroAxis8():
    command = "Z8" + "\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    almStatusLab.config(text="J8 Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="J8 Calibration Forced to Zero", style="Warn.TLabel")
    message = "J8 Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime + " - " + message)
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))
    response = str(ser.readline().strip(), "utf-8")
    displayPosition(response)


def zeroAxis9():
    command = "Z9" + "\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    almStatusLab.config(text="J9 Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="J9 Calibration Forced to Zero", style="Warn.TLabel")
    message = "J9 Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime + " - " + message)
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))
    response = str(ser.readline().strip(), "utf-8")
    displayPosition(response)


def sendPos():
    command = (
        "SP"
        + "A"
        + str(J1AngCur)
        + "B"
        + str(J2AngCur)
        + "C"
        + str(J3AngCur)
        + "D"
        + str(J4AngCur)
        + "E"
        + str(J5AngCur)
        + "F"
        + str(J6AngCur)
        + "G"
        + str(J7PosCur)
        + "H"
        + str(J8PosCur)
        + "I"
        + str(J9PosCur)
        + "\n"
    )
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = ser.read()


def CalZeroPos():
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    command = "SPA0B0C0D0E0F0\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = ser.read()
    requestPos()
    almStatusLab.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    message = "Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    tab6.ElogView.insert(END, Curtime + " - " + message)
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))


def CalRestPos():
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    command = "SPA0B0C-89D0E0F0\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = ser.read()
    requestPos()
    almStatusLab.config(text="Calibration Forced to Vertical Rest Pos", style="Warn.TLabel")
    almStatusLab2.config(text="Calibration Forced to Vertical Rest Pos", style="Warn.TLabel")
    message = "Calibration Forced to Vertical - this is for commissioning and testing - be careful!"
    tab6.ElogView.insert(END, Curtime + " - " + message)
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))


def ResetDrives():
    ResetDriveBut = Button(tab1, text="Reset Drives", command=ResetDrives)
    ResetDriveBut.place(x=307, y=42)
    command = "RD" + "\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = ser.read()
    almStatusLab.config(text="DRIVES RESET - PLEASE CHECK CALIBRATION", style="Warn.TLabel")
    almStatusLab2.config(text="DRIVES RESET - PLEASE CHECK CALIBRATION", style="Warn.TLabel")
    requestPos()


def displayPosition(response):
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7StepCur
    global XcurPos
    global YcurPos
    global ZcurPos
    global RxcurPos
    global RycurPos
    global RzcurPos
    global J7PosCur
    global J8PosCur
    global J9PosCur
    global WC

    cmdRecEntryField.delete(0, "end")
    cmdRecEntryField.insert(0, response)
    J1AngIndex = response.find("A")
    J2AngIndex = response.find("B")
    J3AngIndex = response.find("C")
    J4AngIndex = response.find("D")
    J5AngIndex = response.find("E")
    J6AngIndex = response.find("F")
    XposIndex = response.find("G")
    YposIndex = response.find("H")
    ZposIndex = response.find("I")
    RzposIndex = response.find("J")
    RyposIndex = response.find("K")
    RxposIndex = response.find("L")
    SpeedVioIndex = response.find("M")
    DebugIndex = response.find("N")
    FlagIndex = response.find("O")
    J7PosIndex = response.find("P")
    J8PosIndex = response.find("Q")
    J9PosIndex = response.find("R")
    J1AngCur = response[J1AngIndex + 1 : J2AngIndex].strip()
    J2AngCur = response[J2AngIndex + 1 : J3AngIndex].strip()
    J3AngCur = response[J3AngIndex + 1 : J4AngIndex].strip()
    J4AngCur = response[J4AngIndex + 1 : J5AngIndex].strip()
    J5AngCur = response[J5AngIndex + 1 : J6AngIndex].strip()
    J6AngCur = response[J6AngIndex + 1 : XposIndex].strip()

    if float(J5AngCur) > 0:
        WC = "F"
    else:
        WC = "N"
    XcurPos = response[XposIndex + 1 : YposIndex].strip()
    YcurPos = response[YposIndex + 1 : ZposIndex].strip()
    ZcurPos = response[ZposIndex + 1 : RzposIndex].strip()
    RzcurPos = response[RzposIndex + 1 : RyposIndex].strip()
    RycurPos = response[RyposIndex + 1 : RxposIndex].strip()
    RxcurPos = response[RxposIndex + 1 : SpeedVioIndex].strip()
    SpeedVioation = response[SpeedVioIndex + 1 : DebugIndex].strip()
    Debug = response[DebugIndex + 1 : FlagIndex].strip()
    Flag = response[FlagIndex + 1 : J7PosIndex].strip()
    J7PosCur = float(response[J7PosIndex + 1 : J8PosIndex].strip())
    J8PosCur = float(response[J8PosIndex + 1 : J9PosIndex].strip())
    J9PosCur = float(response[J9PosIndex + 1 :].strip())

    J1curAngEntryField.delete(0, "end")
    J1curAngEntryField.insert(0, J1AngCur)
    J2curAngEntryField.delete(0, "end")
    J2curAngEntryField.insert(0, J2AngCur)
    J3curAngEntryField.delete(0, "end")
    J3curAngEntryField.insert(0, J3AngCur)
    J4curAngEntryField.delete(0, "end")
    J4curAngEntryField.insert(0, J4AngCur)
    J5curAngEntryField.delete(0, "end")
    J5curAngEntryField.insert(0, J5AngCur)
    J6curAngEntryField.delete(0, "end")
    J6curAngEntryField.insert(0, J6AngCur)
    XcurEntryField.delete(0, "end")
    XcurEntryField.insert(0, XcurPos)
    YcurEntryField.delete(0, "end")
    YcurEntryField.insert(0, YcurPos)
    ZcurEntryField.delete(0, "end")
    ZcurEntryField.insert(0, ZcurPos)
    RzcurEntryField.delete(0, "end")
    RzcurEntryField.insert(0, RzcurPos)
    RycurEntryField.delete(0, "end")
    RycurEntryField.insert(0, RycurPos)
    RxcurEntryField.delete(0, "end")
    RxcurEntryField.insert(0, RxcurPos)
    J7curAngEntryField.delete(0, "end")
    J7curAngEntryField.insert(0, J7PosCur)
    J8curAngEntryField.delete(0, "end")
    J8curAngEntryField.insert(0, J8PosCur)
    J9curAngEntryField.delete(0, "end")
    J9curAngEntryField.insert(0, J9PosCur)
    J1jogslide.set(J1AngCur)
    J2jogslide.set(J2AngCur)
    J3jogslide.set(J3AngCur)
    J4jogslide.set(J4AngCur)
    J5jogslide.set(J5AngCur)
    J6jogslide.set(J6AngCur)
    J7jogslide.set(J7PosCur)
    J8jogslide.set(J8PosCur)
    J9jogslide.set(J9PosCur)
    manEntryField.delete(0, "end")
    manEntryField.insert(0, Debug)
    savePosData()
    if Flag != "":
        ErrorHandler(Flag)
    if SpeedVioation == "1":
        Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
        message = "Max Speed Violation - Reduce Speed Setpoint or Travel Distance"
        tab6.ElogView.insert(END, Curtime + " - " + message)
        value = tab6.ElogView.get(0, END)
        pickle.dump(value, open("ErrorLog", "wb"))
        almStatusLab.config(text=message, style="Warn.TLabel")
        almStatusLab2.config(text=message, style="Warn.TLabel")


def SaveAndApplyCalibration():
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global XcurPos
    global YcurPos
    global ZcurPos
    global RxcurPos
    global RycurPos
    global RzcurPos
    global J7PosCur
    global J8PosCur
    global J9PosCur
    global VisFileLoc
    global VisProg
    global VisOrigXpix
    global VisOrigXmm
    global VisOrigYpix
    global VisOrigYmm
    global VisEndXpix
    global VisEndXmm
    global VisEndYpix
    global VisEndYmm
    global J1calOff
    global J2calOff
    global J3calOff
    global J4calOff
    global J5calOff
    global J6calOff
    global J7calOff
    global J8calOff
    global J9calOff
    global J1OpenLoopVal
    global J2OpenLoopVal
    global J3OpenLoopVal
    global J4OpenLoopVal
    global J5OpenLoopVal
    global J6OpenLoopVal
    global J1CalStatVal
    global J2CalStatVal
    global J3CalStatVal
    global J4CalStatVal
    global J5CalStatVal
    global J6CalStatVal
    global J1CalStatVal2
    global J2CalStatVal2
    global J3CalStatVal2
    global J4CalStatVal2
    global J5CalStatVal2
    global J6CalStatVal2
    global J7axisLimPos
    global J7rotation
    global J7steps
    global J8length
    global J8rotation
    global J8steps
    global J9length
    global J9rotation
    global J9steps
    global IncJogStat
    J7PosCur = J7curAngEntryField.get()
    J8PosCur = J8curAngEntryField.get()
    J9PosCur = J9curAngEntryField.get()
    VisFileLoc = VisFileLocEntryField.get()
    VisProg = visoptions.get()
    VisOrigXpix = float(VisPicOxPEntryField.get())
    VisOrigXmm = float(VisPicOxMEntryField.get())
    VisOrigYpix = float(VisPicOyPEntryField.get())
    VisOrigYmm = float(VisPicOyMEntryField.get())
    VisEndXpix = float(VisPicXPEntryField.get())
    VisEndXmm = float(VisPicXMEntryField.get())
    VisEndYpix = float(VisPicYPEntryField.get())
    VisEndYmm = float(VisPicYMEntryField.get())
    J1calOff = float(J1calOffEntryField.get())
    J2calOff = float(J2calOffEntryField.get())
    J3calOff = float(J3calOffEntryField.get())
    J4calOff = float(J4calOffEntryField.get())
    J5calOff = float(J5calOffEntryField.get())
    J6calOff = float(J6calOffEntryField.get())
    J7calOff = float(J7calOffEntryField.get())
    J8calOff = float(J8calOffEntryField.get())
    J9calOff = float(J9calOffEntryField.get())
    J1OpenLoopVal = int(J1OpenLoopStat.get())
    J2OpenLoopVal = int(J2OpenLoopStat.get())
    J3OpenLoopVal = int(J3OpenLoopStat.get())
    J4OpenLoopVal = int(J4OpenLoopStat.get())
    J5OpenLoopVal = int(J5OpenLoopStat.get())
    J6OpenLoopVal = int(J6OpenLoopStat.get())
    J1CalStatVal = int(J1CalStat.get())
    J2CalStatVal = int(J2CalStat.get())
    J3CalStatVal = int(J3CalStat.get())
    J4CalStatVal = int(J4CalStat.get())
    J5CalStatVal = int(J5CalStat.get())
    J6CalStatVal = int(J6CalStat.get())
    J1CalStatVal2 = int(J1CalStat2.get())
    J2CalStatVal2 = int(J2CalStat2.get())
    J3CalStatVal2 = int(J3CalStat2.get())
    J4CalStatVal2 = int(J4CalStat2.get())
    J5CalStatVal2 = int(J5CalStat2.get())
    J6CalStatVal2 = int(J6CalStat2.get())
    J7axisLimPos = float(axis7lengthEntryField.get())
    J7rotation = float(axis7rotEntryField.get())
    J7steps = float(axis7stepsEntryField.get())
    J8length = float(axis8lengthEntryField.get())
    J8rotation = float(axis8rotEntryField.get())
    J8steps = float(axis8stepsEntryField.get())
    J9length = float(axis9lengthEntryField.get())
    J9rotation = float(axis9rotEntryField.get())
    J9steps = float(axis9stepsEntryField.get())
    try:
        toolFrame()
        time.sleep(0.5)
        calExtAxis()
    except:
        print("no serial connection with Teensy board")
    savePosData()


def savePosData():
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global XcurPos
    global YcurPos
    global ZcurPos
    global RxcurPos
    global RycurPos
    global RzcurPos
    global J7axisLimPos
    global J7rotation
    global J7steps
    global J8length
    global J8rotation
    global J8steps
    global J9length
    global J9rotation
    global J9steps
    global mX1
    global mY1
    global mX2
    global mY2
    calibration.delete(0, END)
    calibration.insert(END, J1AngCur)
    calibration.insert(END, J2AngCur)
    calibration.insert(END, J3AngCur)
    calibration.insert(END, J4AngCur)
    calibration.insert(END, J5AngCur)
    calibration.insert(END, J6AngCur)
    calibration.insert(END, XcurPos)
    calibration.insert(END, YcurPos)
    calibration.insert(END, ZcurPos)
    calibration.insert(END, RzcurPos)
    calibration.insert(END, RycurPos)
    calibration.insert(END, RxcurPos)
    calibration.insert(END, comPortEntryField.get())
    calibration.insert(END, ProgEntryField.get())
    calibration.insert(END, servo0onEntryField.get())
    calibration.insert(END, servo0offEntryField.get())
    calibration.insert(END, servo1onEntryField.get())
    calibration.insert(END, servo1offEntryField.get())
    calibration.insert(END, DO1onEntryField.get())
    calibration.insert(END, DO1offEntryField.get())
    calibration.insert(END, DO2onEntryField.get())
    calibration.insert(END, DO2offEntryField.get())
    calibration.insert(END, TFxEntryField.get())
    calibration.insert(END, TFyEntryField.get())
    calibration.insert(END, TFzEntryField.get())
    calibration.insert(END, TFrxEntryField.get())
    calibration.insert(END, TFryEntryField.get())
    calibration.insert(END, TFrzEntryField.get())
    calibration.insert(END, J7curAngEntryField.get())
    calibration.insert(END, J8curAngEntryField.get())
    calibration.insert(END, J9curAngEntryField.get())
    calibration.insert(END, VisFileLocEntryField.get())
    calibration.insert(END, visoptions.get())
    calibration.insert(END, VisPicOxPEntryField.get())
    calibration.insert(END, VisPicOxMEntryField.get())
    calibration.insert(END, VisPicOyPEntryField.get())
    calibration.insert(END, VisPicOyMEntryField.get())
    calibration.insert(END, VisPicXPEntryField.get())
    calibration.insert(END, VisPicXMEntryField.get())
    calibration.insert(END, VisPicYPEntryField.get())
    calibration.insert(END, VisPicYMEntryField.get())
    calibration.insert(END, J1calOffEntryField.get())
    calibration.insert(END, J2calOffEntryField.get())
    calibration.insert(END, J3calOffEntryField.get())
    calibration.insert(END, J4calOffEntryField.get())
    calibration.insert(END, J5calOffEntryField.get())
    calibration.insert(END, J6calOffEntryField.get())
    calibration.insert(END, J1OpenLoopVal)
    calibration.insert(END, J2OpenLoopVal)
    calibration.insert(END, J3OpenLoopVal)
    calibration.insert(END, J4OpenLoopVal)
    calibration.insert(END, J5OpenLoopVal)
    calibration.insert(END, J6OpenLoopVal)
    calibration.insert(END, com2PortEntryField.get())
    calibration.insert(END, theme)
    calibration.insert(END, J1CalStatVal)
    calibration.insert(END, J2CalStatVal)
    calibration.insert(END, J3CalStatVal)
    calibration.insert(END, J4CalStatVal)
    calibration.insert(END, J5CalStatVal)
    calibration.insert(END, J6CalStatVal)
    calibration.insert(END, J7axisLimPos)
    calibration.insert(END, J7rotation)
    calibration.insert(END, J7steps)
    calibration.insert(END, J7StepCur)  # is this used?
    calibration.insert(END, J1CalStatVal2)
    calibration.insert(END, J2CalStatVal2)
    calibration.insert(END, J3CalStatVal2)
    calibration.insert(END, J4CalStatVal2)
    calibration.insert(END, J5CalStatVal2)
    calibration.insert(END, J6CalStatVal2)
    calibration.insert(END, VisBrightSlide.get())
    calibration.insert(END, VisContrastSlide.get())
    calibration.insert(END, VisBacColorEntryField.get())
    calibration.insert(END, VisScoreEntryField.get())
    calibration.insert(END, VisX1PixEntryField.get())
    calibration.insert(END, VisY1PixEntryField.get())
    calibration.insert(END, VisX2PixEntryField.get())
    calibration.insert(END, VisY2PixEntryField.get())
    calibration.insert(END, VisX1RobEntryField.get())
    calibration.insert(END, VisY1RobEntryField.get())
    calibration.insert(END, VisX2RobEntryField.get())
    calibration.insert(END, VisY2RobEntryField.get())
    calibration.insert(END, VisZoomSlide.get())
    calibration.insert(END, pick180.get())
    calibration.insert(END, pickClosest.get())
    calibration.insert(END, visoptions.get())
    calibration.insert(END, fullRot.get())
    calibration.insert(END, autoBG.get())
    calibration.insert(END, mX1)
    calibration.insert(END, mY1)
    calibration.insert(END, mX2)
    calibration.insert(END, mY2)
    calibration.insert(END, J8length)
    calibration.insert(END, J8rotation)
    calibration.insert(END, J8steps)
    calibration.insert(END, J9length)
    calibration.insert(END, J9rotation)
    calibration.insert(END, J9steps)
    calibration.insert(END, J7calOffEntryField.get())
    calibration.insert(END, J8calOffEntryField.get())
    calibration.insert(END, J9calOffEntryField.get())

    ###########
    value = calibration.get(0, END)
    pickle.dump(value, open("ARbot.cal", "wb"))


def checkSpeedVals():
    speedtype = speedOption.get()
    Speed = float(speedEntryField.get())
    if speedtype == "mm per Sec":
        if Speed <= 0.01:
            speedEntryField.delete(0, "end")
            speedEntryField.insert(0, "5")
    if speedtype == "Seconds":
        if Speed <= 0.001:
            speedEntryField.delete(0, "end")
            speedEntryField.insert(0, "1")
    if speedtype == "Percent":
        if Speed <= 0.01 or Speed > 100:
            speedEntryField.delete(0, "end")
            speedEntryField.insert(0, "10")
    ACCspd = float(ACCspeedField.get())
    if ACCspd <= 0.01 or ACCspd > 100:
        ACCspeedField.delete(0, "end")
        ACCspeedField.insert(0, "10")
    DECspd = float(DECspeedField.get())
    if DECspd <= 0.01 or DECspd >= 100:
        DECspeedField.delete(0, "end")
        DECspeedField.insert(0, "10")
    ACCramp = float(ACCrampField.get())
    if ACCramp <= 0.01 or ACCramp > 100:
        ACCrampField.delete(0, "end")
        ACCrampField.insert(0, "50")


def ErrorHandler(response):
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    cmdRecEntryField.delete(0, "end")
    cmdRecEntryField.insert(0, response)
    ##AXIS LIMIT ERROR
    if response[1:2] == "L":
        if response[2:3] == "1":
            message = "J1 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[3:4] == "1":
            message = "J2 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[4:5] == "1":
            message = "J3 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[5:6] == "1":
            message = "J4 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[6:7] == "1":
            message = "J5 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[7:8] == "1":
            message = "J6 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[8:9] == "1":
            message = "J7 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[9:10] == "1":
            message = "J8 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        if response[10:11] == "1":
            message = "J9 Axis Limit"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
        cmdRecEntryField.delete(0, "end")
        cmdRecEntryField.insert(0, response)
        message = "Axis Limit Error - See Log"
        almStatusLab.config(text=message, style="Alarm.TLabel")
        almStatusLab2.config(text=message, style="Alarm.TLabel")
        # stopProg()
    ##COLLISION ERROR
    elif response[1:2] == "C":
        if response[2:3] == "1":
            message = "J1 Collision or Motor Error"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
            correctPos()
            stopProg()
            message = "Collision or Motor Error - See Log"
            almStatusLab.config(text=message, style="Alarm.TLabel")
            almStatusLab2.config(text=message, style="Alarm.TLabel")
        if response[3:4] == "1":
            message = "J2 Collision or Motor Error"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
            correctPos()
            stopProg()
            message = "Collision or Motor Error - See Log"
            almStatusLab.config(text=message, style="Alarm.TLabel")
            almStatusLab2.config(text=message, style="Alarm.TLabel")
        if response[4:5] == "1":
            message = "J3 Collision or Motor Error"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
            correctPos()
            stopProg()
            message = "Collision or Motor Error - See Log"
            almStatusLab.config(text=message, style="Alarm.TLabel")
            almStatusLab2.config(text=message, style="Alarm.TLabel")
        if response[5:6] == "1":
            message = "J4 Collision or Motor Error"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
            correctPos()
            stopProg()
            message = "Collision or Motor Error - See Log"
            almStatusLab.config(text=message, style="Alarm.TLabel")
            almStatusLab2.config(text=message, style="Alarm.TLabel")
        if response[6:7] == "1":
            message = "J5 Collision or Motor Error"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
            correctPos()
            stopProg()
            message = "Collision or Motor Error - See Log"
            almStatusLab.config(text=message, style="Alarm.TLabel")
            almStatusLab2.config(text=message, style="Alarm.TLabel")
        if response[7:8] == "1":
            message = "J6 Collision or Motor Error"
            tab6.ElogView.insert(END, Curtime + " - " + message)
            value = tab6.ElogView.get(0, END)
            pickle.dump(value, open("ErrorLog", "wb"))
            correctPos()
            stopProg()
            message = "Collision or Motor Error - See Log"
            almStatusLab.config(text=message, style="Alarm.TLabel")
            almStatusLab2.config(text=message, style="Alarm.TLabel")

    ##REACH ERROR
    elif response[1:2] == "R":
        stopProg()
        message = "Position Out of Reach"
        tab6.ElogView.insert(END, Curtime + " - " + message)
        value = tab6.ElogView.get(0, END)
        pickle.dump(value, open("ErrorLog", "wb"))
        almStatusLab.config(text=message, style="Alarm.TLabel")
        almStatusLab2.config(text=message, style="Alarm.TLabel")

    elif response[1:2] == "S":
        stopProg()
        message = "Spline Can Only Have Move L Types"
        tab6.ElogView.insert(END, Curtime + " - " + message)
        value = tab6.ElogView.get(0, END)
        pickle.dump(value, open("ErrorLog", "wb"))
        almStatusLab.config(text=message, style="Alarm.TLabel")
        almStatusLab2.config(text=message, style="Alarm.TLabel")

    else:
        stopProg()
        message = "Unknown Error"
        tab6.ElogView.insert(END, Curtime + " - " + message)
        value = tab6.ElogView.get(0, END)
        pickle.dump(value, open("ErrorLog", "wb"))
        almStatusLab.config(text=message, style="Alarm.TLabel")
        almStatusLab2.config(text=message, style="Alarm.TLabel")


