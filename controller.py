
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
                    value = float(incrementEntryField.get())
                    if (mainmode == 2 and event.code == "ABS_HAT0Y"):
                        if ( event.state == -1 and jogMode == 1):
                            XjogNeg(value)
                        elif ( event.state == 1 and jogMode == 1):
                            XjogPos(value)
                        elif ( event.state == 1
                            and jogMode == 1
                        ):
                            YjogNeg(value)
                        elif ( event.state == -1
                            and jogMode == 1
                        ):
                            YjogPos(value)
                        elif ( event.state == 1
                            and jogMode == 2
                        ):
                            ZjogNeg(value)
                        elif ( event.state == -1
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
