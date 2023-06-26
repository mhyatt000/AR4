import os
from servo import Servo, DO
import json
import os.path as osp
import pickle
import tkinter as tk
import tkinter.ttk as ttk

from calibrate import JointCal
from com import COM
from frames import AxisFrame, ExtJointFrame, JointFrame, ToolFrame
from gui.base import GUI, EntryField
from joint import JointCTRL
import theme
import vision

get_cfg = lambda: osp.join(GUI.assets, "cfg.json")


def read_calfile():
    """docstring"""

    # TODO use json not pickle
    try:
        with open(get_cfg(),'r') as file:
            cfg = json.load(file)
        return cfg
    except:
        raise Exception
        return {}


def load_presets():
    """docstring"""

    calibration = tk.Listbox(GUI.tabs["2"], height=60)
    GUI.register("calibration", calibration)
    calibration.place(x=10, y=10)

    read_calfile()

    # TODO wouldnt this happen automatically if tk.intvar

    angles = [calibration.get(i) for i in range(6)]
    for J, angle in zip(JointCTRL.main, angles):
        J.gui.entry.insert(0, angle)

    axis_pos = [calibration.get(6 + i) for i in range(6)]
    for A, pos in zip(AxisFrame.active.values(), axis_pos):
        pass

    COM.teensy.value = calibration.get("12")

    # NOTE tag Prog prog EntryField
    EntryField.active["prog"].value = calibration.get("13")

    Servo0on = calibration.get("14")
    Servo0off = calibration.get("15")
    Servo1on = calibration.get("16")
    Servo1off = calibration.get("17")
    DO1on = calibration.get("18")
    DO1off = calibration.get("19")
    DO2on = calibration.get("20")
    DO2off = calibration.get("21")

    for i, TF in enumerate(ToolFrame.active.values()):
        TF.value = calibration.get(22 + i)
        TF.entry.insert(0, str(TF.value))

    for i, J in enumerate(JointCTRL.external):
        J.gui.value = calibration.get(28 + i)

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

    idxs = range(47, 53)
    for J, idx in zip(JointCTRL.main, idxs):
        open_loop = calibration.get(idx)
        open_loop = int(open_loop) if open_loop != "" else 0
        J.open_loop.set(open_loop)

    COM.arduino.value = calibration.get("53")

    select_theme = calibration.get("54")

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

    offsets = [calibration.get(41 + i) for i in range(6)]
    offsets += [calibration.get(99 + i) for i in range(3)]
    for J, offset in zip(JointCal.active, offsets):
        J.offset.entry.insert(0, str(offset))

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

    EntryField.active["VisFileLoc"].entry.insert(0, str(VisFileLoc))

    # GUI.visoptions.set(VisProg)

    EntryField.active["VisPicOxP"].entry.insert(0, str(VisOrigXpix))
    EntryField.active["VisPicOxM"].entry.insert(0, str(VisOrigXmm))
    EntryField.active["VisPicOyP"].entry.insert(0, str(VisOrigYpix))
    EntryField.active["VisPicOyM"].entry.insert(0, str(VisOrigYmm))
    EntryField.active["VisPicXP"].entry.insert(0, str(VisEndXpix))
    EntryField.active["VisPicXM"].entry.insert(0, str(VisEndXmm))
    EntryField.active["VisPicYP"].entry.insert(0, str(VisEndYpix))
    EntryField.active["VisPicYM"].entry.insert(0, str(VisEndYmm))

    ####

    # if select_theme == 1:
    # theme.dark_theme(GUI.root)
    # else:
    # theme.light_theme(GUI.root)

    calstats = [calibration.get(55 + i) for i in range(6)]
    for J, calstat in zip(JointCal.active[:6], calstats):
        J.no_autocal.set(bool(calstat))

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

    for i, J in enumerate(JointCal.external):
        _labels = labels[i]
        for k in J.vars.keys():
            J.vars[k].set(_labels[k])
            J.fields[k].entry.insert(0, _labels[k])

    GUI.VisBrightSlide.set(VisBrightVal)
    GUI.VisContrastSlide.set(VisContVal)
    GUI.VisZoomSlide.set(zoom)

    EntryField.active["VisBacColor"].entry.insert(0, str(VisBacColor))
    EntryField.active["VisScore"].entry.insert(0, str(VisScore))
    EntryField.active["VisX1Pix"].entry.insert(0, str(VisX1Val))
    EntryField.active["VisY1Pix"].entry.insert(0, str(VisY1Val))
    EntryField.active["VisX2Pix"].entry.insert(0, str(VisX2Val))
    EntryField.active["VisY2Pix"].entry.insert(0, str(VisY2Val))
    EntryField.active["VisX1Rob"].entry.insert(0, str(VisRobX1Val))
    EntryField.active["VisY1Rob"].entry.insert(0, str(VisRobY1Val))
    EntryField.active["VisX2Rob"].entry.insert(0, str(VisRobX2Val))
    EntryField.active["VisY2Rob"].entry.insert(0, str(VisRobY2Val))

    GUI.pickClosest.set(pickClosestVal == 1)
    GUI.pick180.set(pick180Val == 1)
    GUI.full_rot.set(GUI.full_rotVal == 1)
    GUI.autoBG.set(autoBGVal == 1)

    GUI.visoptions.set(curCam)
    mX1 = mX1val
    mY1 = mY1val
    mX2 = mX2val
    mY2 = mY2val

    # TODO what is autoBG
    # vision.updateVisOp(GUI.tabs)
    # vision.checkAutoBG(autoBG, VisBacColorEntryField)

    # TODO what does this do?
    # manEntryField.delete(0, 'end')
    # manEntryField.insert(0,value)


