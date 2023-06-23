import serial
import time
import pickle
import tkinter as tk
import datetime as dt

class COM:
    """singleton communication handler"""

    ser = [None, None]
    alms = []
    tabs = None
    style, text = None,None
    startup=None

    def __init__(self, tabs, start_func):
        COM.tabs = tabs
        COM.startup = start_func

    @classmethod
    def set(cls, idx=0):
        """set serial communication"""

        now = dt.datetime.now().strftime("%B %d %Y - %I:%M%p")
        board = ["TEENSY 4.1 CONTROLLER", "ARDUINO IO BOARD"][idx]
        baud = [9600, 115200][idx]

        def log_message(msg):
            try: 
                COM.tabs["6"].ElogView.insert(tk.END, f"{now} - {msg}")
                value = COM.tabs["6"].ElogView.get(0, tk.END)
                pickle.dump(value, open("ErrorLog", "wb"))
            except Exception as ex:
                print(ex)

        try:
            port = "/dev/cu.usbmodem123843001"
            COM.ser[idx] = serial.Serial(port, baud)

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
            raise ex
            COM.alarm(text, True)
            log_message(text)



    @classmethod
    def register_alm(cls,alm):
        """registers alarm label"""
        COM.alms.append(alm)

    def alarm(text, red=True):
        """docstring"""

        style = "Warn.TLabel" if red else  "OK.TLabel"
        if not style:
            raise Exception('TODO get new style')

        for alm in COM.alms:
            alm.config(text=text, style=style)



    @classmethod
    def serial_write(cls,command):
        """send message to serial port"""

        ser = COM.ser[0]

        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        return response
