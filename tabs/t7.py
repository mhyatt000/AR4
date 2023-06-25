import os
import os.path as osp
import tkinter as tk
from gui.base import GUI
import tkinter.ttk as ttk

def callback():
    webbrowser.open_new(r"https://www.paypal.me/ChrisAnnin")


def build():
    """docstring"""

    link = Label(
        tabs["7"], font="12", text="https://www.anninrobotics.com/tutorials", cursor="hand2"
    )
    link.bind("<Button-1>", lambda event: webbrowser.open(link.cget("text")))
    link.place(x=10, y=9)

    donateBut = Button(tabs["7"], command=callback)
    donatePhoto = tk.PhotoImage(file=osp.join("assets", "pp.gif"))
    donateBut.config(image=donatePhoto)
    donateBut.place(x=1250, y=2)

    scroll = Scrollbar(tabs["7"])
    scroll.pack(side=RIGHT, fill=Y)
    configfile = Text(tabs["7"], wrap=WORD, width=166, height=40, yscrollcommand=scroll.set)
    filename = osp.join("assets", "information.txt")
    with open(filename, "r", encoding="utf-8-sig") as file:
        configfile.insert(INSERT, file.read())
    configfile.pack(side="left")
    scroll.config(command=configfile.yview)
    configfile.place(x=10, y=40)
