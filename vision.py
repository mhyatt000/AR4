import datetime
import math
from multiprocessing.resource_sharer import stop
import os
from os import execv
import pathlib
import pickle
import threading
import time
from tkinter import *
from tkinter import messagebox, simpledialog, ttk
import tkinter.messagebox
from tkinter.ttk import *
import webbrowser

from PIL import Image, ImageTk
import cv2
from matplotlib import pyplot as plt
import numpy as np
from numpy import mean
import serial
from ttkthemes import ThemedStyle


def testvis():
    visprog = visoptions.get()
    if visprog[:] == "Openvision":
        openvision()
    if visprog[:] == "Roborealm 1.7.5":
        roborealm175()
    if visprog[:] == "x,y,r":
        xyr()


def openvision():
    Xpos, Ypos, VisEndYmm = None, None, None

    visfail = 1
    while visfail == 1:
        value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        while value == 0:
            try:
                f = open(VisFileLoc, "r")
                value = f.readlines()[-1]  # .decode()
            except:
                value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        x = int(value[110:122])
        y = int(value[130:142])
        viscalc(x, y)
        if Ypos > VisEndYmm:
            visfail = 1
            time.sleep(0.1)
        else:
            visfail = 0
    open(VisFileLoc, "w").close()
    VisXfindEntryField.delete(0, "end")
    VisXfindEntryField.insert(0, Xpos)
    VisYfindEntryField.delete(0, "end")
    VisYfindEntryField.insert(0, Ypos)
    VisRZfindEntryField.delete(0, "end")
    VisRZfindEntryField.insert(0, 0)
    ##
    VisXpixfindEntryField.delete(0, "end")
    VisXpixfindEntryField.insert(0, x)
    VisYpixfindEntryField.delete(0, "end")
    VisYpixfindEntryField.insert(0, y)
    ##
    SP_1_E1_EntryField.delete(0, "end")
    SP_1_E1_EntryField.insert(0, Xpos)
    SP_1_E2_EntryField.delete(0, "end")
    SP_1_E2_EntryField.insert(0, Ypos)


def roborealm175():
    global Xpos
    global Ypos
    global VisEndYmm
    visfail = 1
    while visfail == 1:
        value = 0
        almStatusLab.config(text="WAITING FOR CAMERA", style="Alarm.TLabel")
        almStatusLab2.config(text="WAITING FOR CAMERA", style="Alarm.TLabel")
        while value == 0:
            try:
                f = open(VisFileLoc, "r")
                value = f.readlines()[-1]  # .decode()
            except:
                value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        Index = value.index(",")
        x = float(value[:Index])
        y = float(value[Index + 1 :])
        viscalc(x, y)
        if float(Ypos) > float(VisEndYmm):
            visfail = 1
            time.sleep(0.1)
        else:
            visfail = 0
    open(VisFileLoc, "w").close()
    VisXfindEntryField.delete(0, "end")
    VisXfindEntryField.insert(0, Xpos)
    VisYfindEntryField.delete(0, "end")
    VisYfindEntryField.insert(0, Ypos)
    VisRZfindEntryField.delete(0, "end")
    VisRZfindEntryField.insert(0, 0)
    ##
    VisXpixfindEntryField.delete(0, "end")
    VisXpixfindEntryField.insert(0, x)
    VisYpixfindEntryField.delete(0, "end")
    VisYpixfindEntryField.insert(0, y)
    ##
    SP_1_E1_EntryField.delete(0, "end")
    SP_1_E1_EntryField.insert(0, Xpos)
    SP_1_E2_EntryField.delete(0, "end")
    SP_1_E2_EntryField.insert(0, Ypos)


def xyr():
    global Xpos
    global Ypos
    global VisEndYmm
    visfail = 1
    while visfail == 1:
        value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        while value == 0:
            try:
                f = open(VisFileLoc, "r")
                value = f.readlines()[-1]  # .decode()
            except:
                value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        Index = value.index(",")
        x = float(value[:Index])
        value2 = value[Index + 1 :]
        Index2 = value2.index(",")
        y = float(value2[:Index2])
        r = float(value2[Index2 + 1 :])
        viscalc(x, y)
        if Ypos > float(VisEndYmm):
            visfail = 1
            time.sleep(0.1)
        else:
            visfail = 0
    open(VisFileLoc, "w").close()
    VisXfindEntryField.delete(0, "end")
    VisXfindEntryField.insert(0, Xpos)
    VisYfindEntryField.delete(0, "end")
    VisYfindEntryField.insert(0, Ypos)
    VisRZfindEntryField.delete(0, "end")
    VisRZfindEntryField.insert(0, r)
    ##
    VisXpixfindEntryField.delete(0, "end")
    VisXpixfindEntryField.insert(0, x)
    VisYpixfindEntryField.delete(0, "end")
    VisYpixfindEntryField.insert(0, y)
    ##
    SP_1_E1_EntryField.delete(0, "end")
    SP_1_E1_EntryField.insert(0, str(Xpos))
    SP_1_E2_EntryField.delete(0, "end")
    SP_1_E2_EntryField.insert(0, str(Ypos))
    SP_1_E3_EntryField.delete(0, "end")
    SP_1_E3_EntryField.insert(0, r)


def viscalc():
    global xMMpos
    global yMMpos
    # origin x1 y1
    VisOrigXpix = float(VisX1PixEntryField.get())
    VisOrigXmm = float(VisX1RobEntryField.get())
    VisOrigYpix = float(VisY1PixEntryField.get())
    VisOrigYmm = float(VisY1RobEntryField.get())
    # x2 y2
    VisEndXpix = float(VisX2PixEntryField.get())
    VisEndXmm = float(VisX2RobEntryField.get())
    VisEndYpix = float(VisY2PixEntryField.get())
    VisEndYmm = float(VisY2RobEntryField.get())

    x = float(VisRetXpixEntryField.get())
    y = float(VisRetYpixEntryField.get())

    XPrange = float(VisEndXpix) - float(VisOrigXpix)
    XPratio = (x - float(VisOrigXpix)) / XPrange
    XMrange = float(VisEndXmm) - float(VisOrigXmm)
    XMpos = float(XMrange) * float(XPratio)
    xMMpos = float(VisOrigXmm) + XMpos
    ##
    YPrange = float(VisEndYpix) - float(VisOrigYpix)
    YPratio = (y - float(VisOrigYpix)) / YPrange
    YMrange = float(VisEndYmm) - float(VisOrigYmm)
    YMpos = float(YMrange) * float(YPratio)
    yMMpos = float(VisOrigYmm) + YMpos
    return (xMMpos, yMMpos)


# Define function to show frame
def show_frame():

    if cam_on:

        ret, frame = cap.read()

        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image).resize((480, 320))
            imgtk = ImageTk.PhotoImage(image=img)
            live_lbl.imgtk = imgtk
            live_lbl.configure(image=imgtk)

        live_lbl.after(10, show_frame)


def start_vid():
    global cam_on, cap
    global cap
    stop_vid()
    cam_on = True
    curVisStingSel = visoptions.get()
    l = len(camList)
    for i in range(l):
        if visoptions.get() == camList[i]:
            selectedCam = i
    cap = cv2.VideoCapture(selectedCam)
    show_frame()


def stop_vid():
    global cam_on
    cam_on = False

    if cap:
        cap.release()


# vismenu.size


