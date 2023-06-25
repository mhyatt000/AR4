import os
import os.path as osp
import tkinter as tk
import tkinter.ttk as ttk

import calibrate
import controller
from exc import execution
import frames
from frames import AxisFrame, ExtJointFrame, JointFrame, ToolFrame
from gui.base import GUI, EntryField
import teach
import theme
from joint import JointCTRL


def build():
    """docstring"""

    ToolFrame(GUI.tabs["2"], 0, 0, "x")
    ToolFrame(GUI.tabs["2"], 0, 1, "y")
    ToolFrame(GUI.tabs["2"], 0, 2, "z")
    #
    ToolFrame(GUI.tabs["2"], 1, 0, "rx")
    ToolFrame(GUI.tabs["2"], 1, 1, "ry")
    ToolFrame(GUI.tabs["2"], 1, 2, "rz")

    almStatusLab2 = ttk.Label(
        GUI.tabs["2"], text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel"
    )
    almStatusLab2.place(x=25, y=20)

    ToolFrameLab = ttk.Label(GUI.tabs["2"], text="Tool Frame Offset")
    ToolFrameLab.place(x=970, y=60)

    UFxLab = ttk.Label(GUI.tabs["2"], font=("Arial", 11), text="X")
    UFxLab.place(x=920, y=90)

    UFyLab = ttk.Label(GUI.tabs["2"], font=("Arial", 11), text="Y")
    UFyLab.place(x=960, y=90)

    UFzLab = ttk.Label(GUI.tabs["2"], font=("Arial", 11), text="Z")
    UFzLab.place(x=1000, y=90)

    UFRxLab = ttk.Label(GUI.tabs["2"], font=("Arial", 11), text="Rz")
    UFRxLab.place(x=1040, y=90)

    UFRyLab = ttk.Label(GUI.tabs["2"], font=("Arial", 11), text="Ry")
    UFRyLab.place(x=1080, y=90)

    UFRzLab = ttk.Label(GUI.tabs["2"], font=("Arial", 11), text="Rx")
    UFRzLab.place(x=1120, y=90)

    comLab = ttk.Label(GUI.tabs["2"], text="Communication")
    comLab.place(x=72, y=60)

    jointCalLab = ttk.Label(GUI.tabs["2"], text="Robot Calibration")
    jointCalLab.place(x=290, y=60)

    axis7Lab = ttk.Label(GUI.tabs["2"], text="7th Axis Calibration")
    axis7Lab.place(x=665, y=300)

    axis7lengthLab = ttk.Label(GUI.tabs["2"], text="7th Axis Length:")
    axis7lengthLab.place(x=651, y=340)

    axis7rotLab = ttk.Label(GUI.tabs["2"], text="MM per Rotation:")
    axis7rotLab.place(x=645, y=370)

    axis7stepsLab = ttk.Label(GUI.tabs["2"], text="Drive Steps:")
    axis7stepsLab.place(x=675, y=400)

    axis7pinsetLab = ttk.Label(
        GUI.tabs["2"], font=("Arial", 8), text="StepPin = 12 / DirPin = 13 / CalPin = 36"
    )
    axis7pinsetLab.place(x=627, y=510)

    axis8pinsetLab = ttk.Label(
        GUI.tabs["2"], font=("Arial", 8), text="StepPin = 32 / DirPin = 33 / CalPin = 37"
    )
    axis8pinsetLab.place(x=827, y=510)

    axis9pinsetLab = ttk.Label(
        GUI.tabs["2"], font=("Arial", 8), text="StepPin = 34 / DirPin = 35 / CalPin = 38"
    )
    axis9pinsetLab.place(x=1027, y=510)

    axis8Lab = ttk.Label(GUI.tabs["2"], text="8th Axis Calibration")
    axis8Lab.place(x=865, y=300)

    axis8lengthLab = ttk.Label(GUI.tabs["2"], text="8th Axis Length:")
    axis8lengthLab.place(x=851, y=340)

    axis8rotLab = ttk.Label(GUI.tabs["2"], text="MM per Rotation:")
    axis8rotLab.place(x=845, y=370)

    axis8stepsLab = ttk.Label(GUI.tabs["2"], text="Drive Steps:")
    axis8stepsLab.place(x=875, y=400)

    axis9Lab = ttk.Label(GUI.tabs["2"], text="9th Axis Calibration")
    axis9Lab.place(x=1065, y=300)

    axis9lengthLab = ttk.Label(GUI.tabs["2"], text="9th Axis Length:")
    axis9lengthLab.place(x=1051, y=340)

    axis9rotLab = ttk.Label(GUI.tabs["2"], text="MM per Rotation:")
    axis9rotLab.place(x=1045, y=370)

    axis9stepsLab = ttk.Label(GUI.tabs["2"], text="Drive Steps:")
    axis9stepsLab.place(x=1075, y=400)

    CalibrationOffsetsLab = ttk.Label(GUI.tabs["2"], text="Calibration Offsets")
    CalibrationOffsetsLab.place(x=485, y=60)

    J1calLab = ttk.Label(GUI.tabs["2"], text="J1 Offset")
    J1calLab.place(x=480, y=90)

    J2calLab = ttk.Label(GUI.tabs["2"], text="J2 Offset")
    J2calLab.place(x=480, y=120)

    J3calLab = ttk.Label(GUI.tabs["2"], text="J3 Offset")
    J3calLab.place(x=480, y=150)

    J4calLab = ttk.Label(GUI.tabs["2"], text="J4 Offset")
    J4calLab.place(x=480, y=180)

    J5calLab = ttk.Label(GUI.tabs["2"], text="J5 Offset")
    J5calLab.place(x=480, y=210)

    J6calLab = ttk.Label(GUI.tabs["2"], text="J6 Offset")
    J6calLab.place(x=480, y=240)

    J7calLab = ttk.Label(GUI.tabs["2"], text="J7 Offset")
    J7calLab.place(x=480, y=280)

    J8calLab = ttk.Label(GUI.tabs["2"], text="J8 Offset")
    J8calLab.place(x=480, y=310)

    J9calLab = ttk.Label(GUI.tabs["2"], text="J9 Offset")
    J9calLab.place(x=480, y=340)

    CalibrationOffsetsLab = ttk.Label(GUI.tabs["2"], text="Encoder Control")
    CalibrationOffsetsLab.place(x=715, y=60)

    cmdSentLab = ttk.Label(GUI.tabs["2"], text="Last Command Sent to Controller")
    cmdSentLab.place(x=10, y=565)

    cmdRecLab = ttk.Label(GUI.tabs["2"], text="Last Response From Controller")
    cmdRecLab.place(x=10, y=625)

    ToolFrameLab = ttk.Label(GUI.tabs["2"], text="Theme")
    ToolFrameLab.place(x=1225, y=60)

    ### 2 BUTTONS################################################################
    #############################################################################

    lightBut = tk.Button(GUI.tabs["2"], text="  Light  ", command=theme.light_theme)
    lightBut.place(x=1190, y=90)

    darkBut = tk.Button(GUI.tabs["2"], text="  Dark   ", command=theme.dark_theme)
    darkBut.place(x=1250, y=90)

    autoCalBut = tk.Button(GUI.tabs["2"], text="  Auto Calibrate  ", command=calibrate.calRobotAll)
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
            tk.Checkbutton(GUI.tabs["2"], text=J.name, variable=J.no_calibrate),
            tk.Checkbutton(GUI.tabs["2"], text=J.name, variable=J.no_calibrate2),
        ]
        btns[0].place(**cal_pos[J.name][0])
        btns[1].place(**cal_pos[J.name][1])
        cal_btns[J.name] = btns

    J7zerobut = tk.Button(
        GUI.tabs["2"], text="Set Axis 7 Calibration to Zero", width=28, command=calibrate.zeroAxis7
    )
    J7zerobut.place(x=627, y=440)

    J8zerobut = tk.Button(
        GUI.tabs["2"], text="Set Axis 8 Calibration to Zero", width=28, command=calibrate.zeroAxis8
    )
    J8zerobut.place(x=827, y=440)

    J9zerobut = tk.Button(
        GUI.tabs["2"], text="Set Axis 9 Calibration to Zero", width=28, command=calibrate.zeroAxis9
    )
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
        btn = tk.Button(
            GUI.tabs["2"], text=f"Calibrate {J.name} Only", command=lambda: calRobot(J.idx)
        )
        btn.place(**autocal_pos[J.name])
        autocal_btns[J.name] = btn

    CalZeroBut = tk.Button(
        GUI.tabs["2"], text="Force Cal. to 0° Home", width=20, command=calibrate.CalZeroPos
    )
    CalZeroBut.place(x=270, y=425)

    CalRestBut = tk.Button(
        GUI.tabs["2"], text="Force Cal. to Vert. Rest", width=20, command=calibrate.CalRestPos
    )
    CalRestBut.place(x=270, y=460)

    # NOTE tag for grep OpenLoop open_loop
    mk_autocal = lambda J: dict(
        x=665, y=90 + 20 * J.idx, text="{J.name} Open Loop (disable encoder)"
    )
    autocal_pos = [mk_autocal(J) for J in JointCTRL.main]
    for J, item in zip(JointCTRL.main, autocal_pos):
        btn = tk.Checkbutton(GUI.tabs["2"], text=item["text"], variable=J.open_loop)
        btn.place(x=item["x"], y=item["y"])

    saveCalBut = tk.Button(
        GUI.tabs["2"], text="    SAVE    ", width=26, command=calibrate.SaveAndApplyCalibration
    )
    saveCalBut.place(x=1150, y=630)

    #### 2 ENTRY FIELDS##########################################################
    #############################################################################

    cmdSentEntryField = tk.Entry(GUI.tabs["2"], width=95)
    EntryField(GUI.tabs["2"], name="cmd_sent", width=95)

    # TODO needs to be placed
    EntryField(GUI.tabs["2"], name="cmd_rec", width=95)

    caloff_entry_pos = [dict(x=540, y=90 + 30 * J.idx) for J in JointCTRL.active]
    for J in JointCTRL.active:
        x, y = caloff_entry_pos[J.idx].values()
        J.caloff_entry = tk.Entry(GUI.tabs["2"], width=8)
        J.caloff_entry.place(x=x, y=y)

    # NOTE this was axis7lengthEntryField
    mk_entry = lambda: tk.Entry(GUI.tabs["2"], width=6)
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
