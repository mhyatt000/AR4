""" NOTE
dont use black yet... 
the command expands 20+ lines
"""

import pickle
from pprint import pprint
import tkinter as tk

from com import COM
from frames import (GUI, AxisFrame,  # make so its the same pattern as joint
                    EntryField)
from joint import JointCTRL


def log_message(msg):
    """docstring"""

    now = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(tk.END, f"{now} - {msg}")
    value = tab6.ElogView.get(0, tk.END)
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
    response = COM.serial_write(command)
    handle_response(response, msg)
    log_message(message)


def mk_suffix(mode="caloff"):
    """docstring"""

    if mode == "caloff":
        letters = ["J", "K", "L", "M", "N", "O", "P", "Q", "R"]
        caloff = None
        suffix = sum([sum(a, b) for a, b in zip(letters, caloff)])
    return suffix


def calRobotAll():

    ##### STAGE 1 ########
    joints = [None] * 6
    caloff = [x.caloff for x in joints]

    calstat = [x.calstat for x in joints]
    command = f"LLA{J1CalStatVal}B{J2CalStatVal}C{J3CalStatVal}D{J4CalStatVal}E{J5CalStatVal}F{J6CalStatVal}G0H0I0{mk_suffix(mode='caloff')}\n"

    msg = "Stage 1 Auto"
    cal(command, msg)

    ##### STAGE 2 ########
    calstat2 = [x.calstat2 for x in joints]
    if CalStatVal2 > 0:

        command = f"LLA{J1CalStatVal2}B{J2CalStatVal2}C{J3CalStatVal2}D{J4CalStatVal2}E{J5CalStatVal2}F{J6CalStatVal2}G0H0I0{mk_suffix(mode='caloff')}\n"

        msg = "Stage 1 Auto"
        cal(command, msg)


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
    suffix = mk_suffix(mode="caloff")
    command = commands[idx] + suffix
    cal(command, joint=idx + 1)


def calRobotMid():
    print("foo")
    # add mid command


def correctPos():
    command = "CP\n"
    response = COM.serial_write(command)
    displayPosition(response)


def requestPos():
    command = "RP\n"
    response = COM.serial_write(command)
    print("response")
    print(response)
    displayPosition(response)


def toolFrame(
    TFxEntryField,
    TFyEntryField,
    TFzEntryField,
    TFrzEntryField,
    TFryEntryField,
    TFrxEntryField,
):

    TFx = TFxEntryField.get()
    TFy = TFyEntryField.get()
    TFz = TFzEntryField.get()
    TFrz = TFrzEntryField.get()
    TFry = TFryEntryField.get()
    TFrx = TFrxEntryField.get()
    command = "TF" + "A" + TFx + "B" + TFy + "C" + TFz + "D" + TFrz + "E" + TFry + "F" + TFrx + "\n"
    response = COM.serial_write(command)


def calExtAxis():

    positions = [J.gui.entry.get() for J in JointCTRL.external]
    positions = [float(p) if p else 0.0 for p in positions]

    raise Exception("not implemented")

    # TODO
    rotations = None
    steps = None

    prefix = "CE"
    command = f"A{J7axisLimPos}B{J7rotation}C{J7steps}D{J8axisLimPos}E{J8rotation}F{J8steps}G{J9axisLimPos}H{J9rotation}I{J9steps}\n"
    response = COM.serial_write(command)


def zero(joint, command):
    """basic zero axis"""

    response = COM.serial_write(command)

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
    value = tab6.ElogView.get(0, tk.END)
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

    j = JointCTRL.main[0]

    print(j.__dict__)

    angles = [J.angle for J in JointCTRL.active]
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    command = "".join([f"{a}{b}" for a, b in zip(letters, angles)])
    command = f"SP{command}\n"
    response = COM.serial_write(command)


def CalZeroPos():
    command = "SPA0B0C0D0E0F0\n"
    response = COM.serial_write(command)
    requestPos()
    almStatusLab.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    message = "Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    log_message(message)


def CalRestPos():
    command = "SPA0B0C-89D0E0F0\n"
    response = COM.serial_write(command)
    requestPos()
    COM.alarm("Calibration Forced to Vertical Rest Pos")
    message = "Calibration Forced to Vertical - this is for commissioning and testing - be careful!"
    log_message(message)


def ResetDrives():
    command = "RD" + "\n"
    response = COM.serial_write(command)
    COM.alarm( "DRIVES RESET - PLEASE CHECK CALIBRATION")
    requestPos()


