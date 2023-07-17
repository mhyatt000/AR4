import os
import os.path as osp
import tkinter as tk
import tkinter.ttk as ttk

from gui.base import GUI
from com import COM


def on_closing():
    # if messagebox.askokcancel("Close Program", "Do you want to quit?"):

    try:
        command = "CL"
        COM.quick_write(command)
    except Exception as ex:
        print(ex)

    COM.close()
    GUI.root.destroy()


def init_app():
    """docstring"""

    GUI.root = tk.Tk()
    GUI.root.wm_title("AR4 Software Ver 3.0")
    GUI.root.iconbitmap(r"AR.ico")
    GUI.root.resizable(width=True, height=True)
    GUI.root.geometry("1536x792+0+0")
    GUI.root.runTrue = 0

    GUI.root.rowconfigure(0, weight=1)
    GUI.root.columnconfigure(0, weight=1)

    GUI.root.wm_protocol("WM_DELETE_WINDOW", on_closing)

    JogStepsStat = tk.IntVar()

    is_increment = tk.IntVar()
    GUI.register("is_increment", is_increment)
    GUI.full_rot = tk.IntVar()
    GUI.pick180 = tk.IntVar()
    GUI.pickClosest = tk.IntVar()
    GUI.autoBG = tk.IntVar()
    SplineTrue = False

    cam_on = False
    cap = None


def init_tabs():
    """docstring"""

    nb = ttk.Notebook(GUI.root, width=1536, height=792)
    nb.grid(row=0, column=0, sticky="nsew")

    tabs = {str(i): ttk.Frame(nb) for i in range(1, 10 + 1)}
    GUI.register("tabs", tabs)
    tabnames = [
        " Main Controls ",
        "  Config Settings  ",
        " Inputs Outputs ",
        "   Registers    ",
        "   Vision    ",
        "      Log      ",
        "   Info    ",
    ]
    for tab, name in zip(tabs.values(), tabnames):
        nb.add(tab, text=name)

def build():
    """docstring"""

    init_app()
    init_tabs()
