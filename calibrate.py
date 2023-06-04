""" NOTE
dont use black yet... 
the command expands 20+ lines
"""


def log_message(msg):
    """docstring"""

    now = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, f"{now} - {msg}")
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))


def handle_response2(response, msg):
    """another way to handle a response
    maybe try case switch with other file?
    """

    def _handle():
        """docstring"""
        pass

    if response[:1] == "A":
        displayPosition(response)
        msg = "Calibration Successful"
        style = "OK.TLabel"
    else:
        msg = "Calibration Failed"
        style = "Alarm.TLabel"

    almStatusLab.config(text=msg, style=style)
    almStatusLab2.config(text=msg, style=style)
    return msg


def cal(command, msg="", joint=None):
    """basic calibrate"""

    assert msg or joint
    msg = f"{joint.name}" if not msg else msg
    response = serial_write(ser,command)
    handle_response(response, msg)
    log_message(message)



def mk_suffix(mode='caloff'):
    """docstring"""

    if mode == 'caloff':
        letters = ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
        caloff = None
        suffix = sum([sum(a,b) for a,b in zip(letters,caloff)])
    return suffix

def calRobotAll():

    ##### STAGE 1 ########
    joints = [None] * 6
    caloff = [x.caloff for x in joints]

    calstat = [x.calstat for x in joints]
    command = f"LLA{J1CalStatVal}B{J2CalStatVal}C{J3CalStatVal}D{J4CalStatVal}E{J5CalStatVal}F{J6CalStatVal}G0H0I0{mk_suffix(mode='caloff')}\n"

    msg = "Stage 1 Auto"
    cal(command,msg)

    ##### STAGE 2 ########
    calstat2 = [x.calstat2 for x in joints]
    if CalStatVal2 > 0:

        command = f"LLA{J1CalStatVal2}B{J2CalStatVal2}C{J3CalStatVal2}D{J4CalStatVal2}E{J5CalStatVal2}F{J6CalStatVal2}G0H0I0{mk_suffix(mode='caloff')}\n"

        msg = "Stage 1 Auto"
        cal(command,msg)

        


def calRobot(idx):
    """docstring"""

    assert idx in list(range(9))
    commands = [
        f"LLA1B0C0D0E0F0G0H0I0",
        f"LLA0B1C0D0E0F0G0H0I0",
        f"LLA0B0C1D0E0F0G0H0I0",
        f"LLA0B0C0D1E0F0G0H0I0",
        f"LLA0B0C0D0E1F0G0H0I0",
        f"LLA0B0C0D0E0F1G0H0I0",
        f"LLA0B0C0D0E0F0G1H0I0",
        f"LLA0B0C0D0E0F0G0H1I0",
        f"LLA0B0C0D0E0F0G0H0I1",
    ]
    suffix = mk_suffix(mode='caloff')
    command = commands[idx] + suffix
    cal(command, joint=idx+1)


def calRobotMid():
    print("foo")
    # add mid command


def correctPos():
    command = "CP\n"
    response = serial_write(ser,command)
    displayPosition(response)


def requestPos():
    command = "RP\n"
    response = serial_write(ser,command)
    displayPosition(response)


def toolFrame():
    TFx = TFxEntryField.get()
    TFy = TFyEntryField.get()
    TFz = TFzEntryField.get()
    TFrz = TFrzEntryField.get()
    TFry = TFryEntryField.get()
    TFrx = TFrxEntryField.get()
    command = "TF" + "A" + TFx + "B" + TFy + "C" + TFz + "D" + TFrz + "E" + TFry + "F" + TFrx + "\n"
    response = serial_write(ser,command)


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

    command = f"CEA{J7axisLimPos}B{J7rotation}C{J7steps}D{J8axisLimPos}E{J8rotation}F{J8steps}G{J9axisLimPos}H{J9rotation}I{J9steps}\n"
    response = serial_write(ser,command)

def zero(joint, command):
    """basic zero axis"""

    response = serial_write(ser,command)

    # TODO: can you handle_response?
    text = f"{joint} Calibration Forced to Zero"
    style = "Warn.TLabel"
    almStatusLab.config(text=text, style=style)
    almStatusLab2.config(text=text, style=style)

    message = (
        f"{joint} Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    )

    log_message(message)

    # TODO: feel like this should have been above
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))
    response = str(ser.readline().strip(), "utf-8")
    displayPosition(response)


def zeroAxis7():
    command = "Z7" + "\n"
    zero("J7", command)


def zeroAxis8():
    command = "Z8" + "\n"
    zero("J8", command)


def zeroAxis9():
    command = "Z9" + "\n"
    zero("J9", command)


def sendPos():
    angcur = [j.ang_cur for j in joints]
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    command = sum([sum((a,b)) for a,b in zip(letters,angcur)])
    command = f"SP{command}\n"
    response = serial_write(ser,command)


def CalZeroPos():
    command = "SPA0B0C0D0E0F0\n"
    response = serial_write(ser,command)
    requestPos()
    almStatusLab.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    message = "Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    log_message(message)

def CalRestPos():
    command = "SPA0B0C-89D0E0F0\n"
    response = serial_write(ser,command)
    requestPos()
    almStatusLab.config(text="Calibration Forced to Vertical Rest Pos", style="Warn.TLabel")
    almStatusLab2.config(text="Calibration Forced to Vertical Rest Pos", style="Warn.TLabel")
    message = "Calibration Forced to Vertical - this is for commissioning and testing - be careful!"
    log_message(message)


