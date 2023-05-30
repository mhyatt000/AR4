

##############################################################################################################################################################
### BUTTON JOGGING DEFS ############################################################################################################## BUTTON JOGGING DEFS ###
##############################################################################################################################################################


def xbox():
    def threadxbox():
        from inputs import get_gamepad

        global xboxUse
        jogMode = 1
        if xboxUse == 0:
            xboxUse = 1
            mainMode = 1
            jogMode = 1
            grip = 0
            almStatusLab.config(text="JOGGING JOINTS 1 & 2", style="Warn.TLabel")
            almStatusLab2.config(text="JOGGING JOINTS 1 & 2", style="Warn.TLabel")
            xbcStatusLab.config(
                text="Xbox ON",
            )
            ChgDis(2)

        else:
            xboxUse = 0
            almStatusLab.config(text="XBOX CONTROLLER OFF", style="Warn.TLabel")
            almStatusLab2.config(text="XBOX CONTROLLER OFF", style="Warn.TLabel")
            xbcStatusLab.config(
                text="Xbox OFF",
            )

        while xboxUse == 1:
            try:
                # if (TRUE):
                events = get_gamepad()
                for event in events:

                    ##DISTANCE
                    if event.code == "ABS_RZ" and event.state >= 100:
                        ChgDis(0)
                    elif event.code == "ABS_Z" and event.state >= 100:
                        ChgDis(1)

                    ##SPEED
                    elif event.code == "BTN_TR" and event.state == 1:
                        ChgSpd(0)
                    elif event.code == "BTN_TL" and event.state == 1:
                        ChgSpd(1)

                    ##JOINT MODE
                    elif event.code == "BTN_WEST" and event.state == 1:
                        if mainMode != 1:
                            mainMode = 1
                            jogMode = 1
                            almStatusLab.config(text="JOGGING JOINTS 1 & 2", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING JOINTS 1 & 2", style="Warn.TLabel")
                        else:
                            jogMode += 1
                        if jogMode == 2:
                            almStatusLab.config(text="JOGGING JOINTS 3 & 4", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING JOINTS 3 & 4", style="Warn.TLabel")
                        elif jogMode == 3:
                            almStatusLab.config(text="JOGGING JOINTS 5 & 6", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING JOINTS 5 & 6", style="Warn.TLabel")
                        elif jogMode == 4:
                            jogMode = 1
                            almStatusLab.config(text="JOGGING JOINTS 1 & 2", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING JOINTS 1 & 2", style="Warn.TLabel")

                    ##JOINT JOG
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0X"
                        and event.state == 1
                        and jogMode == 1
                    ):
                        J1jogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0X"
                        and event.state == -1
                        and jogMode == 1
                    ):
                        J1jogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0Y"
                        and event.state == -1
                        and jogMode == 1
                    ):
                        J2jogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0Y"
                        and event.state == 1
                        and jogMode == 1
                    ):
                        J2jogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0Y"
                        and event.state == -1
                        and jogMode == 2
                    ):
                        J3jogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0Y"
                        and event.state == 1
                        and jogMode == 2
                    ):
                        J3jogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0X"
                        and event.state == 1
                        and jogMode == 2
                    ):
                        J4jogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0X"
                        and event.state == -1
                        and jogMode == 2
                    ):
                        J4jogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0Y"
                        and event.state == -1
                        and jogMode == 3
                    ):
                        J5jogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0Y"
                        and event.state == 1
                        and jogMode == 3
                    ):
                        J5jogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0X"
                        and event.state == 1
                        and jogMode == 3
                    ):
                        J6jogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 1
                        and event.code == "ABS_HAT0X"
                        and event.state == -1
                        and jogMode == 3
                    ):
                        J6jogPos(float(incrementEntryField.get()))

                    ##CARTESIAN DIR MODE
                    elif event.code == "BTN_SOUTH" and event.state == 1:
                        if mainMode != 2:
                            mainMode = 2
                            jogMode = 1
                            almStatusLab.config(text="JOGGING X & Y AXIS", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING X & Y AXIS", style="Warn.TLabel")
                        else:
                            jogMode += 1
                        if jogMode == 2:
                            almStatusLab.config(text="JOGGING Z AXIS", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING Z AXIS", style="Warn.TLabel")
                        elif jogMode == 3:
                            jogMode = 1
                            almStatusLab.config(text="JOGGING X & Y AXIS", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING X & Y AXIS", style="Warn.TLabel")

                    ##CARTESIAN DIR JOG
                    elif (
                        mainMode == 2
                        and event.code == "ABS_HAT0Y"
                        and event.state == -1
                        and jogMode == 1
                    ):
                        XjogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 2
                        and event.code == "ABS_HAT0Y"
                        and event.state == 1
                        and jogMode == 1
                    ):
                        XjogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 2
                        and event.code == "ABS_HAT0X"
                        and event.state == 1
                        and jogMode == 1
                    ):
                        YjogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 2
                        and event.code == "ABS_HAT0X"
                        and event.state == -1
                        and jogMode == 1
                    ):
                        YjogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 2
                        and event.code == "ABS_HAT0Y"
                        and event.state == 1
                        and jogMode == 2
                    ):
                        ZjogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 2
                        and event.code == "ABS_HAT0Y"
                        and event.state == -1
                        and jogMode == 2
                    ):
                        ZjogPos(float(incrementEntryField.get()))

                    ##CARTESIAN ORIENTATION MODE
                    elif event.code == "BTN_EAST" and event.state == 1:
                        if mainMode != 3:
                            mainMode = 3
                            jogMode = 1
                            almStatusLab.config(text="JOGGING Rx & Ry AXIS", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING Rx & Ry AXIS", style="Warn.TLabel")
                        else:
                            jogMode += 1
                        if jogMode == 2:
                            almStatusLab.config(text="JOGGING Rz AXIS", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING Rz AXIS", style="Warn.TLabel")
                        elif jogMode == 3:
                            jogMode = 1
                            almStatusLab.config(text="JOGGING Rx & Ry AXIS", style="Warn.TLabel")
                            almStatusLab2.config(text="JOGGING Rx & Ry AXIS", style="Warn.TLabel")

                    ##CARTESIAN ORIENTATION JOG
                    elif (
                        mainMode == 3
                        and event.code == "ABS_HAT0X"
                        and event.state == -1
                        and jogMode == 1
                    ):
                        RxjogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 3
                        and event.code == "ABS_HAT0X"
                        and event.state == 1
                        and jogMode == 1
                    ):
                        RxjogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 3
                        and event.code == "ABS_HAT0Y"
                        and event.state == 1
                        and jogMode == 1
                    ):
                        RyjogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 3
                        and event.code == "ABS_HAT0Y"
                        and event.state == -1
                        and jogMode == 1
                    ):
                        RyjogPos(float(incrementEntryField.get()))
                    elif (
                        mainMode == 3
                        and event.code == "ABS_HAT0X"
                        and event.state == 1
                        and jogMode == 2
                    ):
                        RzjogNeg(float(incrementEntryField.get()))
                    elif (
                        mainMode == 3
                        and event.code == "ABS_HAT0X"
                        and event.state == -1
                        and jogMode == 2
                    ):
                        RzjogPos(float(incrementEntryField.get()))

                    ##J7 MODE
                    elif event.code == "BTN_START" and event.state == 1:
                        mainMode = 4
                        almStatusLab.config(text="JOGGING TRACK", style="Warn.TLabel")
                        almStatusLab2.config(text="JOGGING TRACK", style="Warn.TLabel")

                    ##TRACK JOG
                    elif mainMode == 4 and event.code == "ABS_HAT0X" and event.state == 1:
                        J7jogPos(float(incrementEntryField.get()))
                    elif mainMode == 4 and event.code == "ABS_HAT0X" and event.state == -1:
                        J7jogNeg(float(incrementEntryField.get()))

                    ##TEACH POS
                    elif event.code == "BTN_NORTH" and event.state == 1:
                        teachInsertBelSelected()

                    ##GRIPPER
                    elif event.code == "BTN_SELECT" and event.state == 1:
                        if grip == 0:
                            grip = 1
                            outputNum = DO1offEntryField.get()
                            command = "OFX" + outputNum + "\n"
                            ser2.write(command.encode())
                            ser2.flushInput()
                            time.sleep(0.2)
                            ser2.read()
                        else:
                            grip = 0
                            outputNum = DO1onEntryField.get()
                            command = "ONX" + outputNum + "\n"
                            ser2.write(command.encode())
                            ser2.flushInput()
                            time.sleep(0.2)
                            ser2.read()
                            time.sleep(0.1)
                    else:
                        pass
            except:
                # else:
                almStatusLab.config(text="XBOX CONTROLLER NOT RESPONDING", style="Alarm.TLabel")
                almStatusLab2.config(text="XBOX CONTROLLER NOT RESPONDING", style="Alarm.TLabel")

    t = threading.Thread(target=threadxbox)
    t.start()


