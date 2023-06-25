import os

from servo import DO
import os.path as osp
import tkinter as tk
from gui.base import GUI
import tkinter.ttk as ttk

import tkinter as tk

from gui.base import GUI, ButtonEntry, EntryField
from program import *
from servo import DO, RContainer, Servo


def build():
    """docstring"""
    GUI.tabs = GUI.tabs

    mk_label = lambda: tk.Label(GUI.tabs["3"], text="=")
    eq_labels = [mk_label() for _ in range(20)]

    eq_pos = [{"x": 70, "y": 12 + i * 40} for i in range(20)]
    for pos, label in zip(eq_pos, eq_labels):
        x, y = list(pos.values())
        label.place(x=x, y=y)

    io_labels = [
        "NOTE: the following are available when using the default Nano board for IO:   Inputs = 2-7  /  Outputs = 8-13  /  Servos = A0-A7",
        "If using IO on Teensy board:  Inputs = 32-36  /  Outputs = 37-41 - if using IO on Teensy you must manually change the command from 'Out On =' to 'ToutOn ='",
    ]
    io_labels = [tk.Label(GUI.tabs["3"], text=text) for text in io_labels]
    io_labels[0].place(x=10, y=640)
    io_labels[1].place(x=10, y=655)

    for _ in range(3):
        Servo(GUI.tabs["3"])

    for _ in range(6):
        DO(GUI.tabs["3"])
