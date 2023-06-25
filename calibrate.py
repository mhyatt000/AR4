import datetime
from pprint import pprint
from servo import Servo, DO
import pickle
from pprint import pprint
import tkinter as tk

from com import COM
from frames import AxisFrame  , ToolFrame # make so its the same pattern as joint
from gui.base import GUI, EntryField
from joint import JointCTRL


def stopProg():
    """see exc/execution.py 110"""
    pass


def log_message(msg):
    """docstring"""

    print(msg)
    now = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    GUI.tabs["6"].ElogView.insert(tk.END, f"{now} - {msg}")
    value = GUI.tabs["6"].ElogView.get(0, tk.END)
    pickle.dump(value, open("ErrorLog", "wb"))


def handle_response2(response, message):
    """another way to handle a response
    maybe try case switch with other file?
    """

    def _handle():
        """docstring"""
        pass

    if response[:1] == "A":
        display_position(response)
        msg = "Calibration Successful"
        style = "OK.TLabel"
    else:
        msg = "Calibration Failed"
        style = "Alarm.TLabel"

    COM.alarm(message)
    return msg


def cal(command, msg="", joint=None):
    """basic calibrate"""

    assert msg or joint
    msg = f"{joint.name}" if not msg else msg
    response = COM.serial_write(command)
    handle_response2(response, msg)
    log_message(msg)


def mk_suffix(mode="caloff"):
    """docstring"""

    # TODO make some kind of check to see if the command is valid
    # before sending to teensy

    if mode == "caloff":
        letters = ["J", "K", "L", "M", "N", "O", "P", "Q", "R"]
        caloffs = [J.no_calibrate.get() for J in JointCTRL.active]
        suffix = ''.join([f'{a}{b}' for a, b in zip(letters, caloffs)])
    return suffix


def calRobotAll():

    ##### STAGE 1 ########
    caloffs = [J.no_calibrate.get() for J in JointCTRL.main]
    calstat = caloffs

    command = f"LLA{caloffs[0]}B{caloffs[1]}C{caloffs[2]}D{caloffs[3]}E{caloffs[4]}F{caloffs[5]}G0H0I0{mk_suffix(mode='caloff')}\n"

    msg = "Stage 1 Auto"
    cal(command, msg)

    ##### STAGE 2 ########
    # NOTE maybe this is the other direction??
    caloffs = [J.no_calibrate2.get() for J in JointCTRL.main]
    calstat2 = caloffs
    if CalStatVal2 > 0:

        command = f"LLA{J1CalStatVal2}B{J2CalStatVal2}C{J3CalStatVal2}D{J4CalStatVal2}E{J5CalStatVal2}F{J6CalStatVal2}G0H0I0{mk_suffix(mode='caloff')}\n"

        msg = "Stage 1 Auto"
        cal(command, msg)


def calRobot(idx):
    """docstring"""

    print(idx)
    quit()

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
    cal(command, joint=JointCTRL.active[idx] )


def calRobotMid():
    print("foo")
    # add mid command


def correctPos():
    command = "CP\n"
    response = COM.serial_write(command)
    display_position(response)


def request_pos():
    command = "RP\n"
    response = COM.serial_write(command)
    display_position(response)


def tool_frame():
    """what does this do"""

    chars = ["A", "B", "C", "D", "E", "F"]
    TF = {k:v.entry.get() for k,v in ToolFrame.active.items()}

    command = "".join([f'{a}{b}' for a,b in zip(chars,TF.values())])
    command = f"TF{command}\n"
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
    value = GUI.tabs["6"].ElogView.get(0, tk.END)
    pickle.dump(value, open("ErrorLog", "wb"))
    response = str(ser.readline().strip(), "utf-8")
    display_position(response)


def zeroAxis7():
    command = "Z7" + "\n"
    zero("J7", command)


def zeroAxis8():
    command = "Z8" + "\n"
    zero("J8", command)


def zeroAxis9():
    command = "Z9" + "\n"
    zero("J9", command)


def send_pos():

    angles = [J.angle for J in JointCTRL.active]
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    command = "".join([f"{a}{b}" for a, b in zip(letters, angles)])
    command = f"SP{command}\n"
    response = COM.serial_write(command)


def CalZeroPos():
    command = "SPA0B0C0D0E0F0\n"
    response = COM.serial_write(command)
    request_pos()
    almStatusLab.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    message = "Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    log_message(message)


def CalRestPos():
    command = "SPA0B0C-89D0E0F0\n"
    response = COM.serial_write(command)
    request_pos()
    COM.alarm("Calibration Forced to Vertical Rest Pos")
    message = "Calibration Forced to Vertical - this is for commissioning and testing - be careful!"
    log_message(message)


def ResetDrives():
    command = "RD" + "\n"
    response = COM.serial_write(command)
    COM.alarm("DRIVES RESET - PLEASE CHECK CALIBRATION")
    request_pos()


