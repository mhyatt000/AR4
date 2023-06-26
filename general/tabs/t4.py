import os
import os.path as osp
import tkinter as tk
import tkinter.ttk as ttk

from gui.base import GUI, ButtonEntry, EntryField
from program import *
from servo import DO, RContainer, Servo


def build():

    for _ in range(16):
        RContainer(GUI.tabs["4"])

    label_texts = [f"PR{i+1}" for i in range(16)]
    labels = []
    x, y = 640, 30

    for label_text in label_texts:
        label = tk.Label(GUI.tabs["4"], text=label_text)
        label.place(x=x, y=y)
        labels.append(label)
        y += 30

    label_texts = ["X", "Y", "Z", "Rz", "Ry", "Rx"]
    labels = []
    x, y = 410, 10

    for label_text in label_texts:
        label = tk.Label(GUI.tabs["4"], text=label_text)
        label.place(x=x, y=y)
        labels.append(label)
        x += 40

    """refactored: SP_9_E1 is now sp_entry[0][8] """
    mk_entry = lambda: tk.Entry(GUI.tabs["4"], width=5)
    sp_entries = [[mk_entry() for e in range(16)] for sp in range(6)]

    coordinates = [[(400 + (40 * j), 30 * (i + 1)) for i in range(16)] for j in range(6)]

    # list flatten
    sp_entries = sum(sp_entries, [])
    coordinates = sum(coordinates, [])

    for entry, (x, y) in zip(sp_entries, coordinates):
        entry.place(x=x, y=y)

    for entry in sp_entries:
        entry.insert(0, "0")