def displayPosition(response):

    # TODO
    # cmdRecEntryField.delete(0, "end")
    # cmdRecEntryField.insert(0, response)

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

    joint_idxs = [
        J1AngIndex,
        J2AngIndex,
        J3AngIndex,
        J4AngIndex,
        J5AngIndex,
        J6AngIndex,
    ]
    for J, idx in zip(JointCTRL.main,joint_idxs):
        raise Exception('TODO right now')


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

    # TODO
    # TODO abstract with display.py

    Frames = [J.gui for J in JointCTRL.main]

    join_angles = [
        J1AngCur,
        J2AngCur,
        J3AngCur,
        J4AngCur,
        J5AngCur,
        J6AngCur,
        J7PosCur,
        J8PosCur,
        J9PosCur,
    ]

    # current angle or current position

    for F, val in zip(Frames, join_angles):
        F.label(val)
        F.slider.set(val)

    axispos = {
        "x": None,
        "y": None,
        "z": None,
        #
        "rx": None,
        "ry": None,
        "rz": None,
    }

    for k, A in AxisFrame.active.items():
        A.label(axispos[k])

    print("calibrate.py")
    print(EntryField)
    EntryField.active["man"].label(Debug)  # what is man ... what is debug

    savePosData()

    if Flag != "":
        ErrorHandler(Flag)
    if SpeedVioation == "1":
        Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
        message = "Max Speed Violation - Reduce Speed Setpoint or Travel Distance"
        tab6.ElogView.insert(tk.END, Curtime + " - " + message)
        value = tab6.ElogView.get(0, tk.END)
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

    GUI.calibration.delete(0, tk.END)

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
        GUI.comPortEntryField.get(),
        EntryField.active["prog"].entry.get(),
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
        GUI.calibration.insert(tk.END, item)

    value = GUI.calibration.get(0, tk.END)
    pickle.dump(value, open("ARbot.cal", "wb"))


class SpeedValidator:
    """used in check_speed"""

    default_values = {"mm per Sec": "5", "Seconds": "1", "Percent": "10"}

    def __init__(self, speed_option,entry):
        self.speed_option = speed_option
        self.entry=entry

    def validate(self):
        speed_type = self.speed_option.get()
        speed = float(self.entry.get())

        if self._is_speed_invalid(speed_type, speed):
            self._reset_to_default(speed_type)

    def _is_speed_invalid(self, speed_type, speed):
        if speed_type == "Percent":
            return speed <= 0.01 or speed > 100
        return speed <= 0.01

    def _reset_to_default(self, speed_type):
        self.entry.delete(0, "end")
        self.entry.insert(0, self.default_values.get(speed_type, "10"))


class FieldValidator:
    """used in check_speed"""

    default_value = "10"

    def __init__(self, entry):
        self.entry = entry

    def validate(self):
        value = float(self.entry.get())
        if value <= 0.01 or value > 100:
            self._reset_to_default()

    def _reset_to_default(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, self.default_value)


def check_speeds():
    speed_validator = SpeedValidator(speedOption, speedEntryField)
    speed_validator.validate()

    ACCspd_validator = FieldValidator(ACCspeedField)
    ACCspd_validator.validate()

    DECspd_validator = FieldValidator(DECspeedField)
    DECspd_validator.validate()

    ACCramp_validator = FieldValidator(ACCrampField)
    ACCramp_validator.validate()


def ErrorHandler(response):
    # TODO: are these 2 lines needed?
    cmdRecEntryField.delete(0, "end")
    cmdRecEntryField.insert(0, response)

    ##AXIS LIMIT ERROR
    if response[1:2] == "L":

        for i, j in enumerate(joints):
            if response[i + 2 : i + 3] == "1":
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
            if response[i + 2 : i + 3] == "1":
                send_msg("{j.name} Collision or Motor Error")
                correctPos()
                stopProg()
                message = "Collision or Motor Error - See Log"
                almStatusLab.config(text=message, style="Alarm.TLabel")
                almStatusLab2.config(text=message, style="Alarm.TLabel")

    ##REACH ERROR
    else:
        if response[1:2] == "R":
            message = "Position Out of Reach"
        elif response[1:2] == "S":
            message = "Spline Can Only Have Move L Types"
        else:
            message = "Unknown Error"
        stopProg()
        log_message(message)