def display_position(response):
    """displays positional into"""

    # TODO
    # cmdRecEntryField.delete(0, "end")
    # cmdRecEntryField.insert(0, response)

    responses = {
        "J1": "A",
        "J2": "B",
        "J3": "C",
        "J4": "D",
        "J5": "E",
        "J6": "F",
        #
        "x": "G",
        "y": "H",
        "z": "I",
        "rz": "J",
        "ry": "K",
        "rx": "L",
        #
        "speed_vio": "M",
        "debug": "N",
        "flag": "O",
        #
        "J7": "P",
        "J8": "Q",
        "J9": "R",
    }


    idxs = [response.find(v) for k, v in responses.items()]
    a = idxs.pop(0)
    for i, (k, v) in enumerate(responses.items()):
        # get next index or all the way to the end
        b = idxs.pop(0) if len(idxs) else 2 * len(responses.keys())
        responses[k] = response[a + 1 : b].strip()
        a = b

    Frames = [J.gui for J in JointCTRL.active]

    # NOTE J9 is '' because there is no 9th driver in the control box
    angles = [float(v if v != "" else 0.0) for k, v in responses.items() if "J" in k]
    for F, J, a in zip(Frames, JointCTRL.active, angles):
        J.angle = a

        F.label(a)
        F.slider.set(a)

    for k, A in AxisFrame.main.items():
        pos = responses[k]
        A.position = pos
        A.label(pos)

    # NOTE used in other files
    WC = "F" if float(JointCTRL.active[4].angle) > 0 else "N"

    # what is man ... what is debug
    speed_vio = responses["speed_vio"]
    debug = responses["debug"]
    flag = responses["flag"]

    EntryField.active["man"].label(debug)

    pprint(responses)

    save_pos_data()

    if flag != "":
        print(f'flag: {flag}')
        print(f'len flag: {len(flag)}')
        handle_error(flag)

    if speed_vio == "1":
        Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
        message = "Max Speed Violation - Reduce Speed Setpoint or Travel Distance"
        GUI.tabs["6"].ElogView.insert(tk.END, Curtime + " - " + message)
        value = GUI.tabs["6"].ElogView.get(0, tk.END)
        pickle.dump(value, open("ErrorLog", "wb"))
        COM.alarm(message)


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
    save_pos_data()


def save_pos_data():

    # i think angular current
    ang_cur = [None] * 6

    GUI.calibration.delete(0, tk.END)

    # TODO: clean
    # TODO finish now!
    toinsert = [
        *[J.angle for J in JointCTRL.main],
        *[A.position for A in AxisFrame.main.values()],
        #
        COM.teensy.entry.get(),
        EntryField.active["prog"].entry.get(),
        #
        Servo.active[0].on.entry.get(),
        Servo.active[0].off.entry.get(),
        Servo.active[1].on.entry.get(),
        Servo.active[1].off.entry.get(),
        #
        DO.active[0].on.entry.get(),
        DO.active[0].off.entry.get(),
        DO.active[1].on.entry.get(),
        DO.active[1].off.entry.get(),
        #
        *[x.entry.get() for x in ToolFrame.active.values()],
        *[J.gui.entry.get() for J in JointCTRL.external],
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
        GUI.full_rot.get(),
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

    # TODO why make variables to save in calibrate only to read them again?
    # is it because of pickle maybe?
    for item in toinsert:
        GUI.calibration.insert(tk.END, item)

    value = GUI.calibration.get(0, tk.END)
    # save to file for the next time it is opened
    pickle.dump(value, open("ErrorLog", "wb"))


class SpeedValidator:
    """used in check_speed"""

    default_values = {"mm per Sec": "5", "Seconds": "1", "Percent": "10"}

    def __init__(self, speed_option, entry):
        self.speed_option = speed_option
        # TODO this needs clean up
        self.entry = entry.entry

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
        self.entry = entry.entry

    def validate(self):
        value = float(self.entry.get())
        if value <= 0.01 or value > 100:
            self._reset_to_default()

    def _reset_to_default(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, self.default_value)


def check_speed():
    speed_validator = SpeedValidator(GUI.speed_option, EntryField.active["speed"])
    speed_validator.validate()

    ACCspd_validator = FieldValidator(EntryField.active["ACCspeed"])  # TODO rename
    ACCspd_validator.validate()

    DECspd_validator = FieldValidator(EntryField.active["DECspeed"])
    DECspd_validator.validate()

    ACCramp_validator = FieldValidator(EntryField.active["ACCramp"])
    ACCramp_validator.validate()


def handle_error(response):

    # TODO: are these 2 lines needed?
    # TODO yes ... but okay to remove for now.
    def record_response(response):
        EntryField.active["cmd_rec"].entry.delete(0, "end")
        EntryField.active["cmd_rec"].entry.insert(0, response)

    record_response(response)

    ##AXIS LIMIT ERROR
    if response[1:2] == "L":

        for i, j in enumerate(joints):
            if response[i + 2 : i + 3] == "1":
                log_message("{j.name} Axis Limit")

        message = "Axis Limit Error - See Log"
        COM.alarm(message)
        stopProg()

    ##COLLISION ERROR
    elif response[1:2] == "C":

        for i, J in enumerate(JointCTRL.main):
            if response[i + 2 : i + 3] == "1":
                log_message(f"{J.name} Collision or Motor Error")
                correctPos()
                stopProg()
                message = "Collision or Motor Error - See Log"
                COM.alarm(message)

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