def take_pic():
    global selectedCam
    global cap
    global BGavg
    global mX1
    global mY1
    global mX2
    global mY2

    if cam_on == True:
        ret, frame = cap.read()
    else:
        curVisStingSel = visoptions.get()
        l = len(camList)
        for i in range(l):
            if visoptions.get() == camList[i]:
                selectedCam = i
                # print(selectedCam)
        cap = cv2.VideoCapture(selectedCam)
        ret, frame = cap.read()

    brightness = int(VisBrightSlide.get())
    contrast = int(VisContrastSlide.get())
    zoom = int(VisZoomSlide.get())

    # manEntryField.delete(0, 'end')
    # manEntryField.insert(0,str(zoom))

    frame = np.int16(frame)
    frame = frame * (contrast / 127 + 1) - contrast + brightness
    frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # get the webcam size
    height, width = cv2image.shape

    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(zoom * height / 100), int(zoom * width / 100)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = cv2image[minX:maxX, minY:maxY]
    cv2image = cv2.resize(cropped, (width, height))

    autoBGVal = int(autoBG.get())
    if autoBGVal == 1:
        BG1 = cv2image[int(VisX1PixEntryField.get())][int(VisY1PixEntryField.get())]
        BG2 = cv2image[int(VisX1PixEntryField.get())][int(VisY2PixEntryField.get())]
        BG3 = cv2image[int(VisX2PixEntryField.get())][int(VisY2PixEntryField.get())]
        avg = int(mean([BG1, BG2, BG3]))
        BGavg = (avg, avg, avg)
        background = avg
        VisBacColorEntryField.configure(state="enabled")
        VisBacColorEntryField.delete(0, "end")
        VisBacColorEntryField.insert(0, str(BGavg))
        VisBacColorEntryField.configure(state="disabled")
    else:
        temp = VisBacColorEntryField.get()
        startIndex = temp.find("(")
        endIndex = temp.find(",")
        background = int(temp[startIndex + 1 : endIndex])
        # background = eval(VisBacColorEntryField.get())

    h = cv2image.shape[0]
    w = cv2image.shape[1]
    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            # change the pixel
            cv2image[y, x] = (
                background if x >= mX2 or x <= mX1 or y <= mY1 or y >= mY2 else cv2image[y, x]
            )

    img = Image.fromarray(cv2image).resize((640, 480))

    imgtk = ImageTk.PhotoImage(image=img)
    vid_lbl.imgtk = imgtk
    vid_lbl.configure(image=imgtk)
    filename = "curImage.jpg"
    cv2.imwrite(filename, cv2image)


def mask_pic():
    global selectedCam
    global cap
    global BGavg
    global mX1
    global mY1
    global mX2
    global mY2

    if cam_on == True:
        ret, frame = cap.read()
    else:
        curVisStingSel = visoptions.get()
        l = len(camList)
        for i in range(l):
            if visoptions.get() == camList[i]:
                selectedCam = i
                # print(selectedCam)
        cap = cv2.VideoCapture(selectedCam)
        ret, frame = cap.read()
    brightness = int(VisBrightSlide.get())
    contrast = int(VisContrastSlide.get())
    zoom = int(VisZoomSlide.get())
    frame = np.int16(frame)
    frame = frame * (contrast / 127 + 1) - contrast + brightness
    frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # get the webcam size
    height, width = cv2image.shape
    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(zoom * height / 100), int(zoom * width / 100)
    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY
    cropped = cv2image[minX:maxX, minY:maxY]
    cv2image = cv2.resize(cropped, (width, height))
    # img = Image.fromarray(cv2image).resize((640,480))
    # imgtk = ImageTk.PhotoImage(image=img)
    # vid_lbl.imgtk = imgtk
    # vid_lbl.configure(image=imgtk)
    filename = "curImage.jpg"
    cv2.imwrite(filename, cv2image)


def mask_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    global oriImage
    global box_points
    global button_down
    global mX1
    global mY1
    global mX2
    global mY2

    cropDone = False

    if (button_down == False) and (event == cv2.EVENT_LBUTTONDOWN):
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
        button_down = True
        box_points = [(x, y)]

    # Mouse is Moving
    elif (button_down == True) and (event == cv2.EVENT_MOUSEMOVE):
        if cropping == True:
            image_copy = oriImage.copy()
            x_end, y_end = x, y
            point = (x, y)
            cv2.rectangle(image_copy, box_points[0], point, (0, 255, 0), 2)
            cv2.imshow("image", image_copy)

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        button_down = False
        box_points.append((x, y))
        cv2.rectangle(oriImage, box_points[0], box_points[1], (0, 255, 0), 2)
        cv2.imshow("image", oriImage)
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished

        mX1 = x_start + 3
        mY1 = y_start + 3
        mX2 = x_end - 3
        mY2 = y_end - 3

        autoBGVal = int(autoBG.get())
        if autoBGVal == 1:
            BG1 = oriImage[int(VisX1PixEntryField.get())][int(VisY1PixEntryField.get())]
            BG2 = oriImage[int(VisX1PixEntryField.get())][int(VisY2PixEntryField.get())]
            BG3 = oriImage[int(VisX2PixEntryField.get())][int(VisY2PixEntryField.get())]
            avg = int(mean([BG1, BG2, BG3]))
            BGavg = (avg, avg, avg)
            background = avg
            VisBacColorEntryField.configure(state="enabled")
            VisBacColorEntryField.delete(0, "end")
            VisBacColorEntryField.insert(0, str(BGavg))
            VisBacColorEntryField.configure(state="disabled")
        else:
            background = eval(VisBacColorEntryField.get())

        h = oriImage.shape[0]
        w = oriImage.shape[1]
        # loop over the image
        for y in range(0, h):
            for x in range(0, w):
                # change the pixel
                oriImage[y, x] = (
                    background if x >= mX2 or x <= mX1 or y <= mY1 or y >= mY2 else oriImage[y, x]
                )

        img = Image.fromarray(oriImage)
        imgtk = ImageTk.PhotoImage(image=img)
        vid_lbl.imgtk = imgtk
        vid_lbl.configure(image=imgtk)
        filename = "curImage.jpg"
        cv2.imwrite(filename, oriImage)
        cv2.destroyAllWindows()


def selectMask():
    global oriImage
    global button_down
    button_down = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    mask_pic()

    image = cv2.imread("curImage.jpg")
    oriImage = image.copy()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mask_crop)
    cv2.imshow("image", image)


def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    global oriImage
    global box_points
    global button_down

    cropDone = False

    if (button_down == False) and (event == cv2.EVENT_LBUTTONDOWN):
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
        button_down = True
        box_points = [(x, y)]

    # Mouse is Moving
    elif (button_down == True) and (event == cv2.EVENT_MOUSEMOVE):
        if cropping == True:
            image_copy = oriImage.copy()
            x_end, y_end = x, y
            point = (x, y)
            cv2.rectangle(image_copy, box_points[0], point, (0, 255, 0), 2)
            cv2.imshow("image", image_copy)

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        button_down = False
        box_points.append((x, y))
        cv2.rectangle(oriImage, box_points[0], box_points[1], (0, 255, 0), 2)
        cv2.imshow("image", oriImage)
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished

        refPoint = [(x_start + 3, y_start + 3), (x_end - 3, y_end - 3)]

        if len(refPoint) == 2:  # when two points were found
            roi = oriImage[refPoint[0][1] : refPoint[1][1], refPoint[0][0] : refPoint[1][0]]

            cv2.imshow("Cropped", roi)
            USER_INP = simpledialog.askstring(title="Teach Vision Object", prompt="Save Object As:")
            templateName = USER_INP + ".jpg"
            cv2.imwrite(templateName, roi)
            cv2.destroyAllWindows()
            updateVisOp()


