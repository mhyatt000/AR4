import numpy as np
import time

MAX_DOFS = 9
LOW=0
HIGH=1


SE = np.zeros(MAX_DOFS, dtype=float)
PE = np.zeros(MAX_DOFS, dtype=float)

class CTLR():
    """microcontroller"""

    def __init__(self):
        self.pins = {}
        self.steps = {}

    def digitalWrite(self, pin, state):

        if not pin in self.pins:
            self.pins[pin] = state
            self.steps[pin] = 0
        else:
            past = self.pins[pin]
            change = past != state
            self.pins[pin] = state

            if change:
                self.steps[pin] += 1

    def delayMicroseconds(self, microseconds):
        print('ms: ', microseconds)
        time.sleep(0.1)

ctrl = CTLR()

cur = np.zeros(MAX_DOFS, dtype=int)
step = np.random.random(MAX_DOFS)*500
stepPin = [int(x*100) for x in np.random.random(MAX_DOFS)]
dir = np.zeros(MAX_DOFS, dtype=int)
StepM = np.zeros(MAX_DOFS, dtype=int)
PE = np.zeros(MAX_DOFS, dtype=float)
LO1 = np.zeros(MAX_DOFS, dtype=float)
LO2 = np.zeros(MAX_DOFS, dtype=float)
SE1 = np.zeros(MAX_DOFS, dtype=float)
SE2 = np.zeros(MAX_DOFS, dtype=float)

curDelay = 0
highCur = 0
ACCStep = 0
DCCStep = 0
calcACCstepInc = 10
calcDCCstepInc = 10
debug = 1
high = 20
calcStepGap = 10

while any(c < s for c, s in zip(cur, step)):
    print("loop")

    if highCur <= ACCStep:
        curDelay -= calcACCstepInc
    elif highCur >= (high - DCCStep):
        curDelay += calcDCCstepInc
    else:
        curDelay = calcStepGap

    distDelay = 60 if debug != 1 else 0
    disDelayCur = 0

    for i in range(MAX_DOFS):
        PE[i] = high / step[i]
        LO1[i] = high - (step[i] * PE[i])

        SE1[i] = (high / LO1[i]) if LO1[i] > 0 else 0
        LO2[i] = high - ((step[i] * PE[i]) + ((step[i] * PE[i]) / SE1[i])) if SE1[i] > 0 else 0
        SE2[i] = (high / LO2[i]) if LO2[i] > 0 else 0

    for i in range(MAX_DOFS):
        if cur[i] < step[i]:
            ctrl.digitalWrite(stepPin[i], LOW)

    ctrl.delayMicroseconds(distDelay)

    for i in range(MAX_DOFS):
        if cur[i] < step[i]:
            disDelayCur += distDelay

            cur[i] += 1
            StepM[i] -= 1 if dir[i] == 0 else -1

            if cur[i] % (PE[i] + SE[i]) == 0:
                if cur[i] % SE2[i] != 0:
                    ctrl.digitalWrite(stepPin[i], HIGH)

    highCur += 1

    for i in range(MAX_DOFS):
        ctrl.digitalWrite(stepPin[i], HIGH)

    if debug == 0:
        ctrl.delayMicroseconds(curDelay - disDelayCur)

    rndSpeed = curDelay

    print(ctrl.steps)
    print()
