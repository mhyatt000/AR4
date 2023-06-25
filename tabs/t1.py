
import frames
import controller
from exc import execution
import calibrate
import teach
from frames import JointFrame , ExtJointFrame, AxisFrame, ToolFrame
from gui.base import GUI, EntryField
import os
import os.path as osp
import tkinter as tk
from gui.base import GUI
import tkinter.ttk as ttk

import program


def build():
    """docstring"""

    # left side
    left = ttk.Frame(GUI.tabs["1"])
    left.grid(row=0, column=0, sticky="nsew")

    # right side
    right = ttk.Frame(GUI.tabs["1"])
    right.grid(row=0, column=1, sticky="nsew", padx=10)


    CartjogFrame = ttk.Frame(GUI.tabs["1"])
    CartjogFrame.place(x=330, y=0)


    curRowLab = ttk.Label(left, text="Current Row:")
    curRowLab.grid(row=0, column=0)

    almStatusLab = ttk.Label(left, text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel")
    almStatusLab.grid(row=1, column=0)

    xbcStatusLab = ttk.Label(left, text="Xbox OFF")
    xbcStatusLab.grid(row=2, column=0)

    runStatusLab = ttk.Label(left, text="PROGRAM STOPPED")
    runStatusLab.grid(row=3, column=0)


    ProgLab = ttk.Label(left, text="Program:")
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
    axes = ttk.Frame(right, width=450)
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

    fields = ttk.Frame(left)
    fields.grid(row=11, column=0)

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

    ###BUTTONS################################################################
    ##########################################################################


    def posRegFieldVisible(self):
        curCmdtype = options.get()
        if curCmdtype == "Move PR" or curCmdtype == "OFF PR " or curCmdtype == "Teach PR":
            SavePosEntryField.place(x=780, y=183)
        else:
            SavePosEntryField.place_forget()


    subframes = dict()
    subframes["btn"] = ttk.Frame(right, width=500)
    subframes["btn"].grid(row=4, column=0, columnspan=3, sticky="nsew", pady=20)

    manInsBut = tk.Button(subframes["btn"], text="  Insert  ", command=program.manInsItem)
    manRepBut = tk.Button(subframes["btn"], text="Replace", command=program.manReplItem)
    getSelBut = tk.Button(subframes["btn"], text="Get Selected", command=program.getSel)
    speed_option = tk.StringVar(subframes["btn"])
    GUI.register('speed_option',speed_option)
    speedMenu = tk.OptionMenu(subframes["btn"], speed_option, "Percent", "Percent", "Seconds", "mm per Sec")
    teachInsBut = tk.Button(subframes["btn"], text="Teach New Position", command=teach.teachInsertBelSelected)
    teachReplaceBut = tk.Button(subframes["btn"], text="Modify Position", command=teach.teachReplaceSelected)
    deleteBut = tk.Button(subframes["btn"], text="Delete", command=program.deleteitem)
    CalibrateBut = tk.Button(subframes["btn"], text="Auto Calibrate CMD", command=program.insCalibrate)
    camOnBut = tk.Button(subframes["btn"], text="Camera On", command=program.cameraOn)
    camOffBut = tk.Button(subframes["btn"], text="Camera Off", command=program.cameraOff)

    # single tk.Buttons

    options = tk.StringVar(left)
    menu = ttk.OptionMenu(
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

    waitTimeBut = tk.Button(subframes["btn"], text="Wait Time (seconds)", command=program.waitTime)
    waitInputOnBut = tk.Button(subframes["btn"], text="Wait Input ON", command=program.waitInputOn)
    waitInputOffBut = tk.Button(subframes["btn"], text="Wait Input OFF", command=program.waitInputOff)
    setOutputOnBut = tk.Button(subframes["btn"], text="Set Output On", command=program.setOutputOn)
    setOutputOffBut = tk.Button(subframes["btn"], text="Set Output OFF", command=program.setOutputOff)
    tabNumBut = tk.Button(subframes["btn"], text="Create Tab", command=program.tabNumber)
    jumpTabBut = tk.Button(subframes["btn"], text="Jump to Tab", command=program.jumpTab)

    subframes["fields"] = fields

    EntryField(subframes["fields"], name="waitTime")
    EntryField(subframes["fields"], name="waitInput")
    EntryField(subframes["fields"], name="waitInputOff")
    EntryField(subframes["fields"], name="outputOn")
    EntryField(subframes["fields"], name="outputOff")
    EntryField(subframes["fields"], name="tabNum")
    EntryField(subframes["fields"], name="jumpTab")

    # buttons with multiple entry

    IfOnjumpTabBut = tk.Button(subframes["btn"], text="If On Jump", command=program.IfOnjumpTab)
    IfOffjumpTabBut = tk.Button(subframes["btn"], text="If Off Jump", command=program.IfOffjumpTab)
    servoBut = tk.Button(subframes["btn"], text="Servo", command=program.move_servo)
    RegNumBut = tk.Button(subframes["btn"], text="Register", command=program.insertRegister)
    RegJmpBut = tk.Button(subframes["btn"], text="If Register Jump", command=program.IfRegjumpTab)
    StorPosBut = tk.Button(subframes["btn"], text="Position Register", command=program.storPos)
    callBut = tk.Button(subframes["btn"], text="Call Program", command=program.insertCallProg)
    returnBut = tk.Button(subframes["btn"], text="Return", command=program.insertReturn)
    visFindBut = tk.Button(subframes["btn"], text="Vision Find", command=program.insertvisFind)

    EntryField(subframes["fields"], name="IfOnjumpInputTab")
    EntryField(subframes["fields"], name="IfOnjumpNumberTab")
    EntryField(subframes["fields"], name="IfOffjumpInputTab")
    EntryField(subframes["fields"], name="IfOffjumpNumberTab")
    EntryField(subframes["fields"], name="servoNum")
    EntryField(subframes["fields"], name="servoPos")
    EntryField(subframes["fields"], name="regNum")
    EntryField(subframes["fields"], name="regEq")
    EntryField(subframes["fields"], name="regNumJmp")
    EntryField(subframes["fields"], name="regEqJmp")
    EntryField(subframes["fields"], name="regTabJmp")
    EntryField(subframes["fields"], name="storPosNum")
    EntryField(subframes["fields"], name="storPosEl")
    EntryField(subframes["fields"], name="storPosVal")
    EntryField(subframes["fields"], name="changeProg")
    EntryField(subframes["fields"], name="visPass")
    EntryField(subframes["fields"], name="visFail")

    ProgBut = tk.Button(subframes["btn"], text="Load Program", command=program.loadProg)
    revBut = tk.Button(subframes["btn"], text="REV ", command=execution.stepRev)
    fwdBut = tk.Button(subframes["btn"], text="FWD", command=execution.stepFwd)
    ResetDriveBut = tk.Button(subframes["btn"], text="Reset Drives", command=calibrate.ResetDrives)
    IncJogCbut = tk.Checkbutton(subframes["btn"], text="Incremental Jog", variable=GUI.is_increment)

    runProgBut = tk.Button(subframes["btn"], command=execution.runProg)
    playPhoto = tk.PhotoImage(file=osp.join(GUI.assets, "play-icon.gif"))
    runProgBut.config(image=playPhoto)

    xboxBut = tk.Button(subframes["btn"], command=controller.xbox)
    xboxPhoto = tk.PhotoImage(file=osp.join(GUI.assets, "xbox.gif"))
    xboxBut.config(image=xboxPhoto)

    stopProgBut = tk.Button(subframes["btn"], command=calibrate.stopProg)
    stopPhoto = tk.PhotoImage(file=osp.join(GUI.assets, "stop-icon.gif"))
    stopProgBut.config(image=stopPhoto)

    frames.assign_grid(subframes["btn"], 5, 5)
    frames.assign_grid(subframes["fields"], 2, 2)
