import datetime
import math
from multiprocessing.resource_sharer import stop
import os
from os import execv
import os.path as osp
import pathlib
import pickle
import threading
import time
# from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import tkinter.messagebox
from tkinter.ttk import *
import webbrowser

from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
import numpy as np
from numpy import mean

from calibrate import *
import controller
from exc.execution import *
import frames
from frames import GUI, AxisFrame, EntryField, ExtJointFrame, JointFrame
from jog import *
from jog import jog_buttons, jog_cmd
from joint import JointCTRL
from program import *
from teach import *
from theme import *

# from pygrabber.dshow_graph import FilterGraph

ROOT = osp.dirname(__file__)
ASSETS = osp.join(ROOT, "assets")

cropping = False

root = tk.Tk()
root.wm_title("AR4 Software Ver 3.0")
root.iconbitmap(r"AR.ico")
# root.resizable(width=False, height=False)
root.geometry("1536x792+0+0")
root.runTrue = 0

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)


def on_closing():
    if messagebox.askokcancel("Close Program", "Do you want to quit?"):
        try:
            command = "CL"
            ser.write(command.encode())
        except:
            print("foo")
        ser.close()
        root.destroy()


# root.wm_protocol("WM_DELETE_WINDOW", on_closing)

JogStepsStat = tk.IntVar()
xboxUse = None

is_increment = tk.IntVar()
fullRot = tk.IntVar()
pick180 = tk.IntVar()
pickClosest = tk.IntVar()
autoBG = tk.IntVar()
SplineTrue = False

############################################################################
### DEFINE TABS ############################################################
############################################################################

nb = tkinter.ttk.Notebook(root, width=1536, height=792)
nb.grid(row=0, column=0, sticky="nsew")

tabs = {str(i): tkinter.ttk.Frame(nb) for i in range(1, 10 + 1)}
tabnames = [
    " Main Controls ",
    "  Config Settings  ",
    " Inputs Outputs ",
    "   Registers    ",
    "   Vision    ",
    "      Log      ",
    "   Info    ",
]
for tab, name in zip(tabs.values(), tabnames):
    nb.add(tab, text=name)

cam_on = False
cap = None

###############################################################################################################################################################
### STARTUP DEFS #################################################################################################################
###############################################################################################################################################################


### Tool Frame ###

TFxEntryField = Entry(tabs["2"], width=5)
TFxEntryField.place(x=910, y=115)
TFyEntryField = Entry(tabs["2"], width=5)
TFyEntryField.place(x=950, y=115)
TFzEntryField = Entry(tabs["2"], width=5)
TFzEntryField.place(x=990, y=115)
TFrzEntryField = Entry(tabs["2"], width=5)
TFrzEntryField.place(x=1030, y=115)
TFryEntryField = Entry(tabs["2"], width=5)
TFryEntryField.place(x=1070, y=115)
TFrxEntryField = Entry(tabs["2"], width=5)
TFrxEntryField.place(x=1110, y=115)


def startup():
    moveInProc = 0
    toolFrame(
        TFxEntryField,
        TFyEntryField,
        TFzEntryField,
        TFrzEntryField,
        TFryEntryField,
        TFrxEntryField,
    )
    # TODO later
    # calExtAxis()
    sendPos()
    requestPos()


### COMMUNICATION DEFS

print("initiate serial communitation")
com = COM(tabs, startup)


##### TAB 1 #####


##### LABELS #####

# TODO: seems like cartjog is the other important frame. maybe make a frame organizer somehow?

# left side
left = tk.Frame(tabs["1"])
left.grid(row=0, column=0, sticky="nsew")

# right side
right = tk.Frame(tabs["1"])
right.grid(row=0, column=1, sticky="nsew", padx=10)


CartjogFrame = Frame(tabs["1"])
CartjogFrame.place(x=330, y=0)


curRowLab = Label(left, text="Current Row:")
curRowLab.grid(row=0, column=0)

almStatusLab = Label(left, text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel")
almStatusLab.grid(row=1, column=0)
COM.register_alm(almStatusLab)

xbcStatusLab = Label(left, text="Xbox OFF")
xbcStatusLab.grid(row=2, column=0)

runStatusLab = Label(left, text="PROGRAM STOPPED")
runStatusLab.grid(row=3, column=0)


ProgLab = Label(left, text="Program:")
ProgLab.grid(row=4, column=0)

joint_frames = [
    JointFrame(right, x=0, y=0),
    JointFrame(right, x=0, y=1),
    JointFrame(right, x=0, y=2),
    JointFrame(right, x=1, y=0),
    JointFrame(right, x=1, y=1),
    JointFrame(right, x=1, y=2),
    #
    ExtJointFrame(right, x=2, y=0),
    ExtJointFrame(right, x=2, y=1),
    ExtJointFrame(right, x=2, y=2),
]

# or call it ax_frames
axes = tk.Frame(right, width=450)
axes.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=20)

AxisFrame(axes, 0, 0, "x")
AxisFrame(axes, 0, 1, "y")
AxisFrame(axes, 0, 2, "z")
AxisFrame(axes, 0, 3, "rz")
AxisFrame(axes, 0, 4, "ry")
AxisFrame(axes, 0, 5, "rx")
#
AxisFrame(axes, 1, 0, "tx")
AxisFrame(axes, 1, 1, "ty")
AxisFrame(axes, 1, 2, "tz")
AxisFrame(axes, 1, 3, "trz")
AxisFrame(axes, 1, 4, "try")
AxisFrame(axes, 1, 5, "trx")


####ENTRY FIELDS##########################################################
##########################################################################

# TODO: how to clean this up?

fields = tk.Frame(left)
fields.grid(row=11, column=0)

EntryField(fields, name="increment")
EntryField(fields, name="curRow")
EntryField(fields, name="man")
EntryField(fields, name="prog")
EntryField(fields, name="speed")
EntryField(fields, name="ACCspeed", alt='Acceleration (%)')
EntryField(fields, name="DECspeed", alt='Decceleration (%)')
EntryField(fields, name="ACCramp", alt='Acceleration Ramp (%)')
EntryField(fields, name="round", alt='Rounding (mm)')
EntryField(fields, name="savepos")