def ChgDis(val):

    curSpd = int(incrementEntryField.get())

    if curSpd >= 100 and val == 0:
        curSpd = 100
    elif curSpd < 5 and val == 0:
        curSpd += 1
    elif val == 0:
        curSpd += 5

    if curSpd <= 1 and val == 1:
        curSpd = 1
    elif curSpd <= 5 and val == 1:
        curSpd -= 1
    elif val == 1:
        curSpd -= 5
    elif val == 2:
        curSpd = 5

    incrementEntryField.delete(0, "end")
    incrementEntryField.insert(0, str(curSpd))

    time.sleep(0.3)


def ChgSpd(val):

    curSpd = int(speedEntryField.get())

    if curSpd >= 100 and val == 0:
        curSpd = 100
    elif curSpd < 5 and val == 0:
        curSpd += 1
    elif val == 0:
        curSpd += 5

    if curSpd <= 1 and val == 1:
        curSpd = 1
    elif curSpd <= 5 and val == 1:
        curSpd -= 1
    elif val == 1:
        curSpd -= 5
    elif val == 2:
        curSpd = 5

    speedEntryField.delete(0, "end")
    speedEntryField.insert(0, str(curSpd))


def J1jogNeg(value):

    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur

    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()

    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")

    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"

    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"

    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()

    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )

    command = (
        "RJ"
        + "A"
        + str(float(J1AngCur) - value)
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )

    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J1jogPos(value):

    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()

    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )

    command = ( "RJ" + "A" + str(float(J1AngCur) + value) + "B" + J2AngCur + "C" + J3AngCur + "D" + J4AngCur + "E" + J5AngCur + "F" + J6AngCur + "J7" + str(J7PosCur) + "J8" + str(J8PosCur) + "J9" + str(J9PosCur) + speedPrefix + Speed + "Ac" + ACCspd + "Dc" + DECspd + "Rm" + ACCramp + "W" + WC + "Lm" + LoopMode + "\n")

    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J2jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + str(float(J2AngCur) - value)
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J2jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + str(float(J2AngCur) + value)
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J3jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + str(float(J3AngCur) - value)
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J3jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + str(float(J3AngCur) + value)
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J4jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + str(float(J4AngCur) - value)
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J4jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + str(float(J4AngCur) + value)
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J5jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + str(float(J5AngCur) - value)
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J5jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + str(float(J5AngCur) + value)
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J6jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + str(float(J6AngCur) - value)
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J6jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + str(float(J6AngCur) + value)
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J7jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(float(J7PosCur) - value)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J7jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(float(J7PosCur) + value)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J8jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(float(J8PosCur) - value)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J8jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(float(J8PosCur) + value)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J9jogNeg(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(float(J9PosCur) - value)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J9jogPos(value):
    global xboxUse
    global J1AngCur
    global J2AngCur
    global J3AngCur
    global J4AngCur
    global J5AngCur
    global J6AngCur
    global J7PosCur
    global J8PosCur
    global J9PosCur
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(float(J9PosCur) + value)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def LiveJointJog(value):
    global xboxUse
    almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
    almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    checkSpeedVals()
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "LJ"
        + "V"
        + str(value)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.1)
    ser.read()


