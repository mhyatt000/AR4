import time

def delay(x):
    """sleep milliseconds"""
    time.sleep(x/1000)


def sendRobotPos():
    """docstring"""

    sendPos = (
        f"A{JangleIn[0]:.3f}B{JangleIn[1]:.3f}C{JangleIn[2]:.3f}D{JangleIn[3]:.3f}"
        f"E{JangleIn[4]:.3f}F{JangleIn[5]:.3f}G{xyzuvw_Out[0]:.3f}H{xyzuvw_Out[1]:.3f}"
        f"I{xyzuvw_Out[2]:.3f}J{xyzuvw_Out[3]:.3f}K{xyzuvw_Out[4]:.3f}L{xyzuvw_Out[5]:.3f}"
        f"M{speedViolation}N{debug}O{flag}P{J7_pos}Q{J8_pos}R{J9_pos}"
    )

    delay(5)
    print(sendPos)
    speedViolation = "0"
    flag = ""


def sendRobotPosSpline():
    """docstring"""

    sendPos = (
        f"A{JangleIn[0]:.3f}B{JangleIn[1]:.3f}C{JangleIn[2]:.3f}D{JangleIn[3]:.3f}"
        f"E{JangleIn[4]:.3f}F{JangleIn[5]:.3f}G{xyzuvw_Out[0]:.3f}H{xyzuvw_Out[1]:.3f}"
        f"I{xyzuvw_Out[2]:.3f}J{xyzuvw_Out[3]:.3f}K{xyzuvw_Out[4]:.3f}L{xyzuvw_Out[5]:.3f}"
        f"M{speedViolation}N{debug}O{flag}P{J7_pos}Q{J8_pos}R{J9_pos}"
    )

    delay(5)
    print(sendPos)
    speedViolation = "0"


def updatePos():
    """docstring"""

    JangleIn[0] = (J1StepM - J1zeroStep) / J1StepDeg
    JangleIn[1] = (J2StepM - J2zeroStep) / J2StepDeg
    JangleIn[2] = (J3StepM - J3zeroStep) / J3StepDeg
    JangleIn[3] = (J4StepM - J4zeroStep) / J4StepDeg
    JangleIn[4] = (J5StepM - J5zeroStep) / J5StepDeg
    JangleIn[5] = (J6StepM - J6zeroStep) / J6StepDeg

    J7_pos = (J7StepM - J7zeroStep) / J7StepDeg
    J8_pos = (J8StepM - J8zeroStep) / J8StepDeg
    J9_pos = (J9StepM - J9zeroStep) / J9StepDeg

    SolveFowardKinematic()


def correctRobotPos():

    J1StepM = J1encPos.read() / J1encMult
    J2StepM = J2encPos.read() / J2encMult
    J3StepM = J3encPos.read() / J3encMult
    J4StepM = J4encPos.read() / J4encMult
    J5StepM = J5encPos.read() / J5encMult
    J6StepM = J6encPos.read() / J6encMult

    JangleIn = np.zeros(6)
    JangleIn[0] = (J1StepM - J1zeroStep) / J1StepDeg
    JangleIn[1] = (J2StepM - J2zeroStep) / J2StepDeg
    JangleIn[2] = (J3StepM - J3zeroStep) / J3StepDeg
    JangleIn[3] = (J4StepM - J4zeroStep) / J4StepDeg
    JangleIn[4] = (J5StepM - J5zeroStep) / J5StepDeg
    JangleIn[5] = (J6StepM - J6zeroStep) / J6StepDeg

    SolveFowardKinematic()

    sendPos = (
        "A"
        + str(round(JangleIn[0], 3))
        + "B"
        + str(round(JangleIn[1], 3))
        + "C"
        + str(round(JangleIn[2], 3))
        + "D"
        + str(round(JangleIn[3], 3))
        + "E"
        + str(round(JangleIn[4], 3))
        + "F"
        + str(round(JangleIn[5], 3))
        + "G"
        + str(round(xyzuvw_Out[0], 3))
        + "H"
        + str(round(xyzuvw_Out[1], 3))
        + "I"
        + str(round(xyzuvw_Out[2], 3))
        + "J"
        + str(round(xyzuvw_Out[3], 3))
        + "K"
        + str(round(xyzuvw_Out[4], 3))
        + "L"
        + str(round(xyzuvw_Out[5], 3))
        + "M"
        + speedViolation
        + "N"
        + debug
        + "O"
        + flag
        + "P"
        + J7_pos
        + "Q"
        + J8_pos
        + "R"
        + J9_pos
    )
    delay(5)
    print(sendPos)
    speedViolation = "0"
    flag = ""
