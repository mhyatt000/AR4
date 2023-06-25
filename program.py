import tkinter as tk
from gui.base import GUI



def deleteitem():
    selRow = tab1.progView.curselection()[0]
    selection = tab1.progView.curselection()
    tab1.progView.delete(selection[0])
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def manInsItem():
    """what does this do"""
    """something insert item"""

    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)

    tab1.progView.insert(selRow, manEntryField.get())
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    selRow = tab1.progView.curselection()[0]
    curRowEntryField.delete(0, "end")
    curRowEntryField.insert(0, selRow)
    tab1.progView.itemconfig(selRow, {"fg": "darkgreen"})
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def manReplItem():
    # selRow = curRowEntryField.get()
    selRow = tab1.progView.curselection()[0]
    tab1.progView.delete(selRow)
    tab1.progView.insert(selRow, manEntryField.get())
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    tab1.progView.itemconfig(selRow, {"fg": "darkgreen"})
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def waitTime():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    seconds = waitTimeEntryField.get()
    newTime = "Wait Time = " + seconds
    tab1.progView.insert(selRow, newTime)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def waitInputOn():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    input = waitInputEntryField.get()
    newInput = "Wait Input On = " + input
    tab1.progView.insert(selRow, newInput)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def waitInputOff():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    input = waitInputOffEntryField.get()
    newInput = "Wait Off Input = " + input
    tab1.progView.insert(selRow, newInput)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def setOutputOn():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    output = outputOnEntryField.get()
    newOutput = "Out On = " + output
    tab1.progView.insert(selRow, newOutput)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def setOutputOff():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    output = outputOffEntryField.get()
    newOutput = "Out Off = " + output
    tab1.progView.insert(selRow, newOutput)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def tabNumber():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    tabNum = tabNumEntryField.get()
    tabins = "Tab Number " + tabNum
    tab1.progView.insert(selRow, tabins)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def jumpTab():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    tabNum = jumpTabEntryField.get()
    tabjmp = "Jump Tab-" + tabNum
    tab1.progView.insert(selRow, tabjmp)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def cameraOn():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    value = "Cam On"
    tab1.progView.insert(selRow, value)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def cameraOff():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    value = "Cam Off"
    tab1.progView.insert(selRow, value)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def IfOnjumpTab():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    inpNum = IfOnjumpInputTabEntryField.get()
    tabNum = IfOnjumpNumberTabEntryField.get()
    tabjmp = "If On Jump - Input-" + inpNum + " Jump to Tab-" + tabNum
    tab1.progView.insert(selRow, tabjmp)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def IfOffjumpTab():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    inpNum = IfOffjumpInputTabEntryField.get()
    tabNum = IfOffjumpNumberTabEntryField.get()
    tabjmp = "If Off Jump - Input-" + inpNum + " Jump to Tab-" + tabNum
    tab1.progView.insert(selRow, tabjmp)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def move_servo():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    servoNum = servoNumEntryField.get()
    servoPos = servoPosEntryField.get()
    servoins = "Servo number " + servoNum + " to position: " + servoPos
    tab1.progView.insert(selRow, servoins)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def loadProg():
    progframe = tk.Frame(GUI.tabs['1'])
    progframe.place(x=7, y=174)

    scrollbar = tk.Scrollbar(progframe)
    scrollbar.pack(side=RIGHT, fill=Y)

    GUI.tabs['1'].progView = Listbox(progframe, width=105, height=31, yscrollcommand=scrollbar.set)
    GUI.tabs['1'].progView.bind("<<ListboxSelect>>", progViewselect)

    try:
        prog = pickle.load(open(ProgEntryField.get(), "rb"))
    except:
        try:
            prog = ["##BEGINNING OF PROGRAM##", "Tab Number 1"]
            pickle.dump(Prog, open(ProgEntryField.get(), "wb"))
        except:
            prog = ["##BEGINNING OF PROGRAM##", "Tab Number 1"]
            pickle.dump(Prog, open("new", "wb"))
            ProgEntryField.insert(0, "new")

    time.sleep(0.2)
    for item in prog:
        GUI.tabs['1'].progView.insert(END, item)
    GUI.tabs['1'].progView.pack()
    scrollbar.config(command=GUI.tabs['1'].progView.yview)
    save_pos_data()


