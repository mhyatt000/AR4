from gui import GUI
import tkinter as tk
from jog.jog_cmd import stop_jog

def mk_button(frame, text, start_func, stop_func, x, y):
    """docstring"""

    btn = tk.Button(frame, text=text, width=3)
    btn.bind("<ButtonPress>", start_func)
    btn.bind("<ButtonRelease>", stop_func)
    btn.place(x=x, y=y, width=30, height=25)


def btn_jog(func, value):
    """docstring"""
    is_increment = int(GUI.is_increment.get())
    if is_increment :
        func(float(incrementEntryField.get()))
    else:
        LiveCarJog(value)

def main(frame):
    """docstring"""

    # TODO 
    # you can delete these eventually
    # saved for now as a reminder of axis cartesian jog

    SelXjogNeg = lambda: btn_jog(XjogNeg, 10)
    SelXjogPos = lambda: btn_jog(XjogPos, 11)
    SelYjogNeg = lambda: btn_jog(YjogNeg, 20)
    SelYjogPos = lambda: btn_jog(YjogPos, 21)
    SelZjogNeg = lambda: btn_jog(ZjogNeg, 30)
    SelZjogPos = lambda: btn_jog(ZjogPos, 31)

    SelRzjogNeg = lambda: btn_jog(RzjogNeg, 40)
    SelRzjogPos = lambda: btn_jog(RzjogPos, 41)
    SelRyjogNeg = lambda: btn_jog(RyjogNeg, 50)
    SelRyjogPos = lambda: btn_jog(RyjogPos, 51)
    SelRxjogNeg = lambda: btn_jog(RxjogNeg, 60)
    SelRxjogPos = lambda: btn_jog(RxjogPos, 61)

    SelTxjogNeg = lambda: btn_jog(TXjogNeg, 10)
    SelTxjogPos = lambda: btn_jog(TXjogPos, 11)
    SelTyjogNeg = lambda: btn_jog(TYjogNeg, 20)
    SelTyjogPos = lambda: btn_jog(TYjogPos, 21)
    SelTzjogNeg = lambda: btn_jog(TZjogNeg, 30)
    SelTzjogPos = lambda: btn_jog(TZjogPos, 31)

    SelTRzjogNeg = lambda: btn_jog(TRzjogNeg, 40)
    SelTRzjogPos = lambda: btn_jog(TRzjogPos, 41)
    SelTRyjogNeg = lambda: btn_jog(TRyjogNeg, 50)
    SelTRyjogPos = lambda: btn_jog(TRyjogPos, 51)
    SelTRxjogNeg = lambda: btn_jog(TRxjogNeg, 60)
    SelTRxjogPos = lambda: btn_jog(TRxjogPos, 61)
