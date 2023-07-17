import datetime
import os.path as osp
import pickle
from pprint import pprint
import string
import tkinter as tk
import tkinter.ttk as ttk

from com import COM
from frames import AxisFrame  # make so its the same pattern as joint
from frames import ToolFrame
from gui.base import GUI, EntryField
from joint import JointCTRL
import load
from servo import DO, Servo
import util


class JointCal:
    """Joint Calibrator and GUI interface
    Located on Tab 2
    """

    active = []
    main = []
    external = []

    def __init__(self, parent):

        self.idx = len(JointCal.active)
        self.name = f"J{self.idx+1}"

        # can some of this be combined since it shares with JointJog
        self.frame = ttk.Frame(parent)
        self.frame.grid(row=self.idx, column=0, pady=10)

        self.vars = {
            "autocal": tk.IntVar(),
            "openloop": tk.IntVar(),
            "offset": tk.IntVar(),
        }

        self.mk_sf()
        self.mk_buttons()

        self.offset = EntryField(self.sf, name=f"{self.name} offset")
        self.offset.grid(row=0, column=2)

        JointCal.active.append(self)
        if self.idx < 6:
            JointCal.main.append(self)
        else:
            JointCal.external.append(self)

        util.vgrid(self.frame)

    def mk_sf(self):
        """makes subframe for spacing"""

        self.sf = ttk.Frame(self.frame)

    def mk_buttons(self):
        """docstring"""

        self.buttons = {
            "autocal": ttk.Checkbutton(self.sf, text=self.name, variable=self.vars["autocal"]),
            "cal": ttk.Button(
                self.sf, text=f"Calibrate {self.name} Only", command=lambda: cal_joint(self.idx)
            ),
            "open_loop": ttk.Checkbutton(
                self.sf, text=f"{self.name} Open Loop", variable=self.vars["openloop"]
            ),
        }

        for i, btn in zip([0, 1, 3], self.buttons.values()):
            btn.grid(row=0, column=i)


class ExtJointCal(JointCal):
    """External Joint Calibrator"""

    def __init__(self, parent):
        super(ExtJointCal, self).__init__(parent)

        self.mk_specs()
        self.mk_zero()
        util.vgrid(self.frame)

        self.extvars = {
            "length": tk.IntVar(),
            "rotation": tk.IntVar(),
            "steps": tk.IntVar(),
        }

    def mk_specs(self):
        """docstring"""

        self.mk_sf()
        self.fields = {
            "length": EntryField(self.sf, name=f"{self.name}_length", alt="Length"),
            "rotation": EntryField(self.sf, name="{self.name}_rot", alt="MM / Rotation"),
            "steps": EntryField(self.sf, name="{self.name}_steps", alt="Drive Steps"),
        }
        util.hgrid(self.sf)

    def mk_zero(self):
        """docstring"""

        self.mk_sf()
        self.zero = ttk.Button(self.sf, text=f"Set {self.name} to Zero", command=self.zero_joint)
        self.pins_label = ttk.Label(self.sf, text="TODO pins")
        util.hgrid(self.sf)

        """
        axis7pinsetLab = ttk.Label(
            left, font=("Arial", 8), text="StepPin = 12 / DirPin = 13 / CalPin = 36"
        )
        axis8pinsetLab = ttk.Label(
            left, font=("Arial", 8), text="StepPin = 32 / DirPin = 33 / CalPin = 37"
        )
        axis9pinsetLab = ttk.Label(
            left, font=("Arial", 8), text="StepPin = 34 / DirPin = 35 / CalPin = 38"
        )
        """

    def zero_joint(self):
        """docstring"""
        raise Exception


def cal(command, msg="", joint=None):
    """basic calibrate"""

    assert msg or joint
    msg = f"{joint.name}" if not msg else msg
    response = COM.write(command)
    msg = handle_response2(response, msg)
    log_message(msg)


def cal_joint(idx):
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
    suffix = mk_suffix(mode="calibration")
    command = commands[idx] + suffix
    cal(command, joint=JointCTRL.active[idx])


def mk_suffix(mode="calibration"):
    """docstring"""

    # TODO make some kind of check to see if the command is valid
    # before sending to teensy

    if mode == "calibration":
        letters = ["J", "K", "L", "M", "N", "O", "P", "Q", "R"]
        caloffs = [J.no_calibrate.get() for J in JointCTRL.active]
        suffix = "".join([f"{a}{b}" for a, b in zip(letters, caloffs)])
    return suffix


