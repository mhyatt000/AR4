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
                    value = float(incrementEntryField.get()
                    if mainmode == 2 and event.code == "ABS_HAT0Y"
                        elif (
                            and event.state == -1
                            and jogMode == 1
                        ):
                            XjogNeg(value)
                        elif (
                            and event.state == 1
                            and jogMode == 1
                        ):
                            XjogPos(value)
                        elif (
                            and event.state == 1
                            and jogMode == 1
                        ):
                            YjogNeg(value)
                        elif (
                            and event.state == -1
                            and jogMode == 1
                        ):
                            YjogPos(value)
                        elif (
                            and event.state == 1
                            and jogMode == 2
                        ):
                            ZjogNeg(value)
                        elif (
                            and event.state == -1
                            and jogMode == 2
                        ):
                            ZjogPos(value)

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
                        grip = 1 if grip == 0 else 0
                        outputNum = DO1onEntryField.get()
                        command = "ONX" + outputNum + "\n"
                        serial_write(ser2,command)
                    else:
                        pass
            except:
                # else:
                almStatusLab.config(text="XBOX CONTROLLER NOT RESPONDING", style="Alarm.TLabel")
                almStatusLab2.config(text="XBOX CONTROLLER NOT RESPONDING", style="Alarm.TLabel")

    t = threading.Thread(target=threadxbox)
    t.start()


def modify_speed(entry_field, val):
    cur_spd = int(entry_field.get())

    if val == 0:
        cur_spd = min(100, cur_spd + 1 if cur_spd < 5 else cur_spd + 5)
    elif val == 1:
        cur_spd = max(1, cur_spd - 1 if cur_spd <= 5 else cur_spd - 5)
    elif val == 2:
        cur_spd = 5

    entry_field.delete(0, "end")
    entry_field.insert(0, str(cur_spd))
    time.sleep(0.3)


def ChgDis(val):
    modify_speed(incrementEntryField, val)


def ChgSpd(val):
    modify_speed(speedEntryField, val)


def serial_write(ser, command):
    """docstring"""

    ser.write(command.encode())
    ser.flushInput()
    time.sleep(0.2)
    response = str(ser.readline().strip(), "utf-8")
    return response


def serial_err_handle(response):
    """docstring"""

    response = serial_write(command)
    if response[:1] == "E":
        ErrorHandler(response)
    else:
        displayPosition(response)


def get_loopmode():
    return sum(map(lambda x: str(x.openloop_stat.get()), joints))


def joint_jog(joint, value, command):
    """basic jog... positive or negative value indicates direction"""

    xboxuse = None
    ang_cur = [None] * 9

    checkSpeedVals()
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")

    if xboxUse != 1:
        for alm in [almStatusLab, almStatusLab2]:
            alm.config(text="SYSTEM READY", style="OK.TLabel")

    speedtype = speedOption.get()

    speedPrefix = {"Seconds": "Ss", "Percent": "Sp"}.get(speedtype, None)

    if speedtype == "mm per Sec":
        OptionMenu(tab1, speedOption, "Percent", "Percent", "Seconds", "mm per Sec")
        speedPrefix = "Sp"
        speedEntryField.delete(0, "end")
        speedEntryField.insert(0, "50")

    fields = [speedEntryField, ACCspeedField, DECspeedField, ACCrampField]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.get(), fields)

    joints = [
        J1,
        J2,
        J3,
        J4,
        J5,
        J6,
    ]
    loopmode = get_loopmode()

    command = f"RJA{float(J1AngCur) - value}B{J2AngCur}C{J3AngCur}D{J4AngCur}E{J5AngCur}F{J6AngCur}J7{J7PosCur}J8{J8PosCur}J9{J9PosCur}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    cmdSentEntryField.delete(0, "end")
    cmdSentEntryField.insert(0, command)

    response = serial_write(command)
    serial_err_handle(response)