def ResetDrives():
    ResetDriveBut = Button(tab1, text="Reset Drives", command=ResetDrives)
    ResetDriveBut.place(x=307, y=42)
    command = "RD" + "\n"
    response = serial_write(ser,command)
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

    WC = "F" if float(J5AngCur) > 0 else "N"

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

    # i think angular current
    ang_cur = [None] * 6

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

    # TODO: clean
    toinsert = [
        J1AngCur,
        J2AngCur,
        J3AngCur,
        J4AngCur,
        J5AngCur,
        J6AngCur,
        XcurPos,
        YcurPos,
        ZcurPos,
        RzcurPos,
        RycurPos,
        RxcurPos,
        #
        comPortEntryField.get(),
        ProgEntryField.get(),
        servo0onEntryField.get(),
        servo0offEntryField.get(),
        servo1onEntryField.get(),
        servo1offEntryField.get(),
        DO1onEntryField.get(),
        DO1offEntryField.get(),
        DO2onEntryField.get(),
        DO2offEntryField.get(),
        #
        TFxEntryField.get(),
        TFyEntryField.get(),
        TFzEntryField.get(),
        TFrxEntryField.get(),
        TFryEntryField.get(),
        TFrzEntryField.get(),
        #
        J7curAngEntryField.get(),
        J8curAngEntryField.get(),
        J9curAngEntryField.get(),
        VisFileLocEntryField.get(),
        visoptions.get(),
        #
        VisPicOxPEntryField.get(),
        VisPicOxMEntryField.get(),
        VisPicOyPEntryField.get(),
        VisPicOyMEntryField.get(),
        VisPicXPEntryField.get(),
        VisPicXMEntryField.get(),
        VisPicYPEntryField.get(),
        VisPicYMEntryField.get(),
        #
        J1calOffEntryField.get(),
        J2calOffEntryField.get(),
        J3calOffEntryField.get(),
        J4calOffEntryField.get(),
        J5calOffEntryField.get(),
        J6calOffEntryField.get(),
        #
        J1OpenLoopVal,
        J2OpenLoopVal,
        J3OpenLoopVal,
        J4OpenLoopVal,
        J5OpenLoopVal,
        J6OpenLoopVal,
        #
        com2PortEntryField.get(),
        theme,
        #
        J1CalStatVal,
        J2CalStatVal,
        J3CalStatVal,
        J4CalStatVal,
        J5CalStatVal,
        J6CalStatVal,
        J7axisLimPos,
        J7rotation,
        J7steps,
        J7StepCur,
        J1CalStatVal2,
        J2CalStatVal2,
        J3CalStatVal2,
        J4CalStatVal2,
        J5CalStatVal2,
        J6CalStatVal2,
        #
        VisBrightSlide.get(),
        VisContrastSlide.get(),
        VisBacColorEntryField.get(),
        VisScoreEntryField.get(),
        VisX1PixEntryField.get(),
        VisY1PixEntryField.get(),
        VisX2PixEntryField.get(),
        VisY2PixEntryField.get(),
        VisX1RobEntryField.get(),
        VisY1RobEntryField.get(),
        VisX2RobEntryField.get(),
        VisY2RobEntryField.get(),
        #
        VisZoomSlide.get(),
        pick180.get(),
        pickClosest.get(),
        visoptions.get(),
        fullRot.get(),
        autoBG.get(),
        mX1,
        mY1,
        mX2,
        mY2,
        J8length,
        J8rotation,
        J8steps,
        J9length,
        J9rotation,
        J9steps,
        J7calOffEntryField.get(),
        J8calOffEntryField.get(),
        J9calOffEntryField.get(),
    ]

    for item in toinsert:
        calibration.insert(END, item)

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
    # TODO: are these 2 lines needed?
    cmdRecEntryField.delete(0, "end")
    cmdRecEntryField.insert(0, response)

    ##AXIS LIMIT ERROR
    if response[1:2] == "L":

        for i, j in enumerate(joints):
            if response[i+2:i+3] == '1':
                send_msg("{j.name} Axis Limit")

        cmdRecEntryField.delete(0, "end")
        cmdRecEntryField.insert(0, response)
        message = "Axis Limit Error - See Log"
        almStatusLab.config(text=message, style="Alarm.TLabel")
        almStatusLab2.config(text=message, style="Alarm.TLabel")
        # stopProg() # NOTE: creator commented out

    ##COLLISION ERROR
    elif response[1:2] == "C":

        for i, j in enumerate(joints[:6]):
            if response[i+2:i+3] == '1':
                send_msg("{j.name} Collision or Motor Error")
                correctPos()
                stopProg()
                message = "Collision or Motor Error - See Log"
                almStatusLab.config(text=message, style="Alarm.TLabel")
                almStatusLab2.config(text=message, style="Alarm.TLabel")

    ##REACH ERROR
    else :
        if response[1:2] == "R":
            message = "Position Out of Reach"
        elif response[1:2] == "S":
            message = "Spline Can Only Have Move L Types"
        else:
            message = "Unknown Error"
        stopProg()
        log_message(message)