def stopProg():
    """see exc/execution.py 110"""
    pass


def log_message(msg):
    """docstring"""

    print("msg:", msg)
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


def cal_all():

    autocal = [J.vars["autocal"].get() for J in JointCal.active]
    offsets = [J.vars["offset"].get() for J in JointCal.active]

    prefix = "LL"
    chars = list(string.ascii_uppercase[:18])
    command = "".join([f"{a}{b}" for a, b in zip(chars, autocal + offsets)]) 
    command = prefix + command + '\n'

    msg = "Stage 1 Auto"
    cal(command, msg)


def calRobotMid():
    print("foo")
    # add mid command


def correctPos():
    command = "CP\n"
    response = COM.write(command)
    display_position(response)


def request_pos():
    command = "RP\n"
    response = COM.write(command)
    display_position(response)


def tool_frame():
    """what does this do"""

    chars = ["A", "B", "C", "D", "E", "F"]
    TF = {k: v.entry.get() for k, v in ToolFrame.active.items()}

    command = "".join([f"{a}{b}" for a, b in zip(chars, TF.values())])
    command = f"TF{command}\n"
    response = COM.write(command)


def calExtAxis():

    positions = [J.gui.entry.get() for J in JointCTRL.external]
    positions = [float(p) if p else 0.0 for p in positions]

    raise Exception("not implemented")

    # TODO
    rotations = None
    steps = None

    prefix = "CE"
    command = f"A{J7axisLimPos}B{J7rotation}C{J7steps}D{J8axisLimPos}E{J8rotation}F{J8steps}G{J9axisLimPos}H{J9rotation}I{J9steps}\n"
    response = COM.write(command)


def zero(joint, command):
    """basic zero axis"""

    response = COM.write(command)

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
    response = COM.write(command)


def CalZeroPos():
    command = "SPA0B0C0D0E0F0\n"
    response = COM.write(command)
    request_pos()
    almStatusLab.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    almStatusLab2.config(text="Calibration Forced to Zero", style="Warn.TLabel")
    message = "Calibration Forced to Zero - this is for commissioning and testing - be careful!"
    log_message(message)


def CalRestPos():
    command = "SPA0B0C-89D0E0F0\n"
    response = COM.write(command)
    request_pos()
    COM.alarm("Calibration Forced to Vertical Rest Pos")
    message = "Calibration Forced to Vertical - this is for commissioning and testing - be careful!"
    log_message(message)


def ResetDrives():
    command = "RD" + "\n"
    response = COM.write(command)
    COM.alarm("DRIVES RESET - PLEASE CHECK CALIBRATION")
    request_pos()


def display_position(response):
    """displays positional into"""

    if response in [None, ""]:
        return
    handle_error(response)

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
        "flag": "O", # this is the error message
        #
        "J7": "P",
        "J8": "Q",
        "J9": "R",
    }

    idxs = [response.find(v) for k, v in responses.items()]
    a = idxs.pop(0)
    for i, (k, v) in enumerate(responses.items()):
        # get next index or all the way to the end
        b = idxs.pop(0) if len(idxs) else int(1e3)
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
        A.position = float(responses[k])
        A.label(A.position)

    print('angles:',[int(J.angle) for J in JointCTRL.active])
    print('pos:', {k:int(A.position) for k,A in AxisFrame.main.items()})

    # NOTE used in other files
    WC = "F" if float(JointCTRL.active[4].angle) > 0 else "N"

    # what is man ... what is debug
    speed_vio = responses["speed_vio"]
    debug = responses["debug"]
    flag = responses["flag"]

    EntryField.active["man"].label(debug)

    # pprint(responses)

    load.save_cfg()

    if flag != "":
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
    VisProg = GUI.visoptions.get()

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
    load.save_cfg()


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

    if response[0] != 'E': # if not error
        return

    # TODO: are these 2 lines needed?
    # TODO yes ... but okay to remove for now.
    def record_response(response):
        EntryField.active["cmd_rec"].entry.delete(0, "end")
        EntryField.active["cmd_rec"].entry.insert(0, response)

    record_response(response)

    ##AXIS LIMIT ERROR
    if response[1:2] == "L":

        for i, J in enumerate(JointCTRL.main):
            if response[i + 2 : i + 3] == "1":
                log_message("{J.name} Axis Limit")

        message = "Axis Limit Error - See Log"
        COM.alarm(message)
        stopProg()

    ##COLLISION ERROR
    elif response[1:2] == "C":

        print(response)
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

    print()
