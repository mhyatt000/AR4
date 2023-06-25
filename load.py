
def load_presets():
    """docstring"""

    ##############################################################################################################################################################
    ### OPEN CAL FILE AND LOAD LIST ##############################################################################################################################
    ##############################################################################################################################################################

    calibration = Listbox(tabs["2"], height=60)
    GUI.register("calibration", calibration)

    try:
        Cal = pickle.load(open("ErrorLog", "rb"))
    except:
        Cal = "0"
        pickle.dump(Cal, open("ErrorLog", "wb"))
    for item in Cal:
        calibration.insert(tk.END, item)
    global mX1
    global mY1
    global mX2
    global mY2

    # TODO wouldnt this happen automatically if tk.intvar

    J1AngCur = calibration.get("0")
    J2AngCur = calibration.get("1")
    J3AngCur = calibration.get("2")
    J4AngCur = calibration.get("3")
    J5AngCur = calibration.get("4")
    J6AngCur = calibration.get("5")

    XcurPos = calibration.get("6")
    YcurPos = calibration.get("7")
    ZcurPos = calibration.get("8")

    RxcurPos = calibration.get("9")
    RycurPos = calibration.get("10")
    RzcurPos = calibration.get("11")

    COM.teensy.value = calibration.get("12")

    # NOTE tag Prog prog EntryField
    EntryField.active['prog'].value = calibration.get("13")

    Servo0on = calibration.get("14")
    Servo0off = calibration.get("15")
    Servo1on = calibration.get("16")
    Servo1off = calibration.get("17")
    DO1on = calibration.get("18")
    DO1off = calibration.get("19")
    DO2on = calibration.get("20")
    DO2off = calibration.get("21")

    for i,TF in enumerate(ToolFrame.active.values()):
        TF.value = calibration.get(22+i)
        TF.entry.insert(0,str(TF.value))

    for i, J in enumerate(JointCTRL.external):
        J.gui.value = calibration.get(28+i)

    VisFileLoc = calibration.get("31")
    VisProg = calibration.get("32")
    VisOrigXpix = calibration.get("33")
    VisOrigXmm = calibration.get("34")
    VisOrigYpix = calibration.get("35")
    VisOrigYmm = calibration.get("36")
    VisEndXpix = calibration.get("37")
    VisEndXmm = calibration.get("38")
    VisEndYpix = calibration.get("39")
    VisEndYmm = calibration.get("40")

    J1calOff = calibration.get("41")
    J2calOff = calibration.get("42")
    J3calOff = calibration.get("43")
    J4calOff = calibration.get("44")
    J5calOff = calibration.get("45")
    J6calOff = calibration.get("46")

    idxs = range(47,53)
    for J,idx in zip(JointCTRL.main, idxs):
        open_loop = calibration.get(idx)
        open_loop = int(open_loop) if open_loop != '' else 0
        J.open_loop.set(open_loop)

    COM.arduino.value = calibration.get("53")

    theme = calibration.get("54")
    J1CalStatVal = calibration.get("55")
    J2CalStatVal = calibration.get("56")
    J3CalStatVal = calibration.get("57")
    J4CalStatVal = calibration.get("58")
    J5CalStatVal = calibration.get("59")
    J6CalStatVal = calibration.get("60")

    J1CalStatVal2 = calibration.get("65")
    J2CalStatVal2 = calibration.get("66")
    J3CalStatVal2 = calibration.get("67")
    J4CalStatVal2 = calibration.get("68")
    J5CalStatVal2 = calibration.get("69")
    J6CalStatVal2 = calibration.get("70")
    VisBrightVal = calibration.get("71")
    VisContVal = calibration.get("72")
    VisBacColor = calibration.get("73")
    VisScore = calibration.get("74")
    VisX1Val = calibration.get("75")
    VisY1Val = calibration.get("76")
    VisX2Val = calibration.get("77")
    VisY2Val = calibration.get("78")
    VisRobX1Val = calibration.get("79")
    VisRobY1Val = calibration.get("80")
    VisRobX2Val = calibration.get("81")
    VisRobY2Val = calibration.get("82")
    zoom = calibration.get("83")
    pick180Val = calibration.get("84")
    pickClosestVal = calibration.get("85")
    curCam = calibration.get("86")
    GUI.full_rotVal = calibration.get("87")
    autoBGVal = calibration.get("88")
    mX1val = calibration.get("89")
    mY1val = calibration.get("90")
    mX2val = calibration.get("91")
    mY2val = calibration.get("92")


    J7StepCur = calibration.get("64")  # is this used ??? keep for now


    J7calOff = calibration.get("99")
    J8calOff = calibration.get("100")
    J9calOff = calibration.get("101")

    # NOTE now insert calibrations

    for x in [COM.teensy, COM.arduino]:
        x.entry.insert(0, str(x.value))

    EntryField.active["increment"].label("10")
    EntryField.active["speed"].label("25")
    EntryField.active["ACCspeed"].label("10")
    EntryField.active["DECspeed"].label("10")
    EntryField.active["ACCramp"].label("100")
    EntryField.active["round"].label("0")
    EntryField.active["prog"].display()
    EntryField.active["savepos"].label("1")



    for J in JointCTRL.external:
        J.gui.entry.insert(0, str(J.gui.value))

    VisFileLocEntryField.insert(0, str(VisFileLoc))


    # visoptions.set(VisProg)

    VisPicOxPEntryField.insert(0, str(VisOrigXpix))
    VisPicOxMEntryField.insert(0, str(VisOrigXmm))
    VisPicOyPEntryField.insert(0, str(VisOrigYpix))
    VisPicOyMEntryField.insert(0, str(VisOrigYmm))
    VisPicXPEntryField.insert(0, str(VisEndXpix))
    VisPicXMEntryField.insert(0, str(VisEndXmm))
    VisPicYPEntryField.insert(0, str(VisEndYpix))
    VisPicYMEntryField.insert(0, str(VisEndYmm))

    caloffs = [
        J1calOff,
        J2calOff,
        J3calOff,
        J4calOff,
        J5calOff,
        J6calOff,
        J7calOff,
        J8calOff,
        J9calOff,
    ]

    for J, caloff in zip(JointCTRL.main, caloffs):
        J.caloff_entry.insert(0, str(caloff))



    ####


    if theme == 1:
        dark_theme(root)
    else:
        light_theme(root)

    if J1CalStatVal == 1:
        J1CalStat.set(True)
    if J2CalStatVal == 1:
        J2CalStat.set(True)
    if J3CalStatVal == 1:
        J3CalStat.set(True)
    if J4CalStatVal == 1:
        J4CalStat.set(True)
    if J5CalStatVal == 1:
        J5CalStat.set(True)
    if J6CalStatVal == 1:
        J6CalStat.set(True)

    if J1CalStatVal2 == 1:
        J1CalStat2.set(True)
    if J2CalStatVal2 == 1:
        J2CalStat2.set(True)
    if J3CalStatVal2 == 1:
        J3CalStat2.set(True)
    if J4CalStatVal2 == 1:
        J4CalStat2.set(True)
    if J5CalStatVal2 == 1:
        J5CalStat2.set(True)
    if J6CalStatVal2 == 1:
        J6CalStat2.set(True)

    limpos = [None] * 3
    # TODO

    J7length = calibration.get("61")
    J7rotation = calibration.get("62")
    J7steps = calibration.get("63")
    J8length = calibration.get("93")
    J8rotation = calibration.get("94")
    J8steps = calibration.get("95")
    J9length = calibration.get("96")
    J9rotation = calibration.get("97")
    J9steps = calibration.get("98")

    labels = [
        {
            "length": J7length,
            "rotation": J7rotation,
            "steps": J7steps,
        },
        {
            "length": J8length,
            "rotation": J8rotation,
            "steps": J8steps,
        },
        {
            "length": J9length,
            "rotation": J9rotation,
            "steps": J9steps,
        },
    ]


    for i, J in enumerate(JointCTRL.external):
        _labels = labels[i]
        for key, field in J.gui.fields.items():
            field.insert(0, _labels[key])

    # TODO abstract and add to vision
    """
    VisBrightSlide.set(VisBrightVal)
    VisContrastSlide.set(VisContVal)
    VisBacColorEntryField.insert(0, str(VisBacColor))
    VisScoreEntryField.insert(0, str(VisScore))
    VisX1PixEntryField.insert(0, str(VisX1Val))
    VisY1PixEntryField.insert(0, str(VisY1Val))
    VisX2PixEntryField.insert(0, str(VisX2Val))
    VisY2PixEntryField.insert(0, str(VisY2Val))
    VisX1RobEntryField.insert(0, str(VisRobX1Val))
    VisY1RobEntryField.insert(0, str(VisRobY1Val))
    VisX2RobEntryField.insert(0, str(VisRobX2Val))
    VisY2RobEntryField.insert(0, str(VisRobY2Val))

    VisZoomSlide.set(zoom)

    if pickClosestVal == 1:
        pickClosest.set(True)
    if pick180Val == 1:
        pick180.set(True)
    visoptions.set(curCam)
    if GUI.full_rotVal == 1:
        GUI.full_rot.set(True)
    if autoBGVal == 1:
        autoBG.set(True)
    mX1 = mX1val
    mY1 = mY1val
    mX2 = mX2val
    mY2 = mY2val

    updateVisOp(tabs)
    checkAutoBG(autoBG, VisBacColorEntryField)  # TODO what is autoBG
    """



    # manEntryField.delete(0, 'end')
    # manEntryField.insert(0,value)