def selectTemplate():
    global oriImage
    global button_down
    button_down = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    image = cv2.imread("curImage.jpg")
    oriImage = image.copy()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)
    cv2.imshow("image", image)


def snapFind():
    global selectedTemplate
    global BGavg
    take_pic()
    template = selectedTemplate.get()
    min_score = float(VisScoreEntryField.get()) * 0.01
    autoBGVal = int(autoBG.get())
    if autoBGVal == 1:
        background = BGavg
        VisBacColorEntryField.configure(state="enabled")
        VisBacColorEntryField.delete(0, "end")
        VisBacColorEntryField.insert(0, str(BGavg))
        VisBacColorEntryField.configure(state="disabled")
    else:
        background = eval(VisBacColorEntryField.get())
    visFind(template, min_score, background)


def rotate_image(img, angle, background):
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.0)
    result = cv2.warpAffine(
        img,
        rot_mat,
        img.shape[1::-1],
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=background,
        flags=cv2.INTER_LINEAR,
    )
    return result


def visFind(template, min_score, background):
    global xMMpos
    global yMMpos
    global autoBG
    # manEntryField.delete(0, 'end')
    # manEntryField.insert(0,min_score)

    if background == "Auto":
        background = BGavg
        VisBacColorEntryField.configure(state="enabled")
        VisBacColorEntryField.delete(0, "end")
        VisBacColorEntryField.insert(0, str(BGavg))
        VisBacColorEntryField.configure(state="disabled")

    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    dkgreen = (0, 128, 0)
    status = "fail"
    highscore = 0
    img1 = cv2.imread("curImage.jpg")  # target Image
    img2 = cv2.imread(template)  # target Image

    # method = cv2.TM_CCOEFF_NORMED
    # method = cv2.TM_CCORR_NORMED

    img = img1.copy()

    fullRotVal = int(fullRot.get())

    for i in range(1):
        if i == 0:
            method = cv2.TM_CCOEFF_NORMED
        else:
            # method = cv2.TM_CCOEFF_NORMED
            method = cv2.TM_CCORR_NORMED

        # USE 1/3 - EACH SIDE SEARCH
        if fullRotVal == 0:
            ## fist pass 1/3rds
            curangle = 0
            highangle = 0
            highscore = 0
            highmax_loc = 0
            for x in range(3):
                template = img2
                template = rotate_image(img2, curangle, background)
                w, h = template.shape[1::-1]
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > highscore:
                    highscore = max_val
                    highangle = curangle
                    highmax_loc = max_loc
                    highw, highh = w, h
                curangle += 120

            # check each side and narrow in
            while True:
                curangle = curangle / 2
                if curangle < 0.9:
                    break
                nextangle1 = highangle + curangle
                nextangle2 = highangle - curangle
                template = img2
                template = rotate_image(img2, nextangle1, background)
                w, h = template.shape[1::-1]
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > highscore:
                    highscore = max_val
                    highangle = nextangle1
                    highmax_loc = max_loc
                    highw, highh = w, h
                template = img2
                template = rotate_image(img2, nextangle2, background)
                w, h = template.shape[1::-1]
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > highscore:
                    highscore = max_val
                    highangle = nextangle2
                    highmax_loc = max_loc
                    highw, highh = w, h

        # USE FULL 360 SEARCh
        else:
            for i in range(720):
                template = rotate_image(img2, i, background)
                w, h = template.shape[1::-1]

                img = img1.copy()
                # Apply template Matching
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                highscore = max_val
                highangle = i
                highmax_loc = max_loc
                highw, highh = w, h
                if highscore >= min_score:
                    break
        if i == 1:
            highscore = highscore * 0.5
        if highscore >= min_score:
            break

    if highscore >= min_score:
        status = "pass"
        # normalize angle to increment of +180 to -180
        if highangle > 180:
            highangle = -360 + highangle
        # pick closest 180
        pick180Val = int(pick180.get())
        if pick180Val == 1:
            if highangle > 90:
                highangle = -180 + highangle
            elif highangle < -90:
                highangle = 180 + highangle
        # try closest
        pickClosestVal = int(pickClosest.get())
        if pickClosestVal == highangle and highangle > J6axisLimPos:
            highangle = J6axisLimPos
        elif pickClosestVal == 0 and highangle > J6axisLimPos:
            status = "fail"
        if pickClosestVal == 1 and highangle < (J6axisLimNeg * -1):
            highangle = J6axisLimNeg * -1
        elif pickClosestVal == 0 and highangle < (J6axisLimNeg * -1):
            status = "fail"

        top_left = highmax_loc
        bottom_right = (top_left[0] + highw, top_left[1] + highh)
        # find center
        center = (top_left[0] + highw / 2, top_left[1] + highh / 2)
        xPos = int(center[1])
        yPos = int(center[0])

        imgxPos = int(center[0])
        imgyPos = int(center[1])

        # find line 1 end
        line1x = int(imgxPos + 60 * math.cos(math.radians(highangle - 90)))
        line1y = int(imgyPos + 60 * math.sin(math.radians(highangle - 90)))
        cv2.line(img, (imgxPos, imgyPos), (line1x, line1y), green, 3)

        # find line 2 end
        line2x = int(imgxPos + 60 * math.cos(math.radians(highangle + 90)))
        line2y = int(imgyPos + 60 * math.sin(math.radians(highangle + 90)))
        cv2.line(img, (imgxPos, imgyPos), (line2x, line2y), green, 3)

        # find line 3 end
        line3x = int(imgxPos + 30 * math.cos(math.radians(highangle)))
        line3y = int(imgyPos + 30 * math.sin(math.radians(highangle)))
        cv2.line(img, (imgxPos, imgyPos), (line3x, line3y), green, 3)

        # find line 4 end
        line4x = int(imgxPos + 30 * math.cos(math.radians(highangle + 180)))
        line4y = int(imgyPos + 30 * math.sin(math.radians(highangle + 180)))
        cv2.line(img, (imgxPos, imgyPos), (line4x, line4y), green, 3)

        # find tip start
        lineTx = int(imgxPos + 56 * math.cos(math.radians(highangle - 90)))
        lineTy = int(imgyPos + 56 * math.sin(math.radians(highangle - 90)))
        cv2.line(img, (lineTx, lineTy), (line1x, line1y), dkgreen, 2)

        cv2.circle(img, (imgxPos, imgyPos), 20, green, 1)
        # cv2.rectangle(img,top_left, bottom_right, green, 2)
        cv2.imwrite("temp.jpg", img)
        img = Image.fromarray(img).resize((640, 480))
        imgtk = ImageTk.PhotoImage(image=img)
        vid_lbl.imgtk = imgtk
        vid_lbl.configure(image=imgtk)
        VisRetScoreEntryField.delete(0, "end")
        VisRetScoreEntryField.insert(0, str(round((highscore * 100), 2)))
        VisRetAngleEntryField.delete(0, "end")
        VisRetAngleEntryField.insert(0, str(highangle))
        VisRetXpixEntryField.delete(0, "end")
        VisRetXpixEntryField.insert(0, str(xPos))
        VisRetYpixEntryField.delete(0, "end")
        VisRetYpixEntryField.insert(0, str(yPos))
        viscalc()
        VisRetXrobEntryField.delete(0, "end")
        VisRetXrobEntryField.insert(0, str(round(xMMpos, 2)))
        VisRetYrobEntryField.delete(0, "end")
        VisRetYrobEntryField.insert(0, str(round(yMMpos, 2)))

        # break
        # if (score > highscore):
        # highscore=score

    if status == "fail":
        cv2.rectangle(img, (5, 5), (635, 475), red, 5)
        cv2.imwrite("temp.jpg", img)
        img = Image.fromarray(img).resize((640, 480))
        imgtk = ImageTk.PhotoImage(image=img)
        vid_lbl.imgtk = imgtk
        vid_lbl.configure(image=imgtk)
        VisRetScoreEntryField.delete(0, "end")
        VisRetScoreEntryField.insert(0, str(round((highscore * 100), 2)))
        VisRetAngleEntryField.delete(0, "end")
        VisRetAngleEntryField.insert(0, "NA")
        VisRetXpixEntryField.delete(0, "end")
        VisRetXpixEntryField.insert(0, "NA")
        VisRetYpixEntryField.delete(0, "end")
        VisRetYpixEntryField.insert(0, "NA")

    return status


