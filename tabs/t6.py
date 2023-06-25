import os
import os.path as osp
import tkinter as tk
from gui.base import GUI
import tkinter.ttk as ttk

def clearLog():
    tabs["6"].ElogView.delete(1, tk.END)
    value = tabs["6"].ElogView.get(0, tk.END)
    pickle.dump(value, open("ErrorLog", "wb"))


def build():
    """docstring"""

    Elogframe = Frame(tabs["6"])
    Elogframe.place(x=40, y=15)
    scrollbar = Scrollbar(Elogframe)
    scrollbar.pack(side=RIGHT, fill=Y)
    tabs["6"].ElogView = Listbox(Elogframe, width=150, height=40, yscrollcommand=scrollbar.set)
    try:
        Elog = pickle.load(open("ErrorLog", "rb"))
    except:
        Elog = ["##BEGINNING OF LOG##"]
        pickle.dump(Elog, open("ErrorLog", "wb"))
    time.sleep(0.2)
    for item in Elog:
        tabs["6"].ElogView.insert(tk.END, item)
    tabs["6"].ElogView.pack()
    scrollbar.config(command=tabs["6"].ElogView.yview)

    clearLogBut = Button(tabs["6"], text="Clear Log", width=26, command=clearLog)
    clearLogBut.place(x=1000, y=630)