def save_cfg():

    cfg = {
        "angles": [J.angle for J in JointCTRL.main],
        "coord": [A.position for A in AxisFrame.main.values()],  # cartesian coordinates
        "teensy": COM.teensy.entry.get(),
        "program": EntryField.active["prog"].entry.get(),
        "servos": [
            {k: v.entry.get() for k, v in zip(["on", "off"], [x.on, x.off])} for x in Servo.active
        ],
        "DO": [
            DO.active[0].on.entry.get(),
            DO.active[0].off.entry.get(),
            DO.active[1].on.entry.get(),
            DO.active[1].off.entry.get(),
        ],
        "tool_frame": [x.entry.get() for x in ToolFrame.active.values()],
        "positions": [J.gui.entry.get() for J in JointCTRL.external],
        "vision": [
            {k: v.entry.get() for k, v in EntryField.active.items() if "Vis" in k},
            GUI.visoptions.get(),
            GUI.VisBrightSlide.get(),
            GUI.VisContrastSlide.get(),
        ],
        "offsets": [J.offset.entry.get() for J in JointCal.active],
        "open_loop": [int(J.open_loop.get()) for J in JointCal.main],
        "arduino": COM.arduino.entry.get(),
        "theme": 1,
        "autocal": [J.no_autocal.get() for J in JointCal.main],  # why no autocal?
        "calstat": [0 for J in JointCTRL.active],  # calstat2
        "external": {
            J.name: {
                "fields": [x.get() for x in JCal.vars.values()],
                "x": J.angle,  # TODO double check this
            }
            for J, JCal in zip(JointCTRL.external, JointCal.external)
        },
        "other": [
            GUI.VisZoomSlide.get(),
            GUI.pick180.get(),
            GUI.pickClosest.get(),
            GUI.visoptions.get(),
            GUI.full_rot.get(),
            GUI.autoBG.get(),
            *[0 for _ in range(4)],  # *[mX1, mY1, mX2, mY2],
        ],
    }

    GUI.cfg = cfg
    with open(get_cfg(), 'w') as file:
        json.dump(cfg,file)