# initial vis attempt using sift with flann pattern match
# def visFind(template):
#  take_pic()
#  MIN_MATCH_COUNT = 10
#  img1 = cv2.imread(template)  # query Image
#  img2 = cv2.imread('curImage.jpg')  # target Image
#  # Initiate SIFT detector
#  sift = cv2.SIFT_create()
#  # find the keypoints and descriptors with SIFT
#  kp1, des1 = sift.detectAndCompute(img1,None)
#  kp2, des2 = sift.detectAndCompute(img2,None)
#  FLANN_INDEX_KDTREE = 1
#  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#  search_params = dict(checks = 50)
#  flann = cv2.FlannBasedMatcher(index_params, search_params)
#  matches = flann.knnMatch(des1,des2,k=2)
#  # store all the good matches as per Lowe's ratio test.
#  good = []
#  for m,n in matches:
#      if m.distance < 1.1*n.distance:
#          good.append(m)

#  if len(good)>MIN_MATCH_COUNT:
#      src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
#      dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
#      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
#      matchesMask = mask.ravel().tolist()
#      h,w,c = img1.shape
#      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#      dst = cv2.perspectiveTransform(pts,M)
#      #img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
#
#      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#      dst = cv2.perspectiveTransform(pts,M)
#
#      crosspts = np.float32([ [w/2,0],[w/2,h-1],[0,h/2],[w-1,h/2] ]).reshape(-1,1,2)
#      crossCoord = cv2.perspectiveTransform(crosspts,M)
#
#      cenPt = np.float32([w/2,h/2]).reshape(-1,1,2)
#      cenCoord = cv2.perspectiveTransform(cenPt,M)
#
#      cenResult = cenCoord[0].reshape(1,-1).flatten().tolist()
#      theta = - math.atan2(M[0,1], M[0,0]) * 180 / math.pi
#
#      xPos = cenResult[0]
#      yPos = cenResult[1]
#
#      cross1Result = crossCoord[0].reshape(2,-1).flatten().tolist()
#      cross2Result = crossCoord[1].reshape(2,-1).flatten().tolist()
#      cross3Result = crossCoord[2].reshape(2,-1).flatten().tolist()
#      cross4Result = crossCoord[3].reshape(2,-1).flatten().tolist()
#
#      x1Pos = int(cross1Result[0])
#      y1Pos = int(cross1Result[1])
#      x2Pos = int(cross2Result[0])
#      y2Pos = int(cross2Result[1])
#      x3Pos = int(cross3Result[0])
#      y3Pos = int(cross3Result[1])
#      x4Pos = int(cross4Result[0])
#      y4Pos = int(cross4Result[1])
#
#
#      print(xPos)
#      print(yPos)
#      print(theta)
#
#
#      #draw bounding box
#      #img2 = cv2.polylines(img2, [np.int32(dst)], True, (0,255,0),3, cv2.LINE_AA)
#
#      #draw circle
#      img2 = cv2.circle(img2, (int(xPos),int(yPos)), radius=30, color=(0, 255, 0), thickness=3)
#
#      #draw line 1
#      cv2.line(img2, (x1Pos,y1Pos), (x2Pos,y2Pos), (0,255,0), 3)
#      #draw line 2
#      cv2.line(img2, (x3Pos,y3Pos), (x4Pos,y4Pos), (0,255,0), 3)
#
#      #save image
#      cv2.imwrite('curImage.jpg', img2)
#      img = Image.fromarray(img2)
#      imgtk = ImageTk.PhotoImage(image=img)
#      vid_lbl.imgtk = imgtk
#      vid_lbl.configure(image=imgtk)
#
#
#
#
#  else:
#      print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
#      matchesMask = None


def updateVisOp():
    global selectedTemplate
    selectedTemplate = StringVar()
    folder = os.path.dirname(os.path.realpath(__file__))
    filelist = [fname for fname in os.listdir(folder) if fname.endswith(".jpg")]
    Visoptmenu = ttk.Combobox(
        tab5, textvariable=selectedTemplate, values=filelist, state="readonly"
    )
    Visoptmenu.place(x=390, y=52)
    Visoptmenu.bind("<<ComboboxSelected>>", VisOpUpdate)


def VisOpUpdate(foo):
    global selectedTemplate
    file = selectedTemplate.get()
    print(file)
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    TARGET_PIXEL_AREA = 22500

    ratio = float(img.shape[1]) / float(img.shape[0])
    new_h = int(math.sqrt(TARGET_PIXEL_AREA / ratio) + 0.5)
    new_w = int((new_h * ratio) + 0.5)

    img = cv2.resize(img, (new_w, new_h))

    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    template_lbl.imgtk = imgtk
    template_lbl.configure(image=imgtk)


def zeroBrCn():
    global mX1
    global mY1
    global mX2
    global mY2
    mX1 = 0
    mY1 = 0
    mX2 = 640
    mY2 = 480
    VisBrightSlide.set(0)
    VisContrastSlide.set(0)
    # VisZoomSlide.set(50)
    take_pic()


def VisUpdateBriCon(foo):
    take_pic()


def motion(event):
    y = event.x
    x = event.y

    if x <= 240 and y <= 320:
        VisX1PixEntryField.delete(0, "end")
        VisX1PixEntryField.insert(0, x)
        VisY1PixEntryField.delete(0, "end")
        VisY1PixEntryField.insert(0, y)
    elif x > 240:
        VisX2PixEntryField.delete(0, "end")
        VisX2PixEntryField.insert(0, x)
    elif y > 320:
        VisY2PixEntryField.delete(0, "end")
        VisY2PixEntryField.insert(0, y)

    # print(str(x) +","+str(y))


def checkAutoBG():
    autoBGVal = int(autoBG.get())
    if autoBGVal == 1:
        VisBacColorEntryField.configure(state="disabled")
    else:
        VisBacColorEntryField.configure(state="enabled")


