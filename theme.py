import tkinter as tk
from tkinter import ttk

from ttkthemes import ThemedStyle

theme = 1


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
        "light": ["red", "dark orange", "green", "dark blue", "black"],
        "dark": ["IndianRed1", "orange", "light green", "light blue", "white"],
    }
    colors = colors[mode]

    style.configure("Alarm.TLabel", foreground=colors[0], font=font)
    style.configure("AlarmBut.TButton", foreground=colors[0])

    style.configure("Warn.TLabel", foreground=colors[1], font=font)
    style.configure("OK.TLabel", foreground=colors[2], font=font)
    style.configure("Jointlim.TLabel", foreground=colors[3], font=font)
    style.configure("Frame1.TFrame", background=colors[4])


def lightTheme(root):
    set_theme(root, mode="light")


def darkTheme(root):
    lightTheme(root)
    # set_theme(root, mode="dark")
