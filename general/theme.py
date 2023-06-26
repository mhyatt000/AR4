import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedStyle

from gui.base import GUI

class ThemeManager:

    def __init__(self, root):

        self.root = root
        self.style = ThemedStyle(self.root)
        self.colors = {
            "light": ["red", "dark orange", "green", "dark blue", "black"],
            "dark": ["IndianRed1", "orange", "light green", "light blue", "keramik"],
        }

    @classmethod
    def set_theme(self, mode="light"):
        """sets the theme of the GUI"""

        assert mode in ["light", "dark"]
        self.style.set_theme("black" if mode == "dark" else "keramik")

        font = ("Arial", "10", "bold")
        colors = self.colors[mode]

        ttk_style = ttk.Style()
 
        # Prepare configuration parameters
        widgets = {
                "Alarm.TLabel": 0,
                "AlarmBut.TButton": 0,
                "Warn.TLabel": 1,
                "OK.TLabel": 2,
                "Jointlim.TLabel": 3,
                "Frame.TFrame": 4,
        }

        for  widget,i in widgets.items():
            ttk_style.configure( widget, foreground=colors[i], font=font)

    def light_theme(self):
        self.set_theme(mode="light")

    def dark_theme(self):
        self.set_theme(mode="dark")


def set_theme(root, mode="light"):
    """sets the theme of the GUI"""

    assert mode in ["light", "dark"]
    darkmode = mode == "dark"

    theme = 0 if darkmode else 1

    style = ThemedStyle(root)
    style.set_theme("black" if darkmode else "keramik")
    style = ttk.Style()

    font = ("Arial", "10", "bold")
    colors = {
        "light": ["red", "dark orange", "green", "dark blue", "keramik"],
        "dark": ["IndianRed1", "orange", "light green", "light blue", "keramik"],
    }
    colors = colors[mode]

    style.configure("Alarm.TLabel", foreground=colors[0], font=font)
    style.configure("AlarmBut.TButton", foreground=colors[0])

    style.configure("Warn.TLabel", foreground=colors[1], font=font)
    style.configure("OK.TLabel", foreground=colors[2], font=font)
    style.configure("Jointlim.TLabel", foreground=colors[3], font=font)
    style.configure("TFrame", background=colors[4])
    style.configure("TLabel", background=colors[4])

    style.configure("TFrame", bordercolor='red')

def light_theme(root):
    set_theme(root, mode="light")


def dark_theme(root):
    set_theme(root, mode="dark")