def insertCallProg():
    try:
        selRow = GUI.tabs['1'].progView.curselection()[0]
        selRow += 1
    except:
        last = GUI.tabs['1'].progView.index("end")
        selRow = last
        GUI.tabs['1'].progView.select_set(selRow)
    newProg = changeProgEntryField.get()
    changeProg = "Call Program - " + newProg
    GUI.tabs['1'].progView.insert(selRow, changeProg)
    GUI.tabs['1'].progView.selection_clear(0, END)
    GUI.tabs['1'].progView.select_set(selRow)
    value = GUI.tabs['1'].progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def insertReturn():
    try:
        selRow = GUI.tabs['1'].progView.curselection()[0]
        selRow += 1
    except:
        last = GUI.tabs['1'].progView.index("end")
        selRow = last
        GUI.tabs['1'].progView.select_set(selRow)
    value = "Return"
    GUI.tabs['1'].progView.insert(selRow, value)
    GUI.tabs['1'].progView.selection_clear(0, END)
    GUI.tabs['1'].progView.select_set(selRow)
    value = GUI.tabs['1'].progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def insertvisFind():
    global ZcurPos
    global RxcurPos
    global RycurPos
    global RzcurPos
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    template = selectedTemplate.get()
    if template == "":
        template = "None_Selected.jpg"
    autoBGVal = int(autoBG.get())
    if autoBGVal == 1:
        BGcolor = "(Auto)"
    else:
        BGcolor = VisBacColorEntryField.get()
    score = VisScoreEntryField.get()
    passTab = visPassEntryField.get()
    failTab = visFailEntryField.get()
    value = (
        "Vis Find - "
        + template
        + " - BGcolor "
        + BGcolor
        + " Score "
        + score
        + " Pass "
        + passTab
        + " Fail "
        + failTab
    )
    # value = "Vis Find - "+template+" - BGcolor "+BGcolor+" Score "+score+" Z Height "+ZcurPos+" Rz "+RzcurPos+" Ry "+RycurPos+" Rx "+RxcurPos+" Pass "+passTab+" Fail "+failTab
    tab1.progView.insert(selRow, value)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value = tab1.progView.get(0, END)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))


def IfRegjumpTab():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    regNum = regNumJmpEntryField.get()
    regEqNum = regEqJmpEntryField.get()
    tabNum = regTabJmpEntryField.get()
    tabjmp = "If Register " + regNum + " = " + regEqNum + " Jump to Tab " + tabNum
    tab1.progView.insert(selRow, tabjmp)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def insertRegister():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    regNum = regNumEntryField.get()
    regCmd = regEqEntryField.get()
    regIns = "Register " + regNum + " = " + regCmd
    tab1.progView.insert(selRow, regIns)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def storPos():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    regNum = storPosNumEntryField.get()
    regElmnt = storPosElEntryField.get()
    regCmd = storPosValEntryField.get()
    regIns = "Position Register " + regNum + " Element " + regElmnt + " = " + regCmd
    tab1.progView.insert(selRow, regIns)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def insCalibrate():
    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    insCal = "Calibrate Robot"
    tab1.progView.insert(selRow, insCal)
    value = tab1.progView.get(0, END)
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    pickle.dump(value, open(ProgEntryField.get(), "wb"))
    tabNumEntryField.delete(0, "end")


def progViewselect(e):
    selRow = tab1.progView.curselection()[0]
    curRowEntryField.delete(0, "end")
    curRowEntryField.insert(0, selRow)


def getSel():
    selRow = tab1.progView.curselection()[0]
    tab1.progView.see(selRow + 2)
    data = list(map(int, tab1.progView.curselection()))
    command = tab1.progView.get(data[0])
    manEntryField.delete(0, "end")
    manEntryField.insert(0, command)

def TestString():
    message = testSendEntryField.get()
    command = "TM" + message + "\n"
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0)
    echo = ser.readline()
    testRecEntryField.delete(0, "end")
    testRecEntryField.insert(0, echo)


def ClearTestString():
    testRecEntryField.delete(0, "end")


def CalcLinDist(X2, Y2, Z2):
    global XcurPos
    global YcurPos
    global ZcurPos
    global LineDist
    X1 = XcurPos
    Y1 = YcurPos
    Z1 = ZcurPos
    LineDist = (((X2 - X1) ** 2) + ((Y2 - Y1) ** 2) + ((Z2 - Z1) ** 2)) ** 0.5
    return LineDist


def CalcLinVect(X2, Y2, Z2):
    global XcurPos
    global YcurPos
    global ZcurPos
    global Xv
    global Yv
    global Zv
    X1 = XcurPos
    Y1 = YcurPos
    Z1 = ZcurPos
    Xv = X2 - X1
    Yv = Y2 - Y1
    Zv = Z2 - Z1
    return (Xv, Yv, Zv)


def CalcLinWayPt( CX, CY, CZ, curWayPt):
    pass
    # TODO what is this

