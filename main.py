import datetime
import math
from multiprocessing.resource_sharer import stop
import os
from os import execv
import pathlib
import pickle
import threading
import time
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import tkinter.messagebox
from tkinter.ttk import *
import webbrowser

from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
import numpy as np
from numpy import mean
import serial
from ttkthemes import ThemedStyle

from program import *
from teach import *
from exc.execution import *


# from pygrabber.dshow_graph import FilterGraph

DIR = pathlib.Path(__file__).parent.resolve()

cropping = False

root = Tk()
root.wm_title("AR4 Software Ver 3.0")
root.iconbitmap(r"AR.ico")
root.resizable(width=False, height=False)
root.geometry("1536x792+0+0")
root.runTrue = 0


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

JogStepsStat = IntVar()
xboxUse = None

IncJogStat = IntVar()
fullRot = IntVar()
pick180 = IntVar()
pickClosest = IntVar()
autoBG = IntVar()
SplineTrue = False

############################################################################
### DEFINE TABS ############################################################
############################################################################

nb = tkinter.ttk.Notebook(root, width=1536, height=792)
nb.place(x=0, y=0)

tabs = {str(i):tkinter.ttk.Frame(nb) for i in range(1,7+1)}
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
### STARTUP DEFS ################################################################################################################# COMMUNICATION DEFS ###
###############################################################################################################################################################


def startup():
    moveInProc = 0
    toolFrame()
    calExtAxis()
    sendPos()
    requestPos()


###############################################################################################################################################################
### COMMUNICATION DEFS ################################################################################################################# COMMUNICATION DEFS ###
###############################################################################################################################################################

serials = [None, None]


def setCom():

    now = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    boards = ["TEENSY 4.1 CONTROLLER", "ARDUINO IO BOARD"]

    def set_status(text, style):
        almStatusLab.config(text=text, style=style)
        almStatusLab2.config(text=text, style=style)

    try:
        # port = "COM" + comPortEntryField.get()
        # baud = 9600

        ser2 = None
        if ser2:
            pass
        """ 
        port = "COM" + com2PortEntryField.get()
        baud = 115200
        ser 2 = serial.Serial(port, baud)
        """

        # TODO: mhyatt temp
        port = "/dev/cu.usbmodem123843001"
        serials[0] = serial.Serial(port, baud)

        text = f"COMMUNICATIONS STARTED WITH {board}"
        style = "OK.TLabel"

        set_status(text, style)
        tab6.ElogView.insert(END, f"{now} - {text}")
        value = tab6.ElogView.get(0, END)
        pickle.dump(value, open("ErrorLog", "wb"))

        time.sleep(1)
        ser.flushInput()
        startup()

    except Exception as ex:

        text = (f"UNABLE TO ESTABLISH COMMUNICATIONS WITH {board}",)
        style = ("Alarm.TLabel",)

        set_status(text, style)
        tab6.ElogView.insert(END, f"{now} - {text}")
        value = tab6.ElogView.get(0, END)
        pickle.dump(value, open("ErrorLog", "wb"))


##### TAB 1 #####


##### LABELS #####

# TODO: seems like cartjog is the other important frame. maybe make a frame organizer somehow?

CartjogFrame = Frame(
    tabs['1'],
    width=1536,
    height=792,
)
CartjogFrame.place(x=330, y=0)

curRowLab = Label(tabs['1'], text="Current Row:")
curRowLab.place(x=98, y=120)


