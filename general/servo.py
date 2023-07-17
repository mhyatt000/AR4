import load
import tkinter as tk

from gui.base import GUI, ButtonEntry, EntryField
from program import *


class Servo():
    """GUI for servo"""

    active = []

    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.idx = len(Servo.active)
        self.name = f"servo{self.idx}"

        self.on = ButtonEntry(self.frame, name=f"{self.name}_on")
        self.off = ButtonEntry(self.frame, name=f"{self.name}_off")

        self.on.command = lambda : Servo.command(self.on, on=True)
        self.off.command = lambda : Servo.command(self.off, on=False)

        Servo.active.append(self)

        self.on.entry.insert(0, str(self.on.func))
        self.off.entry.insert(0, str(self.off.func))


    @classmethod
    def command(cls, obj, on=True):
        load.save_cfg()
        servoPos = obj.entry.get()
        command = f"SV0P{servoPos}\n"
        COM.write(command, serial_idx=1)



class DO():
    """what is this?"""

    active = []

    def __init__(self, parent):
        self.frame = tk.Frame(parent)

        self.idx = len(DO.active)
        self.name = f"DO{self.idx}"

        self.on = ButtonEntry(self.frame, name=f"{self.name}_on")
        self.off = ButtonEntry(self.frame, name=f"{self.name}_off")

        self.on.command = lambda : DO.command(self.on, on=True)
        self.off.command = lambda : DO.command(self.off, on=False)

        DO.active.append(self)

        self.on.entry.insert(0, str(self.on.func))
        self.off.entry.insert(0, str(self.off.func))

    @classmethod
    def command(cls, obj, on=True):
        """
        what is this function?
        maybe for arduino...
        """

        value = obj.entry.get()
        command = f'{"ONX" if on else "OFX"}{val}\n'
        COM.write(command, serial_idx=1)



class RContainer:

    active = []

    def __init__(self, parent):

        self.idx = len(RContainer.active)
        self.name = f"R{self.idx}"
        self.frame = tk.Frame(parent)

        self.label = tk.Label(self.frame, text=self.name)
        self.label.grid(row=0, column=0)

        self.entry = tk.Entry(self.frame, width=5)
        self.entry.grid(row=0, column=1)
        self.entry.insert(0, "0")
