
def teachInsertBelSelected():

    global XcurPos
    global YcurPos
    global ZcurPos
    global RxcurPos
    global RycurPos
    global RzcurPos
    global WC
    global J7PosCur

    checkSpeedVals()

    try:
        selRow = tab1.progView.curselection()[0]
        selRow += 1
    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)

    Speed = speedEntryField.get()
    speedtype = speed_option.get()

    if speedtype == "Seconds":
        speedPrefix = "Ss"
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    if speedtype == "Percent":
        speedPrefix = "Sp"

    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    Rounding = roundEntryField.get()
    movetype = options.get()
    
    def get_new_pos():
        """docstring"""

        return  (
            f"{movetype} [*] X {XcurPos} Y {YcurPos} Z {ZcurPos} Rz {RzcurPos} "
            f"Ry {RycurPos} Rx {RxcurPos} J7 {J7PosCur} J8 {J8PosCur} J9 {J9PosCur} "
            f"{speedPrefix} {Speed} Ac {ACCspd} Dc {DECspd} Rm {ACCramp} $ {WC}"
        )

    def case1():
        """docstring"""

        tab1.progView.insert(selRow, get_new_pos())
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))

    def case2():
        """docstring"""

        tab1.progView.insert(selRow, alt_new_pos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))


    if movetype == "OFF J":
        movetype = movetype + " [ PR: " + str(SavePosEntryField.get()) + " ]"
        case1()

    if movetype == "Move Vis":
        movetype = movetype + " [ PR: " + str(SavePosEntryField.get()) + " ]"
        case1()

    elif movetype == "Move PR":
        movetype = movetype + " [ PR: " + str(SavePosEntryField.get()) + " ]"
        case1()

    elif movetype == "OFF PR ":
        movetype = (
            movetype
            + " [ PR: "
            + str(SavePosEntryField.get())
            + " ] offs [ *PR: "
            + str(int(SavePosEntryField.get()) + 1)
            + " ] "
        )
        case1()

    elif movetype == "Move J":
        case1()

    elif movetype == "Move L":
        case1()

    elif movetype == "Move R":
        case1()

    elif movetype == "Move A Mid":
        case1()

    elif movetype == "Move A End":
        case1()

    elif movetype == "Move C Center":
        case1()

    elif movetype == "Move C Start":

        alt_new_pos = movetype + " [*] X " + XcurPos + " Y " + YcurPos + " Z " + ZcurPos
        case2()

    elif movetype == "Move C Plane":

        alt_new_pos = movetype + " [*] X " + XcurPos + " Y " + YcurPos + " Z " + ZcurPos
        case2()

    elif movetype == "Start Spline" or movetype == "End Spline":

        alt_new_pos = movetype
        case2()

    elif movetype == "Teach PR":
        PR = str(SavePosEntryField.get())
        SPE6 = "Position Register " + PR + " Element 6 = " + RxcurPos
        tab1.progView.insert(selRow, SPE6)
        SPE5 = "Position Register " + PR + " Element 5 = " + RycurPos
        tab1.progView.insert(selRow, SPE5)
        SPE4 = "Position Register " + PR + " Element 4 = " + RzcurPos
        tab1.progView.insert(selRow, SPE4)
        SPE3 = "Position Register " + PR + " Element 3 = " + ZcurPos
        tab1.progView.insert(selRow, SPE3)
        SPE2 = "Position Register " + PR + " Element 2 = " + YcurPos
        tab1.progView.insert(selRow, SPE2)
        SPE1 = "Position Register " + PR + " Element 1 = " + XcurPos
        tab1.progView.insert(selRow, SPE1)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))


def teachReplaceSelected():
    try:
        deleteitem()
        selRow = tab1.progView.curselection()[0]
        tab1.progView.select_set(selRow - 1)

    except:
        last = tab1.progView.index("end")
        selRow = last
        tab1.progView.select_set(selRow)
    teachInsertBelSelected()


