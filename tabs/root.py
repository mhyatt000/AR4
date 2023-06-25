import os
import os.path as osp
import tkinter as tk
from gui.base import GUI
import tkinter.ttk as ttk



def build():
    """docstring"""

    cropping = False

    root = tk.Tk()
    root.wm_title("AR4 Software Ver 3.0")
    root.iconbitmap(r"AR.ico")
    # root.resizable(width=False, height=False)
    root.geometry("1536x792+0+0")
    root.runTrue = 0

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)


    def on_closing():
        if messagebox.askokcancel("Close Program", "Do you want to quit?"):
            try:
                command = "CL"
                ser.write(command.encode())
            except:
                print("foo")
            ser.close()
            root.destroy()


    # root.wm_protocol("WM_DELETE_WINDOW", on_closing)

    JogStepsStat = tk.IntVar()

    is_increment = tk.IntVar()
    GUI.register("is_increment", is_increment)
    full_rot = tk.IntVar()
    GUI.register('full_rot',GUI.full_rot)
    pick180 = tk.IntVar()
    pickClosest = tk.IntVar()
    autoBG = tk.IntVar()
    SplineTrue = False

    ############################################################################
    ### DEFINE TABS ############################################################
    ############################################################################

    nb = ttk.Notebook(root, width=1536, height=792)
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

    cam_on = False
    cap = None


