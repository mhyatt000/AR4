import datetime
import load

import math
from multiprocessing.resource_sharer import stop
import os
from os import execv
import os.path as osp
import pathlib
import pickle
import threading
import time
# from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import tkinter.messagebox
from tkinter.ttk import *
import webbrowser

from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
import numpy as np
from numpy import mean

import calibrate
from com import COM
import controller
import exc.commands
from exc.execution import *
import frames
from frames import AxisFrame, ExtJointFrame, JointFrame, ToolFrame
from gui.base import GUI, EntryField
from jog import *
from jog import  jog_cmd
from joint import JointCTRL
from program import *
import servo
from teach import *
import theme

# from pygrabber.dshow_graph import FilterGraph

from tabs import root, t1, t2, t3, t4, t5, t6, t7, t10

def main():
    """docstring"""

    ROOT = osp.dirname(osp.dirname(__file__))
    print(ROOT)
    assets = osp.join(ROOT, "assets")
    GUI.register("assets", assets)

    root.build()

    t1.build()
    t2.build()
    t3.build()
    t4.build()
    t5.build()
    t6.build()
    t7.build()
    t10.build()

    def startup():
        moveInProc = 0
        calibrate.tool_frame()
        # TODO later
        # calRobotAll()
        # calExtAxis()
        commands.read_encoders()
        calibrate.send_pos()
        calibrate.request_pos()

    # TODO i think this was in the way of other buttons
    # loadProg(tabs)

    def show_license():
        """docstring"""

        msg = """
        AR3 and AR4 are registered trademarks of Annin Robotics
        Copyright © 2022 by Annin Robotics. All Rights Reserved
        """

        tkinter.messagebox.showwarning("AR4 License / Copyright notice", msg)

    GUI.use_xbox = 0

    # COM(startup)
    # load.load_cfg()

    # COM.set()

    def limit():
        """docstring"""

        while True:
            commands.test_limit_switch()
            time.sleep(0.21)


    # limit()
    GUI.tabs["1"].mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        raise ex
        print(ex)
        load.save_cfg()
        COM.close()