def testvis():
    visprog = visoptions.get()
    if visprog[:] == "Openvision":
        openvision()
    if visprog[:] == "Roborealm 1.7.5":
        roborealm175()
    if visprog[:] == "x,y,r":
        xyr()


def openvision():
    Xpos, Ypos, VisEndYmm = None, None, None

    visfail = 1
    while visfail == 1:
        value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        while value == 0:
            try:
                f = open(VisFileLoc, "r")
                value = f.readlines()[-1]  # .decode()
            except:
                value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        x = int(value[110:122])
        y = int(value[130:142])
        viscalc(x, y)
        if Ypos > VisEndYmm:
            visfail = 1
            time.sleep(0.1)
        else:
            visfail = 0
    open(VisFileLoc, "w").close()
    VisXfindEntryField.delete(0, "end")
    VisXfindEntryField.insert(0, Xpos)
    VisYfindEntryField.delete(0, "end")
    VisYfindEntryField.insert(0, Ypos)
    VisRZfindEntryField.delete(0, "end")
    VisRZfindEntryField.insert(0, 0)
    ##
    VisXpixfindEntryField.delete(0, "end")
    VisXpixfindEntryField.insert(0, x)
    VisYpixfindEntryField.delete(0, "end")
    VisYpixfindEntryField.insert(0, y)
    ##
    SP_1_E1_EntryField.delete(0, "end")
    SP_1_E1_EntryField.insert(0, Xpos)
    SP_1_E2_EntryField.delete(0, "end")
    SP_1_E2_EntryField.insert(0, Ypos)


def roborealm175():
    global Xpos
    global Ypos
    global VisEndYmm
    visfail = 1
    while visfail == 1:
        value = 0
        almStatusLab.config(text="WAITING FOR CAMERA", style="Alarm.TLabel")
        almStatusLab2.config(text="WAITING FOR CAMERA", style="Alarm.TLabel")
        while value == 0:
            try:
                f = open(VisFileLoc, "r")
                value = f.readlines()[-1]  # .decode()
            except:
                value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        Index = value.index(",")
        x = float(value[:Index])
        y = float(value[Index + 1 :])
        viscalc(x, y)
        if float(Ypos) > float(VisEndYmm):
            visfail = 1
            time.sleep(0.1)
        else:
            visfail = 0
    open(VisFileLoc, "w").close()
    VisXfindEntryField.delete(0, "end")
    VisXfindEntryField.insert(0, Xpos)
    VisYfindEntryField.delete(0, "end")
    VisYfindEntryField.insert(0, Ypos)
    VisRZfindEntryField.delete(0, "end")
    VisRZfindEntryField.insert(0, 0)
    ##
    VisXpixfindEntryField.delete(0, "end")
    VisXpixfindEntryField.insert(0, x)
    VisYpixfindEntryField.delete(0, "end")
    VisYpixfindEntryField.insert(0, y)
    ##
    SP_1_E1_EntryField.delete(0, "end")
    SP_1_E1_EntryField.insert(0, Xpos)
    SP_1_E2_EntryField.delete(0, "end")
    SP_1_E2_EntryField.insert(0, Ypos)


def xyr():
    global Xpos
    global Ypos
    global VisEndYmm
    visfail = 1
    while visfail == 1:
        value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        while value == 0:
            try:
                f = open(VisFileLoc, "r")
                value = f.readlines()[-1]  # .decode()
            except:
                value = 0
        almStatusLab.config(text="SYSTEM READY", style="OK.TLabel")
        almStatusLab2.config(text="SYSTEM READY", style="OK.TLabel")
        Index = value.index(",")
        x = float(value[:Index])
        value2 = value[Index + 1 :]
        Index2 = value2.index(",")
        y = float(value2[:Index2])
        r = float(value2[Index2 + 1 :])
        viscalc(x, y)
        if Ypos > float(VisEndYmm):
            visfail = 1
            time.sleep(0.1)
        else:
            visfail = 0
    open(VisFileLoc, "w").close()
    VisXfindEntryField.delete(0, "end")
    VisXfindEntryField.insert(0, Xpos)
    VisYfindEntryField.delete(0, "end")
    VisYfindEntryField.insert(0, Ypos)
    VisRZfindEntryField.delete(0, "end")
    VisRZfindEntryField.insert(0, r)
    ##
    VisXpixfindEntryField.delete(0, "end")
    VisXpixfindEntryField.insert(0, x)
    VisYpixfindEntryField.delete(0, "end")
    VisYpixfindEntryField.insert(0, y)
    ##
    SP_1_E1_EntryField.delete(0, "end")
    SP_1_E1_EntryField.insert(0, str(Xpos))
    SP_1_E2_EntryField.delete(0, "end")
    SP_1_E2_EntryField.insert(0, str(Ypos))
    SP_1_E3_EntryField.delete(0, "end")
    SP_1_E3_EntryField.insert(0, r)


def viscalc():
    global xMMpos
    global yMMpos
    # origin x1 y1
    VisOrigXpix = float(VisX1PixEntryField.get())
    VisOrigXmm = float(VisX1RobEntryField.get())
    VisOrigYpix = float(VisY1PixEntryField.get())
    VisOrigYmm = float(VisY1RobEntryField.get())
    # x2 y2
    VisEndXpix = float(VisX2PixEntryField.get())
    VisEndXmm = float(VisX2RobEntryField.get())
    VisEndYpix = float(VisY2PixEntryField.get())
    VisEndYmm = float(VisY2RobEntryField.get())

    x = float(VisRetXpixEntryField.get())
    y = float(VisRetYpixEntryField.get())

    XPrange = float(VisEndXpix) - float(VisOrigXpix)
    XPratio = (x - float(VisOrigXpix)) / XPrange
    XMrange = float(VisEndXmm) - float(VisOrigXmm)
    XMpos = float(XMrange) * float(XPratio)
    xMMpos = float(VisOrigXmm) + XMpos
    ##
    YPrange = float(VisEndYpix) - float(VisOrigYpix)
    YPratio = (y - float(VisOrigYpix)) / YPrange
    YMrange = float(VisEndYmm) - float(VisOrigYmm)
    YMpos = float(YMrange) * float(YPratio)
    yMMpos = float(VisOrigYmm) + YMpos
    return (xMMpos, yMMpos)


# Define function to show frame
def show_frame():

    if cam_on:

        ret, frame = cap.read()

        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image).resize((480, 320))
            imgtk = ImageTk.PhotoImage(image=img)
            live_lbl.imgtk = imgtk
            live_lbl.configure(image=imgtk)

        live_lbl.after(10, show_frame)


def start_vid():
    global cam_on, cap
    global cap
    stop_vid()
    cam_on = True
    curVisStingSel = visoptions.get()
    l = len(camList)
    for i in range(l):
        if visoptions.get() == camList[i]:
            selectedCam = i
    cap = cv2.VideoCapture(selectedCam)
    show_frame()


def stop_vid():
    global cam_on
    cam_on = False

    if cap:
        cap.release()


# vismenu.size


