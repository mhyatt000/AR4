import os
import vision
from PIL import Image, ImageTk
import os.path as osp
import tkinter as tk
import tkinter.ttk as ttk

import calibrate
import controller
from exc import execution
import frames
from frames import AxisFrame, ExtJointFrame, JointFrame, ToolFrame
from gui.base import GUI, EntryField
from joint import JointCTRL
import teach
import theme

# NOTE tag vision Vis


def mk_img(path):
    """docstring"""
    return ImageTk.PhotoImage(Image.open(osp.join("assets", path)))


def build():
    """docstring"""

    VisBackdropImg = mk_img("VisBackdrop.png")
    VisBackdromLbl = ttk.Label(GUI.tabs["5"], image=VisBackdropImg)
    VisBackdromLbl.place(x=15, y=215)

    # cap= cv2.VideoCapture(0)
    video_frame = tk.Frame(GUI.tabs["5"], width=640, height=480)
    video_frame.place(x=50, y=250)

    vid_lbl = ttk.Label(video_frame)
    vid_lbl.place(x=0, y=0)

    vid_lbl.bind("<Button-1>", vision.motion)

    LiveLab = ttk.Label(GUI.tabs["5"], text="LIVE VIDEO FEED")
    LiveLab.place(x=750, y=390)

    liveCanvas = tk.Canvas(GUI.tabs["5"], width=490, height=330)
    liveCanvas.place(x=750, y=410)

    live_frame = tk.Frame(GUI.tabs["5"], width=480, height=320)
    live_frame.place(x=757, y=417)

    live_lbl = ttk.Label(live_frame)
    live_lbl.place(x=0, y=0)

    template_frame = tk.Frame(GUI.tabs["5"], width=150, height=150)
    template_frame.place(x=575, y=50)

    template_lbl = ttk.Label(template_frame)
    template_lbl.place(x=0, y=0)

    FoundValuesLab = ttk.Label(GUI.tabs["5"], text="FOUND VALUES")
    FoundValuesLab.place(x=750, y=30)

    CalValuesLab = ttk.Label(GUI.tabs["5"], text="CALIBRATION VALUES")
    CalValuesLab.place(x=900, y=30)

    texts = [
        "Choose Vision Format",
        "X found position (mm)",
        "Y found position (mm)",
        "R found position (ang)",
        "X pixes returned from camera",
        "Y pixes returned from camera",
    ]
    labels = [ttk.Label(GUI.tabs["5"], text=t) for t in texts]

    (
        VisInTypeLab,
        VisXfoundLab,
        VisYfoundLab,
        VisRZfoundLab,
        VisXpixfoundLab,
        VisYpixfoundLab,
    ) = labels

    # TODO: finish abstracting labels above

    ### 5 BUTTONS################################################################
    #############################################################################

    try:
        graph = FilterGraph()
        camList = graph.get_input_devices()
    except:
        camList = ["Select a Camera"]
    visoptions = tk.StringVar(GUI.tabs["5"])
    visoptions.set("Select a Camera")
    vismenu = tk.OptionMenu(GUI.tabs["5"], visoptions, camList[0], *camList)
    vismenu.config(width=20)
    vismenu.place(x=10, y=10)

    StartCamBut = tk.Button(GUI.tabs["5"], text="Start Camera", width=15, command=vision.start_vid)
    StartCamBut.place(x=200, y=10)

    StopCamBut = tk.Button(GUI.tabs["5"], text="Stop Camera", width=15, command=vision.stop_vid)
    StopCamBut.place(x=315, y=10)

    CapImgBut = tk.Button(GUI.tabs["5"], text="Snap Image", width=15, command=vision.take_pic)
    CapImgBut.place(x=10, y=50)

    TeachImgBut = tk.Button(GUI.tabs["5"], text="Teach Object", width=15, command=vision.selectTemplate)
    TeachImgBut.place(x=140, y=50)

    FindVisBut = tk.Button(GUI.tabs["5"], text="Snap & Find", width=15, command=vision.snapFind)
    FindVisBut.place(x=270, y=50)

    ZeroBrCnBut = tk.Button(GUI.tabs["5"], text="Zero", width=5, command=vision.zeroBrCn)
    ZeroBrCnBut.place(x=10, y=110)

    maskBut = tk.Button(GUI.tabs["5"], text="Mask", width=5, command=vision.selectMask)
    maskBut.place(x=10, y=150)

    VisZoomSlide = tk.Scale(GUI.tabs["5"], from_=50, to=1, length=250, orient=tk.HORIZONTAL)
    VisZoomSlide.bind("<ButtonRelease-1>", vision.VisUpdateBriCon)
    VisZoomSlide.place(x=75, y=95)
    VisZoomSlide.set(50)

    VisZoomLab = ttk.Label(GUI.tabs["5"], text="Zoom")
    VisZoomLab.place(x=75, y=115)

    VisBrightSlide = tk.Scale(GUI.tabs["5"], from_=-127, to=127, length=250, orient=tk.HORIZONTAL)
    VisBrightSlide.bind("<ButtonRelease-1>", vision.VisUpdateBriCon)
    VisBrightSlide.place(x=75, y=130)

    VisBrightLab = ttk.Label(GUI.tabs["5"], text="Brightness")
    VisBrightLab.place(x=75, y=150)

    VisContrastSlide = tk.Scale(GUI.tabs["5"], from_=-127, to=127, length=250, orient=tk.HORIZONTAL)
    VisContrastSlide.bind("<ButtonRelease-1>", vision.VisUpdateBriCon)
    VisContrastSlide.place(x=75, y=165)

    VisContrastLab = ttk.Label(GUI.tabs["5"], text="Contrast")
    VisContrastLab.place(x=75, y=185)

    GUI.full_rotCbut = tk.Checkbutton(GUI.tabs["5"], text="Full Rotation Search", variable=GUI.full_rot)
    GUI.full_rotCbut.place(x=900, y=255)

    pick180Cbut = tk.Checkbutton(GUI.tabs["5"], text="Pick Closest 180°", variable=pick180)
    pick180Cbut.place(x=900, y=275)

    pickClosestCbut = tk.Checkbutton(
        GUI.tabs["5"], text="Try Closest When Out of Range", variable=pickClosest
    )
    pickClosestCbut.place(x=900, y=295)

    saveCalBut = Button(
        GUI.tabs["5"], text="SAVE VISION DATA", width=26, command=calibrate.SaveAndApplyCalibration
    )
    saveCalBut.place(x=915, y=340)

    #### 5 ENTRY FIELDS##########################################################
    #############################################################################

    def make_entry_field(tab, text, x, y):
        """makes a new entry field"""

        field = tk.Entry(tab, width=15)
        field.place(x=x, y=y)
        label = ttk.Label(tab, text=text)
        label.place(x=x, y=y + 20)
        return field, label

    bgAutoCbut = tk.Checkbutton(GUI.tabs["5"], command=vision.checkAutoBG, text="Auto", variable=autoBG)
    bgAutoCbut.place(x=490, y=101)

    a, b = make_entry_field(GUI.tabs["5"], "Background Color", 390, 100)
    VisBacColorEntryField, VisBacColorLab = a, b

    a, b = make_entry_field(GUI.tabs["5"], "Score Threshold", 390, 150)
    VisScoreEntryField, VisScoreLab = a, b

    # TODO: finish abstracting

    EntryField(GUI.tabs["5"],name='VisRetScore' ,alt="Scored Value")
    EntryField(GUI.tabs["5"],name='VisRetAngle' ,alt="Found Angle")
    EntryField(GUI.tabs["5"],name='VisRetXpix' ,alt="Pixel X Position")
    EntryField(GUI.tabs["5"],name='VisRetYpix' ,alt="Pixel Y Position")
    EntryField(GUI.tabs["5"],name='VisRetXrob' ,alt="Robot X Position")
    EntryField(GUI.tabs["5"],name='VisRetYrob' ,alt="Robot Y Position")
    EntryField(GUI.tabs["5"],name='VisX1Pix' ,alt="X1 Pixel Pos")
    EntryField(GUI.tabs["5"],name='VisY1Pix' ,alt="Y1 Pixel Pos")
    EntryField(GUI.tabs["5"],name='VisX2Pix' ,alt="X2 Pixel Pos")
    EntryField(GUI.tabs["5"],name='VisY2Pix' ,alt="Y2 Pixel Pos")
    EntryField(GUI.tabs["5"],name='VisX1Rob' ,alt="X1 Robot Pos")
    EntryField(GUI.tabs["5"],name='VisY1Rob' ,alt="Y1 Robot Pos")
    EntryField(GUI.tabs["5"],name='VisX2Rob' ,alt="X2 Robot Pos")
    EntryField(GUI.tabs["5"],name='VisY2Rob' ,alt="Y2 Robot Pos")

    EntryField(GUI.tabs["5"],name='VisFileLoc' ,alt="Vision File Location:")

    VisPicOxPEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisPicOxMEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisPicOyPEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisPicOyMEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisPicXPEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisPicXMEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisPicYPEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisPicYMEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisXfindEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisYfindEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisRZfindEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisXpixfindEntryField = tk.Entry(GUI.tabs["5"], width=5)
    VisYpixfindEntryField = tk.Entry(GUI.tabs["5"], width=5)

    VisCalPixLab = ttk.Label(GUI.tabs["5"], text="Calibration Pixels:")
    VisCalmmLab = ttk.Label(GUI.tabs["5"], text="Calibration Robot MM:")
    VisCalOxLab = ttk.Label(GUI.tabs["5"], text="Orig: X")
    VisCalOyLab = ttk.Label(GUI.tabs["5"], text="Orig: Y")
    VisCalXLab = ttk.Label(GUI.tabs["5"], text="End: X")
    VisCalYLab = ttk.Label(GUI.tabs["5"], text="End: Y")

