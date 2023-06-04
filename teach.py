##############################################################################################################################################################
### TEACH DEFS ################################################################################################################################ TEACH DEFS ###
##############################################################################################################################################################


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
    speedtype = speedOption.get()
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
    if movetype == "OFF J":
        movetype = movetype + " [ PR: " + str(SavePosEntryField.get()) + " ]"
        newPos = (
            movetype
            + " [*] X "
            + XcurPos
            + " Y "
            + YcurPos
            + " Z "
            + ZcurPos
            + " Rz "
            + RzcurPos
            + " Ry "
            + RycurPos
            + " Rx "
            + RxcurPos
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    if movetype == "Move Vis":
        movetype = movetype + " [ PR: " + str(SavePosEntryField.get()) + " ]"
        newPos = (
            movetype
            + " [*] X "
            + XcurPos
            + " Y "
            + YcurPos
            + " Z "
            + ZcurPos
            + " Rz "
            + RzcurPos
            + " Ry "
            + RycurPos
            + " Rx "
            + RxcurPos
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move PR":
        movetype = movetype + " [ PR: " + str(SavePosEntryField.get()) + " ]"
        newPos = (
            movetype
            + " [*]"
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "OFF PR ":
        movetype = (
            movetype
            + " [ PR: "
            + str(SavePosEntryField.get())
            + " ] offs [ *PR: "
            + str(int(SavePosEntryField.get()) + 1)
            + " ] "
        )
        newPos = (
            movetype
            + " [*]"
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move J":
        newPos = (
            movetype
            + " [*] X "
            + XcurPos
            + " Y "
            + YcurPos
            + " Z "
            + ZcurPos
            + " Rz "
            + RzcurPos
            + " Ry "
            + RycurPos
            + " Rx "
            + RxcurPos
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move L":
        newPos = (
            movetype
            + " [*] X "
            + XcurPos
            + " Y "
            + YcurPos
            + " Z "
            + ZcurPos
            + " Rz "
            + RzcurPos
            + " Ry "
            + RycurPos
            + " Rx "
            + RxcurPos
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " Rnd "
            + Rounding
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move R":
        newPos = (
            movetype
            + " [*] J1 "
            + J1AngCur
            + " J2 "
            + J2AngCur
            + " J3 "
            + J3AngCur
            + " J4 "
            + J4AngCur
            + " J5 "
            + J5AngCur
            + " J6 "
            + J6AngCur
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move A Mid":
        newPos = (
            movetype
            + " [*] X "
            + XcurPos
            + " Y "
            + YcurPos
            + " Z "
            + ZcurPos
            + " Rz "
            + RzcurPos
            + " Ry "
            + RycurPos
            + " Rx "
            + RxcurPos
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move A End":
        newPos = (
            movetype
            + " [*] X "
            + XcurPos
            + " Y "
            + YcurPos
            + " Z "
            + ZcurPos
            + " Rz "
            + RzcurPos
            + " Ry "
            + RycurPos
            + " Rx "
            + RxcurPos
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move C Center":
        newPos = (
            movetype
            + " [*] X "
            + XcurPos
            + " Y "
            + YcurPos
            + " Z "
            + ZcurPos
            + " Rz "
            + RzcurPos
            + " Ry "
            + RycurPos
            + " Rx "
            + RxcurPos
            + " J7 "
            + str(J7PosCur)
            + " J8 "
            + str(J8PosCur)
            + " J9 "
            + str(J9PosCur)
            + " "
            + speedPrefix
            + " "
            + Speed
            + " Ac "
            + ACCspd
            + " Dc "
            + DECspd
            + " Rm "
            + ACCramp
            + " $ "
            + WC
        )
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move C Start":
        newPos = movetype + " [*] X " + XcurPos + " Y " + YcurPos + " Z " + ZcurPos
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Move C Plane":
        newPos = movetype + " [*] X " + XcurPos + " Y " + YcurPos + " Z " + ZcurPos
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
    elif movetype == "Start Spline" or movetype == "End Spline":
        newPos = movetype
        tab1.progView.insert(selRow, newPos)
        tab1.progView.selection_clear(0, END)
        tab1.progView.select_set(selRow)
        value = tab1.progView.get(0, END)
        pickle.dump(value, open(ProgEntryField.get(), "wb"))
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

