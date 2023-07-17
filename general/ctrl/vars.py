pins = {
    "J1": {"step": 0, "dir": 1, "limit": 26},
    "J2": {"step": 2, "dir": 3, "limit": 27},
    "J3": {"step": 4, "dir": 5, "limit": 28},
    "J4": {"step": 6, "dir": 7, "limit": 29},
    "J5": {"step": 8, "dir": 9, "limit": 30},
    "J6": {"step": 10, "dir": 11, "limit": 31},
    "J7": {"step": 12, "dir": 13, "limit": 36},
    "J8": {"step": 32, "dir": 33, "limit": 37},
    "J9": {"step": 34, "dir": 35, "limit": 38},
}

Input39 = 39

Output40 = 40
Output41 = 41


# set encoder multiplier
encoder_mult[10, 10, 10, 10, 5, 10]

# set encoder pins
class Encoder:
    """C class"""

    def __init__(self, pins, mult):
        self.pins = pins  # TODO what are they for
        self.mult = mult
        self.steps = 0
        self.open_loop = False


encoder_pins = [Encoder(14 + i, 15 + i, m[i]) for i, m in enumerate(encoder_mult)]


# define axis limits in degrees
limits_info = [
    {"limit": (170, 170), "stepdeg": 44.44444444, "offset": -1},
    {"limit": (90, 42), "stepdeg": 55.55555556, "offset": 2},
    {"limit": (52, 89), "stepdeg": 55.55555556, "offset": 4.1},
    {"limit": (165, 165), "stepdeg": 42.72664356, "offset": -1.5},
    {"limit": (105, 105), "stepdeg": 21.86024888, "offset": 3},
    {"limit": (155, 155), "stepdeg": 22.22222222, "offset": -7},
    {"limit": (3450, 0), "stepdeg": 14.28571429, "offset": 0},
    {"limit": (3450, 0), "stepdeg": 14.28571429, "offset": 0},
    {"limit": (3450, 0), "stepdeg": 14.28571429, "offset": 0},
]

limits = [Limit(x["pin"], x["limit"], x["stepdeg"], x["offset"]) for x in limit_info]


KinematicError = 0


class Limit:
    """docstring"""

    def __init__(self, pin, limits, stepdeg, offset):

        self.pin = pin
        self.limits = limits
        self.total = sum([abs(x) for x in self.limits])  # define total axis travel
        self.stepdeg = stepdeg  # steps per degree

        self.step_limit = self.total * self.stepdeg  # steps full movement of each axis
        selt.step_zero = self.limits[0] * self.stepdeg  # steps for zero position
        self.step_master = self.zerostep

        self.offset = offset  # degrees from limit switch to offset calibration
        self.pressed = 0  # collision


external = [
    {"length": 0, "rotation": 0, "steps": 0, "pos": 0},
    {"length": 0, "rotation": 0, "steps": 0, "pos": 0},
    {"length": 0, "rotation": 0, "steps": 0, "pos": 0},
]


lineDist = 0
WristCon = ""
Quadrant = 0

debounce_time = [0 for _ in range(6)]
debounceDelay = 50

Alarm = "0"
speedViolation = "0"
maxSpeedDelay = 3000
minSpeedDelay = 350
linWayDistSP = 2
debug = ""
flag = ""
TRACKrotdir = 0

"""
#define ROBOT_nDOFs 6
typedef float tRobotJoints[ROBOT_nDOFs]
typedef float tRobotPose[ROBOT_nDOFs]

//declare in out vars
float xyzuvw_Out[ROBOT_nDOFs]
float xyzuvw_In[ROBOT_nDOFs]
float xyzuvw_Temp[ROBOT_nDOFs]

float JangleOut[ROBOT_nDOFs]
float JangleIn[ROBOT_nDOFs]
float joints_estimate[ROBOT_nDOFs]
float SolutionMatrix[ROBOT_nDOFs][4]

float J7_In
float J8_In
float J9_In


String moveSequence

# TODO
# define rounding vars
float rndArcStart[6]
float rndArcMid[6]
float rndArcEnd[6]
float rndCalcCen[6]
String rndData
bool rndTrue
float rndSpeed
bool splineTrue
bool splineEndReceived
"""


# DENAVIT HARTENBERG PARAMETERS
DH_params = [
    [0, 0, 169.77, 0],
    [-90, -90, 0, 64.2],
    [0, 0, 0, 305],
    [0, -90, 222.63, 0],
    [0, 90, 0, 0],
    [180, -90, 36.25, 0],
]
