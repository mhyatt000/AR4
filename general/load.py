import json
import util
import os
import os.path as osp
import pickle
import tkinter as tk
import tkinter.ttk as ttk

from calibrate import JointCal
from com import COM
from frames import AxisFrame, ExtJointFrame, JointFrame, ToolFrame
from gui.base import GUI, EntryField
from joint import JointCTRL
from servo import DO, Servo
import theme
import vision

get_cfg = lambda: osp.join(GUI.assets, "cfg.json")


def read_cfg():
    """docstring"""

    # TODO use json not pickle
    try:
        with open(get_cfg(), "r") as file:
            cfg = json.load(file)
        return cfg
    except:
        raise Exception
        return {}


def load_cfg():
    """docstring"""

    # NOTE depricated
    # calibration = tk.Listbox(GUI.tabs["2"], height=60)
    # GUI.register("calibration", calibration)
    # calibration.place(x=10, y=10)

    cfg = read_cfg()

    # TODO wouldnt this happen automatically if tk.intvar

    angles = cfg["angles"]
    for J, angle in zip(JointCTRL.main, angles):
        util.display(J.gui.entry,angle)
        J.gui.slider.set(angle)
        J.gui.labels['slider'].config(text=angle)

    coordinates = cfg["coord"]
    for A, pos in zip(AxisFrame.active.values(), coordinates):
        A.position = pos
        util.display(A.entry,pos)

    COM.arduino.value = cfg["arduino"]
    COM.teensy.value = cfg["teensy"]
    for x in [COM.teensy, COM.arduino]:
        util.display(x.entry,x.value)

    toolframe = cfg["tool_frame"]
    for k, v in toolframe.items():
        TF = ToolFrame.active[k]
        TF.value = v
        util.display(TF.entry,v)

    positions = cfg["positions"]
    for J, pos in zip(JointCTRL.external, positions):
        J.gui.value = pos

    open_loop = cfg["open_loop"]
    for J, loop in zip(JointCTRL.main, open_loop):
        J.open_loop.set(loop)

    offsets = cfg["offsets"]
    for J, offset in zip(JointCal.active, offsets):
        util.display(J.offset.entry,offset)

    speed = cfg['speed'] # TODO can you make a better name
    for k,v in speed.items():
        # TODO forgot about EntryField .label function ... use more often
        EntryField.active[k].label(v)

    for J in JointCTRL.external:
        util.display(J.gui.entry,J.gui.value)

    autocal = cfg['autocal'] 
    for J, a in zip(JointCal.active, autocal):
        J.vars['autocal'].set(bool(a))

    limits = cfg['limits']
    # TODO do something with the limits

    external = cfg["external"]
    for J, E in zip(JointCal.external, external.values()):
        for k, v in E.items():
            J.extvars[k].set(v)
            util.display(J.fields[k].entry,v)

    # NOTE depricated ... 100 lines vvv

    # Servo0on = calibration.get("14")
    # Servo0off = calibration.get("15")
    # Servo1on = calibration.get("16")
    # Servo1off = calibration.get("17")
    # DO1on = calibration.get("18")
    # DO1off = calibration.get("19")
    # DO2on = calibration.get("20")
    # DO2off = calibration.get("21")

    # VisFileLoc = calibration.get("31")
    # VisProg = calibration.get("32")
    # VisOrigXpix = calibration.get("33")
    # VisOrigXmm = calibration.get("34")
    # VisOrigYpix = calibration.get("35")
    # VisOrigYmm = calibration.get("36")
    # VisEndXpix = calibration.get("37")
    # VisEndXmm = calibration.get("38")
    # VisEndYpix = calibration.get("39")
    # VisEndYmm = calibration.get("40")

    # VisBrightVal = calibration.get("71")
    # VisContVal = calibration.get("72")
    # VisBacColor = calibration.get("73")
    # VisScore = calibration.get("74")
    # VisX1Val = calibration.get("75")
    # VisY1Val = calibration.get("76")
    # VisX2Val = calibration.get("77")
    # VisY2Val = calibration.get("78")
    # VisRobX1Val = calibration.get("79")
    # VisRobY1Val = calibration.get("80")
    # VisRobX2Val = calibration.get("81")
    # VisRobY2Val = calibration.get("82")

    # EntryField.active["prog"].display()
    # EntryField.active["savepos"].label("1")

    # EntryField.active["VisFileLoc"].entry.insert(0, str(VisFileLoc))
    # EntryField.active["VisPicOxP"].entry.insert(0, str(VisOrigXpix))
    # EntryField.active["VisPicOxM"].entry.insert(0, str(VisOrigXmm))
    # EntryField.active["VisPicOyP"].entry.insert(0, str(VisOrigYpix))
    # EntryField.active["VisPicOyM"].entry.insert(0, str(VisOrigYmm))
    # EntryField.active["VisPicXP"].entry.insert(0, str(VisEndXpix))
    # EntryField.active["VisPicXM"].entry.insert(0, str(VisEndXmm))
    # EntryField.active["VisPicYP"].entry.insert(0, str(VisEndYpix))
    # EntryField.active["VisPicYM"].entry.insert(0, str(VisEndYmm))

    # EntryField.active["VisBacColor"].entry.insert(0, str(VisBacColor))
    # EntryField.active["VisScore"].entry.insert(0, str(VisScore))
    # EntryField.active["VisX1Pix"].entry.insert(0, str(VisX1Val))
    # EntryField.active["VisY1Pix"].entry.insert(0, str(VisY1Val))
    # EntryField.active["VisX2Pix"].entry.insert(0, str(VisX2Val))
    # EntryField.active["VisY2Pix"].entry.insert(0, str(VisY2Val))
    # EntryField.active["VisX1Rob"].entry.insert(0, str(VisRobX1Val))
    # EntryField.active["VisY1Rob"].entry.insert(0, str(VisRobY1Val))
    # EntryField.active["VisX2Rob"].entry.insert(0, str(VisRobX2Val))
    # EntryField.active["VisY2Rob"].entry.insert(0, str(VisRobY2Val))

    # select_theme = calibration.get("54")
    # zoom = calibration.get("83")
    # pick180Val = calibration.get("84")
    # pickClosestVal = calibration.get("85")
    # curCam = calibration.get("86")
    # GUI.full_rotVal = calibration.get("87")
    # autoBGVal = calibration.get("88")
    # mX1val = calibration.get("89")
    # mY1val = calibration.get("90")
    # mX2val = calibration.get("91")
    # mY2val = calibration.get("92")
    # GUI.visoptions.set(VisProg)

    # GUI.VisBrightSlide.set(VisBrightVal)
    # GUI.VisContrastSlide.set(VisContVal)
    # GUI.VisZoomSlide.set(zoom)
    # GUI.pickClosest.set(pickClosestVal == 1)
    # GUI.pick180.set(pick180Val == 1)
    # GUI.full_rot.set(GUI.full_rotVal == 1)
    # GUI.autoBG.set(autoBGVal == 1)
    # GUI.visoptions.set(curCam)
    # mX1 = mX1val
    # mY1 = mY1val
    # mX2 = mX2val
    # mY2 = mY2val

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
        "tool_frame": {k:v.entry.get() for k,v in ToolFrame.active.items()},
        "positions": [J.gui.entry.get() for J in JointCTRL.external],
        "vision": [
            {k: v.entry.get() for k, v in EntryField.active.items() if "Vis" in k},
            GUI.visoptions.get(),
            GUI.VisBrightSlide.get(),
            GUI.VisContrastSlide.get(),
        ],
        "arduino": COM.arduino.entry.get(),
        "theme": 1,
        "offsets": [J.vars['offset'].get() for J in JointCal.active],
        "open_loop": [int(J.vars['openloop'].get()) for J in JointCal.active],
        "autocal": [J.vars['autocal'].get() for J in JointCal.active],  # why no autocal?
        "calstat": [0 for J in JointCTRL.active],  # calstat2
        "external": {
            J.name: { k:v.get() for k,v in JCal.extvars.items()}
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
        "speed": {
            k: EntryField.active[k].entry.get()
            for k in ["increment", "speed", "ACCspeed", "DECspeed", "ACCramp", "round"]
        },
        'limits':[('TODO','TODO') for _ in range(9)],
    }

    GUI.cfg = cfg
    with open(get_cfg(), "w") as file:
        json.dump(cfg, file)