def mk_jog_cmd():
    """returns the jog command"""

    joints = [None] * 9
    ang_cur = list(map(lambda x: x.ang_cur(), joints))

    ang_cur[idx - 1] = joints[idx - 1] + value

    command = "RJ"
    prefixes = ["A", "B", "C", "D", "E", "F", "J7", "J8", "J9"]
    for p, joint in zip(prefixes, joints):
        command += f"{p}{joint}"

    command += f"{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    return command


def LiveJointJog(value):
    command = f"LJV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    return command


def LiveCarJog(value):
    command = f"LCV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    return command


def LiveToolJog(value):
    command = f"LTV{value}{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{LoopMode}\n"
    return command


def StopJog(self):
    command = "S\n"
    IncJogStatVal = int(IncJogStat.get())
    if IncJogStatVal == 0:
        response = serial_write(command)
        serial_err_handle(response)


def jog_position(value, axis):
    """instead of jogging a joint, jog in x,y,z"""

    checkSpeedVals()

    xboxUse = None
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")

    speedtype = speedOption.get()
    options = {"mm per Sec": "Sm", "Seconds": "Ss", "Percent": "Sp"}
    speedPrefix = options.get(speedtype)

    fields = [speedEntryField, ACCspeedField, DECspeedField, ACCrampField]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.get(), fields)

    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos

    position_updates = {
        "x": lambda: xVal + value,
        "y": lambda: yVal + value,
        "z": lambda: zVal + value,
        "rx": lambda: rxVal + value,
        "ry": lambda: ryVal + value,
        "rz": lambda: rzVal + value,
    }

    update_position = position_updates.get(axis)
    if update_position:
        xVal = update_position()

    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)

    loopmode = get_loopmode()

    command = (
        f"MJX{xVal}Y{yVal}Z{zVal}Rz{rzVal}Ry{ryVal}Rx{rxVal}J7{j7Val}J8{j8Val}J9{j9Val}"
        f"{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    )

    response = serial_write(command)
    serial_err_handle(response)


def tjog_position(value, axis):
    """instead of jogging a joint, jog in x,y,z"""

    checkSpeedVals()

    xboxUse = None
    if xboxUse != 1:
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")

    speedtype = speedOption.get()
    options = {"mm per Sec": "Sm", "Seconds": "Ss", "Percent": "Sp"}
    speedPrefix = options.get(speedtype)

    fields = [speedEntryField, ACCspeedField, DECspeedField, ACCrampField]
    Speed, ACCspd, DECspd, ACCramp = map(lambda x: x.get(), fields)

    xVal = XcurPos
    yVal = YcurPos
    zVal = ZcurPos
    rzVal = RzcurPos
    ryVal = RycurPos
    rxVal = RxcurPos

    position_updates = {
        "x": lambda: xVal + value,
        "y": lambda: yVal + value,
        "z": lambda: zVal + value,
        "rx": lambda: rxVal + value,
        "ry": lambda: ryVal + value,
        "rz": lambda: rzVal + value,
    }

    update_position = position_updates.get(axis)
    if update_position:
        xVal = update_position()

    j7Val = str(J7PosCur)
    j8Val = str(J8PosCur)
    j9Val = str(J9PosCur)

    loopmode = get_loopmode()

    command = (
        f"MJX{xVal}Y{yVal}Z{zVal}Rz{rzVal}Ry{ryVal}Rx{rxVal}J7{j7Val}J8{j8Val}J9{j9Val}"
        f"{speedPrefix}{Speed}Ac{ACCspd}Dc{DECspd}Rm{ACCramp}W{WC}Lm{loopmode}\n"
    )

    response = serial_write(command)
    serial_err_handle(response)


def tjog_command(axis, value):

    prefixes = {"TX": "JTX", "TY": "JTY", "TZ": "JTZ", "TRx": "JTW", "TRy": "JTP", "TRz": "JTR"}

    assert axis in prefixes, f"Invalid axis: {axis}"

    prefix = prefixes[axis]
    prefix += "1" if val < 0 else "0"
    val = abs(val)

    command = f"{prefix}{value}{speedPrefix}{Speed}G{ACCspd}H{DECspd}I{ACCramp}Lm{LoopMode}\n"
    return command