def take_pic():
    global selectedCam
    global cap
    global BGavg
    global mX1
    global mY1
    global mX2
    global mY2

    if cam_on == True:
        ret, frame = cap.read()
    else:
        curVisStingSel = visoptions.get()
        l = len(camList)
        for i in range(l):
            if visoptions.get() == camList[i]:
                selectedCam = i
                # print(selectedCam)
        cap = cv2.VideoCapture(selectedCam)
        ret, frame = cap.read()

    brightness = int(VisBrightSlide.get())
    contrast = int(VisContrastSlide.get())
    zoom = int(VisZoomSlide.get())

    # manEntryField.delete(0, 'end')
    # manEntryField.insert(0,str(zoom))

    frame = np.int16(frame)
    frame = frame * (contrast / 127 + 1) - contrast + brightness
    frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # get the webcam size
    height, width = cv2image.shape

    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(zoom * height / 100), int(zoom * width / 100)

    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY

    cropped = cv2image[minX:maxX, minY:maxY]
    cv2image = cv2.resize(cropped, (width, height))

    autoBGVal = int(autoBG.get())
    if autoBGVal == 1:
        BG1 = cv2image[int(VisX1PixEntryField.get())][int(VisY1PixEntryField.get())]
        BG2 = cv2image[int(VisX1PixEntryField.get())][int(VisY2PixEntryField.get())]
        BG3 = cv2image[int(VisX2PixEntryField.get())][int(VisY2PixEntryField.get())]
        avg = int(mean([BG1, BG2, BG3]))
        BGavg = (avg, avg, avg)
        background = avg
        VisBacColorEntryField.configure(state="enabled")
        VisBacColorEntryField.delete(0, "end")
        VisBacColorEntryField.insert(0, str(BGavg))
        VisBacColorEntryField.configure(state="disabled")
    else:
        temp = VisBacColorEntryField.get()
        startIndex = temp.find("(")
        endIndex = temp.find(",")
        background = int(temp[startIndex + 1 : endIndex])
        # background = eval(VisBacColorEntryField.get())

    h = cv2image.shape[0]
    w = cv2image.shape[1]
    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            # change the pixel
            cv2image[y, x] = (
                background if x >= mX2 or x <= mX1 or y <= mY1 or y >= mY2 else cv2image[y, x]
            )

    img = Image.fromarray(cv2image).resize((640, 480))

    imgtk = ImageTk.PhotoImage(image=img)
    vid_lbl.imgtk = imgtk
    vid_lbl.configure(image=imgtk)
    filename = "curImage.jpg"
    cv2.imwrite(filename, cv2image)


def mask_pic():
    global selectedCam
    global cap
    global BGavg
    global mX1
    global mY1
    global mX2
    global mY2

    if cam_on == True:
        ret, frame = cap.read()
    else:
        curVisStingSel = visoptions.get()
        l = len(camList)
        for i in range(l):
            if visoptions.get() == camList[i]:
                selectedCam = i
                # print(selectedCam)
        cap = cv2.VideoCapture(selectedCam)
        ret, frame = cap.read()
    brightness = int(VisBrightSlide.get())
    contrast = int(VisContrastSlide.get())
    zoom = int(VisZoomSlide.get())
    frame = np.int16(frame)
    frame = frame * (contrast / 127 + 1) - contrast + brightness
    frame = np.clip(frame, 0, 255)
    frame = np.uint8(frame)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # get the webcam size
    height, width = cv2image.shape
    # prepare the crop
    centerX, centerY = int(height / 2), int(width / 2)
    radiusX, radiusY = int(zoom * height / 100), int(zoom * width / 100)
    minX, maxX = centerX - radiusX, centerX + radiusX
    minY, maxY = centerY - radiusY, centerY + radiusY
    cropped = cv2image[minX:maxX, minY:maxY]
    cv2image = cv2.resize(cropped, (width, height))
    # img = Image.fromarray(cv2image).resize((640,480))
    # imgtk = ImageTk.PhotoImage(image=img)
    # vid_lbl.imgtk = imgtk
    # vid_lbl.configure(image=imgtk)
    filename = "curImage.jpg"
    cv2.imwrite(filename, cv2image)


def mask_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    global oriImage
    global box_points
    global button_down
    global mX1
    global mY1
    global mX2
    global mY2

    cropDone = False

    if (button_down == False) and (event == cv2.EVENT_LBUTTONDOWN):
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
        button_down = True
        box_points = [(x, y)]

    # Mouse is Moving
    elif (button_down == True) and (event == cv2.EVENT_MOUSEMOVE):
        if cropping == True:
            image_copy = oriImage.copy()
            x_end, y_end = x, y
            point = (x, y)
            cv2.rectangle(image_copy, box_points[0], point, (0, 255, 0), 2)
            cv2.imshow("image", image_copy)

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        button_down = False
        box_points.append((x, y))
        cv2.rectangle(oriImage, box_points[0], box_points[1], (0, 255, 0), 2)
        cv2.imshow("image", oriImage)
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished

        mX1 = x_start + 3
        mY1 = y_start + 3
        mX2 = x_end - 3
        mY2 = y_end - 3

        autoBGVal = int(autoBG.get())
        if autoBGVal == 1:
            BG1 = oriImage[int(VisX1PixEntryField.get())][int(VisY1PixEntryField.get())]
            BG2 = oriImage[int(VisX1PixEntryField.get())][int(VisY2PixEntryField.get())]
            BG3 = oriImage[int(VisX2PixEntryField.get())][int(VisY2PixEntryField.get())]
            avg = int(mean([BG1, BG2, BG3]))
            BGavg = (avg, avg, avg)
            background = avg
            VisBacColorEntryField.configure(state="enabled")
            VisBacColorEntryField.delete(0, "end")
            VisBacColorEntryField.insert(0, str(BGavg))
            VisBacColorEntryField.configure(state="disabled")
        else:
            background = eval(VisBacColorEntryField.get())

        h = oriImage.shape[0]
        w = oriImage.shape[1]
        # loop over the image
        for y in range(0, h):
            for x in range(0, w):
                # change the pixel
                oriImage[y, x] = (
                    background if x >= mX2 or x <= mX1 or y <= mY1 or y >= mY2 else oriImage[y, x]
                )

        img = Image.fromarray(oriImage)
        imgtk = ImageTk.PhotoImage(image=img)
        vid_lbl.imgtk = imgtk
        vid_lbl.configure(image=imgtk)
        filename = "curImage.jpg"
        cv2.imwrite(filename, oriImage)
        cv2.destroyAllWindows()


def selectMask():
    global oriImage
    global button_down
    button_down = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    mask_pic()

    image = cv2.imread("curImage.jpg")
    oriImage = image.copy()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mask_crop)
    cv2.imshow("image", image)


def mouse_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping
    global oriImage
    global box_points
    global button_down

    cropDone = False

    if (button_down == False) and (event == cv2.EVENT_LBUTTONDOWN):
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
        button_down = True
        box_points = [(x, y)]

    # Mouse is Moving
    elif (button_down == True) and (event == cv2.EVENT_MOUSEMOVE):
        if cropping == True:
            image_copy = oriImage.copy()
            x_end, y_end = x, y
            point = (x, y)
            cv2.rectangle(image_copy, box_points[0], point, (0, 255, 0), 2)
            cv2.imshow("image", image_copy)

    # if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        button_down = False
        box_points.append((x, y))
        cv2.rectangle(oriImage, box_points[0], box_points[1], (0, 255, 0), 2)
        cv2.imshow("image", oriImage)
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished

        refPoint = [(x_start + 3, y_start + 3), (x_end - 3, y_end - 3)]

        if len(refPoint) == 2:  # when two points were found
            roi = oriImage[refPoint[0][1] : refPoint[1][1], refPoint[0][0] : refPoint[1][0]]

            cv2.imshow("Cropped", roi)
            USER_INP = simpledialog.askstring(title="Teach Vision Object", prompt="Save Object As:")
            templateName = USER_INP + ".jpg"
            cv2.imwrite(templateName, roi)
            cv2.destroyAllWindows()
            updateVisOp()