def LiveCarJog(value):
    global xboxUse
    almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
    almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    checkSpeedVals()
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "LC"
        + "V"
        + str(value)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.1)
    ser.read()


def LiveToolJog(value):
    global xboxUse
    almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
    almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    checkSpeedVals()
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "LT"
        + "V"
        + str(value)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.1)
    ser.read()


def StopJog(self):
    command = "S\n"
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 0:
        ser.write(command.encode())
        ser.flushInput()
        time.sleep(0.2)
        response = str(ser.readline().strip(), "utf-8")
        if response[:1] == "E":
            ErrorHandler(response)
        else:
            displayPosition(response)


def J7jogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(float(J7PosCur) - value)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J7jogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(float(J7PosCur) + value)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J8jogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(float(J8PosCur) - value)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J8jogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(float(J8PosCur) + value)
        + "J9"
        + str(J9PosCur)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J9jogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(float(J9PosCur) - value)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def J9jogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to percent
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "RJ"
        + "A"
        + J1AngCur
        + "B"
        + J2AngCur
        + "C"
        + J3AngCur
        + "D"
        + J4AngCur
        + "E"
        + J5AngCur
        + "F"
        + J6AngCur
        + "J7"
        + str(J7PosCur)
        + "J8"
        + str(J8PosCur)
        + "J9"
        + str(float(J9PosCur) + value)
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def XjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = str(float(XcurPos) - value)
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def YjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = str(float(YcurPos) - value)
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def ZjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = str(float(ZcurPos) - value)
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def RxjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = str(float(RxcurPos) - value)
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def RyjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = str(float(RycurPos) - value)
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def RzjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = str(float(RzcurPos) - value)
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def XjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = str(float(XcurPos) + value)
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def YjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = str(float(YcurPos) + value)
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def ZjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = str(float(ZcurPos) + value)
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def RxjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = str(float(RxcurPos) + value)
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def RyjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = str(float(RycurPos) + value)
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def RzjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # mm/sec
    if speedtype == "mm per Sec":
        speedPrefix = "Sm"
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = str(float(RzcurPos) + value)
    ryVal = RycurPos
    rxVal = RxcurPos
    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "MJ"
        + "X"
        + xVal
        + "Y"
        + yVal
        + "Z"
        + zVal
        + "Rz"
        + rzVal
        + "Ry"
        + ryVal
        + "Rx"
        + rxVal
        + "J7"
        + j7Val
        + "J8"
        + j8Val
        + "J9"
        + j9Val
        + speedPrefix
        + Speed
        + "Ac"
        + ACCspd
        + "Dc"
        + DECspd
        + "Rm"
        + ACCramp
        + "W"
        + WC
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TXjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTX1"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TYjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTY1"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TZjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTZ1"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TRxjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTW1"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TRyjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTP1"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TRzjogNeg(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTR1"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TXjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTX0"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TYjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTY0"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TZjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTZ0"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TRxjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTW0"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TRyjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTP0"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def TRzjogPos(value):
    global xboxUse
    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
    speedtype = speedOption.get()
    # dont allow mm/sec - switch to sec
    if speedtype == "mm per Sec":
        speedMenu = OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Ss"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")
    # seconds
    if speedtype == "Seconds":
        speedPrefix = "Ss"
    # percent
    if speedtype == "Percent":
        speedPrefix = "Sp"
    Speed = speedEntryField.get()
    ACCspd = ACCspeedField.get()
    DECspd = DECspeedField.get()
    ACCramp = ACCrampField.get()
    LoopMode = (
        str(J1OpenLoopStat.get())
        + str(J2OpenLoopStat.get())
        + str(J3OpenLoopStat.get())
        + str(J4OpenLoopStat.get())
        + str(J5OpenLoopStat.get())
        + str(J6OpenLoopStat.get())
    )
    command = (
        "JTR0"
        + str(value)
        + speedPrefix
        + Speed
        + "G"
        + ACCspd
        + "H"
        + DECspd
        + "I"
        + ACCramp
        + "Lm"
        + LoopMode
        + "\n"
    )
    ser.write(command.encode())
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)

