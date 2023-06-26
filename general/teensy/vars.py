
String cmdBuffer1;
String cmdBuffer2;
String cmdBuffer3;
String inData;
String recData;
String checkData;
String function;
volatile byte state = LOW;

const int debugg = 0;

pins = {
        'J1':{'step': 0, 'dir':1, 'cal':26},
        'J2':{'step': 2, 'dir':3, 'cal':27},
        'J3':{'step': 4, 'dir':5, 'cal':28},
        'J4':{'step': 6, 'dir':7, 'cal':29},
        'J5':{'step': 8, 'dir':9, 'cal':30},
        'J6':{'step': 10, 'dir':11, 'cal':31},
        'J7':{'step': 12, 'dir':13, 'cal':36},
        'J8':{'step': 32, 'dir':33, 'cal':37},
        'J9':{'step': 34, 'dir':35, 'cal':38},
}

const int Input39 = 39;

const int Output40 = 40;
const int Output41 = 41;


# set encoder multiplier
encoder_mult [ 10, 10, 10, 10, 5, 10, ]

# set encoder pins
class Encoder():
    """C class"""

    def __init__(self ):
        pass

encoder_pins= [
    Encoder J1encPos(14, 15),
    Encoder J2encPos(17, 16),
    Encoder J3encPos(19, 18),
    Encoder J4encPos(20, 21),
    Encoder J5encPos(23, 22),
    Encoder J6encPos(24, 25),
]


# define axis limits in degrees
limits = [
( 170, 170),
( 90, 42),
( 52, 89),
( 165, 165),
( 105, 105),
( 155, 155),
( 3450, 0),
( 3450, 0),
( 3450, 0),
]

//define total axis travel
float J1axisLim = J1axisLimPos + J1axisLimNeg;
float J2axisLim = J2axisLimPos + J2axisLimNeg;
float J3axisLim = J3axisLimPos + J3axisLimNeg;
float J4axisLim = J4axisLimPos + J4axisLimNeg;
float J5axisLim = J5axisLimPos + J5axisLimNeg;
float J6axisLim = J6axisLimPos + J6axisLimNeg;
float J7axisLim = J7axisLimPos + J7axisLimNeg;
float J8axisLim = J8axisLimPos + J8axisLimNeg;
float J9axisLim = J9axisLimPos + J9axisLimNeg;

//motor steps per degree
float J1StepDeg = 44.44444444;
float J2StepDeg = 55.55555556;
float J3StepDeg = 55.55555556;
float J4StepDeg = 42.72664356;
float J5StepDeg = 21.86024888;
float J6StepDeg = 22.22222222;
float J7StepDeg = 14.28571429;
float J8StepDeg = 14.28571429;
float J9StepDeg = 14.28571429;

//steps full movement of each axis
int J1StepLim = J1axisLim * J1StepDeg;
int J2StepLim = J2axisLim * J2StepDeg;
int J3StepLim = J3axisLim * J3StepDeg;
int J4StepLim = J4axisLim * J4StepDeg;
int J5StepLim = J5axisLim * J5StepDeg;
int J6StepLim = J6axisLim * J6StepDeg;
int J7StepLim = J7axisLim * J7StepDeg;
int J8StepLim = J8axisLim * J8StepDeg;
int J9StepLim = J9axisLim * J9StepDeg;

//step and axis zero
int J1zeroStep = J1axisLimNeg * J1StepDeg;
int J2zeroStep = J2axisLimNeg * J2StepDeg;
int J3zeroStep = J3axisLimNeg * J3StepDeg;
int J4zeroStep = J4axisLimNeg * J4StepDeg;
int J5zeroStep = J5axisLimNeg * J5StepDeg;
int J6zeroStep = J6axisLimNeg * J6StepDeg;
int J7zeroStep = J7axisLimNeg * J7StepDeg;
int J8zeroStep = J8axisLimNeg * J8StepDeg;
int J9zeroStep = J9axisLimNeg * J9StepDeg;

//start master step count at Jzerostep
int J1StepM = J1zeroStep;
int J2StepM = J2zeroStep;
int J3StepM = J3zeroStep;
int J4StepM = J4zeroStep;
int J5StepM = J5zeroStep;
int J6StepM = J6zeroStep;
int J7StepM = J7zeroStep;
int J8StepM = J8zeroStep;
int J9StepM = J9zeroStep;



//degrees from limit switch to offset calibration
float J1calBaseOff = -1;
float J2calBaseOff = 2;
float J3calBaseOff = 4.1;
float J4calBaseOff = -1.5;
float J5calBaseOff = 3;
float J6calBaseOff = -7;
float J7calBaseOff = 0;
float J8calBaseOff = 0;
float J9calBaseOff = 0;

//reset collision indicators
int J1collisionTrue = 0;
int J2collisionTrue = 0;
int J3collisionTrue = 0;
int J4collisionTrue = 0;
int J5collisionTrue = 0;
int J6collisionTrue = 0;
int TotalCollision = 0;
int KinematicError = 0;

float J7length;
float J7rot;
float J7steps;

float J8length;
float J8rot;
float J8steps;

float J9length;
float J9rot;
float J9steps;

float lineDist;

String WristCon;
int Quadrant;

unsigned long J1DebounceTime = 0;
unsigned long J2DebounceTime = 0;
unsigned long J3DebounceTime = 0;
unsigned long J4DebounceTime = 0;
unsigned long J5DebounceTime = 0;
unsigned long J6DebounceTime = 0;
unsigned long debounceDelay = 50;

String Alarm = "0";
String speedViolation = "0";
float maxSpeedDelay = 3000;
float minSpeedDelay = 350;
float linWayDistSP = 2;
String debug = "";
String flag = "";
const int TRACKrotdir = 0;

int J1EncSteps;
int J2EncSteps;
int J3EncSteps;
int J4EncSteps;
int J5EncSteps;
int J6EncSteps;

int J1LoopMode;
int J2LoopMode;
int J3LoopMode;
int J4LoopMode;
int J5LoopMode;
int J6LoopMode;

#define ROBOT_nDOFs 6
typedef float tRobotJoints[ROBOT_nDOFs];
typedef float tRobotPose[ROBOT_nDOFs];

//declare in out vars
float xyzuvw_Out[ROBOT_nDOFs];
float xyzuvw_In[ROBOT_nDOFs];
float xyzuvw_Temp[ROBOT_nDOFs];

float JangleOut[ROBOT_nDOFs];
float JangleIn[ROBOT_nDOFs];
float joints_estimate[ROBOT_nDOFs];
float SolutionMatrix[ROBOT_nDOFs][4];

//external axis
float J7_pos;
float J8_pos;
float J9_pos;

float J7_In;
float J8_In;
float J9_In;

#define Table_Size 6
typedef float Matrix4x4[16];
typedef float tRobot[66];

float pose[16];

String moveSequence;

//define rounding vars
float rndArcStart[6];
float rndArcMid[6];
float rndArcEnd[6];
float rndCalcCen[6];
String rndData;
bool rndTrue;
float rndSpeed;
bool splineTrue;
bool splineEndReceived;



//DENAVIT HARTENBERG PARAMETERS

float DHparams[6][4] = {
  {    0,      0,  169.77,      0  },
  {  -90,    -90,       0,   64.2  },
  {    0,      0,       0,    305  },
  {    0,    -90,  222.63,      0  },
  {    0,     90,       0,      0  },
  {  180,    -90,   36.25,      0  }
};