def selectTemplate():
    global oriImage
    global button_down
    button_down = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0
    image = cv2.imread("curImage.jpg")
    oriImage = image.copy()

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", mouse_crop)
    cv2.imshow("image", image)


def snapFind():
    global selectedTemplate
    global BGavg
    take_pic()
    template = selectedTemplate.get()
    min_score = float(VisScoreEntryField.get()) * 0.01
    autoBGVal = int(autoBG.get())
    if autoBGVal == 1:
        background = BGavg
        VisBacColorEntryField.configure(state="enabled")
        VisBacColorEntryField.delete(0, "end")
        VisBacColorEntryField.insert(0, str(BGavg))
        VisBacColorEntryField.configure(state="disabled")
    else:
        background = eval(VisBacColorEntryField.get())
    visFind(template, min_score, background)


def rotate_image(img, angle, background):
    image_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.0)
    result = cv2.warpAffine(
        img,
        rot_mat,
        img.shape[1::-1],
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=background,
        flags=cv2.INTER_LINEAR,
    )
    return result


def visFind(template, min_score, background):
    global xMMpos
    global yMMpos
    global autoBG
    # manEntryField.delete(0, 'end')
    # manEntryField.insert(0,min_score)

    if background == "Auto":
        background = BGavg
        VisBacColorEntryField.configure(state="enabled")
        VisBacColorEntryField.delete(0, "end")
        VisBacColorEntryField.insert(0, str(BGavg))
        VisBacColorEntryField.configure(state="disabled")

    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    dkgreen = (0, 128, 0)
    status = "fail"
    highscore = 0
    img1 = cv2.imread("curImage.jpg")  # target Image
    img2 = cv2.imread(template)  # target Image

    # method = cv2.TM_CCOEFF_NORMED
    # method = cv2.TM_CCORR_NORMED

    img = img1.copy()

    fullRotVal = int(fullRot.get())

    for i in range(1):
        if i == 0:
            method = cv2.TM_CCOEFF_NORMED
        else:
            # method = cv2.TM_CCOEFF_NORMED
            method = cv2.TM_CCORR_NORMED

        # USE 1/3 - EACH SIDE SEARCH
        if fullRotVal == 0:
            ## fist pass 1/3rds
            curangle = 0
            highangle = 0
            highscore = 0
            highmax_loc = 0
            for x in range(3):
                template = img2
                template = rotate_image(img2, curangle, background)
                w, h = template.shape[1::-1]
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > highscore:
                    highscore = max_val
                    highangle = curangle
                    highmax_loc = max_loc
                    highw, highh = w, h
                curangle += 120

            # check each side and narrow in
            while True:
                curangle = curangle / 2
                if curangle < 0.9:
                    break
                nextangle1 = highangle + curangle
                nextangle2 = highangle - curangle
                template = img2
                template = rotate_image(img2, nextangle1, background)
                w, h = template.shape[1::-1]
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > highscore:
                    highscore = max_val
                    highangle = nextangle1
                    highmax_loc = max_loc
                    highw, highh = w, h
                template = img2
                template = rotate_image(img2, nextangle2, background)
                w, h = template.shape[1::-1]
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if max_val > highscore:
                    highscore = max_val
                    highangle = nextangle2
                    highmax_loc = max_loc
                    highw, highh = w, h

        # USE FULL 360 SEARCh
        else:
            for i in range(720):
                template = rotate_image(img2, i, background)
                w, h = template.shape[1::-1]

                img = img1.copy()
                # Apply template Matching
                res = cv2.matchTemplate(img, template, method)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                highscore = max_val
                highangle = i
                highmax_loc = max_loc
                highw, highh = w, h
                if highscore >= min_score:
                    break
        if i == 1:
            highscore = highscore * 0.5
        if highscore >= min_score:
            break

    if highscore >= min_score:
        status = "pass"
        # normalize angle to increment of +180 to -180
        if highangle > 180:
            highangle = -360 + highangle
        # pick closest 180
        pick180Val = int(pick180.get())
        if pick180Val == 1:
            if highangle > 90:
                highangle = -180 + highangle
            elif highangle < -90:
                highangle = 180 + highangle
        # try closest
        pickClosestVal = int(pickClosest.get())
        if pickClosestVal == highangle and highangle > J6axisLimPos:
            highangle = J6axisLimPos
        elif pickClosestVal == 0 and highangle > J6axisLimPos:
            status = "fail"
        if pickClosestVal == 1 and highangle < (J6axisLimNeg * -1):
            highangle = J6axisLimNeg * -1
        elif pickClosestVal == 0 and highangle < (J6axisLimNeg * -1):
            status = "fail"

        top_left = highmax_loc
        bottom_right = (top_left[0] + highw, top_left[1] + highh)
        # find center
        center = (top_left[0] + highw / 2, top_left[1] + highh / 2)
        xPos = int(center[1])
        yPos = int(center[0])

        imgxPos = int(center[0])
        imgyPos = int(center[1])

        # find line 1 end
        line1x = int(imgxPos + 60 * math.cos(math.radians(highangle - 90)))
        line1y = int(imgyPos + 60 * math.sin(math.radians(highangle - 90)))
        cv2.line(img, (imgxPos, imgyPos), (line1x, line1y), green, 3)

        # find line 2 end
        line2x = int(imgxPos + 60 * math.cos(math.radians(highangle + 90)))
        line2y = int(imgyPos + 60 * math.sin(math.radians(highangle + 90)))
        cv2.line(img, (imgxPos, imgyPos), (line2x, line2y), green, 3)

        # find line 3 end
        line3x = int(imgxPos + 30 * math.cos(math.radians(highangle)))
        line3y = int(imgyPos + 30 * math.sin(math.radians(highangle)))
        cv2.line(img, (imgxPos, imgyPos), (line3x, line3y), green, 3)

        # find line 4 end
        line4x = int(imgxPos + 30 * math.cos(math.radians(highangle + 180)))
        line4y = int(imgyPos + 30 * math.sin(math.radians(highangle + 180)))
        cv2.line(img, (imgxPos, imgyPos), (line4x, line4y), green, 3)

        # find tip start
        lineTx = int(imgxPos + 56 * math.cos(math.radians(highangle - 90)))
        lineTy = int(imgyPos + 56 * math.sin(math.radians(highangle - 90)))
        cv2.line(img, (lineTx, lineTy), (line1x, line1y), dkgreen, 2)

        cv2.circle(img, (imgxPos, imgyPos), 20, green, 1)
        # cv2.rectangle(img,top_left, bottom_right, green, 2)
        cv2.imwrite("temp.jpg", img)
        img = Image.fromarray(img).resize((640, 480))
        imgtk = ImageTk.PhotoImage(image=img)
        vid_lbl.imgtk = imgtk
        vid_lbl.configure(image=imgtk)
        VisRetScoreEntryField.delete(0, "end")
        VisRetScoreEntryField.insert(0, str(round((highscore * 100), 2)))
        VisRetAngleEntryField.delete(0, "end")
        VisRetAngleEntryField.insert(0, str(highangle))
        VisRetXpixEntryField.delete(0, "end")
        VisRetXpixEntryField.insert(0, str(xPos))
        VisRetYpixEntryField.delete(0, "end")
        VisRetYpixEntryField.insert(0, str(yPos))
        viscalc()
        VisRetXrobEntryField.delete(0, "end")
        VisRetXrobEntryField.insert(0, str(round(xMMpos, 2)))
        VisRetYrobEntryField.delete(0, "end")
        VisRetYrobEntryField.insert(0, str(round(yMMpos, 2)))

        # break
        # if (score > highscore):
        # highscore=score

    if status == "fail":
        cv2.rectangle(img, (5, 5), (635, 475), red, 5)
        cv2.imwrite("temp.jpg", img)
        img = Image.fromarray(img).resize((640, 480))
        imgtk = ImageTk.PhotoImage(image=img)
        vid_lbl.imgtk = imgtk
        vid_lbl.configure(image=imgtk)
        VisRetScoreEntryField.delete(0, "end")
        VisRetScoreEntryField.insert(0, str(round((highscore * 100), 2)))
        VisRetAngleEntryField.delete(0, "end")
        VisRetAngleEntryField.insert(0, "NA")
        VisRetXpixEntryField.delete(0, "end")
        VisRetXpixEntryField.insert(0, "NA")
        VisRetYpixEntryField.delete(0, "end")
        VisRetYpixEntryField.insert(0, "NA")

    return status


