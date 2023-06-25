import datetime as dt
import pickle
import time
import tkinter as tk

import serial

from gui.base import GUI, ButtonEntry


class COMPortFrame(ButtonEntry):
    """docstring"""

    # TODO migrate to frames

    def __init__(self, parent, name=None, serial_idx=None):
        super(COMPortFrame, self).__init__(parent, name)

        assert not serial_idx is None
        self.serial_idx = serial_idx
        self.label = tk.Label(self.frame, text=f"{self.name.upper()} COM PORT:")
        # TODO fix layout
        self.label.grid(row=1, column=0)

    def command(self):
        COM.set(self.serial_idx)


class COM:
    """singleton communication handler"""

    ser = [None, None]
    alms = []
    style, text = None, None
    startup = None

    teensy, arduino = None, None

    def __init__(self, start_func):
        print("initiate serial communitation")

        if self.teensy is None:
            COM.teensy = COMPortFrame(GUI.tabs["2"], name="teensy", serial_idx=0)
        if self.arduino is None:
            COM.arduino = COMPortFrame(GUI.tabs["2"], name="arduino", serial_idx=1)
        COM.startup = start_func

    @classmethod
    def set(cls, idx=0):
        """set serial communication"""

        now = dt.datetime.now().strftime("%B %d %Y - %I:%M%p")
        board = ["TEENSY 4.1 CONTROLLER", "ARDUINO IO BOARD"][idx]
        baud = [9600, 115200][idx]

        def log_message(msg):
            try:
                GUI.tabs["6"].ElogView.insert(tk.END, f"{now} - {msg}")
                value = GUI.tabs["6"].ElogView.get(0, tk.END)
                pickle.dump(value, open("ErrorLog", "wb"))
            except Exception as ex:
                print(ex)

        try:
            port = "/dev/cu.usbmodem123843001"
            COM.ser[idx] = serial.Serial(port, baud)  # , timeout=2)

            text = f"COMMUNICATIONS STARTED WITH {board}"

            # TODO: use log_message()
            # TODO: make util.py

            print(text)
            COM.alarm(text, False)
            log_message(text)
            time.sleep(1)
            COM.ser[idx].flushInput()
            COM.startup()

        except Exception as ex:

            text = f"UNABLE TO ESTABLISH COMMUNICATIONS WITH {board}"
            print(text)
            COM.alarm(text, True)
            log_message(text)

    @classmethod
    def register_alm(cls, alm):
        """registers alarm label"""
        COM.alms.append(alm)

    def alarm(text, red=True):
        """docstring"""

        style = "Warn.TLabel" if red else "OK.TLabel"
        if not style:
            raise Exception("TODO get new style")

        for alm in COM.alms:
            alm.config(text=text, style=style)

    @classmethod
    def serial_write(cls, command, idx=0):
        """send message to serial port"""

        print("command:", command.strip("\n"))
        ser = COM.ser[idx]

        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        print("response:", response)
        print()
        return response
