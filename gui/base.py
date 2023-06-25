import tkinter as tk

class GUI:
    """GUI manager for everyting"""

    def __init__( self):
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


    def display(self, value=None):
        """docstring"""

        value = self.value if value is None else value
        if value is None:
            raise Exception

        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))


    def label(self, value):
        """labels entry with a value"""
        # TODO abstract with other frames
        # TODO call this "display()"

        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))


class ButtonEntry:
    """docstring"""

    active = {}

    def __init__(self, parent, name=None):

        self.idx = len(ButtonEntry.active)
        self.name = f"{type(self).__name__}{self.idx}" if not name else name
        self.frame = tk.Frame(parent)

        self.button = tk.Button(self.frame, text=self.name, command=self.command)
        self.button.grid(row=0, column=0)

        self.entry = tk.Entry(self.frame, width=5)
        self.entry.grid(row=0, column=1)

        ButtonEntry.active[self.name] = self

        self.func = 'TODO'

    def command(self):
        raise Exception("not implemented")
