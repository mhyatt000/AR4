import tkinter as tk
from tkinter import ttk

from jog import jog_cmd
from joint import JointCTRL


def assign_grid(parent, nrow, ncol):

    items = list(parent.children.values())
    for i, item in enumerate(items):
        row = i // ncol
        col = i % ncol
        item.grid(row=row, column=col)


def center(widget):
    """docstring"""
    widget.rowconfigure(0, weight=1)
    widget.columnconfigure(0, weight=1)


def center_child(frame):
    """docstring"""

    rows = frame.grid_size()[1]
    columns = frame.grid_size()[0]

    for row in range(rows):
        frame.grid_rowconfigure(row, weight=1)
    for column in range(columns):
        frame.grid_columnconfigure(column, weight=1)


class JointFrame:
    """a GUI frame for a joint"""

    active = []

    def __init__(self, parent, x, y):

        self.ctrl = JointCTRL(self)

        self.frame = tk.Frame(parent, width=340, height=50)
        self.frame.grid(row=x, column=y, sticky="nsew")

        self.entry = tk.Entry(self.frame, width=5)
        # self.entry.place(x=35, y=9)
        self.entry.grid(row=0, column=1, sticky="nsew")

        self.locations = {
            "main": dict(row=0, column=0, rowspan=2, sticky="nsew"),
            "neg": dict(row=0, column=1, sticky="nsew"),
            "pos": dict(row=0, column=3, sticky="nsew"),
            "slide": dict(row=0, column=2, sticky="nsew"),
        }

        self.mk_labels()
        self.mk_buttons()
        self.mk_slider(180)
        JointFrame.active.append(self)

    def mk_buttons(self):
        """makes jogging buttons"""

        button = lambda text: tk.Button(self.frame, text=text, width=3)
        self.buttons = {
            "neg": button("-"),
            "pos": button("+"),
        }
        for col, (k, button) in zip([1, 3], self.buttons.items()):
            button.bind("<ButtonRelease>", lambda *args : jog_cmd.stop_jog())
            button.grid(row=1, column=col, sticky="nsew")

        self.buttons["neg"].bind("<ButtonPress>", lambda *args : jog_cmd.joint_jog(self.ctrl.idx, 5))
        self.buttons["pos"].bind("<ButtonPress>", lambda *args : jog_cmd.joint_jog(self.ctrl.idx, 5))

    def mk_labels(self):
        """docstring"""

        self.labels = {
            "main": ttk.Label(self.frame, font=("Arial", 18), text=self.ctrl.name),
            "neg": ttk.Label(
                self.frame,
                font=("Arial", 8),
                text=str(-self.ctrl.limits["neg"]),
                # style="Jointlim.TLabel",
            ),
            "pos": ttk.Label(
                self.frame,
                font=("Arial", 8),
                text=str(self.ctrl.limits["pos"]),
                style="Jointlim.TLabel",
            ),
            "slide": ttk.Label(self.frame),
        }

        for k, label in self.labels.items():
            loc = self.locations[k]
            label.grid(**loc)

    def mk_slider(self, length):
        """makes slider"""

        self.slider = tk.Scale(
            self.frame,
            from_=-self.ctrl.limits["neg"],
            to=self.ctrl.limits["pos"],
            length=length,
            orient=tk.HORIZONTAL,
            command=self.sliderUpdate,
        )
        self.slider.bind("<ButtonRelease-1>", self.sliderExecute)
        # self.slider.place(x=x, y=y)
        self.slider.grid(row=1, column=2, sticky="nsew")

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
        is_increment = int(GUI.is_increment.get())
        if is_increment :
            J1jogNeg(float(incrementEntryField.get()))
        else:
            LiveJointJog(live)

    def SeljogPos(self):
        """
        if incremental, jog incremental
        else live jog
        """

        live = self.idx * 10 + 1
        is_increment = int(GUI.is_increment.get())
        if is_increment :
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
        jog_cmd.joint_jog(self.ctrl.idx, self.delta)
        func = jogNeg if self.delta < 0 else jogPos
        func(abs(self.delta))

    def label(self, value):
        """labels entry with a value"""

        self.entry.delete(0, "end")
        self.entry.insert(0, value)


class ExtJointFrame(JointFrame):
    """JointFrame for external axis"""

    def __init__(self, parent, x, y):
        super(ExtJointFrame, self).__init__(parent, x, y)

        self.frame.config(relief="raised")
        self.frame.grid(row=x, column=y, sticky="nsew")


class AxisFrame:
    """Positional Axis Frame"""

    "ie: XcurEntryField"

    active = dict()

    def __init__(self, parent, x, y, name):

        self.frame = tk.Frame(parent)
        self.frame.grid(row=x, column=y, sticky="nsew", padx=10, pady=10)

        self.entry = tk.Entry(self.frame, width=5)
        self.entry.grid(row=0, column=1, columnspan=2)

        self.name = name

        self.mk_buttons()

        font = ("Arial", 18)
        self.labels = {"main": tk.Label(self.frame, font=font, text=name.upper())}
        self.labels["main"].grid(row=0, column=0,  sticky="ew")
        center(self.labels["main"])

        AxisFrame.active[name] = self

    def label(self, value):
        """labels entry with a value"""
        # TODO abstract with other frames

        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))

    def mk_buttons(self):
        """makes jogging buttons"""

        button = lambda text: tk.Button(self.frame, text=text, width=3)
        self.buttons = {
            "neg": button("-"),
            "pos": button("+"),
        }
        for k, button in self.buttons.items():
            button.bind("<ButtonRelease>", jog_cmd.stop_jog)
        self.buttons["neg"].grid(row=1, column=0)
        self.buttons["pos"].grid(row=1, column=1)

        self.buttons["neg"].bind("<ButtonPress>", lambda: self.jog(False))
        self.buttons["pos"].bind("<ButtonPress>", lambda: self.jog(True))

    def jog(self, fwd):
        """jogs in a direction"""
        raise "not implemented"
        # NOTE see jog/jog_buttons.py


class GUI:
    """GUI manager for everyting"""

    def __init__(
        self,
    ):
        pass

    @classmethod
    def register(cls, k, v):
        setattr(GUI, k, v)


class EntryField:
    """generic entry field"""

    active = dict()

    def __init__(self, parent, width=5, name='',alt=''):

        self.name = name

        self.frame = tk.Frame(parent) 

        self.lab = tk.Label(self.frame, text=name if not alt else alt)
        self.lab.grid(row=0, column=0, sticky="nsew")
        self.entry = tk.Entry(self.frame,width=width) if width else tk.Entry(self.frame)
        self.entry.grid(row=0, column=1, sticky="nsew")

        EntryField.active[name] = self

    def grid(self, *args, **kwargs):
        """docstring"""
        self.frame.grid(*args, **kwargs)


    def label(self, value):
        """labels entry with a value"""
        # TODO abstract with other frames
        # TODO call this "display()"

        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))