###BUTTONS################################################################
##########################################################################


def posRegFieldVisible(self):
    curCmdtype = options.get()
    if curCmdtype == "Move PR" or curCmdtype == "OFF PR " or curCmdtype == "Teach PR":
        SavePosEntryField.place(x=780, y=183)
    else:
        SavePosEntryField.place_forget()


subframes = dict()
subframes["btn"] = tk.Frame(right, width=500)
subframes["btn"].grid(row=4, column=0, columnspan=3, sticky="nsew", pady=20)

manInsBut = Button(subframes["btn"], text="  Insert  ", command=manInsItem)
manRepBut = Button(subframes["btn"], text="Replace", command=manReplItem)
getSelBut = Button(subframes["btn"], text="Get Selected", command=getSel)
speedOption = tk.StringVar(subframes["btn"])
speedMenu = OptionMenu(subframes["btn"], speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
teachInsBut = Button(
    subframes["btn"], text="Teach New Position",  command=teachInsertBelSelected
)
teachReplaceBut = Button(
    subframes["btn"], text="Modify Position",  command=teachReplaceSelected
)
deleteBut = Button(subframes["btn"], text="Delete",  command=deleteitem)
CalibrateBut = Button(subframes["btn"], text="Auto Calibrate CMD",  command=insCalibrate)
camOnBut = Button(subframes["btn"], text="Camera On",  command=cameraOn)
camOffBut = Button(subframes["btn"], text="Camera Off",  command=cameraOff)

# single buttons

options = tk.StringVar(left)
menu = OptionMenu(
    subframes["btn"],
    options,
    "Move J",
    "Move J",
    "OFF J",
    "Move L",
    "Move R",
    "Move A Mid",
    "Move A End",
    "Move C Center",
    "Move C Start",
    "Move C Plane",
    "Start Spline",
    "End Spline",
    "Move PR",
    "OFF PR ",
    "Teach PR",
    "Move Vis",
    command=posRegFieldVisible,
)
# menu.grid(row=1, column=3)
menu.config()

waitTimeBut = Button(subframes["btn"], text="Wait Time (seconds)",  command=waitTime)
waitInputOnBut = Button(subframes["btn"], text="Wait Input ON",  command=waitInputOn)
waitInputOffBut = Button(subframes["btn"], text="Wait Input OFF",  command=waitInputOff)
setOutputOnBut = Button(subframes["btn"], text="Set Output On",  command=setOutputOn)
setOutputOffBut = Button(subframes["btn"], text="Set Output OFF",  command=setOutputOff)
tabNumBut = Button(subframes["btn"], text="Create Tab",  command=tabNumber)
jumpTabBut = Button(subframes["btn"], text="Jump to Tab",  command=jumpTab)

subframes["fields"] = fields

EntryField(subframes["fields"], name="waitTime")
EntryField(subframes["fields"], name="waitInput")
EntryField(subframes["fields"], name="waitInputOff")
EntryField(subframes["fields"], name="outputOn")
EntryField(subframes["fields"], name="outputOff")
EntryField(subframes["fields"], name="tabNum")
EntryField(subframes["fields"], name="jumpTab")

# buttons with multiple entry

IfOnjumpTabBut = Button(subframes['btn'], text="If On Jump",  command=IfOnjumpTab)
IfOffjumpTabBut = Button(subframes['btn'], text="If Off Jump",  command=IfOffjumpTab)
servoBut = Button(subframes['btn'], text="Servo",  command=Servo)
RegNumBut = Button(subframes['btn'], text="Register",  command=insertRegister)
RegJmpBut = Button(subframes['btn'], text="If Register Jump",  command=IfRegjumpTab)
StorPosBut = Button(subframes['btn'], text="Position Register",  command=storPos)
callBut = Button(subframes['btn'], text="Call Program",  command=insertCallProg)
returnBut = Button(subframes['btn'], text="Return",  command=insertReturn)
visFindBut = Button(subframes['btn'], text="Vision Find",  command=insertvisFind)

EntryField(subframes['fields'],  name='IfOnjumpInputTab')
EntryField(subframes['fields'],  name='IfOnjumpNumberTab')
EntryField(subframes['fields'],  name='IfOffjumpInputTab')
EntryField(subframes['fields'],  name='IfOffjumpNumberTab')
EntryField(subframes['fields'],  name='servoNum')
EntryField(subframes['fields'],  name='servoPos')
EntryField(subframes['fields'],  name='regNum')
EntryField(subframes['fields'],  name='regEq')
EntryField(subframes['fields'],  name='regNumJmp')
EntryField(subframes['fields'],  name='regEqJmp')
EntryField(subframes['fields'],  name='regTabJmp')
EntryField(subframes['fields'],  name='storPosNum')
EntryField(subframes['fields'],  name='storPosEl')
EntryField(subframes['fields'],  name='storPosVal')
EntryField(subframes['fields'],  name='changeProg')
EntryField(subframes['fields'],  name='visPass')
EntryField(subframes['fields'],  name='visFail')

ProgBut = Button(subframes['btn'], text="Load Program", command=loadProg)
revBut = Button(subframes['btn'], text="REV ", command=stepRev)
fwdBut = Button(subframes['btn'], text="FWD", command=stepFwd)
ResetDriveBut = Button(subframes["btn"], text="Reset Drives", command=ResetDrives)
IncJogCbut = Checkbutton(subframes['btn'], text="Incremental Jog", variable=is_increment)
GUI.register('is_increment',IncJogCbut)

runProgBut = Button(subframes['btn'], command=runProg)
playPhoto = tk.PhotoImage(file=osp.join(ASSETS, "play-icon.gif"))
runProgBut.config(image=playPhoto)

xboxBut = Button(subframes['btn'], command=controller.xbox)
xboxPhoto = tk.PhotoImage(file=osp.join(ASSETS, "xbox.gif"))
xboxBut.config(image=xboxPhoto)

stopProgBut = Button(subframes['btn'], command=stopProg)
stopPhoto = tk.PhotoImage(file=osp.join(ASSETS, "stop-icon.gif"))
stopProgBut.config(image=stopPhoto)


frames.assign_grid(subframes["btn"], 5, 5)
frames.assign_grid(subframes["fields"], 2, 2)


jog_buttons.main(tabs["1"])
tabs["1"].mainloop()


"""
---------- ---------- ----------
TAB 2
---------- ---------- ----------
"""


### 2 LABELS#################################################################
#############################################################################

ComPortLab = Label(tabs["2"], text="TEENSY COM PORT:")
ComPortLab.place(x=66, y=90)

ComPortLab = Label(tabs["2"], text="IO BOARD COM PORT:")
ComPortLab.place(x=60, y=160)

almStatusLab2 = Label(tabs["2"], text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel")
almStatusLab2.place(x=25, y=20)
com.register_alm(almStatusLab)


ToolFrameLab = Label(tabs["2"], text="Tool Frame Offset")
ToolFrameLab.place(x=970, y=60)

UFxLab = Label(tabs["2"], font=("Arial", 11), text="X")
UFxLab.place(x=920, y=90)

UFyLab = Label(tabs["2"], font=("Arial", 11), text="Y")
UFyLab.place(x=960, y=90)

UFzLab = Label(tabs["2"], font=("Arial", 11), text="Z")
UFzLab.place(x=1000, y=90)

UFRxLab = Label(tabs["2"], font=("Arial", 11), text="Rz")
UFRxLab.place(x=1040, y=90)

UFRyLab = Label(tabs["2"], font=("Arial", 11), text="Ry")
UFRyLab.place(x=1080, y=90)

UFRzLab = Label(tabs["2"], font=("Arial", 11), text="Rx")
UFRzLab.place(x=1120, y=90)

comLab = Label(tabs["2"], text="Communication")
comLab.place(x=72, y=60)

jointCalLab = Label(tabs["2"], text="Robot Calibration")
jointCalLab.place(x=290, y=60)

axis7Lab = Label(tabs["2"], text="7th Axis Calibration")
axis7Lab.place(x=665, y=300)

axis7lengthLab = Label(tabs["2"], text="7th Axis Length:")
axis7lengthLab.place(x=651, y=340)

axis7rotLab = Label(tabs["2"], text="MM per Rotation:")
axis7rotLab.place(x=645, y=370)

axis7stepsLab = Label(tabs["2"], text="Drive Steps:")
axis7stepsLab.place(x=675, y=400)

axis7pinsetLab = Label(
    tabs["2"], font=("Arial", 8), text="StepPin = 12 / DirPin = 13 / CalPin = 36"
)
axis7pinsetLab.place(x=627, y=510)

axis8pinsetLab = Label(
    tabs["2"], font=("Arial", 8), text="StepPin = 32 / DirPin = 33 / CalPin = 37"
)
axis8pinsetLab.place(x=827, y=510)

axis9pinsetLab = Label(
    tabs["2"], font=("Arial", 8), text="StepPin = 34 / DirPin = 35 / CalPin = 38"
)
axis9pinsetLab.place(x=1027, y=510)


axis8Lab = Label(tabs["2"], text="8th Axis Calibration")
axis8Lab.place(x=865, y=300)

axis8lengthLab = Label(tabs["2"], text="8th Axis Length:")
axis8lengthLab.place(x=851, y=340)

axis8rotLab = Label(tabs["2"], text="MM per Rotation:")
axis8rotLab.place(x=845, y=370)

axis8stepsLab = Label(tabs["2"], text="Drive Steps:")
axis8stepsLab.place(x=875, y=400)


axis9Lab = Label(tabs["2"], text="9th Axis Calibration")
axis9Lab.place(x=1065, y=300)

axis9lengthLab = Label(tabs["2"], text="9th Axis Length:")
axis9lengthLab.place(x=1051, y=340)

axis9rotLab = Label(tabs["2"], text="MM per Rotation:")
axis9rotLab.place(x=1045, y=370)

axis9stepsLab = Label(tabs["2"], text="Drive Steps:")
axis9stepsLab.place(x=1075, y=400)


CalibrationOffsetsLab = Label(tabs["2"], text="Calibration Offsets")
CalibrationOffsetsLab.place(x=485, y=60)

J1calLab = Label(tabs["2"], text="J1 Offset")
J1calLab.place(x=480, y=90)

J2calLab = Label(tabs["2"], text="J2 Offset")
J2calLab.place(x=480, y=120)

J3calLab = Label(tabs["2"], text="J3 Offset")
J3calLab.place(x=480, y=150)

J4calLab = Label(tabs["2"], text="J4 Offset")
J4calLab.place(x=480, y=180)

J5calLab = Label(tabs["2"], text="J5 Offset")
J5calLab.place(x=480, y=210)

J6calLab = Label(tabs["2"], text="J6 Offset")
J6calLab.place(x=480, y=240)

J7calLab = Label(tabs["2"], text="J7 Offset")
J7calLab.place(x=480, y=280)

J8calLab = Label(tabs["2"], text="J8 Offset")
J8calLab.place(x=480, y=310)

J9calLab = Label(tabs["2"], text="J9 Offset")
J9calLab.place(x=480, y=340)


CalibrationOffsetsLab = Label(tabs["2"], text="Encoder Control")
CalibrationOffsetsLab.place(x=715, y=60)

cmdSentLab = Label(tabs["2"], text="Last Command Sent to Controller")
cmdSentLab.place(x=10, y=565)

cmdRecLab = Label(tabs["2"], text="Last Response From Controller")
cmdRecLab.place(x=10, y=625)

ToolFrameLab = Label(tabs["2"], text="Theme")
ToolFrameLab.place(x=1225, y=60)


### 2 BUTTONS################################################################
#############################################################################

comPortBut = Button(tabs["2"], text="  Set Com Teensy  ", command=com.set)
comPortBut.place(x=85, y=110)

comPortBut2 = Button(tabs["2"], text="Set Com IO Board", command=com.set)
comPortBut2.place(x=85, y=180)


lightBut = Button(tabs["2"], text="  Light  ", command=lightTheme)
lightBut.place(x=1190, y=90)

darkBut = Button(tabs["2"], text="  Dark   ", command=darkTheme)
darkBut.place(x=1250, y=90)


autoCalBut = Button(tabs["2"], text="  Auto Calibrate  ", command=calRobotAll)
autoCalBut.place(x=285, y=90)

# NOTE: what makes these calibration check buttons different from other
# calibration buttons?  needs to be more specific.
cal_pos = {
    "J1": (dict(x=285, y=125), dict(x=285, y=180)),
    "J2": (dict(x=320, y=125), dict(x=320, y=180)),
    "J3": (dict(x=355, y=125), dict(x=355, y=180)),
    "J4": (dict(x=285, y=145), dict(x=285, y=200)),
    "J5": (dict(x=320, y=145), dict(x=320, y=200)),
    "J6": (dict(x=355, y=145), dict(x=355, y=200)),
}

cal_btns = {}
for J in JointCTRL.main:
    btns = [
        Checkbutton(tabs["2"], text=J.name, variable=J.cal_stat[0]),
        Checkbutton(tabs["2"], text=J.name, variable=J.cal_stat[1]),
    ]
    btns[0].place(**cal_pos[J.name][0])
    btns[1].place(**cal_pos[J.name][1])
    cal_btns[J.name] = btns

J7zerobut = Button(tabs["2"], text="Set Axis 7 Calibration to Zero", width=28, command=zeroAxis7)
J7zerobut.place(x=627, y=440)

J8zerobut = Button(tabs["2"], text="Set Axis 8 Calibration to Zero", width=28, command=zeroAxis8)
J8zerobut.place(x=827, y=440)

J9zerobut = Button(tabs["2"], text="Set Axis 9 Calibration to Zero", width=28, command=zeroAxis9)
J9zerobut.place(x=1027, y=440)


autocal_pos = {
    "J1": dict(x=285, y=240),
    "J2": dict(x=285, y=270),
    "J3": dict(x=285, y=300),
    "J4": dict(x=285, y=330),
    "J5": dict(x=285, y=360),
    "J6": dict(x=285, y=390),
    "J7": dict(x=627, y=475),
    "J8": dict(x=827, y=475),
    "J9": dict(x=1027, y=475),
}
autocal_btns = {}
for J in JointCTRL.active:
    btn = Button(tabs["2"], text=f"Calibrate {J.name} Only", command=lambda: calRobot(J.idx))
    btn.place(**autocal_pos[J.name])
    autocal_btns[J.name] = btn


CalZeroBut = Button(tabs["2"], text="Force Cal. to 0° Home", width=20, command=CalZeroPos)
CalZeroBut.place(x=270, y=425)

CalRestBut = Button(tabs["2"], text="Force Cal. to Vert. Rest", width=20, command=CalRestPos)
CalRestBut.place(x=270, y=460)


mk_autocal = lambda J: dict(x=665, y=90 + 20 * J.idx, text="{J.name} Open Loop (disable encoder)")
autocal_pos = [mk_autocal(J) for J in JointCTRL.main]
for J, item in zip(JointCTRL.main, autocal_pos):
    btn = Checkbutton(tabs["2"], text=item["text"], variable=J.open_loop)
    btn.place(x=item["x"], y=item["y"])


saveCalBut = Button(tabs["2"], text="    SAVE    ", width=26, command=SaveAndApplyCalibration)
saveCalBut.place(x=1150, y=630)

#### 2 ENTRY FIELDS##########################################################
#############################################################################

comPortEntryField = Entry(tabs["2"], width=4)
comPortEntryField.place(x=50, y=114)
GUI.register("comPortEntryField", comPortEntryField)

com2PortEntryField = Entry(tabs["2"], width=4)
com2PortEntryField.place(x=50, y=184)
GUI.register("com2PortEntryField", com2PortEntryField)

cmdSentEntryField = Entry(tabs["2"], width=95)
cmdSentEntryField.place(x=10, y=585)

cmdRecEntryField = Entry(tabs["2"], width=95)
cmdRecEntryField.place(x=10, y=645)

caloff_entry_pos = [dict(x=540, y=90 + 30 * J.idx) for J in JointCTRL.active]
for J in JointCTRL.active:
    x, y = caloff_entry_pos[J.idx].values()
    J.caloff_entry = Entry(tabs["2"], width=8)
    J.caloff_entry.place(x=x, y=y)


# NOTE this was axis7lengthEntryField
mk_entry = lambda: Entry(tabs["2"], width=6)
external_fields = [
    {
        "length": mk_entry(),
        "rotation": mk_entry(),
        "steps": mk_entry(),
    }
    for J in JointCTRL.external
]

for i, (J, fields) in enumerate(zip(JointCTRL.external, external_fields)):
    J.gui.fields = fields
    fields = list(fields.values())
    for j, f in enumerate(fields):
        f.place(x=750 + 200 * i, y=340 + 30 * j)

# tab 3,4

import gui

gui.main(tabs)

####TAB 5 ###############################################################################

### 5 LABELS#################################################################


def mk_img(path):
    """docstring"""
    return ImageTk.PhotoImage(Image.open(osp.join("assets", path)))


VisBackdropImg = mk_img("VisBackdrop.png")
VisBackdromLbl = Label(tabs["5"], image=VisBackdropImg)
VisBackdromLbl.place(x=15, y=215)


# cap= cv2.VideoCapture(0)
video_frame = Frame(tabs["5"], width=640, height=480)
video_frame.place(x=50, y=250)


vid_lbl = Label(video_frame)
vid_lbl.place(x=0, y=0)

from vision import *

vid_lbl.bind("<Button-1>", motion)


LiveLab = Label(tabs["5"], text="LIVE VIDEO FEED")
LiveLab.place(x=750, y=390)
liveCanvas = Canvas(tabs["5"], width=490, height=330)
liveCanvas.place(x=750, y=410)
live_frame = Frame(tabs["5"], width=480, height=320)
live_frame.place(x=757, y=417)
live_lbl = Label(live_frame)
live_lbl.place(x=0, y=0)


template_frame = Frame(tabs["5"], width=150, height=150)
template_frame.place(x=575, y=50)

template_lbl = Label(template_frame)
template_lbl.place(x=0, y=0)

FoundValuesLab = Label(tabs["5"], text="FOUND VALUES")
FoundValuesLab.place(x=750, y=30)

CalValuesLab = Label(tabs["5"], text="CALIBRATION VALUES")
CalValuesLab.place(x=900, y=30)


VisFileLocLab = Label(tabs["5"], text="Vision File Location:")
VisCalPixLab = Label(tabs["5"], text="Calibration Pixels:")
VisCalmmLab = Label(tabs["5"], text="Calibration Robot MM:")
VisCalOxLab = Label(tabs["5"], text="Orig: X")
VisCalOyLab = Label(tabs["5"], text="Orig: Y")
VisCalXLab = Label(tabs["5"], text="End: X")
VisCalYLab = Label(tabs["5"], text="End: Y")

texts = [
    "Choose Vision Format",
    "X found position (mm)",
    "Y found position (mm)",
    "R found position (ang)",
    "X pixes returned from camera",
    "Y pixes returned from camera",
]
labels = [Label(tabs["5"], text=t) for t in texts]

VisInTypeLab, VisXfoundLab, VisYfoundLab, VisRZfoundLab, VisXpixfoundLab, VisYpixfoundLab = labels

# TODO: finish abstracting labels above

### 5 BUTTONS################################################################
#############################################################################

try:
    graph = FilterGraph()
    camList = graph.get_input_devices()
except:
    camList = ["Select a Camera"]
visoptions = tk.StringVar(tabs["5"])
visoptions.set("Select a Camera")
vismenu = OptionMenu(tabs["5"], visoptions, camList[0], *camList)
vismenu.config(width=20)
vismenu.place(x=10, y=10)


StartCamBut = Button(tabs["5"], text="Start Camera", width=15, command=start_vid)
StartCamBut.place(x=200, y=10)

StopCamBut = Button(tabs["5"], text="Stop Camera", width=15, command=stop_vid)
StopCamBut.place(x=315, y=10)

CapImgBut = Button(tabs["5"], text="Snap Image", width=15, command=take_pic)
CapImgBut.place(x=10, y=50)

TeachImgBut = Button(tabs["5"], text="Teach Object", width=15, command=selectTemplate)
TeachImgBut.place(x=140, y=50)

FindVisBut = Button(tabs["5"], text="Snap & Find", width=15, command=snapFind)
FindVisBut.place(x=270, y=50)


ZeroBrCnBut = Button(tabs["5"], text="Zero", width=5, command=zeroBrCn)
ZeroBrCnBut.place(x=10, y=110)

maskBut = Button(tabs["5"], text="Mask", width=5, command=selectMask)
maskBut.place(x=10, y=150)


VisZoomSlide = Scale(tabs["5"], from_=50, to=1, length=250, orient=tk.HORIZONTAL)
VisZoomSlide.bind("<ButtonRelease-1>", VisUpdateBriCon)
VisZoomSlide.place(x=75, y=95)
VisZoomSlide.set(50)

VisZoomLab = Label(tabs["5"], text="Zoom")
VisZoomLab.place(x=75, y=115)

VisBrightSlide = Scale(tabs["5"], from_=-127, to=127, length=250, orient=tk.HORIZONTAL)
VisBrightSlide.bind("<ButtonRelease-1>", VisUpdateBriCon)
VisBrightSlide.place(x=75, y=130)

VisBrightLab = Label(tabs["5"], text="Brightness")
VisBrightLab.place(x=75, y=150)

VisContrastSlide = Scale(tabs["5"], from_=-127, to=127, length=250, orient=tk.HORIZONTAL)
VisContrastSlide.bind("<ButtonRelease-1>", VisUpdateBriCon)
VisContrastSlide.place(x=75, y=165)

VisContrastLab = Label(tabs["5"], text="Contrast")
VisContrastLab.place(x=75, y=185)


fullRotCbut = Checkbutton(tabs["5"], text="Full Rotation Search", variable=fullRot)
fullRotCbut.place(x=900, y=255)

pick180Cbut = Checkbutton(tabs["5"], text="Pick Closest 180°", variable=pick180)
pick180Cbut.place(x=900, y=275)

pickClosestCbut = Checkbutton(tabs["5"], text="Try Closest When Out of Range", variable=pickClosest)
pickClosestCbut.place(x=900, y=295)


saveCalBut = Button(tabs["5"], text="SAVE VISION DATA", width=26, command=SaveAndApplyCalibration)
saveCalBut.place(x=915, y=340)


#### 5 ENTRY FIELDS##########################################################
#############################################################################


def make_entry_field(tab, text, x, y):
    """makes a new entry field"""

    field = Entry(tab, width=15)
    field.place(x=x, y=y)
    label = Label(tab, text=text)
    label.place(x=x, y=y + 20)
    return field, label


bgAutoCbut = Checkbutton(tabs["5"], command=checkAutoBG, text="Auto", variable=autoBG)
bgAutoCbut.place(x=490, y=101)

a, b = make_entry_field(tabs["5"], "Background Color", 390, 100)
VisBacColorEntryField, VisBacColorLab = a, b


a, b = make_entry_field(tabs["5"], "Score Threshold", 390, 150)
VisScoreEntryField, VisScoreLab = a, b

# TODO: finish abstracting

VisRetScoreEntryField = Entry(tabs["5"], width=15)
VisRetScoreEntryField.place(x=750, y=55)
VisRetScoreLab = Label(tabs["5"], text="Scored Value")
VisRetScoreLab.place(x=750, y=75)

VisRetAngleEntryField = Entry(tabs["5"], width=15)
VisRetAngleEntryField.place(x=750, y=105)
VisRetAngleLab = Label(tabs["5"], text="Found Angle")
VisRetAngleLab.place(x=750, y=125)

VisRetXpixEntryField = Entry(tabs["5"], width=15)
VisRetXpixEntryField.place(x=750, y=155)
VisRetXpixLab = Label(tabs["5"], text="Pixel X Position")
VisRetXpixLab.place(x=750, y=175)

VisRetYpixEntryField = Entry(tabs["5"], width=15)
VisRetYpixEntryField.place(x=750, y=205)
VisRetYpixLab = Label(tabs["5"], text="Pixel Y Position")
VisRetYpixLab.place(x=750, y=225)

VisRetXrobEntryField = Entry(tabs["5"], width=15)
VisRetXrobEntryField.place(x=750, y=255)
VisRetXrobLab = Label(tabs["5"], text="Robot X Position")
VisRetXrobLab.place(x=750, y=275)

VisRetYrobEntryField = Entry(tabs["5"], width=15)
VisRetYrobEntryField.place(x=750, y=305)
VisRetYrobLab = Label(tabs["5"], text="Robot Y Position")
VisRetYrobLab.place(x=750, y=325)


VisX1PixEntryField = Entry(tabs["5"], width=15)
VisX1PixEntryField.place(x=900, y=55)
VisX1PixLab = Label(tabs["5"], text="X1 Pixel Pos")
VisX1PixLab.place(x=900, y=75)

VisY1PixEntryField = Entry(tabs["5"], width=15)
VisY1PixEntryField.place(x=900, y=105)
VisY1PixLab = Label(tabs["5"], text="Y1 Pixel Pos")
VisY1PixLab.place(x=900, y=125)

VisX2PixEntryField = Entry(tabs["5"], width=15)
VisX2PixEntryField.place(x=900, y=155)
VisX2PixLab = Label(tabs["5"], text="X2 Pixel Pos")
VisX2PixLab.place(x=900, y=175)

VisY2PixEntryField = Entry(tabs["5"], width=15)
VisY2PixEntryField.place(x=900, y=205)
VisY2PixLab = Label(tabs["5"], text="Y2 Pixel Pos")
VisY2PixLab.place(x=900, y=225)


VisX1RobEntryField = Entry(tabs["5"], width=15)
VisX1RobEntryField.place(x=1010, y=55)
VisX1RobLab = Label(tabs["5"], text="X1 Robot Pos")
VisX1RobLab.place(x=1010, y=75)

VisY1RobEntryField = Entry(tabs["5"], width=15)
VisY1RobEntryField.place(x=1010, y=105)
VisY1RobLab = Label(tabs["5"], text="Y1 Robot Pos")
VisY1RobLab.place(x=1010, y=125)

VisX2RobEntryField = Entry(tabs["5"], width=15)
VisX2RobEntryField.place(x=1010, y=155)
VisX2RobLab = Label(tabs["5"], text="X2 Robot Pos")
VisX2RobLab.place(x=1010, y=175)

VisY2RobEntryField = Entry(tabs["5"], width=15)
VisY2RobEntryField.place(x=1010, y=205)
VisY2RobLab = Label(tabs["5"], text="Y2 Robot Pos")
VisY2RobLab.place(x=1010, y=225)


VisFileLocEntryField = Entry(tabs["5"], width=70)

VisPicOxPEntryField = Entry(tabs["5"], width=5)
VisPicOxMEntryField = Entry(tabs["5"], width=5)
VisPicOyPEntryField = Entry(tabs["5"], width=5)
VisPicOyMEntryField = Entry(tabs["5"], width=5)
VisPicXPEntryField = Entry(tabs["5"], width=5)
VisPicXMEntryField = Entry(tabs["5"], width=5)
VisPicYPEntryField = Entry(tabs["5"], width=5)
VisPicYMEntryField = Entry(tabs["5"], width=5)
VisXfindEntryField = Entry(tabs["5"], width=5)
VisYfindEntryField = Entry(tabs["5"], width=5)
VisRZfindEntryField = Entry(tabs["5"], width=5)
VisXpixfindEntryField = Entry(tabs["5"], width=5)
VisYpixfindEntryField = Entry(tabs["5"], width=5)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 6

Elogframe = Frame(tabs["6"])
Elogframe.place(x=40, y=15)
scrollbar = Scrollbar(Elogframe)
scrollbar.pack(side=RIGHT, fill=Y)
tabs["6"].ElogView = Listbox(Elogframe, width=150, height=40, yscrollcommand=scrollbar.set)
try:
    Elog = pickle.load(open("ErrorLog", "rb"))
except:
    Elog = ["##BEGINNING OF LOG##"]
    pickle.dump(Elog, open("ErrorLog", "wb"))
time.sleep(0.2)
for item in Elog:
    tabs["6"].ElogView.insert(tk.END, item)
tabs["6"].ElogView.pack()
scrollbar.config(command=tabs["6"].ElogView.yview)


def clearLog():
    tabs["6"].ElogView.delete(1, tk.END)
    value = tabs["6"].ElogView.get(0, tk.END)
    pickle.dump(value, open("ErrorLog", "wb"))


clearLogBut = Button(tabs["6"], text="Clear Log", width=26, command=clearLog)
clearLogBut.place(x=1000, y=630)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 7

link = Label(tabs["7"], font="12", text="https://www.anninrobotics.com/tutorials", cursor="hand2")
link.bind("<Button-1>", lambda event: webbrowser.open(link.cget("text")))
link.place(x=10, y=9)


def callback():
    webbrowser.open_new(r"https://www.paypal.me/ChrisAnnin")


donateBut = Button(tabs["7"], command=callback)
donatePhoto = tk.PhotoImage(file=osp.join("assets", "pp.gif"))
donateBut.config(image=donatePhoto)
donateBut.place(x=1250, y=2)


scroll = Scrollbar(tabs["7"])
scroll.pack(side=RIGHT, fill=Y)
configfile = Text(tabs["7"], wrap=WORD, width=166, height=40, yscrollcommand=scroll.set)
filename = osp.join("assets", "information.txt")
with open(filename, "r", encoding="utf-8-sig") as file:
    configfile.insert(INSERT, file.read())
configfile.pack(side="left")
scroll.config(command=configfile.yview)
configfile.place(x=10, y=40)


####TAB 10

### 10 LABELS#################################################################

testSendLab = Label(tabs["10"], text="Test string to send to arduino")
testSendLab.place(x=10, y=20)

testRecLab = Label(tabs["10"], text="Message echoed back from arduino")
testRecLab.place(x=10, y=70)

### 10 BUTTONS################################################################

testSendBut = Button(tabs["10"], text="SEND TO ARDUINO", command=TestString)
testSendBut.place(x=10, y=120)

testClearBut = Button(tabs["10"], text="CLEAR RECEIVED", command=ClearTestString)
testClearBut.place(x=180, y=120)

#### 10 ENTRY FIELDS##########################################################

testSendEntryField = Entry(tabs["10"], width=222)
testSendEntryField.place(x=10, y=40)

testRecEntryField = Entry(tabs["10"], width=222)
testRecEntryField.place(x=10, y=90)

##############################################################################################################################################################
### OPEN CAL FILE AND LOAD LIST ##############################################################################################################################
##############################################################################################################################################################

calibration = Listbox(tabs["2"], height=60)
GUI.register("calibration", calibration)

try:
    Cal = pickle.load(open("ARbot.cal", "rb"))
except:
    Cal = "0"
    pickle.dump(Cal, open("ARbot.cal", "wb"))
for item in Cal:
    calibration.insert(tk.END, item)
global mX1
global mY1
global mX2
global mY2

J1AngCur = calibration.get("0")
J2AngCur = calibration.get("1")
J3AngCur = calibration.get("2")
J4AngCur = calibration.get("3")
J5AngCur = calibration.get("4")
J6AngCur = calibration.get("5")

XcurPos = calibration.get("6")
YcurPos = calibration.get("7")
ZcurPos = calibration.get("8")

RxcurPos = calibration.get("9")
RycurPos = calibration.get("10")
RzcurPos = calibration.get("11")

comPort = calibration.get("12")
Prog = calibration.get("13")
Servo0on = calibration.get("14")
Servo0off = calibration.get("15")
Servo1on = calibration.get("16")
Servo1off = calibration.get("17")
DO1on = calibration.get("18")
DO1off = calibration.get("19")
DO2on = calibration.get("20")
DO2off = calibration.get("21")
TFx = calibration.get("22")
TFy = calibration.get("23")
TFz = calibration.get("24")
TFrx = calibration.get("25")
TFry = calibration.get("26")
TFrz = calibration.get("27")

J7PosCur = calibration.get("28")
J8PosCur = calibration.get("29")
J9PosCur = calibration.get("30")

VisFileLoc = calibration.get("31")
VisProg = calibration.get("32")
VisOrigXpix = calibration.get("33")
VisOrigXmm = calibration.get("34")
VisOrigYpix = calibration.get("35")
VisOrigYmm = calibration.get("36")
VisEndXpix = calibration.get("37")
VisEndXmm = calibration.get("38")
VisEndYpix = calibration.get("39")
VisEndYmm = calibration.get("40")
J1calOff = calibration.get("41")
J2calOff = calibration.get("42")
J3calOff = calibration.get("43")
J4calOff = calibration.get("44")
J5calOff = calibration.get("45")
J6calOff = calibration.get("46")
J1OpenLoopVal = calibration.get("47")
J2OpenLoopVal = calibration.get("48")
J3OpenLoopVal = calibration.get("49")
J4OpenLoopVal = calibration.get("50")
J5OpenLoopVal = calibration.get("51")
J6OpenLoopVal = calibration.get("52")
com2Port = calibration.get("53")
theme = calibration.get("54")
J1CalStatVal = calibration.get("55")
J2CalStatVal = calibration.get("56")
J3CalStatVal = calibration.get("57")
J4CalStatVal = calibration.get("58")
J5CalStatVal = calibration.get("59")
J6CalStatVal = calibration.get("60")

J1CalStatVal2 = calibration.get("65")
J2CalStatVal2 = calibration.get("66")
J3CalStatVal2 = calibration.get("67")
J4CalStatVal2 = calibration.get("68")
J5CalStatVal2 = calibration.get("69")
J6CalStatVal2 = calibration.get("70")
VisBrightVal = calibration.get("71")
VisContVal = calibration.get("72")
VisBacColor = calibration.get("73")
VisScore = calibration.get("74")
VisX1Val = calibration.get("75")
VisY1Val = calibration.get("76")
VisX2Val = calibration.get("77")
VisY2Val = calibration.get("78")
VisRobX1Val = calibration.get("79")
VisRobY1Val = calibration.get("80")
VisRobX2Val = calibration.get("81")
VisRobY2Val = calibration.get("82")
zoom = calibration.get("83")
pick180Val = calibration.get("84")
pickClosestVal = calibration.get("85")
curCam = calibration.get("86")
fullRotVal = calibration.get("87")
autoBGVal = calibration.get("88")
mX1val = calibration.get("89")
mY1val = calibration.get("90")
mX2val = calibration.get("91")
mY2val = calibration.get("92")


J7StepCur = calibration.get("64")  # is this used ??? keep for now


J7calOff = calibration.get("99")
J8calOff = calibration.get("100")
J9calOff = calibration.get("101")


####

comPortEntryField.insert(0, str(comPort))
com2PortEntryField.insert(0, str(com2Port))

EntryField.active["increment"].label("10")
EntryField.active["speed"].label("25")
EntryField.active["ACCspeed"].label("10")
EntryField.active["DECspeed"].label("10")
EntryField.active["ACCramp"].label("100")
EntryField.active["round"].label("0")
EntryField.active["prog"].label((Prog))
EntryField.active["savepos"].label("1")

TFxEntryField.insert(0, str(TFx))
TFyEntryField.insert(0, str(TFy))
TFzEntryField.insert(0, str(TFz))
TFrxEntryField.insert(0, str(TFrx))
TFryEntryField.insert(0, str(TFry))
TFrzEntryField.insert(0, str(TFrz))


extpos = [J7PosCur, J7PosCur, J7PosCur]
for J, pos in zip(JointCTRL.external, extpos):
    J.gui.entry.insert(0, str(pos))

VisFileLocEntryField.insert(0, str(VisFileLoc))


# visoptions.set(VisProg)

VisPicOxPEntryField.insert(0, str(VisOrigXpix))
VisPicOxMEntryField.insert(0, str(VisOrigXmm))
VisPicOyPEntryField.insert(0, str(VisOrigYpix))
VisPicOyMEntryField.insert(0, str(VisOrigYmm))
VisPicXPEntryField.insert(0, str(VisEndXpix))
VisPicXMEntryField.insert(0, str(VisEndXmm))
VisPicYPEntryField.insert(0, str(VisEndYpix))
VisPicYMEntryField.insert(0, str(VisEndYmm))

caloffs = [
    J1calOff,
    J2calOff,
    J3calOff,
    J4calOff,
    J5calOff,
    J6calOff,
    J7calOff,
    J8calOff,
    J9calOff,
]

for J, caloff in zip(JointCTRL.main, caloffs):
    J.caloff_entry.insert(0, str(caloff))

if J1OpenLoopVal == 1:
    J1OpenLoopStat.set(True)
if J2OpenLoopVal == 1:
    J2OpenLoopStat.set(True)
if J3OpenLoopVal == 1:
    J3OpenLoopStat.set(True)
if J4OpenLoopVal == 1:
    J4OpenLoopStat.set(True)
if J5OpenLoopVal == 1:
    J5OpenLoopStat.set(True)
if J6OpenLoopVal == 1:
    J6OpenLoopStat.set(True)

if theme == 1:
    lightTheme(root)
else:
    darkTheme(root)

if J1CalStatVal == 1:
    J1CalStat.set(True)
if J2CalStatVal == 1:
    J2CalStat.set(True)
if J3CalStatVal == 1:
    J3CalStat.set(True)
if J4CalStatVal == 1:
    J4CalStat.set(True)
if J5CalStatVal == 1:
    J5CalStat.set(True)
if J6CalStatVal == 1:
    J6CalStat.set(True)
if J1CalStatVal2 == 1:
    J1CalStat2.set(True)
if J2CalStatVal2 == 1:
    J2CalStat2.set(True)
if J3CalStatVal2 == 1:
    J3CalStat2.set(True)
if J4CalStatVal2 == 1:
    J4CalStat2.set(True)
if J5CalStatVal2 == 1:
    J5CalStat2.set(True)
if J6CalStatVal2 == 1:
    J6CalStat2.set(True)

limpos = [None] * 3
# TODO

J7length = calibration.get("61")
J7rotation = calibration.get("62")
J7steps = calibration.get("63")
J8length = calibration.get("93")
J8rotation = calibration.get("94")
J8steps = calibration.get("95")
J9length = calibration.get("96")
J9rotation = calibration.get("97")
J9steps = calibration.get("98")

labels = [
    {
        "length": J7length,
        "rotation": J7rotation,
        "steps": J7steps,
    },
    {
        "length": J8length,
        "rotation": J8rotation,
        "steps": J8steps,
    },
    {
        "length": J9length,
        "rotation": J9rotation,
        "steps": J9steps,
    },
]


for i, J in enumerate(JointCTRL.external):
    _labels = labels[i]
    for key, field in J.gui.fields.items():
        field.insert(0, _labels[key])

# TODO
# VisBrightSlide.set(VisBrightVal)
# VisContrastSlide.set(VisContVal)
VisBacColorEntryField.insert(0, str(VisBacColor))
VisScoreEntryField.insert(0, str(VisScore))
VisX1PixEntryField.insert(0, str(VisX1Val))
VisY1PixEntryField.insert(0, str(VisY1Val))
VisX2PixEntryField.insert(0, str(VisX2Val))
VisY2PixEntryField.insert(0, str(VisY2Val))
VisX1RobEntryField.insert(0, str(VisRobX1Val))
VisY1RobEntryField.insert(0, str(VisRobY1Val))
VisX2RobEntryField.insert(0, str(VisRobX2Val))
VisY2RobEntryField.insert(0, str(VisRobY2Val))
# TODO
# VisZoomSlide.set(zoom)

if pickClosestVal == 1:
    pickClosest.set(True)
if pick180Val == 1:
    pick180.set(True)
visoptions.set(curCam)
if fullRotVal == 1:
    fullRot.set(True)
if autoBGVal == 1:
    autoBG.set(True)
mX1 = mX1val
mY1 = mY1val
mX2 = mX2val
mY2 = mY2val

com.set()

# TODO i think this was in the way of other buttons
# loadProg(tabs)

updateVisOp(tabs)
checkAutoBG(autoBG, VisBacColorEntryField)  # TODO what is autoBG

msg = """
AR3 and AR4 are registered trademarks of Annin Robotics
Copyright © 2022 by Annin Robotics. All Rights Reserved
"""
# you can add back later
# tkinter.messagebox.showwarning("AR4 License / Copyright notice", msg)
xboxUse = 0


tabs["1"].mainloop()


# manEntryField.delete(0, 'end')
# manEntryField.insert(0,value)


def main():
    """docstring"""


if __name__ == "__main__":
    main()
