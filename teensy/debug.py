import datetime as dt
import time
import time
import tkinter as tk

import serial


def write(ser, command, idx=0):
    """docstring"""

    # print("command:", command.strip("\n"))
    # ser = COM.ser[idx]

    ser.write(command.encode())
    ser.flush()
    while ser.in_waiting:
        line = ser.readline().decode("utf-8").strip()
        print(line)

def read(ser):
    """docstring"""

    response = ser.readline().strip().decode("utf-8") or ""

    if response:
        print("response:", response or None)
        print()
    return response


def quick_write(ser, command, idx=0):
    """doesnt wait for a response"""

    # print("command:", command.strip("\n"))
    # ser = COM.ser[idx]

    ser.write(command.encode())
    ser.flush()
    return ""

def close(cls):
    """docstring"""

    print()
    for i, ser in enumerate(COM.ser):
        try:
            ser.close()
            print(f"closed {ser.port}")
        except Exception as ex:
            pass


def main():
    """docstring"""

    port = "/dev/cu.usbmodem123843001"
    baud = 9600
    ser = serial.Serial(port, baud, timeout=10)  # , timeout=2)

    write(ser,'CMD\n')
    while False:

        # try:
            now = dt.datetime.now().strftime("%B %d %Y - %I:%M%p")

            print(now)
            read(ser)
            # time.sleep(0.2)

        # except Exception as ex:
            # print(ex)
            # time.sleep(1)

if __name__ == "__main__":
    print('running main')
    main()
