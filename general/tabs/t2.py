import os
import os.path as osp
import tkinter as tk
import tkinter.ttk as ttk

import calibrate
from com import COM
import controller
from exc import execution
import frames
from frames import AxisFrame, ExtJointFrame, JointFrame, ToolFrame
from gui.base import GUI, EntryField
from joint import  JointCTRL
from calibrate import ExtJointCal, JointCal 
import teach
import theme
import util


def build_header(header):
    """docstring"""

    almStatusLab2 = ttk.Label(header, text="SYSTEM READY - NO ACTIVE ALARMS", style="OK.TLabel")
    COM.register_alm(almStatusLab2)
    COM.build(header)

    util.hgrid(header)


def build_left(left):
    """docstring"""

    autoCalBut = ttk.Button(left, text="Auto Calibrate Selected", command=calibrate.cal_all)

    J7zerobut = ttk.Button(left, text="Set Axis 7 Calibration to Zero", command=calibrate.zeroAxis7)
    J8zerobut = ttk.Button(left, text="Set Axis 8 Calibration to Zero", command=calibrate.zeroAxis8)
    J9zerobut = ttk.Button(left, text="Set Axis 9 Calibration to Zero", command=calibrate.zeroAxis9)

    CalZeroBut = ttk.Button(
        left, text="Force Cal. to 0° Home", width=20, command=calibrate.CalZeroPos
    )
    CalRestBut = ttk.Button(
        left, text="Force Cal. to Vert. Rest", width=20, command=calibrate.CalRestPos
    )

    # jointCalLab = ttk.Label(left, text="Robot Calibration")

    # CalibrationOffsetsLab = ttk.Label(left, text="Calibration Offsets")
    # CalibrationOffsetsLab = ttk.Label(left, text="Encoder Control")

    util.vgrid(left)


def build_mid(mid):
    """docstring"""

    for _ in range(6):
        JointCal(mid)
    for _ in range(3):
        ExtJointCal(mid)


def build_right(right):
    """docstring"""

    ToolFrameLab = ttk.Label(right, text="Theme")
    lightBut = ttk.Button(right, text="Light", command=theme.light_theme)
    darkBut = ttk.Button(right, text="Dark", command=theme.dark_theme)

    # TODO tab 2 needs a tool frame offset not TF jog
    # use EntryField
    #
    # ToolFrame(right, 0, 0, "x")
    # ToolFrame(right, 0, 1, "y")
    # ToolFrame(right, 0, 2, "z")
    #
    # ToolFrame(right, 1, 0, "rx")
    # ToolFrame(right, 1, 1, "ry")
    # ToolFrame(right, 1, 2, "rz")

    ToolFrameLab = ttk.Label(right, text="Tool Frame Offset")

    UFxLab = ttk.Label(right, font=("Arial", 11), text="X")
    UFyLab = ttk.Label(right, font=("Arial", 11), text="Y")
    UFzLab = ttk.Label(right, font=("Arial", 11), text="Z")
    UFRxLab = ttk.Label(right, font=("Arial", 11), text="Rz")
    UFRyLab = ttk.Label(right, font=("Arial", 11), text="Ry")
    UFRzLab = ttk.Label(right, font=("Arial", 11), text="Rx")

    util.vgrid(right)


def build_footer(footer):
    """docstring"""

    cmd_sent = EntryField(footer, name="cmd_sent", alt="Last Command Sent to Controller")
    cmd_rec = EntryField(footer, name="cmd_rec", alt="Last Response From Controller")

    saveCalBut = ttk.Button(
        footer, text="    SAVE    ", width=26, command=calibrate.SaveAndApplyCalibration
    )

    util.hgrid(footer)


def build():
    """docstring"""

    components = util.build_components(GUI.tabs["2"])

    build_header(components["header"])
    build_left(components["left"])
    build_mid(components["mid"])
    build_right(components["right"])
    build_footer(components["footer"])