# initial vis attempt using sift with flann pattern match
# def visFind(template):
#  take_pic()
#  MIN_MATCH_COUNT = 10
#  img1 = cv2.imread(template)  # query Image
#  img2 = cv2.imread('curImage.jpg')  # target Image
#  # Initiate SIFT detector
#  sift = cv2.SIFT_create()
#  # find the keypoints and descriptors with SIFT
#  kp1, des1 = sift.detectAndCompute(img1,None)
#  kp2, des2 = sift.detectAndCompute(img2,None)
#  FLANN_INDEX_KDTREE = 1
#  index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
#  search_params = dict(checks = 50)
#  flann = cv2.FlannBasedMatcher(index_params, search_params)
#  matches = flann.knnMatch(des1,des2,k=2)
#  # store all the good matches as per Lowe's ratio test.
#  good = []
#  for m,n in matches:
#      if m.distance < 1.1*n.distance:
#          good.append(m)

#  if len(good)>MIN_MATCH_COUNT:
#      src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
#      dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
#      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
#      matchesMask = mask.ravel().tolist()
#      h,w,c = img1.shape
#      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#      dst = cv2.perspectiveTransform(pts,M)
#      #img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)
#
#      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
#      dst = cv2.perspectiveTransform(pts,M)
#
#      crosspts = np.float32([ [w/2,0],[w/2,h-1],[0,h/2],[w-1,h/2] ]).reshape(-1,1,2)
#      crossCoord = cv2.perspectiveTransform(crosspts,M)
#
#      cenPt = np.float32([w/2,h/2]).reshape(-1,1,2)
#      cenCoord = cv2.perspectiveTransform(cenPt,M)
#
#      cenResult = cenCoord[0].reshape(1,-1).flatten().tolist()
#      theta = - math.atan2(M[0,1], M[0,0]) * 180 / math.pi
#
#      xPos = cenResult[0]
#      yPos = cenResult[1]
#
#      cross1Result = crossCoord[0].reshape(2,-1).flatten().tolist()
#      cross2Result = crossCoord[1].reshape(2,-1).flatten().tolist()
#      cross3Result = crossCoord[2].reshape(2,-1).flatten().tolist()
#      cross4Result = crossCoord[3].reshape(2,-1).flatten().tolist()
#
#      x1Pos = int(cross1Result[0])
#      y1Pos = int(cross1Result[1])
#      x2Pos = int(cross2Result[0])
#      y2Pos = int(cross2Result[1])
#      x3Pos = int(cross3Result[0])
#      y3Pos = int(cross3Result[1])
#      x4Pos = int(cross4Result[0])
#      y4Pos = int(cross4Result[1])
#
#
#      print(xPos)
#      print(yPos)
#      print(theta)
#
#
#      #draw bounding box
#      #img2 = cv2.polylines(img2, [np.int32(dst)], True, (0,255,0),3, cv2.LINE_AA)
#
#      #draw circle
#      img2 = cv2.circle(img2, (int(xPos),int(yPos)), radius=30, color=(0, 255, 0), thickness=3)
#
#      #draw line 1
#      cv2.line(img2, (x1Pos,y1Pos), (x2Pos,y2Pos), (0,255,0), 3)
#      #draw line 2
#      cv2.line(img2, (x3Pos,y3Pos), (x4Pos,y4Pos), (0,255,0), 3)
#
#      #save image
#      cv2.imwrite('curImage.jpg', img2)
#      img = Image.fromarray(img2)
#      imgtk = ImageTk.PhotoImage(image=img)
#      vid_lbl.imgtk = imgtk
#      vid_lbl.configure(image=imgtk)
#
#
#
#
#  else:
#      print( "Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT) )
#      matchesMask = None


def updateVisOp():
    global selectedTemplate
    selectedTemplate = StringVar()
    folder = os.path.dirname(os.path.realpath(__file__))
    filelist = [fname for fname in os.listdir(folder) if fname.endswith(".jpg")]
    Visoptmenu = ttk.Combobox(
        tab5, textvariable=selectedTemplate, values=filelist, state="readonly"
    )
    Visoptmenu.place(x=390, y=52)
    Visoptmenu.bind("<<ComboboxSelected>>", VisOpUpdate)


def VisOpUpdate(foo):
    global selectedTemplate
    file = selectedTemplate.get()
    print(file)
    img = cv2.imread(file, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    TARGET_PIXEL_AREA = 22500

    ratio = float(img.shape[1]) / float(img.shape[0])
    new_h = int(math.sqrt(TARGET_PIXEL_AREA / ratio) + 0.5)
    new_w = int((new_h * ratio) + 0.5)

    img = cv2.resize(img, (new_w, new_h))

    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    template_lbl.imgtk = imgtk
    template_lbl.configure(image=imgtk)


def zeroBrCn():
    global mX1
    global mY1
    global mX2
    global mY2
    mX1 = 0
    mY1 = 0
    mX2 = 640
    mY2 = 480
    VisBrightSlide.set(0)
    VisContrastSlide.set(0)
    # VisZoomSlide.set(50)
    take_pic()


def VisUpdateBriCon(foo):
    take_pic()


def motion(event):
    y = event.x
    x = event.y

    if x <= 240 and y <= 320:
        VisX1PixEntryField.delete(0, "end")
        VisX1PixEntryField.insert(0, x)
        VisY1PixEntryField.delete(0, "end")
        VisY1PixEntryField.insert(0, y)
    elif x > 240:
        VisX2PixEntryField.delete(0, "end")
        VisX2PixEntryField.insert(0, x)
    elif y > 320:
        VisY2PixEntryField.delete(0, "end")
        VisY2PixEntryField.insert(0, y)

    # print(str(x) +","+str(y))


def checkAutoBG():
    autoBGVal = int(autoBG.get())
    if autoBGVal == 1:
        VisBacColorEntryField.configure(state="disabled")
    else:
        VisBacColorEntryField.configure(state="enabled")

