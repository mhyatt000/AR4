import tkinter as tk
from program import *

def main(tabs):
    """docstring"""


    #### TAB 3 ############################################

    #### 3 LABELS ############################################

    mk_label = lambda: tk.Label(tabs["3"], text="=")
    eq_labels = [mk_label() for _ in range(20)]

    eq_pos = [
        dict(x=70, y=12),
        dict(x=70, y=52),
        dict(x=70, y=92),
        dict(x=70, y=132),
        dict(x=70, y=172),
        dict(x=70, y=212),
        dict(x=70, y=252),
        dict(x=70, y=292),
        #
        dict(x=210, y=12),
        dict(x=210, y=52),
        dict(x=210, y=92),
        dict(x=210, y=132),
        dict(x=210, y=172),
        dict(x=210, y=212),
        dict(x=210, y=252),
        dict(x=210, y=292),
        dict(x=210, y=332),
        dict(x=210, y=372),
        dict(x=210, y=412),
        dict(x=210, y=452),
    ]

    for pos, label in zip(eq_pos, eq_labels):
        x, y = list(pos.values())
        label.place(x=x, y=y)

    io_labels = [
        "NOTE: the following are available when using the default Nano board for IO:   Inputs = 2-7  /  Outputs = 8-13  /  Servos = A0-A7",
        "If using IO on Teensy board:  Inputs = 32-36  /  Outputs = 37-41 - if using IO on Teensy you must manually change the command from 'Out On =' to 'ToutOn ='"
    ]
    io_labels = [tk.Label(tabs['3'],text=text) for text in io_labels]
    io_labels[0].place(x=10, y=640)
    io_labels[1].place(x=10, y=655)

    ### 3 BUTTONS ################################################################

    servo0onBut = tk.Button(tabs['3'], text="Servo 0", command=Servo0on)
    servo0onBut.place(x=10, y=10)
    servo0offBut = tk.Button(tabs['3'], text="Servo 0", command=Servo0off)
    servo0offBut.place(x=10, y=50)
    servo1onBut = tk.Button(tabs['3'], text="Servo 1", command=Servo1on)
    servo1onBut.place(x=10, y=90)
    servo1offBut = tk.Button(tabs['3'], text="Servo 1", command=Servo1off)
    servo1offBut.place(x=10, y=130)
    servo2onBut = tk.Button(tabs['3'], text="Servo 2", command=Servo2on)
    servo2onBut.place(x=10, y=170)
    servo2offBut = tk.Button(tabs['3'], text="Servo 2", command=Servo2off)
    servo2offBut.place(x=10, y=210)
    servo3onBut = tk.Button(tabs['3'], text="Servo 3", command=Servo3on)
    servo3onBut.place(x=10, y=250)
    servo3offBut = tk.Button(tabs['3'], text="Servo 3", command=Servo3off)
    servo3offBut.place(x=10, y=290)

    DO1onBut = tk.Button(tabs['3'], text="DO on", command=DO1on)
    DO1onBut.place(x=150, y=10)
    DO1offBut = tk.Button(tabs['3'], text="DO off", command=DO1off)
    DO1offBut.place(x=150, y=50)
    DO2onBut = tk.Button(tabs['3'], text="DO on", command=DO2on)
    DO2onBut.place(x=150, y=90)
    DO2offBut = tk.Button(tabs['3'], text="DO off", command=DO2off)
    DO2offBut.place(x=150, y=130)
    DO3onBut = tk.Button(tabs['3'], text="DO on", command=DO3on)
    DO3onBut.place(x=150, y=170)
    DO3offBut = tk.Button(tabs['3'], text="DO off", command=DO3off)
    DO3offBut.place(x=150, y=210)
    DO4onBut = tk.Button(tabs['3'], text="DO on", command=DO4on)
    DO4onBut.place(x=150, y=250)
    DO4offBut = tk.Button(tabs['3'], text="DO off", command=DO4off)
    DO4offBut.place(x=150, y=290)
    DO5onBut = tk.Button(tabs['3'], text="DO on", command=DO5on)
    DO5onBut.place(x=150, y=330)
    DO5offBut = tk.Button(tabs['3'], text="DO off", command=DO5off)
    DO5offBut.place(x=150, y=370)
    DO6onBut = tk.Button(tabs['3'], text="DO on", command=DO6on)
    DO6onBut.place(x=150, y=410)
    DO6offBut = tk.Button(tabs['3'], text="DO off", command=DO6off)
    DO6offBut.place(x=150, y=450)

    #### 3 ENTRY FIELDS##########################################################
    #############################################################################

    mk_entry = lambda : tk.Entry(tabs['3'], width=5)
    servo0onEntryField = mk_entry()
    servo0onEntryField.place(x=90, y=15)
    servo0offEntryField = mk_entry()
    servo0offEntryField.place(x=90, y=55)
    servo1onEntryField = mk_entry()
    servo1onEntryField.place(x=90, y=95)
    servo1offEntryField = mk_entry()
    servo1offEntryField.place(x=90, y=135)
    servo2onEntryField = mk_entry()
    servo2onEntryField.place(x=90, y=175)
    servo2offEntryField = mk_entry()
    servo2offEntryField.place(x=90, y=215)
    servo3onEntryField = mk_entry()
    servo3onEntryField.place(x=90, y=255)
    servo3offEntryField = mk_entry()
    servo3offEntryField.place(x=90, y=295)

    DO1onEntryField = mk_entry()
    DO1onEntryField.place(x=230, y=15)
    DO1offEntryField = mk_entry()
    DO1offEntryField.place(x=230, y=55)
    DO2onEntryField = mk_entry()
    DO2onEntryField.place(x=230, y=95)
    DO2offEntryField = mk_entry()
    DO2offEntryField.place(x=230, y=135)
    DO3onEntryField = mk_entry()
    DO3onEntryField.place(x=230, y=175)
    DO3offEntryField = mk_entry()
    DO3offEntryField.place(x=230, y=215)
    DO4onEntryField = mk_entry()
    DO4onEntryField.place(x=230, y=255)
    DO4offEntryField = mk_entry()
    DO4offEntryField.place(x=230, y=295)
    DO5onEntryField = mk_entry()
    DO5onEntryField.place(x=230, y=335)
    DO5offEntryField = mk_entry()
    DO5offEntryField.place(x=230, y=375)
    DO6onEntryField = mk_entry()
    DO6onEntryField.place(x=230, y=415)
    DO6offEntryField = mk_entry()
    DO6offEntryField.place(x=230, y=455)

    ####TAB 4 #####################################################################

    ### 4 LABELS#################################################################

    R1Lab = tk.Label(tabs['4'], text="R1")
    R1Lab.place(x=70, y=30)
    R2Lab = tk.Label(tabs['4'], text="R2")
    R2Lab.place(x=70, y=60)
    R3Lab = tk.Label(tabs['4'], text="R3")
    R3Lab.place(x=70, y=90)
    R4Lab = tk.Label(tabs['4'], text="R4")
    R4Lab.place(x=70, y=120)
    R5Lab = tk.Label(tabs['4'], text="R5")
    R5Lab.place(x=70, y=150)
    R6Lab = tk.Label(tabs['4'], text="R6")
    R6Lab.place(x=70, y=180)
    R7Lab = tk.Label(tabs['4'], text="R7")
    R7Lab.place(x=70, y=210)
    R8Lab = tk.Label(tabs['4'], text="R8")
    R8Lab.place(x=70, y=240)
    R9Lab = tk.Label(tabs['4'], text="R9")
    R9Lab.place(x=70, y=270)
    R10Lab = tk.Label(tabs['4'], text="R10")
    R10Lab.place(x=70, y=300)
    R11Lab = tk.Label(tabs['4'], text="R11")
    R11Lab.place(x=70, y=330)
    R12Lab = tk.Label(tabs['4'], text="R12")
    R12Lab.place(x=70, y=360)
    R13Lab = tk.Label(tabs['4'], text="R14")
    R13Lab.place(x=70, y=390)
    R14Lab = tk.Label(tabs['4'], text="R14")
    R14Lab.place(x=70, y=420)
    R15Lab = tk.Label(tabs['4'], text="R15")
    R15Lab.place(x=70, y=450)
    R16Lab = tk.Label(tabs['4'], text="R16")
    R16Lab.place(x=70, y=480)

    SP1Lab = tk.Label(tabs['4'], text="PR1")
    SP1Lab.place(x=640, y=30)
    SP2Lab = tk.Label(tabs['4'], text="PR2")
    SP2Lab.place(x=640, y=60)
    SP3Lab = tk.Label(tabs['4'], text="PR3")
    SP3Lab.place(x=640, y=90)
    SP4Lab = tk.Label(tabs['4'], text="PR4")
    SP4Lab.place(x=640, y=120)
    SP5Lab = tk.Label(tabs['4'], text="PR5")
    SP5Lab.place(x=640, y=150)
    SP6Lab = tk.Label(tabs['4'], text="PR6")
    SP6Lab.place(x=640, y=180)
    SP7Lab = tk.Label(tabs['4'], text="PR7")
    SP7Lab.place(x=640, y=210)
    SP8Lab = tk.Label(tabs['4'], text="PR8")
    SP8Lab.place(x=640, y=240)
    SP9Lab = tk.Label(tabs['4'], text="PR9")
    SP9Lab.place(x=640, y=270)
    SP10Lab = tk.Label(tabs['4'], text="PR10")
    SP10Lab.place(x=640, y=300)
    SP11Lab = tk.Label(tabs['4'], text="PR11")
    SP11Lab.place(x=640, y=330)
    SP12Lab = tk.Label(tabs['4'], text="PR12")
    SP12Lab.place(x=640, y=360)
    SP13Lab = tk.Label(tabs['4'], text="PR14")
    SP13Lab.place(x=640, y=390)
    SP14Lab = tk.Label(tabs['4'], text="PR14")
    SP14Lab.place(x=640, y=420)
    SP15Lab = tk.Label(tabs['4'], text="PR15")
    SP15Lab.place(x=640, y=450)
    SP16Lab = tk.Label(tabs['4'], text="PR16")
    SP16Lab.place(x=640, y=480)

    SP_E1_Lab = tk.Label(tabs['4'], text="X")
    SP_E1_Lab.place(x=410, y=10)
    SP_E2_Lab = tk.Label(tabs['4'], text="Y")
    SP_E2_Lab.place(x=450, y=10)
    SP_E3_Lab = tk.Label(tabs['4'], text="Z")
    SP_E3_Lab.place(x=490, y=10)
    SP_E4_Lab = tk.Label(tabs['4'], text="Rz")
    SP_E4_Lab.place(x=530, y=10)
    SP_E5_Lab = tk.Label(tabs['4'], text="Ry")
    SP_E5_Lab.place(x=570, y=10)
    SP_E6_Lab = tk.Label(tabs['4'], text="Rx")
    SP_E6_Lab.place(x=610, y=10)

    ### 4 BUTTONS################################################################

    #### 4 ENTRY FIELDS##########################################################

    mk_entry = lambda : tk.Entry(tabs['4'], width=5)
    R1EntryField = mk_entry()
    R1EntryField.place(x=30, y=30)
    R2EntryField = mk_entry()
    R2EntryField.place(x=30, y=60)
    R3EntryField = mk_entry()
    R3EntryField.place(x=30, y=90)
    R4EntryField = mk_entry()
    R4EntryField.place(x=30, y=120)
    R5EntryField = mk_entry()
    R5EntryField.place(x=30, y=150)
    R6EntryField = mk_entry()
    R6EntryField.place(x=30, y=180)
    R7EntryField = mk_entry()
    R7EntryField.place(x=30, y=210)
    R8EntryField = mk_entry()
    R8EntryField.place(x=30, y=240)
    R9EntryField = mk_entry()
    R9EntryField.place(x=30, y=270)
    R10EntryField = mk_entry()
    R10EntryField.place(x=30, y=300)
    R11EntryField = mk_entry()
    R11EntryField.place(x=30, y=330)
    R12EntryField = mk_entry()
    R12EntryField.place(x=30, y=360)
    R13EntryField = mk_entry()
    R13EntryField.place(x=30, y=390)
    R14EntryField = mk_entry()
    R14EntryField.place(x=30, y=420)
    R15EntryField = mk_entry()
    R15EntryField.place(x=30, y=450)
    R16EntryField = mk_entry()
    R16EntryField.place(x=30, y=480)

    R1EntryField.insert(0, "0")
    R2EntryField.insert(0, "0")
    R3EntryField.insert(0, "0")
    R4EntryField.insert(0, "0")
    R5EntryField.insert(0, "0")
    R6EntryField.insert(0, "0")
    R7EntryField.insert(0, "0")
    R8EntryField.insert(0, "0")
    R9EntryField.insert(0, "0")
    R10EntryField.insert(0, "0")
    R11EntryField.insert(0, "0")
    R12EntryField.insert(0, "0")
    R13EntryField.insert(0, "0")
    R14EntryField.insert(0, "0")
    R15EntryField.insert(0, "0")
    R16EntryField.insert(0, "0")


    """refactored: SP_9_E1 is now sp_entry[0][8] """
    mk_entry = lambda : tk.Entry(tabs['4'], width=5)
    sp_entries = [[mk_entry() for e in range(16)] for sp in range(6)]

    coordinates = [[(400 + (40 * j), 30 * (i + 1)) for i in range(16)] for j in range(6)]

    # list flatten
    sp_entries = sum(sp_entries,[])
    coordinates = sum(coordinates,[])

    for entry, (x, y) in zip(sp_entries, coordinates):
        entry.place(x=x, y=y)


    for entry in sp_entries:
        entry.insert(0, "0")

    servo0onEntryField.insert(0, str(Servo0on))
    servo0offEntryField.insert(0, str(Servo0off))
    servo1onEntryField.insert(0, str(Servo1on))
    servo1offEntryField.insert(0, str(Servo1off))

    DO1onEntryField.insert(0, str(DO1on))
    DO1offEntryField.insert(0, str(DO1off))
    DO2onEntryField.insert(0, str(DO2on))
    DO2offEntryField.insert(0, str(DO2off))

if __name__ == '__main__': 
    main()
