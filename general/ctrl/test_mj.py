import os
import time

ser = "/dev/cu.usbmodem123843001"

def send(cmd):
    """docstring"""
    os.system(f"echo {cmd} >> {ser}")
    time.sleep(3)


def main():
    """docstring"""

    cmds = [
        "MJ1000#600#-600#0#0#0#0#0#0",
        "MJ-200#600#-600#0#0#0#0#0#0",
        "MJ-800#-1200#1200#0#0#0#0#0#0",
    ]

    send("MJ0#-1600#0#0#0#0#0#0#0")

    i = -1
    while True:

        for cmd in cmds:
            print('send')
            send(cmd)

        send(f"MJ{i*3000}#{i*-1000}#0#0#0#0#0#0#0")
        i = -i

if __name__ == '__main__': 
    try:
        main()
    except:
        pass
