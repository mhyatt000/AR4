import os
import util
from com import COM
import os.path as osp
import tkinter as tk
import tkinter.ttk as ttk

import calibrate
import controller
from exc import execution
import frames
from frames import AxisFrame, ExtJointFrame, JointFrame, ToolFrame
from gui.base import GUI, EntryField
import program
import teach


def posRegFieldVisible(self):
    curCmdtype = options.get()
    if curCmdtype == "Move PR" or curCmdtype == "OFF PR " or curCmdtype == "Teach PR":
        SavePosEntryField.place(x=780, y=183)
    else:
        SavePosEntryField.place_forget()

def build_header(header):
    """docstring"""

    almStatusLab = ttk.Label(header, text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel")
    fields = ttk.Frame(header)
    build_fields(fields)
    COM.register_alm(almStatusLab)
    util.vgrid(header)

def build_fields(fields):
    """docstring"""

    # curRowLab = ttk.Label(fields, text="Current Row:")
    # curRowLab.grid(row=0, column=0)

    # xbcStatusLab = ttk.Label(fields, text="Xbox OFF")
    # xbcStatusLab.grid(row=2, column=0)

    # runStatusLab = ttk.Label(fields, text="PROGRAM STOPPED")
    # runStatusLab.grid(row=3, column=0)

    # ProgLab = ttk.Label(fields, text="Program:")
    # ProgLab.grid(row=4, column=0)

    # TODO: how to clean this up?

    EntryField(fields, name="increment")
    EntryField(fields, name="curRow")
    EntryField(fields, name="man")
    EntryField(fields, name="prog")
    EntryField(fields, name="speed")
    EntryField(fields, name="ACCspeed", alt="Acceleration (%)")
    EntryField(fields, name="DECspeed", alt="Decceleration (%)")
    EntryField(fields, name="ACCramp", alt="Acceleration Ramp (%)")
    EntryField(fields, name="round", alt="Rounding (mm)")
    EntryField(fields, name="savepos")

    EntryField(fields, name="waitTime")
    EntryField(fields, name="waitInput")
    EntryField(fields, name="waitInputOff")
    EntryField(fields, name="outputOn")
    EntryField(fields, name="outputOff")
    EntryField(fields, name="tabNum")
    EntryField(fields, name="jumpTab")

    EntryField(fields, name="IfOnjumpInputTab")
    EntryField(fields, name="IfOnjumpNumberTab")
    EntryField(fields, name="IfOffjumpInputTab")
    EntryField(fields, name="IfOffjumpNumberTab")
    EntryField(fields, name="servoNum")
    EntryField(fields, name="servoPos")
    EntryField(fields, name="regNum")
    EntryField(fields, name="regEq")
    EntryField(fields, name="regNumJmp")
    EntryField(fields, name="regEqJmp")
    EntryField(fields, name="regTabJmp")
    EntryField(fields, name="storPosNum")
    EntryField(fields, name="storPosEl")
    EntryField(fields, name="storPosVal")
    EntryField(fields, name="changeProg")
    EntryField(fields, name="visPass")
    EntryField(fields, name="visFail")

    util.vgrid(fields, depth=7)


def build_mid(mid):
    """docstring"""

    kwargs = dict(padx=15, pady=10)
    sf = ttk.Frame(mid)

    for _ in range(6):
        JointFrame(sf),
    for _ in range(3):
        ExtJointFrame(sf),

    util.vgrid(sf,depth=3, **kwargs)

    sf = ttk.Frame(mid)

    AxisFrame(sf, "x")
    AxisFrame(sf, "y")
    AxisFrame(sf, "z")
    AxisFrame(sf, "rz")
    AxisFrame(sf, "ry")
    AxisFrame(sf, "rx")
    #
    AxisFrame(sf, "tx")
    AxisFrame(sf, "ty")
    AxisFrame(sf, "tz")
    AxisFrame(sf, "trz")
    AxisFrame(sf, "try")
    AxisFrame(sf, "trx")

    util.vgrid(sf,depth=6, **kwargs)
    util.vgrid(mid, **kwargs)


def build_footer(footer):
    """docstring"""

    manInsBut = ttk.Button(footer, text="  Insert  ", command=program.manInsItem)
    manRepBut = ttk.Button(footer, text="Replace", command=program.manReplItem)
    getSelBut = ttk.Button(footer, text="Get Selected", command=program.getSel)
    speed_option = tk.StringVar(footer)
    GUI.register("speed_option", speed_option)
    speedMenu = ttk.OptionMenu(
        footer, speed_option, "Percent", "Percent", "Seconds", "mm per Sec"
    )
    teachInsBut = ttk.Button(
        footer, text="Teach New Position", command=teach.teachInsertBelSelected
    )
    teachReplaceBut = ttk.Button(
        footer, text="Modify Position", command=teach.teachReplaceSelected
    )
    deleteBut = ttk.Button(footer, text="Delete", command=program.deleteitem)
    CalibrateBut = ttk.Button(
        footer, text="Auto Calibrate CMD", command=program.insCalibrate
    )
    camOnBut = ttk.Button(footer, text="Camera On", command=program.cameraOn)
    camOffBut = ttk.Button(footer, text="Camera Off", command=program.cameraOff)

    # single ttk.Buttons

    options = tk.StringVar(footer)
    menu = ttk.OptionMenu(
        footer,
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

    waitTimeBut = ttk.Button(footer, text="Wait Time (seconds)", command=program.waitTime)
    waitInputOnBut = ttk.Button(footer, text="Wait Input ON", command=program.waitInputOn)
    waitInputOffBut = ttk.Button(
        footer, text="Wait Input OFF", command=program.waitInputOff
    )
    setOutputOnBut = ttk.Button(footer, text="Set Output On", command=program.setOutputOn)
    setOutputOffBut = ttk.Button(
        footer, text="Set Output OFF", command=program.setOutputOff
    )
    tabNumBut = ttk.Button(footer, text="Create Tab", command=program.tabNumber)
    jumpTabBut = ttk.Button(footer, text="Jump to Tab", command=program.jumpTab)

    # buttons with multiple entry

    IfOnjumpTabBut = ttk.Button(footer, text="If On Jump", command=program.IfOnjumpTab)
    IfOffjumpTabBut = ttk.Button(footer, text="If Off Jump", command=program.IfOffjumpTab)
    servoBut = ttk.Button(footer, text="Servo", command=program.move_servo)
    RegNumBut = ttk.Button(footer, text="Register", command=program.insertRegister)
    RegJmpBut = ttk.Button(footer, text="If Register Jump", command=program.IfRegjumpTab)
    StorPosBut = ttk.Button(footer, text="Position Register", command=program.storPos)
    callBut = ttk.Button(footer, text="Call Program", command=program.insertCallProg)
    returnBut = ttk.Button(footer, text="Return", command=program.insertReturn)
    visFindBut = ttk.Button(footer, text="Vision Find", command=program.insertvisFind)

    ProgBut = ttk.Button(footer, text="Load Program", command=program.loadProg)
    revBut = ttk.Button(footer, text="REV ", command=execution.stepRev)
    fwdBut = ttk.Button(footer, text="FWD", command=execution.stepFwd)
    ResetDriveBut = ttk.Button(footer, text="Reset Drives", command=calibrate.ResetDrives)
    IncJogCbut = ttk.Checkbutton(footer, text="Incremental Jog", variable=GUI.is_increment)

    runProgBut = ttk.Button(footer, command=execution.runProg)
    runProgBut.photo= tk.PhotoImage(file=osp.join(GUI.assets, "play-icon.gif"))
    runProgBut.config(image=runProgBut.photo)

    xboxBut = ttk.Button(footer, command=controller.xbox)
    xboxBut.photo= tk.PhotoImage(file=osp.join(GUI.assets, "xbox.gif"))
    xboxBut.config(image=xboxBut.photo)

    stopProgBut = ttk.Button(footer, command=calibrate.stopProg)
    stopProgBut.photo= tk.PhotoImage(file=osp.join(GUI.assets, "stop-icon.gif"))
    stopProgBut.config(image=stopProgBut.photo)
    util.vgrid(footer, depth=10)

def build():
    """docstring"""

    components = util.build_components(GUI.tabs['1'])

    build_header(components['header'])
    build_mid(components['mid'])
    build_footer(components['footer'])