almStatusLab = Label(tabs['1'], text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel")
almStatusLab.place(x=25, y=12)

xbcStatusLab = Label(tabs['1'], text="Xbox OFF")
xbcStatusLab.place(x=1270, y=80)

runStatusLab = Label(tabs['1'], text="PROGRAM STOPPED")
runStatusLab.place(x=20, y=150)


ProgLab = Label(tabs['1'], text="Program:")
ProgLab.place(x=10, y=45)

jogIncrementLab = Label(tabs['1'], text="Increment Value:")
# jogIncrementLab.place(x=370, y=45)

speedLab = Label(tabs['1'], text="Speed")
speedLab.place(x=300, y=83)

ACCLab = Label(tabs['1'], text="Acceleration               %")
ACCLab.place(x=300, y=103)

DECLab = Label(tabs['1'], text="Deceleration               %")
DECLab.place(x=300, y=123)

DECLab = Label(tabs['1'], text="Ramp                           %")
DECLab.place(x=300, y=143)

RoundLab = Label(tabs['1'], text="Rounding               mm")
RoundLab.place(x=525, y=82)


font = ("Arial", 18)
mk_cj_label = lambda text: Label(CartjogFrame, font=font, text=text)
places = {
    "X": dict(x=660, y=162),
    "Y": dict(x=750, y=162),
    "Z": dict(x=840, y=162),
    "Rz": dict(x=930, y=162),
    "Ry": dict(x=1020, y=162),
    "Rx": dict(x=1110, y=162),
    "Tx": dict(x=660, y=265),
    "Ty": dict(x=750, y=265),
    "Tz": dict(x=840, y=265),
    "Trz": dict(x=930, y=265),
    "Try": dict(x=1020, y=265),
    "Trx": dict(x=1110, y=265),
}

# cart jog labels
cj_labels = {x: mk_cj_label(x) for x in places.keys()}
for k,v in cj_labels.items():
    v.place(**places[k])


### JOINT CONTROL ################################################################

class JointCTR:
    """A robotic joint controller"""

    active = []

    # pos, neg
    limits = [
        [170, 170],
        [90, 42],
        [52, 89],
        [165, 165],
        [105, 105],
        [155, 155],
        [340, 0],
        [340, 0],
        [340, 0],
    ]

    def __init__(self):

        JointCTR.active.append(self)

        self.idx = len(JointCTR.active)
        self.name = "J{self.idx}"

        # int
        self.open_loop_stat = None
        self.cal_stat = [None, None]

        self.limits = JointCTR.limits[self.idx]
        self.range = sum(self.limits)
        self.limits = {'pos':self.limits[0], 'neg':self.limits[1]}


# TODO: remove since it was for testing
# joints = [Joint() for _ in range(6)]


class JointFrame:
    """a GUI frame for a joint"""

    active = []

    def __init__(self, x,y):

        self.ctr = JointCTR()

        self.frame = Frame(tabs['1'], width=340, height=40)
        self.frame.place(x=x, y=y)

        self.entry = Entry(self.frame, width=5)
        self.entry.place(x=35, y=9)

        self.locations = [
                (5,5),
                (115,25),
                (270,25),
                (190,25),
        ]
        self.mk_labels()
        self.mk_buttons()
        self.mk_slider(115,7,180)
        JointFrame.active.append(self)

    def mk_buttons(self):
        """makes jogging buttons"""

        button = lambda text: Button(self.frame, text=text, width=3)
        self.buttons = {
            "neg": button("-"),
            "pos": button("+"),
        }
        for x, (k, button) in zip([77, 300], self.buttons.items()):
            pass  # TODO: selJ1jogneg is a function
            button.bind("<ButtonRelease>", self.stop_jog)
            button.place(x=x, y=7, width=30, height=25)

        self.buttons['neg'].bind("<ButtonPress>", self.SeljogNeg)
        self.buttons['pos'].bind("<ButtonPress>", self.SeljogPos)


    def mk_labels(self):
        """docstring"""

        self.labels = {
            'main':Label(self.frame, font=("Arial", 18), text=self.ctr.name),
            "neg_lim": Label(
                self.frame, font=("Arial", 8), text=str(-self.ctr.limits['neg']), style="Jointlim.TLabel"
            ),
            "pos_lim": Label(
                self.frame, font=("Arial", 8), text=str(self.ctr.limits['pos']), style="Jointlim.TLabel"
            ),
            "slide": Label(self.frame),
        }

        for i, (k, label) in enumerate(self.labels.items()):
            loc = {a:b for a,b in zip(['x','y'],self.locations[i])}
            label.place(**loc)



    def mk_slider(self,x,y,length):
        """makes slider"""

        self.slider = Scale(
            self.frame,
            from_=-self.ctr.limits['neg'],
            to=self.ctr.limits['pos'],
            length=length,
            orient=HORIZONTAL,
            command=self.sliderUpdate,
        )
        self.slider.bind("<ButtonRelease-1>", self.sliderExecute)
        self.slider.place(x=x, y=y)

    def stop_jog(self):
        """docstring"""
        pass

    def jog(self):
        """replacement for sel jog"""
        # TODO
        pass

    def SeljogNeg(self):
        """docstring"""
        """
            J1 10,11 pos,neg
            J2 20,21 pos,neg
            J3 30,31 pos,neg
        """
        live = self.idx * 10
        IncJogStatVal = int(IncJogStat.get())
        if IncJogStatVal == 1:
            J1jogNeg(float(incrementEntryField.get()))
        else:
            LiveJointJog(live)

    def SeljogPos(self):
        """docstring"""
        live = self.idx * 10 + 1
        IncJogStatVal = int(IncJogStat.get())
        if IncJogStatVal == 1:
            J1jogPos(float(incrementEntryField.get()))
        else:
            LiveJointJog(live)

    def sliderUpdate(self):
        """docstring"""
        text = round(float(self.labels["slide"].get()), 2)
        self.labels["slide"].config(text=text)

    def sliderExecute(foo):
        """docstring"""
        self.delta = float(self.labels["slide"].get()) - float(self.entry.get())
        # TODO: fix to be just "jog"
        func = jogNeg if self.delta < 0 else jogPos
        func(abs(self.delta))


class ExtJointFrame(JointFrame):
    """JointFrame for external axis"""

    def __init__(self, x,y):
        # super(ExtJointFrame,self).__init__(x,y)

        self.ctr = JointCTR()

        # TODO: finish
        self.frame = Frame(tabs['1'], width=145, height=100)
        self.frame["relief"] = "raised"
        self.frame.place(x=x, y=y)

        self.locations = [
                (15,5),
                (10,30),
                (110,30),
                (60,70),
        ]
        self.mk_labels()
        self.labels['main'].config(text=f'{self.ctr.name} Axis')

        self.entry = Entry(self.frame, width=5)
        self.entry.place(x=95, y=9)

        self.mk_buttons()
        self.mk_slider(x=10,y=43,length=125)

        # TODO: what about cls.active ??

    def mk_buttons(self):
        """makes buttons"""
        super().mk_buttons()

        xy = [dict(x=10, y=65), dict(x=105, y=65)] # relative button coordinates
        for i,(k,button) in enumerate(self.buttons.items()):
            button.place(**xy[i])
        


joint_frames = [
    JointFrame(x=810, y=10),
    JointFrame(x=810, y=55),
    JointFrame(x=810, y=100),
    JointFrame(x=1160, y=10),
    JointFrame(x=1160, y=55),
    #
    ExtJointFrame(x=1340, y=350),
    ExtJointFrame(x=1340, y=460),
    ExtJointFrame(x=1340, y=570),
]

####ENTRY FIELDS##########################################################
##########################################################################

#TODO: how to clean this up?

incrementEntryField = Entry(tabs['1'], width=4)
incrementEntryField.place(x=380, y=45)

curRowEntryField = Entry(tabs['1'], width=4)
curRowEntryField.place(x=174, y=120)

manEntryField = Entry(tabs['1'], width=105)
manEntryField.place(x=10, y=700)

ProgEntryField = Entry(tabs['1'], width=20)
ProgEntryField.place(x=70, y=45)


speedEntryField = Entry(tabs['1'], width=4)
speedEntryField.place(x=380, y=80)

ACCspeedField = Entry(tabs['1'], width=4)
ACCspeedField.place(x=380, y=100)

DECspeedField = Entry(tabs['1'], width=4)
DECspeedField.place(x=380, y=120)

ACCrampField = Entry(tabs['1'], width=4)
ACCrampField.place(x=380, y=140)

roundEntryField = Entry(tabs['1'], width=4)
roundEntryField.place(x=590, y=80)


class CTJogger():
    """Cartesian Jogger GUI Object"""
    "ie: XcurEntryField"
    # NOTE: is cur for current as in time or electricity?

    active = []

    def __init__(self, x,y, label):

        self.entry = Entry(CartjogFrame, width=5)
        self.entry.place(x=x, y=y)


CTJogger(660,195, 'X')
CTJogger(750, 195, 'Y')
CTJogger(840, 195, 'Z')

CTJogger(930, 195, 'Rz')
CTJogger(1020, 195, 'Ry')
CTJogger(1110, 195, 'Rx')


###BUTTONS################################################################
##########################################################################


def posRegFieldVisible(self):
    curCmdtype = options.get()
    if curCmdtype == "Move PR" or curCmdtype == "OFF PR " or curCmdtype == "Teach PR":
        SavePosEntryField.place(x=780, y=183)
    else:
        SavePosEntryField.place_forget()


manInsBut = Button(tabs['1'], text="  Insert  ", command=manInsItem)
manInsBut.place(x=98, y=725)

manRepBut = Button(tabs['1'], text="Replace", command=manReplItem)
manRepBut.place(x=164, y=725)

getSelBut = Button(tabs['1'], text="Get Selected", command=getSel)
getSelBut.place(x=10, y=725)

speedOption = StringVar(tabs['1'])
speedMenu = OptionMenu(tabs['1'], speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
speedMenu.place(x=412, y=76)


# single buttons

options = StringVar(tabs['1'])
menu = OptionMenu(
    tabs['1'],
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
menu.grid(row=2, column=2)
menu.config(width=18)
menu.place(x=700, y=180)

SavePosEntryField = Entry(tabs['1'], width=5)
# SavePosEntryField.place(x=800, y=183)


teachInsBut = Button(tabs['1'], text="Teach New Position", width=22, command=teachInsertBelSelected)
teachInsBut.place(x=700, y=220)

teachReplaceBut = Button(tabs['1'], text="Modify Position", width=22, command=teachReplaceSelected)
teachReplaceBut.place(x=700, y=260)

deleteBut = Button(tabs['1'], text="Delete", width=22, command=deleteitem)
deleteBut.place(x=700, y=300)

CalibrateBut = Button(tabs['1'], text="Auto Calibrate CMD", width=22, command=insCalibrate)
CalibrateBut.place(x=700, y=340)

camOnBut = Button(tabs['1'], text="Camera On", width=22, command=cameraOn)
camOnBut.place(x=700, y=380)

camOffBut = Button(tabs['1'], text="Camera Off", width=22, command=cameraOff)
camOffBut.place(x=700, y=420)


# buttons with 1 entry

waitTimeBut = Button(tabs['1'], text="Wait Time (seconds)", width=22, command=waitTime)
waitTimeBut.place(x=700, y=460)

waitInputOnBut = Button(tabs['1'], text="Wait Input ON", width=22, command=waitInputOn)
waitInputOnBut.place(x=700, y=500)

waitInputOffBut = Button(tabs['1'], text="Wait Input OFF", width=22, command=waitInputOff)
waitInputOffBut.place(x=700, y=540)

setOutputOnBut = Button(tabs['1'], text="Set Output On", width=22, command=setOutputOn)
setOutputOnBut.place(x=700, y=580)

setOutputOffBut = Button(tabs['1'], text="Set Output OFF", width=22, command=setOutputOff)
setOutputOffBut.place(x=700, y=620)

tabNumBut = Button(tabs['1'], text="Create Tab", width=22, command=tabNumber)
tabNumBut.place(x=700, y=660)

jumpTabBut = Button(tabs['1'], text="Jump to Tab", width=22, command=jumpTab)
jumpTabBut.place(x=700, y=700)


waitTimeEntryField = Entry(tabs['1'], width=5)
waitTimeEntryField.place(x=855, y=465)

waitInputEntryField = Entry(tabs['1'], width=5)
waitInputEntryField.place(x=855, y=505)

waitInputOffEntryField = Entry(tabs['1'], width=5)
waitInputOffEntryField.place(x=855, y=545)

outputOnEntryField = Entry(tabs['1'], width=5)
outputOnEntryField.place(x=855, y=585)

outputOffEntryField = Entry(tabs['1'], width=5)
outputOffEntryField.place(x=855, y=625)

tabNumEntryField = Entry(tabs['1'], width=5)
tabNumEntryField.place(x=855, y=665)

jumpTabEntryField = Entry(tabs['1'], width=5)
jumpTabEntryField.place(x=855, y=705)


# buttons with multiple entry

IfOnjumpTabBut = Button(tabs['1'], text="If On Jump", width=22, command=IfOnjumpTab)
IfOnjumpTabBut.place(x=950, y=360)

IfOffjumpTabBut = Button(tabs['1'], text="If Off Jump", width=22, command=IfOffjumpTab)
IfOffjumpTabBut.place(x=950, y=400)

servoBut = Button(tabs['1'], text="Servo", width=22, command=Servo)
servoBut.place(x=950, y=440)

RegNumBut = Button(tabs['1'], text="Register", width=22, command=insertRegister)
RegNumBut.place(x=950, y=480)

RegJmpBut = Button(tabs['1'], text="If Register Jump", width=22, command=IfRegjumpTab)
RegJmpBut.place(x=950, y=520)

StorPosBut = Button(tabs['1'], text="Position Register", width=22, command=storPos)
StorPosBut.place(x=950, y=560)

callBut = Button(tabs['1'], text="Call Program", width=22, command=insertCallProg)
callBut.place(x=950, y=600)

returnBut = Button(tabs['1'], text="Return", width=22, command=insertReturn)
returnBut.place(x=950, y=640)

visFindBut = Button(tabs['1'], text="Vision Find", width=22, command=insertvisFind)
visFindBut.place(x=950, y=680)

##
IfOnjumpInputTabEntryField = Entry(tabs['1'], width=5)
IfOnjumpInputTabEntryField.place(x=1107, y=363)

IfOnjumpNumberTabEntryField = Entry(tabs['1'], width=5)
IfOnjumpNumberTabEntryField.place(x=1147, y=363)

IfOffjumpInputTabEntryField = Entry(tabs['1'], width=5)
IfOffjumpInputTabEntryField.place(x=1107, y=403)

IfOffjumpNumberTabEntryField = Entry(tabs['1'], width=5)
IfOffjumpNumberTabEntryField.place(x=1147, y=403)

servoNumEntryField = Entry(tabs['1'], width=5)
servoNumEntryField.place(x=1107, y=443)

servoPosEntryField = Entry(tabs['1'], width=5)
servoPosEntryField.place(x=1147, y=443)

regNumEntryField = Entry(tabs['1'], width=5)
regNumEntryField.place(x=1107, y=483)

regEqEntryField = Entry(tabs['1'], width=5)
regEqEntryField.place(x=1147, y=483)

regNumJmpEntryField = Entry(tabs['1'], width=5)
regNumJmpEntryField.place(x=1107, y=523)

regEqJmpEntryField = Entry(tabs['1'], width=5)
regEqJmpEntryField.place(x=1147, y=523)

regTabJmpEntryField = Entry(tabs['1'], width=5)
regTabJmpEntryField.place(x=1187, y=523)

storPosNumEntryField = Entry(tabs['1'], width=5)
storPosNumEntryField.place(x=1107, y=563)

storPosElEntryField = Entry(tabs['1'], width=5)
storPosElEntryField.place(x=1147, y=563)

storPosValEntryField = Entry(tabs['1'], width=5)
storPosValEntryField.place(x=1187, y=563)

changeProgEntryField = Entry(tabs['1'], width=22)
changeProgEntryField.place(x=1107, y=603)

visPassEntryField = Entry(tabs['1'], width=5)
visPassEntryField.place(x=1107, y=683)

visFailEntryField = Entry(tabs['1'], width=5)
visFailEntryField.place(x=1147, y=683)


manEntLab = Label(tabs['1'], font=("Arial", 6), text="Manual Program Entry")
manEntLab.place(x=10, y=685)

ifOnLab = Label(tabs['1'], font=("Arial", 6), text=" Input            Tab")
ifOnLab.place(x=1107, y=350)

ifOffLab = Label(tabs['1'], font=("Arial", 6), text=" Input            Tab")
ifOffLab.place(x=1107, y=390)

regEqLab = Label(tabs['1'], font=("Arial", 6), text="Register       (++/--)")
regEqLab.place(x=1107, y=469)

ifregTabJmpLab = Label(tabs['1'], font=("Arial", 6), text="Register        Num         Tab")
ifregTabJmpLab.place(x=1107, y=509)

servoLab = Label(tabs['1'], font=("Arial", 6), text="Number      Position")
servoLab.place(x=1107, y=430)

storPosEqLab = Label(tabs['1'], font=("Arial", 6), text=" Pos Reg      Element       (++/--)")
storPosEqLab.place(x=1107, y=549)

visPassLab = Label(tabs['1'], font=("Arial", 6), text="Pass Tab     Fail Tab")
visPassLab.place(x=1107, y=670)


ProgBut = Button(tabs['1'], text="Load Program", command=loadProg)
ProgBut.place(x=202, y=42)


runProgBut = Button(tabs['1'], command=runProg)
playPhoto = PhotoImage(file="play-icon.gif")
runProgBut.config(image=playPhoto)
runProgBut.place(x=20, y=80)

xboxBut = Button(tabs['1'], command=xbox)
xboxPhoto = PhotoImage(file="xbox.gif")
xboxBut.config(image=xboxPhoto)
xboxBut.place(x=700, y=80)

stopProgBut = Button(tabs['1'], command=stopProg)
stopPhoto = PhotoImage(file="stop-icon.gif")
stopProgBut.config(image=stopPhoto)
stopProgBut.place(x=220, y=80)

revBut = Button(tabs['1'], text="REV ", command=stepRev)
revBut.place(x=105, y=80)

fwdBut = Button(tabs['1'], text="FWD", command=stepFwd)
fwdBut.place(x=160, y=80)


IncJogCbut = Checkbutton(tabs['1'], text="Incremental Jog", variable=IncJogStat)
IncJogCbut.place(x=412, y=46)


def SelXjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        XjogNeg(float(incrementEntryField.get()))
    else:
        LiveCarJog(10)


XjogNegBut = Button(CartjogFrame, text="-", width=3)
XjogNegBut.bind("<ButtonPress>", SelXjogNeg)
XjogNegBut.bind("<ButtonRelease>", StopJog)
XjogNegBut.place(x=642, y=225, width=30, height=25)


def SelXjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        XjogPos(float(incrementEntryField.get()))
    else:
        LiveCarJog(11)


XjogPosBut = Button(CartjogFrame, text="+", width=3)
XjogPosBut.bind("<ButtonPress>", SelXjogPos)
XjogPosBut.bind("<ButtonRelease>", StopJog)
XjogPosBut.place(x=680, y=225, width=30, height=25)


def SelYjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        YjogNeg(float(incrementEntryField.get()))
    else:
        LiveCarJog(20)


YjogNegBut = Button(CartjogFrame, text="-", width=3)
YjogNegBut.bind("<ButtonPress>", SelYjogNeg)
YjogNegBut.bind("<ButtonRelease>", StopJog)
YjogNegBut.place(x=732, y=225, width=30, height=25)


def SelYjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        YjogPos(float(incrementEntryField.get()))
    else:
        LiveCarJog(21)


YjogPosBut = Button(CartjogFrame, text="+", width=3)
YjogPosBut.bind("<ButtonPress>", SelYjogPos)
YjogPosBut.bind("<ButtonRelease>", StopJog)
YjogPosBut.place(x=770, y=225, width=30, height=25)


def SelZjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        ZjogNeg(float(incrementEntryField.get()))
    else:
        LiveCarJog(30)


ZjogNegBut = Button(CartjogFrame, text="-", width=3)
ZjogNegBut.bind("<ButtonPress>", SelZjogNeg)
ZjogNegBut.bind("<ButtonRelease>", StopJog)
ZjogNegBut.place(x=822, y=225, width=30, height=25)


def SelZjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        ZjogPos(float(incrementEntryField.get()))
    else:
        LiveCarJog(31)


ZjogPosBut = Button(CartjogFrame, text="+", width=3)
ZjogPosBut.bind("<ButtonPress>", SelZjogPos)
ZjogPosBut.bind("<ButtonRelease>", StopJog)
ZjogPosBut.place(x=860, y=225, width=30, height=25)


def SelRzjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        RzjogNeg(float(incrementEntryField.get()))
    else:
        LiveCarJog(40)


RzjogNegBut = Button(CartjogFrame, text="-", width=3)
RzjogNegBut.bind("<ButtonPress>", SelRzjogNeg)
RzjogNegBut.bind("<ButtonRelease>", StopJog)
RzjogNegBut.place(x=912, y=225, width=30, height=25)


def SelRzjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        RzjogPos(float(incrementEntryField.get()))
    else:
        LiveCarJog(41)


RzjogPosBut = Button(CartjogFrame, text="+", width=3)
RzjogPosBut.bind("<ButtonPress>", SelRzjogPos)
RzjogPosBut.bind("<ButtonRelease>", StopJog)
RzjogPosBut.place(x=950, y=225, width=30, height=25)


def SelRyjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        RyjogNeg(float(incrementEntryField.get()))
    else:
        LiveCarJog(50)


RyjogNegBut = Button(CartjogFrame, text="-", width=3)
RyjogNegBut.bind("<ButtonPress>", SelRyjogNeg)
RyjogNegBut.bind("<ButtonRelease>", StopJog)
RyjogNegBut.place(x=1002, y=225, width=30, height=25)


def SelRyjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        RyjogPos(float(incrementEntryField.get()))
    else:
        LiveCarJog(51)


RyjogPosBut = Button(CartjogFrame, text="+", width=3)
RyjogPosBut.bind("<ButtonPress>", SelRyjogPos)
RyjogPosBut.bind("<ButtonRelease>", StopJog)
RyjogPosBut.place(x=1040, y=225, width=30, height=25)


def SelRxjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        RxjogNeg(float(incrementEntryField.get()))
    else:
        LiveCarJog(60)


RxjogNegBut = Button(CartjogFrame, text="-", width=3)
RxjogNegBut.bind("<ButtonPress>", SelRxjogNeg)
RxjogNegBut.bind("<ButtonRelease>", StopJog)
RxjogNegBut.place(x=1092, y=225, width=30, height=25)


def SelRxjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        RxjogPos(float(incrementEntryField.get()))
    else:
        LiveCarJog(61)


RxjogPosBut = Button(CartjogFrame, text="+", width=3)
RxjogPosBut.bind("<ButtonPress>", SelRxjogPos)
RxjogPosBut.bind("<ButtonRelease>", StopJog)
RxjogPosBut.place(x=1130, y=225, width=30, height=25)


def SelTxjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TXjogNeg(float(incrementEntryField.get()))
    else:
        LiveToolJog(10)


TXjogNegBut = Button(CartjogFrame, text="-", width=3)
TXjogNegBut.bind("<ButtonPress>", SelTxjogNeg)
TXjogNegBut.bind("<ButtonRelease>", StopJog)
TXjogNegBut.place(x=642, y=300, width=30, height=25)


def SelTxjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TXjogPos(float(incrementEntryField.get()))
    else:
        LiveToolJog(11)


TXjogPosBut = Button(CartjogFrame, text="+", width=3)
TXjogPosBut.bind("<ButtonPress>", SelTxjogPos)
TXjogPosBut.bind("<ButtonRelease>", StopJog)
TXjogPosBut.place(x=680, y=300, width=30, height=25)


def SelTyjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TYjogNeg(float(incrementEntryField.get()))
    else:
        LiveToolJog(20)


TYjogNegBut = Button(CartjogFrame, text="-", width=3)
TYjogNegBut.bind("<ButtonPress>", SelTyjogNeg)
TYjogNegBut.bind("<ButtonRelease>", StopJog)
TYjogNegBut.place(x=732, y=300, width=30, height=25)


def SelTyjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TYjogPos(float(incrementEntryField.get()))
    else:
        LiveToolJog(21)


TYjogPosBut = Button(CartjogFrame, text="+", width=3)
TYjogPosBut.bind("<ButtonPress>", SelTyjogPos)
TYjogPosBut.bind("<ButtonRelease>", StopJog)
TYjogPosBut.place(x=770, y=300, width=30, height=25)


def SelTzjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TZjogNeg(float(incrementEntryField.get()))
    else:
        LiveToolJog(30)


TZjogNegBut = Button(CartjogFrame, text="-", width=3)
TZjogNegBut.bind("<ButtonPress>", SelTzjogNeg)
TZjogNegBut.bind("<ButtonRelease>", StopJog)
TZjogNegBut.place(x=822, y=300, width=30, height=25)


def SelTzjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TZjogPos(float(incrementEntryField.get()))
    else:
        LiveToolJog(31)


TZjogPosBut = Button(CartjogFrame, text="+", width=3)
TZjogPosBut.bind("<ButtonPress>", SelTzjogPos)
TZjogPosBut.bind("<ButtonRelease>", StopJog)
TZjogPosBut.place(x=860, y=300, width=30, height=25)


def SelTRzjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TRzjogNeg(float(incrementEntryField.get()))
    else:
        LiveToolJog(40)


TRzjogNegBut = Button(CartjogFrame, text="-", width=3)
TRzjogNegBut.bind("<ButtonPress>", SelTRzjogNeg)
TRzjogNegBut.bind("<ButtonRelease>", StopJog)
TRzjogNegBut.place(x=912, y=300, width=30, height=25)


def SelTRzjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TRzjogPos(float(incrementEntryField.get()))
    else:
        LiveToolJog(41)


TRzjogPosBut = Button(CartjogFrame, text="+", width=3)
TRzjogPosBut.bind("<ButtonPress>", SelTRzjogPos)
TRzjogPosBut.bind("<ButtonRelease>", StopJog)
TRzjogPosBut.place(x=950, y=300, width=30, height=25)


def SelTRyjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TRyjogNeg(float(incrementEntryField.get()))
    else:
        LiveToolJog(50)


TRyjogNegBut = Button(CartjogFrame, text="-", width=3)
TRyjogNegBut.bind("<ButtonPress>", SelTRyjogNeg)
TRyjogNegBut.bind("<ButtonRelease>", StopJog)
TRyjogNegBut.place(x=1002, y=300, width=30, height=25)


def SelTRyjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TRyjogPos(float(incrementEntryField.get()))
    else:
        LiveToolJog(51)


TRyjogPosBut = Button(CartjogFrame, text="+", width=3)
TRyjogPosBut.bind("<ButtonPress>", SelTRyjogPos)
TRyjogPosBut.bind("<ButtonRelease>", StopJog)
TRyjogPosBut.place(x=1040, y=300, width=30, height=25)


def SelTRxjogNeg(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TRxjogNeg(float(incrementEntryField.get()))
    else:
        LiveToolJog(60)


TRxjogNegBut = Button(CartjogFrame, text="-", width=3)
TRxjogNegBut.bind("<ButtonPress>", SelTRxjogNeg)
TRxjogNegBut.bind("<ButtonRelease>", StopJog)
TRxjogNegBut.place(x=1092, y=300, width=30, height=25)


def SelTRxjogPos(self):
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 1:
        TRxjogPos(float(incrementEntryField.get()))
    else:
        LiveToolJog(61)


TRxjogPosBut = Button(CartjogFrame, text="+", width=3)
TRxjogPosBut.bind("<ButtonPress>", SelTRxjogPos)
TRxjogPosBut.bind("<ButtonRelease>", StopJog)
TRxjogPosBut.place(x=1130, y=300, width=30, height=25)


"""
---------- ---------- ----------
---------- ---------- ----------
---------- ---------- ----------
TAB 2
---------- ---------- ----------
---------- ---------- ----------
---------- ---------- ----------
"""


### 2 LABELS#################################################################
#############################################################################

ComPortLab = Label(tab2, text="TEENSY COM PORT:")
ComPortLab.place(x=66, y=90)

ComPortLab = Label(tab2, text="IO BOARD COM PORT:")
ComPortLab.place(x=60, y=160)

almStatusLab2 = Label(tab2, text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel")
almStatusLab2.place(x=25, y=20)


ToolFrameLab = Label(tab2, text="Tool Frame Offset")
ToolFrameLab.place(x=970, y=60)

UFxLab = Label(tab2, font=("Arial", 11), text="X")
UFxLab.place(x=920, y=90)

UFyLab = Label(tab2, font=("Arial", 11), text="Y")
UFyLab.place(x=960, y=90)

UFzLab = Label(tab2, font=("Arial", 11), text="Z")
UFzLab.place(x=1000, y=90)

UFRxLab = Label(tab2, font=("Arial", 11), text="Rz")
UFRxLab.place(x=1040, y=90)

UFRyLab = Label(tab2, font=("Arial", 11), text="Ry")
UFRyLab.place(x=1080, y=90)

UFRzLab = Label(tab2, font=("Arial", 11), text="Rx")
UFRzLab.place(x=1120, y=90)

comLab = Label(tab2, text="Communication")
comLab.place(x=72, y=60)

jointCalLab = Label(tab2, text="Robot Calibration")
jointCalLab.place(x=290, y=60)

axis7Lab = Label(tab2, text="7th Axis Calibration")
axis7Lab.place(x=665, y=300)

axis7lengthLab = Label(tab2, text="7th Axis Length:")
axis7lengthLab.place(x=651, y=340)

axis7rotLab = Label(tab2, text="MM per Rotation:")
axis7rotLab.place(x=645, y=370)

axis7stepsLab = Label(tab2, text="Drive Steps:")
axis7stepsLab.place(x=675, y=400)

axis7pinsetLab = Label(tab2, font=("Arial", 8), text="StepPin = 12 / DirPin = 13 / CalPin = 36")
axis7pinsetLab.place(x=627, y=510)

axis8pinsetLab = Label(tab2, font=("Arial", 8), text="StepPin = 32 / DirPin = 33 / CalPin = 37")
axis8pinsetLab.place(x=827, y=510)

axis9pinsetLab = Label(tab2, font=("Arial", 8), text="StepPin = 34 / DirPin = 35 / CalPin = 38")
axis9pinsetLab.place(x=1027, y=510)


axis8Lab = Label(tab2, text="8th Axis Calibration")
axis8Lab.place(x=865, y=300)

axis8lengthLab = Label(tab2, text="8th Axis Length:")
axis8lengthLab.place(x=851, y=340)

axis8rotLab = Label(tab2, text="MM per Rotation:")
axis8rotLab.place(x=845, y=370)

axis8stepsLab = Label(tab2, text="Drive Steps:")
axis8stepsLab.place(x=875, y=400)


axis9Lab = Label(tab2, text="9th Axis Calibration")
axis9Lab.place(x=1065, y=300)

axis9lengthLab = Label(tab2, text="9th Axis Length:")
axis9lengthLab.place(x=1051, y=340)

axis9rotLab = Label(tab2, text="MM per Rotation:")
axis9rotLab.place(x=1045, y=370)

axis9stepsLab = Label(tab2, text="Drive Steps:")
axis9stepsLab.place(x=1075, y=400)


CalibrationOffsetsLab = Label(tab2, text="Calibration Offsets")
CalibrationOffsetsLab.place(x=485, y=60)

J1calLab = Label(tab2, text="J1 Offset")
J1calLab.place(x=480, y=90)

J2calLab = Label(tab2, text="J2 Offset")
J2calLab.place(x=480, y=120)

J3calLab = Label(tab2, text="J3 Offset")
J3calLab.place(x=480, y=150)

J4calLab = Label(tab2, text="J4 Offset")
J4calLab.place(x=480, y=180)

J5calLab = Label(tab2, text="J5 Offset")
J5calLab.place(x=480, y=210)

J6calLab = Label(tab2, text="J6 Offset")
J6calLab.place(x=480, y=240)

J7calLab = Label(tab2, text="J7 Offset")
J7calLab.place(x=480, y=280)

J8calLab = Label(tab2, text="J8 Offset")
J8calLab.place(x=480, y=310)

J9calLab = Label(tab2, text="J9 Offset")
J9calLab.place(x=480, y=340)


CalibrationOffsetsLab = Label(tab2, text="Encoder Control")
CalibrationOffsetsLab.place(x=715, y=60)

cmdSentLab = Label(tab2, text="Last Command Sent to Controller")
cmdSentLab.place(x=10, y=565)

cmdRecLab = Label(tab2, text="Last Response From Controller")
cmdRecLab.place(x=10, y=625)

ToolFrameLab = Label(tab2, text="Theme")
ToolFrameLab.place(x=1225, y=60)


### 2 BUTTONS################################################################
#############################################################################

comPortBut = Button(tab2, text="  Set Com Teensy  ", command=setCom)
comPortBut.place(x=85, y=110)

comPortBut2 = Button(tab2, text="Set Com IO Board", command=setCom2)
comPortBut2.place(x=85, y=180)


lightBut = Button(tab2, text="  Light  ", command=lightTheme)
lightBut.place(x=1190, y=90)

darkBut = Button(tab2, text="  Dark   ", command=darkTheme)
darkBut.place(x=1250, y=90)


autoCalBut = Button(tab2, text="  Auto Calibrate  ", command=calRobotAll)
autoCalBut.place(x=285, y=90)

J1calCbut = Checkbutton(tab2, text="J1", variable=J1CalStat)
J1calCbut.place(x=285, y=125)

J2calCbut = Checkbutton(tab2, text="J2", variable=J2CalStat)
J2calCbut.place(x=320, y=125)

J3calCbut = Checkbutton(tab2, text="J3", variable=J3CalStat)
J3calCbut.place(x=355, y=125)

J4calCbut = Checkbutton(tab2, text="J4", variable=J4CalStat)
J4calCbut.place(x=285, y=145)

J5calCbut = Checkbutton(tab2, text="J5", variable=J5CalStat)
J5calCbut.place(x=320, y=145)

J6calCbut = Checkbutton(tab2, text="J6", variable=J6CalStat)
J6calCbut.place(x=355, y=145)


J1calCbut2 = Checkbutton(tab2, text="J1", variable=J1CalStat2)
J1calCbut2.place(x=285, y=180)

J2calCbut2 = Checkbutton(tab2, text="J2", variable=J2CalStat2)
J2calCbut2.place(x=320, y=180)

J3calCbut2 = Checkbutton(tab2, text="J3", variable=J3CalStat2)
J3calCbut2.place(x=355, y=180)

J4calCbut2 = Checkbutton(tab2, text="J4", variable=J4CalStat2)
J4calCbut2.place(x=285, y=200)

J5calCbut2 = Checkbutton(tab2, text="J5", variable=J5CalStat2)
J5calCbut2.place(x=320, y=200)

J6calCbut2 = Checkbutton(tab2, text="J6", variable=J6CalStat2)
J6calCbut2.place(x=355, y=200)


J7zerobut = Button(tab2, text="Set Axis 7 Calibration to Zero", width=28, command=zeroAxis7)
J7zerobut.place(x=627, y=440)

J8zerobut = Button(tab2, text="Set Axis 8 Calibration to Zero", width=28, command=zeroAxis8)
J8zerobut.place(x=827, y=440)

J9zerobut = Button(tab2, text="Set Axis 9 Calibration to Zero", width=28, command=zeroAxis9)
J9zerobut.place(x=1027, y=440)

J7calbut = Button(tab2, text="Autocalibrate Axis 7", width=28, command=calRobotJ7)
J7calbut.place(x=627, y=475)

J8calbut = Button(tab2, text="Autocalibrate Axis 8", width=28, command=calRobotJ8)
J8calbut.place(x=827, y=475)

J9calbut = Button(tab2, text="Autocalibrate Axis 9", width=28, command=calRobotJ9)
J9calbut.place(x=1027, y=475)


CalJ1But = Button(tab2, text="Calibrate J1 Only", command=calRobotJ1)
CalJ1But.place(x=285, y=240)

CalJ2But = Button(tab2, text="Calibrate J2 Only", command=calRobotJ2)
CalJ2But.place(x=285, y=270)

CalJ3But = Button(tab2, text="Calibrate J3 Only", command=calRobotJ3)
CalJ3But.place(x=285, y=300)

CalJ4But = Button(tab2, text="Calibrate J4 Only", command=calRobotJ4)
CalJ4But.place(x=285, y=330)

CalJ5But = Button(tab2, text="Calibrate J5 Only", command=calRobotJ5)
CalJ5But.place(x=285, y=360)

CalJ6But = Button(tab2, text="Calibrate J6 Only", command=calRobotJ6)
CalJ6But.place(x=285, y=390)

CalZeroBut = Button(tab2, text="Force Cal. to 0° Home", width=20, command=CalZeroPos)
CalZeroBut.place(x=270, y=425)

CalRestBut = Button(tab2, text="Force Cal. to Vert. Rest", width=20, command=CalRestPos)
CalRestBut.place(x=270, y=460)

J1OpenLoopCbut = Checkbutton(tab2, text="J1 Open Loop (disable encoder)", variable=J1OpenLoopStat)
J1OpenLoopCbut.place(x=665, y=90)

J2OpenLoopCbut = Checkbutton(tab2, text="J2 Open Loop (disable encoder)", variable=J2OpenLoopStat)
J2OpenLoopCbut.place(x=665, y=110)

J3OpenLoopCbut = Checkbutton(tab2, text="J3 Open Loop (disable encoder)", variable=J3OpenLoopStat)
J3OpenLoopCbut.place(x=665, y=130)

J4OpenLoopCbut = Checkbutton(tab2, text="J4 Open Loop (disable encoder)", variable=J4OpenLoopStat)
J4OpenLoopCbut.place(x=665, y=150)

J5OpenLoopCbut = Checkbutton(tab2, text="J5 Open Loop (disable encoder)", variable=J5OpenLoopStat)
J5OpenLoopCbut.place(x=665, y=170)

J6OpenLoopCbut = Checkbutton(tab2, text="J6 Open Loop (disable encoder)", variable=J6OpenLoopStat)
J6OpenLoopCbut.place(x=665, y=190)

saveCalBut = Button(tab2, text="    SAVE    ", width=26, command=SaveAndApplyCalibration)
saveCalBut.place(x=1150, y=630)

#### 2 ENTRY FIELDS##########################################################
#############################################################################


comPortEntryField = Entry(tab2, width=4)
comPortEntryField.place(x=50, y=114)

com2PortEntryField = Entry(tab2, width=4)
com2PortEntryField.place(x=50, y=184)

cmdSentEntryField = Entry(tab2, width=95)
cmdSentEntryField.place(x=10, y=585)

cmdRecEntryField = Entry(tab2, width=95)
cmdRecEntryField.place(x=10, y=645)


J1calOffEntryField = Entry(tab2, width=8)
J1calOffEntryField.place(x=540, y=90)

J2calOffEntryField = Entry(tab2, width=8)
J2calOffEntryField.place(x=540, y=120)

J3calOffEntryField = Entry(tab2, width=8)
J3calOffEntryField.place(x=540, y=150)

J4calOffEntryField = Entry(tab2, width=8)
J4calOffEntryField.place(x=540, y=180)

J5calOffEntryField = Entry(tab2, width=8)
J5calOffEntryField.place(x=540, y=210)

J6calOffEntryField = Entry(tab2, width=8)
J6calOffEntryField.place(x=540, y=240)

J7calOffEntryField = Entry(tab2, width=8)
J7calOffEntryField.place(x=540, y=280)

J8calOffEntryField = Entry(tab2, width=8)
J8calOffEntryField.place(x=540, y=310)

J9calOffEntryField = Entry(tab2, width=8)
J9calOffEntryField.place(x=540, y=340)


axis7lengthEntryField = Entry(tab2, width=6)
axis7lengthEntryField.place(x=750, y=340)

axis7rotEntryField = Entry(tab2, width=6)
axis7rotEntryField.place(x=750, y=370)

axis7stepsEntryField = Entry(tab2, width=6)
axis7stepsEntryField.place(x=750, y=400)

axis8lengthEntryField = Entry(tab2, width=6)
axis8lengthEntryField.place(x=950, y=340)

axis8rotEntryField = Entry(tab2, width=6)
axis8rotEntryField.place(x=950, y=370)

axis8stepsEntryField = Entry(tab2, width=6)
axis8stepsEntryField.place(x=950, y=400)

axis9lengthEntryField = Entry(tab2, width=6)
axis9lengthEntryField.place(x=1150, y=340)

axis9rotEntryField = Entry(tab2, width=6)
axis9rotEntryField.place(x=1150, y=370)

axis9stepsEntryField = Entry(tab2, width=6)
axis9stepsEntryField.place(x=1150, y=400)


### Tool Frame ###

TFxEntryField = Entry(tab2, width=5)
TFxEntryField.place(x=910, y=115)
TFyEntryField = Entry(tab2, width=5)
TFyEntryField.place(x=950, y=115)
TFzEntryField = Entry(tab2, width=5)
TFzEntryField.place(x=990, y=115)
TFrzEntryField = Entry(tab2, width=5)
TFrzEntryField.place(x=1030, y=115)
TFryEntryField = Entry(tab2, width=5)
TFryEntryField.place(x=1070, y=115)
TFrxEntryField = Entry(tab2, width=5)
TFrxEntryField.place(x=1110, y=115)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 3


### 3 LABELS#################################################################
#############################################################################

servo0onequalsLab = Label(tab3, text="=")
servo0onequalsLab.place(x=70, y=12)

servo0offequalsLab = Label(tab3, text="=")
servo0offequalsLab.place(x=70, y=52)

servo1onequalsLab = Label(tab3, text="=")
servo1onequalsLab.place(x=70, y=92)

servo1offequalsLab = Label(tab3, text="=")
servo1offequalsLab.place(x=70, y=132)

servo2onequalsLab = Label(tab3, text="=")
servo2onequalsLab.place(x=70, y=172)

servo2offequalsLab = Label(tab3, text="=")
servo2offequalsLab.place(x=70, y=212)

servo3onequalsLab = Label(tab3, text="=")
servo3onequalsLab.place(x=70, y=252)

servo3offequalsLab = Label(tab3, text="=")
servo3offequalsLab.place(x=70, y=292)


Do1onequalsLab = Label(tab3, text="=")
Do1onequalsLab.place(x=210, y=12)

Do1offequalsLab = Label(tab3, text="=")
Do1offequalsLab.place(x=210, y=52)

Do2onequalsLab = Label(tab3, text="=")
Do2onequalsLab.place(x=210, y=92)

Do2offequalsLab = Label(tab3, text="=")
Do2offequalsLab.place(x=210, y=132)

Do3onequalsLab = Label(tab3, text="=")
Do3onequalsLab.place(x=210, y=172)

Do3offequalsLab = Label(tab3, text="=")
Do3offequalsLab.place(x=210, y=212)

Do4onequalsLab = Label(tab3, text="=")
Do4onequalsLab.place(x=210, y=252)

Do4offequalsLab = Label(tab3, text="=")
Do4offequalsLab.place(x=210, y=292)

Do5onequalsLab = Label(tab3, text="=")
Do5onequalsLab.place(x=210, y=332)

Do5offequalsLab = Label(tab3, text="=")
Do5offequalsLab.place(x=210, y=372)

Do6onequalsLab = Label(tab3, text="=")
Do6onequalsLab.place(x=210, y=412)

Do6offequalsLab = Label(tab3, text="=")
Do6offequalsLab.place(x=210, y=452)


inoutavailLab = Label(
    tab3,
    text="NOTE: the following are available when using the default Nano board for IO:   Inputs = 2-7  /  Outputs = 8-13  /  Servos = A0-A7",
)
inoutavailLab.place(x=10, y=640)

inoutavailLab = Label(
    tab3,
    text="If using IO on Teensy board:  Inputs = 32-36  /  Outputs = 37-41 - if using IO on Teensy you must manually change the command from 'Out On =' to 'ToutOn ='",
)
inoutavailLab.place(x=10, y=655)


### 3 BUTTONS################################################################
#############################################################################

servo0onBut = Button(tab3, text="Servo 0", command=Servo0on)
servo0onBut.place(x=10, y=10)

servo0offBut = Button(tab3, text="Servo 0", command=Servo0off)
servo0offBut.place(x=10, y=50)

servo1onBut = Button(tab3, text="Servo 1", command=Servo1on)
servo1onBut.place(x=10, y=90)

servo1offBut = Button(tab3, text="Servo 1", command=Servo1off)
servo1offBut.place(x=10, y=130)

servo2onBut = Button(tab3, text="Servo 2", command=Servo2on)
servo2onBut.place(x=10, y=170)

servo2offBut = Button(tab3, text="Servo 2", command=Servo2off)
servo2offBut.place(x=10, y=210)

servo3onBut = Button(tab3, text="Servo 3", command=Servo3on)
servo3onBut.place(x=10, y=250)

servo3offBut = Button(tab3, text="Servo 3", command=Servo3off)
servo3offBut.place(x=10, y=290)


DO1onBut = Button(tab3, text="DO on", command=DO1on)
DO1onBut.place(x=150, y=10)

DO1offBut = Button(tab3, text="DO off", command=DO1off)
DO1offBut.place(x=150, y=50)

DO2onBut = Button(tab3, text="DO on", command=DO2on)
DO2onBut.place(x=150, y=90)

DO2offBut = Button(tab3, text="DO off", command=DO2off)
DO2offBut.place(x=150, y=130)

DO3onBut = Button(tab3, text="DO on", command=DO3on)
DO3onBut.place(x=150, y=170)

DO3offBut = Button(tab3, text="DO off", command=DO3off)
DO3offBut.place(x=150, y=210)

DO4onBut = Button(tab3, text="DO on", command=DO4on)
DO4onBut.place(x=150, y=250)

DO4offBut = Button(tab3, text="DO off", command=DO4off)
DO4offBut.place(x=150, y=290)

DO5onBut = Button(tab3, text="DO on", command=DO5on)
DO5onBut.place(x=150, y=330)

DO5offBut = Button(tab3, text="DO off", command=DO5off)
DO5offBut.place(x=150, y=370)

DO6onBut = Button(tab3, text="DO on", command=DO6on)
DO6onBut.place(x=150, y=410)

DO6offBut = Button(tab3, text="DO off", command=DO6off)
DO6offBut.place(x=150, y=450)


#### 3 ENTRY FIELDS##########################################################
#############################################################################


servo0onEntryField = Entry(tab3, width=5)
servo0onEntryField.place(x=90, y=15)

servo0offEntryField = Entry(tab3, width=5)
servo0offEntryField.place(x=90, y=55)

servo1onEntryField = Entry(tab3, width=5)
servo1onEntryField.place(x=90, y=95)

servo1offEntryField = Entry(tab3, width=5)
servo1offEntryField.place(x=90, y=135)

servo2onEntryField = Entry(tab3, width=5)
servo2onEntryField.place(x=90, y=175)

servo2offEntryField = Entry(tab3, width=5)
servo2offEntryField.place(x=90, y=215)


servo3onEntryField = Entry(tab3, width=5)
servo3onEntryField.place(x=90, y=255)

servo3offEntryField = Entry(tab3, width=5)
servo3offEntryField.place(x=90, y=295)


DO1onEntryField = Entry(tab3, width=5)
DO1onEntryField.place(x=230, y=15)

DO1offEntryField = Entry(tab3, width=5)
DO1offEntryField.place(x=230, y=55)

DO2onEntryField = Entry(tab3, width=5)
DO2onEntryField.place(x=230, y=95)

DO2offEntryField = Entry(tab3, width=5)
DO2offEntryField.place(x=230, y=135)

DO3onEntryField = Entry(tab3, width=5)
DO3onEntryField.place(x=230, y=175)

DO3offEntryField = Entry(tab3, width=5)
DO3offEntryField.place(x=230, y=215)

DO4onEntryField = Entry(tab3, width=5)
DO4onEntryField.place(x=230, y=255)

DO4offEntryField = Entry(tab3, width=5)
DO4offEntryField.place(x=230, y=295)

DO5onEntryField = Entry(tab3, width=5)
DO5onEntryField.place(x=230, y=335)

DO5offEntryField = Entry(tab3, width=5)
DO5offEntryField.place(x=230, y=375)

DO6onEntryField = Entry(tab3, width=5)
DO6onEntryField.place(x=230, y=415)

DO6offEntryField = Entry(tab3, width=5)
DO6offEntryField.place(x=230, y=455)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 4


### 4 LABELS#################################################################
#############################################################################

R1Lab = Label(tab4, text="R1")
R1Lab.place(x=70, y=30)

R2Lab = Label(tab4, text="R2")
R2Lab.place(x=70, y=60)

R3Lab = Label(tab4, text="R3")
R3Lab.place(x=70, y=90)

R4Lab = Label(tab4, text="R4")
R4Lab.place(x=70, y=120)

R5Lab = Label(tab4, text="R5")
R5Lab.place(x=70, y=150)

R6Lab = Label(tab4, text="R6")
R6Lab.place(x=70, y=180)

R7Lab = Label(tab4, text="R7")
R7Lab.place(x=70, y=210)

R8Lab = Label(tab4, text="R8")
R8Lab.place(x=70, y=240)

R9Lab = Label(tab4, text="R9")
R9Lab.place(x=70, y=270)

R10Lab = Label(tab4, text="R10")
R10Lab.place(x=70, y=300)

R11Lab = Label(tab4, text="R11")
R11Lab.place(x=70, y=330)

R12Lab = Label(tab4, text="R12")
R12Lab.place(x=70, y=360)

R13Lab = Label(tab4, text="R14")
R13Lab.place(x=70, y=390)

R14Lab = Label(tab4, text="R14")
R14Lab.place(x=70, y=420)

R15Lab = Label(tab4, text="R15")
R15Lab.place(x=70, y=450)

R16Lab = Label(tab4, text="R16")
R16Lab.place(x=70, y=480)


SP1Lab = Label(tab4, text="PR1")
SP1Lab.place(x=640, y=30)

SP2Lab = Label(tab4, text="PR2")
SP2Lab.place(x=640, y=60)

SP3Lab = Label(tab4, text="PR3")
SP3Lab.place(x=640, y=90)

SP4Lab = Label(tab4, text="PR4")
SP4Lab.place(x=640, y=120)

SP5Lab = Label(tab4, text="PR5")
SP5Lab.place(x=640, y=150)

SP6Lab = Label(tab4, text="PR6")
SP6Lab.place(x=640, y=180)

SP7Lab = Label(tab4, text="PR7")
SP7Lab.place(x=640, y=210)

SP8Lab = Label(tab4, text="PR8")
SP8Lab.place(x=640, y=240)

SP9Lab = Label(tab4, text="PR9")
SP9Lab.place(x=640, y=270)

SP10Lab = Label(tab4, text="PR10")
SP10Lab.place(x=640, y=300)

SP11Lab = Label(tab4, text="PR11")
SP11Lab.place(x=640, y=330)

SP12Lab = Label(tab4, text="PR12")
SP12Lab.place(x=640, y=360)

SP13Lab = Label(tab4, text="PR14")
SP13Lab.place(x=640, y=390)

SP14Lab = Label(tab4, text="PR14")
SP14Lab.place(x=640, y=420)

SP15Lab = Label(tab4, text="PR15")
SP15Lab.place(x=640, y=450)

SP16Lab = Label(tab4, text="PR16")
SP16Lab.place(x=640, y=480)


SP_E1_Lab = Label(tab4, text="X")
SP_E1_Lab.place(x=410, y=10)

SP_E2_Lab = Label(tab4, text="Y")
SP_E2_Lab.place(x=450, y=10)

SP_E3_Lab = Label(tab4, text="Z")
SP_E3_Lab.place(x=490, y=10)

SP_E4_Lab = Label(tab4, text="Rz")
SP_E4_Lab.place(x=530, y=10)

SP_E5_Lab = Label(tab4, text="Ry")
SP_E5_Lab.place(x=570, y=10)

SP_E6_Lab = Label(tab4, text="Rx")
SP_E6_Lab.place(x=610, y=10)


### 4 BUTTONS################################################################
#############################################################################


#### 4 ENTRY FIELDS##########################################################
#############################################################################

R1EntryField = Entry(tab4, width=5)
R1EntryField.place(x=30, y=30)

R2EntryField = Entry(tab4, width=5)
R2EntryField.place(x=30, y=60)

R3EntryField = Entry(tab4, width=5)
R3EntryField.place(x=30, y=90)

R4EntryField = Entry(tab4, width=5)
R4EntryField.place(x=30, y=120)

R5EntryField = Entry(tab4, width=5)
R5EntryField.place(x=30, y=150)

R6EntryField = Entry(tab4, width=5)
R6EntryField.place(x=30, y=180)

R7EntryField = Entry(tab4, width=5)
R7EntryField.place(x=30, y=210)

R8EntryField = Entry(tab4, width=5)
R8EntryField.place(x=30, y=240)

R9EntryField = Entry(tab4, width=5)
R9EntryField.place(x=30, y=270)

R10EntryField = Entry(tab4, width=5)
R10EntryField.place(x=30, y=300)

R11EntryField = Entry(tab4, width=5)
R11EntryField.place(x=30, y=330)

R12EntryField = Entry(tab4, width=5)
R12EntryField.place(x=30, y=360)

R13EntryField = Entry(tab4, width=5)
R13EntryField.place(x=30, y=390)

R14EntryField = Entry(tab4, width=5)
R14EntryField.place(x=30, y=420)

R15EntryField = Entry(tab4, width=5)
R15EntryField.place(x=30, y=450)

R16EntryField = Entry(tab4, width=5)
R16EntryField.place(x=30, y=480)


"""refactored: SP_9_E1 is now sp_entry[0][8] """
mk_entry = lambda: Entry(tab4, width=5)
sp_entry_fields = [[mk_entry() for e in range(16)] for sp in range(6)]

coordinates = [[(400 + (40 * j), 30 * (i + 1)) for i in range(16)] for j in range(6)]

# list flatten
sp_entries = sum(sp_entries)
coordinates = sum(coordinates)

for entry, (x, y) in zip(sp_entries, coordinates):
    entry.place(x=x, y=y)

####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 5


### 5 LABELS#################################################################
#############################################################################

VisBackdropImg = ImageTk.PhotoImage(Image.open("VisBackdrop.png"))
VisBackdromLbl = Label(tab5, image=VisBackdropImg)
VisBackdromLbl.place(x=15, y=215)


# cap= cv2.VideoCapture(0)
video_frame = Frame(tab5, width=640, height=480)
video_frame.place(x=50, y=250)


vid_lbl = Label(video_frame)
vid_lbl.place(x=0, y=0)

vid_lbl.bind("<Button-1>", motion)


LiveLab = Label(tab5, text="LIVE VIDEO FEED")
LiveLab.place(x=750, y=390)
liveCanvas = Canvas(tab5, width=490, height=330)
liveCanvas.place(x=750, y=410)
live_frame = Frame(tab5, width=480, height=320)
live_frame.place(x=757, y=417)
live_lbl = Label(live_frame)
live_lbl.place(x=0, y=0)


template_frame = Frame(tab5, width=150, height=150)
template_frame.place(x=575, y=50)

template_lbl = Label(template_frame)
template_lbl.place(x=0, y=0)

FoundValuesLab = Label(tab5, text="FOUND VALUES")
FoundValuesLab.place(x=750, y=30)

CalValuesLab = Label(tab5, text="CALIBRATION VALUES")
CalValuesLab.place(x=900, y=30)


VisFileLocLab = Label(tab5, text="Vision File Location:")
VisCalPixLab = Label(tab5, text="Calibration Pixels:")
VisCalmmLab = Label(tab5, text="Calibration Robot MM:")
VisCalOxLab = Label(tab5, text="Orig: X")
VisCalOyLab = Label(tab5, text="Orig: Y")
VisCalXLab = Label(tab5, text="End: X")
VisCalYLab = Label(tab5, text="End: Y")

texts = [
    "Choose Vision Format",
    "X found position (mm)",
    "Y found position (mm)",
    "R found position (ang)",
    "X pixes returned from camera",
    "Y pixes returned from camera",
]
labels = [Label(tab5, text=t) for t in texts]

VisInTypeLab, VisXfoundLab, VisYfoundLab, VisRZfoundLab, VisXpixfoundLab, VisYpixfoundLab = labels

# TODO: finish abstracting labels above

### 5 BUTTONS################################################################
#############################################################################

try:
    graph = FilterGraph()
    camList = graph.get_input_devices()
except:
    camList = ["Select a Camera"]
visoptions = StringVar(tab5)
visoptions.set("Select a Camera")
vismenu = OptionMenu(tab5, visoptions, camList[0], *camList)
vismenu.config(width=20)
vismenu.place(x=10, y=10)


StartCamBut = Button(tab5, text="Start Camera", width=15, command=start_vid)
StartCamBut.place(x=200, y=10)

StopCamBut = Button(tab5, text="Stop Camera", width=15, command=stop_vid)
StopCamBut.place(x=315, y=10)

CapImgBut = Button(tab5, text="Snap Image", width=15, command=take_pic)
CapImgBut.place(x=10, y=50)

TeachImgBut = Button(tab5, text="Teach Object", width=15, command=selectTemplate)
TeachImgBut.place(x=140, y=50)

FindVisBut = Button(tab5, text="Snap & Find", width=15, command=snapFind)
FindVisBut.place(x=270, y=50)


ZeroBrCnBut = Button(tab5, text="Zero", width=5, command=zeroBrCn)
ZeroBrCnBut.place(x=10, y=110)

maskBut = Button(tab5, text="Mask", width=5, command=selectMask)
maskBut.place(x=10, y=150)


VisZoomSlide = Scale(tab5, from_=50, to=1, length=250, orient=HORIZONTAL)
VisZoomSlide.bind("<ButtonRelease-1>", VisUpdateBriCon)
VisZoomSlide.place(x=75, y=95)
VisZoomSlide.set(50)

VisZoomLab = Label(tab5, text="Zoom")
VisZoomLab.place(x=75, y=115)

VisBrightSlide = Scale(tab5, from_=-127, to=127, length=250, orient=HORIZONTAL)
VisBrightSlide.bind("<ButtonRelease-1>", VisUpdateBriCon)
VisBrightSlide.place(x=75, y=130)

VisBrightLab = Label(tab5, text="Brightness")
VisBrightLab.place(x=75, y=150)

VisContrastSlide = Scale(tab5, from_=-127, to=127, length=250, orient=HORIZONTAL)
VisContrastSlide.bind("<ButtonRelease-1>", VisUpdateBriCon)
VisContrastSlide.place(x=75, y=165)

VisContrastLab = Label(tab5, text="Contrast")
VisContrastLab.place(x=75, y=185)


fullRotCbut = Checkbutton(tab5, text="Full Rotation Search", variable=fullRot)
fullRotCbut.place(x=900, y=255)

pick180Cbut = Checkbutton(tab5, text="Pick Closest 180°", variable=pick180)
pick180Cbut.place(x=900, y=275)

pickClosestCbut = Checkbutton(tab5, text="Try Closest When Out of Range", variable=pickClosest)
pickClosestCbut.place(x=900, y=295)


saveCalBut = Button(tab5, text="SAVE VISION DATA", width=26, command=SaveAndApplyCalibration)
saveCalBut.place(x=915, y=340)


#### 5 ENTRY FIELDS##########################################################
#############################################################################


def make_entry_field(tab, text, x, y):
    """makes a new entry field"""

    field = Entry(tab, width=15)
    field.place(x, y)
    label = Label(tab, text)
    label.place(x, y + 20)
    return field, label


bgAutoCbut = Checkbutton(tab5, command=checkAutoBG, text="Auto", variable=autoBG)
bgAutoCbut.place(x=490, y=101)

a, b = make_entry_field(tab5, "Background Color", 390, 100)
VisBacColorEntryField, VisBacColorLab = a, b

a, b = make_entry_field(tab5, "Score Threshold", 390, 150)
VisScoreEntryField, VisScoreLab = a, b

# TODO: finish abstracting

VisRetScoreEntryField = Entry(tab5, width=15)
VisRetScoreEntryField.place(x=750, y=55)
VisRetScoreLab = Label(tab5, text="Scored Value")
VisRetScoreLab.place(x=750, y=75)

VisRetAngleEntryField = Entry(tab5, width=15)
VisRetAngleEntryField.place(x=750, y=105)
VisRetAngleLab = Label(tab5, text="Found Angle")
VisRetAngleLab.place(x=750, y=125)

VisRetXpixEntryField = Entry(tab5, width=15)
VisRetXpixEntryField.place(x=750, y=155)
VisRetXpixLab = Label(tab5, text="Pixel X Position")
VisRetXpixLab.place(x=750, y=175)

VisRetYpixEntryField = Entry(tab5, width=15)
VisRetYpixEntryField.place(x=750, y=205)
VisRetYpixLab = Label(tab5, text="Pixel Y Position")
VisRetYpixLab.place(x=750, y=225)

VisRetXrobEntryField = Entry(tab5, width=15)
VisRetXrobEntryField.place(x=750, y=255)
VisRetXrobLab = Label(tab5, text="Robot X Position")
VisRetXrobLab.place(x=750, y=275)

VisRetYrobEntryField = Entry(tab5, width=15)
VisRetYrobEntryField.place(x=750, y=305)
VisRetYrobLab = Label(tab5, text="Robot Y Position")
VisRetYrobLab.place(x=750, y=325)


VisX1PixEntryField = Entry(tab5, width=15)
VisX1PixEntryField.place(x=900, y=55)
VisX1PixLab = Label(tab5, text="X1 Pixel Pos")
VisX1PixLab.place(x=900, y=75)

VisY1PixEntryField = Entry(tab5, width=15)
VisY1PixEntryField.place(x=900, y=105)
VisY1PixLab = Label(tab5, text="Y1 Pixel Pos")
VisY1PixLab.place(x=900, y=125)

VisX2PixEntryField = Entry(tab5, width=15)
VisX2PixEntryField.place(x=900, y=155)
VisX2PixLab = Label(tab5, text="X2 Pixel Pos")
VisX2PixLab.place(x=900, y=175)

VisY2PixEntryField = Entry(tab5, width=15)
VisY2PixEntryField.place(x=900, y=205)
VisY2PixLab = Label(tab5, text="Y2 Pixel Pos")
VisY2PixLab.place(x=900, y=225)


VisX1RobEntryField = Entry(tab5, width=15)
VisX1RobEntryField.place(x=1010, y=55)
VisX1RobLab = Label(tab5, text="X1 Robot Pos")
VisX1RobLab.place(x=1010, y=75)

VisY1RobEntryField = Entry(tab5, width=15)
VisY1RobEntryField.place(x=1010, y=105)
VisY1RobLab = Label(tab5, text="Y1 Robot Pos")
VisY1RobLab.place(x=1010, y=125)

VisX2RobEntryField = Entry(tab5, width=15)
VisX2RobEntryField.place(x=1010, y=155)
VisX2RobLab = Label(tab5, text="X2 Robot Pos")
VisX2RobLab.place(x=1010, y=175)

VisY2RobEntryField = Entry(tab5, width=15)
VisY2RobEntryField.place(x=1010, y=205)
VisY2RobLab = Label(tab5, text="Y2 Robot Pos")
VisY2RobLab.place(x=1010, y=225)


VisFileLocEntryField = Entry(tab5, width=70)

VisPicOxPEntryField = Entry(tab5, width=5)
VisPicOxMEntryField = Entry(tab5, width=5)
VisPicOyPEntryField = Entry(tab5, width=5)
VisPicOyMEntryField = Entry(tab5, width=5)
VisPicXPEntryField = Entry(tab5, width=5)
VisPicXMEntryField = Entry(tab5, width=5)
VisPicYPEntryField = Entry(tab5, width=5)
VisPicYMEntryField = Entry(tab5, width=5)
VisXfindEntryField = Entry(tab5, width=5)
VisYfindEntryField = Entry(tab5, width=5)
VisRZfindEntryField = Entry(tab5, width=5)
VisXpixfindEntryField = Entry(tab5, width=5)
VisYpixfindEntryField = Entry(tab5, width=5)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 6

Elogframe = Frame(tab6)
Elogframe.place(x=40, y=15)
scrollbar = Scrollbar(Elogframe)
scrollbar.pack(side=RIGHT, fill=Y)
tab6.ElogView = Listbox(Elogframe, width=150, height=40, yscrollcommand=scrollbar.set)
try:
    Elog = pickle.load(open("ErrorLog", "rb"))
except:
    Elog = ["##BEGINNING OF LOG##"]
    pickle.dump(Elog, open("ErrorLog", "wb"))
time.sleep(0.2)
for item in Elog:
    tab6.ElogView.insert(END, item)
tab6.ElogView.pack()
scrollbar.config(command=tab6.ElogView.yview)


def clearLog():
    tab6.ElogView.delete(1, END)
    value = tab6.ElogView.get(0, END)
    pickle.dump(value, open("ErrorLog", "wb"))


clearLogBut = Button(tab6, text="Clear Log", width=26, command=clearLog)
clearLogBut.place(x=1000, y=630)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 7

link = Label(tab7, font="12", text="https://www.anninrobotics.com/tutorials", cursor="hand2")
link.bind("<Button-1>", lambda event: webbrowser.open(link.cget("text")))
link.place(x=10, y=9)


def callback():
    webbrowser.open_new(r"https://www.paypal.me/ChrisAnnin")


donateBut = Button(tab7, command=callback)
donatePhoto = PhotoImage(file="pp.gif")
donateBut.config(image=donatePhoto)
donateBut.place(x=1250, y=2)


scroll = Scrollbar(tab7)
scroll.pack(side=RIGHT, fill=Y)
configfile = Text(tab7, wrap=WORD, width=166, height=40, yscrollcommand=scroll.set)
filename = "information.txt"
with open(filename, "r", encoding="utf-8-sig") as file:
    configfile.insert(INSERT, file.read())
configfile.pack(side="left")
scroll.config(command=configfile.yview)
configfile.place(x=10, y=40)


####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################
####TAB 10

### 10 LABELS#################################################################
#############################################################################

testSendLab = Label(tab10, text="Test string to send to arduino")
testSendLab.place(x=10, y=20)

testRecLab = Label(tab10, text="Message echoed back from arduino")
testRecLab.place(x=10, y=70)

### 10 BUTTONS################################################################
#############################################################################

testSendBut = Button(tab10, text="SEND TO ARDUINO", command=TestString)
testSendBut.place(x=10, y=120)

testClearBut = Button(tab10, text="CLEAR RECEIVED", command=ClearTestString)
testClearBut.place(x=180, y=120)

#### 10 ENTRY FIELDS##########################################################
#############################################################################

testSendEntryField = Entry(tab10, width=222)
testSendEntryField.place(x=10, y=40)

testRecEntryField = Entry(tab10, width=222)
testRecEntryField.place(x=10, y=90)


##############################################################################################################################################################
### OPEN CAL FILE AND LOAD LIST ##############################################################################################################################
##############################################################################################################################################################

calibration = Listbox(tab2, height=60)

try:
    Cal = pickle.load(open("ARbot.cal", "rb"))
except:
    Cal = "0"
    pickle.dump(Cal, open("ARbot.cal", "wb"))
for item in Cal:
    calibration.insert(END, item)
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
J7axisLimPos = calibration.get("61")
J7rotation = calibration.get("62")
J7steps = calibration.get("63")
J7StepCur = calibration.get("64")  # is this used
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
J8length = calibration.get("93")
J8rotation = calibration.get("94")
J8steps = calibration.get("95")
J9length = calibration.get("96")
J9rotation = calibration.get("97")
J9steps = calibration.get("98")
J7calOff = calibration.get("99")
J8calOff = calibration.get("100")
J9calOff = calibration.get("101")


####

comPortEntryField.insert(0, str(comPort))
com2PortEntryField.insert(0, str(com2Port))
incrementEntryField.insert(0, "10")
speedEntryField.insert(0, "25")
ACCspeedField.insert(0, "10")
DECspeedField.insert(0, "10")
ACCrampField.insert(0, "100")
roundEntryField.insert(0, "0")
ProgEntryField.insert(0, (Prog))
SavePosEntryField.insert(0, "1")
R1EntryField.insert(0, "0")
R2EntryField.insert(0, "0")
R3EntryField.insert(0, "0")
R4EntryField.insert(0, "0")
R5EntryField.insert(0, "0")
R6EntryField.insert(0, "0")
R7EntryField.insert(0, "0")
R8EntryField.insert(0, "0")
R9EntryField.insert(0, "0")
R10EntryField.insert(0, "0")
R11EntryField.insert(0, "0")
R12EntryField.insert(0, "0")
R13EntryField.insert(0, "0")
R14EntryField.insert(0, "0")
R15EntryField.insert(0, "0")
R16EntryField.insert(0, "0")

for entry in sp_entries:
    entry.insert(0, "0")

servo0onEntryField.insert(0, str(Servo0on))
servo0offEntryField.insert(0, str(Servo0off))
servo1onEntryField.insert(0, str(Servo1on))
servo1offEntryField.insert(0, str(Servo1off))
DO1onEntryField.insert(0, str(DO1on))
DO1offEntryField.insert(0, str(DO1off))
DO2onEntryField.insert(0, str(DO2on))
DO2offEntryField.insert(0, str(DO2off))
TFxEntryField.insert(0, str(TFx))
TFyEntryField.insert(0, str(TFy))
TFzEntryField.insert(0, str(TFz))
TFrxEntryField.insert(0, str(TFrx))
TFryEntryField.insert(0, str(TFry))
TFrzEntryField.insert(0, str(TFrz))
J7curAngEntryField.insert(0, str(J7PosCur))
J8curAngEntryField.insert(0, str(J8PosCur))
J9curAngEntryField.insert(0, str(J9PosCur))
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
J1calOffEntryField.insert(0, str(J1calOff))
J2calOffEntryField.insert(0, str(J2calOff))
J3calOffEntryField.insert(0, str(J3calOff))
J4calOffEntryField.insert(0, str(J4calOff))
J5calOffEntryField.insert(0, str(J5calOff))
J6calOffEntryField.insert(0, str(J6calOff))
J7calOffEntryField.insert(0, str(J7calOff))
J8calOffEntryField.insert(0, str(J8calOff))
J9calOffEntryField.insert(0, str(J9calOff))
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
    lightTheme()
else:
    darkTheme()
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
axis7lengthEntryField.insert(0, str(J7axisLimPos))
axis7rotEntryField.insert(0, str(J7rotation))
axis7stepsEntryField.insert(0, str(J7steps))
VisBrightSlide.set(VisBrightVal)
VisContrastSlide.set(VisContVal)
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
VisZoomSlide.set(zoom)
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
axis8lengthEntryField.insert(0, str(J8length))
axis8rotEntryField.insert(0, str(J8rotation))
axis8stepsEntryField.insert(0, str(J8steps))
axis9lengthEntryField.insert(0, str(J9length))
axis9rotEntryField.insert(0, str(J9rotation))
axis9stepsEntryField.insert(0, str(J9steps))

setCom()
setCom2()

loadProg()
updateVisOp()
checkAutoBG()

msg = """
AR3 and AR4 are registered trademarks of Annin Robotics
Copyright © 2022 by Annin Robotics. All Rights Reserved
"""
tkinter.messagebox.showwarning("AR4 License / Copyright notice", msg)
xboxUse = 0


tabs['1'].mainloop()


# manEntryField.delete(0, 'end')
# manEntryField.insert(0,value)


def main():
    """docstring"""


if __name__ == "__main__":
    main()
