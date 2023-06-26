import os
import program
import os.path as osp
import tkinter as tk
from gui.base import GUI
import tkinter.ttk as ttk


def build():
    """docstring"""

    testSendLab = tk.Label(GUI.tabs["10"], text="Test string to send to arduino")
    testSendLab.place(x=10, y=20)

    testRecLab = tk.Label(GUI.tabs["10"], text="Message echoed back from arduino")
    testRecLab.place(x=10, y=70)

    testSendBut = tk.Button(GUI.tabs["10"], text="SEND TO ARDUINO", command=program.TestString)
    testSendBut.place(x=10, y=120)

    testClearBut = tk.Button(GUI.tabs["10"], text="CLEAR RECEIVED", command=program.ClearTestString)
    testClearBut.place(x=180, y=120)

    testSendEntryField = tk.Entry(GUI.tabs["10"], width=222)
    testSendEntryField.place(x=10, y=40)

    testRecEntryField = tk.Entry(GUI.tabs["10"], width=222)
    testRecEntryField.place(x=10, y=90)

