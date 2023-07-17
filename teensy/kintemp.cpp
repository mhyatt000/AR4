#include <math.h>

#include <iostream>
#include <cstring> 

const int debugg = 0;

const int J1stepPin = 0;
const int J1dirPin = 1;
const int J2stepPin = 2;
const int J2dirPin = 3;
const int J3stepPin = 4;
const int J3dirPin = 5;
const int J4stepPin = 6;
const int J4dirPin = 7;
const int J5stepPin = 8;
const int J5dirPin = 9;
const int J6stepPin = 10;
const int J6dirPin = 11;

const int J7stepPin = 12;
const int J7dirPin = 13;
const int J8stepPin = 32;
const int J8dirPin = 33;
const int J9stepPin = 34;
const int J9dirPin = 35;

// limit switches?
const int J1calPin = 26;
const int J2calPin = 27;
const int J3calPin = 28;
const int J4calPin = 29;
const int J5calPin = 30;
const int J6calPin = 31;
const int J7calPin = 36;
const int J8calPin = 37;
const int J9calPin = 38;


const int Input39 = 39;

const int Output40 = 40;
const int Output41 = 41;


//set encoder multiplier
const float J1encMult = 10;
const float J2encMult = 10;
const float J3encMult = 10;
const float J4encMult = 10;
const float J5encMult = 5;
const float J6encMult = 10;



// GLOBAL VARS //

//define axis limits in degrees
float J1axisLimPos = 170;
float J1axisLimNeg = 170;
float J2axisLimPos = 90;
float J2axisLimNeg = 42;
float J3axisLimPos = 52;
float J3axisLimNeg = 89;
float J4axisLimPos = 165;
float J4axisLimNeg = 165;
float J5axisLimPos = 105;
float J5axisLimNeg = 105;
float J6axisLimPos = 155;
float J6axisLimNeg = 155;
float J7axisLimPos = 3450;
float J7axisLimNeg = 0;
float J8axisLimPos = 3450;
float J8axisLimNeg = 0;
float J9axisLimPos = 3450;
float J9axisLimNeg = 0;

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

int Quadrant;

unsigned long J1DebounceTime = 0;
unsigned long J2DebounceTime = 0;
unsigned long J3DebounceTime = 0;
unsigned long J4DebounceTime = 0;
unsigned long J5DebounceTime = 0;
unsigned long J6DebounceTime = 0;
unsigned long debounceDelay = 50;

float maxSpeedDelay = 3000;
float minSpeedDelay = 350;
float linWayDistSP = 2;
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


//define rounding vars
float rndArcStart[6];
float rndArcMid[6];
float rndArcEnd[6];
float rndCalcCen[6];
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


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//MATRIX OPERATION
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//This allow to return a array as an argument instead of using global pointer

 #define Matrix_Multiply(out,inA,inB)\
  (out)[0] = (inA)[0]*(inB)[0] + (inA)[4]*(inB)[1] + (inA)[8]*(inB)[2];\
  (out)[1] = (inA)[1]*(inB)[0] + (inA)[5]*(inB)[1] + (inA)[9]*(inB)[2];\
  (out)[2] = (inA)[2]*(inB)[0] + (inA)[6]*(inB)[1] + (inA)[10]*(inB)[2];\
  (out)[3] = 0;\
  (out)[4] = (inA)[0]*(inB)[4] + (inA)[4]*(inB)[5] + (inA)[8]*(inB)[6];\
  (out)[5] = (inA)[1]*(inB)[4] + (inA)[5]*(inB)[5] + (inA)[9]*(inB)[6];\
  (out)[6] = (inA)[2]*(inB)[4] + (inA)[6]*(inB)[5] + (inA)[10]*(inB)[6];\
  (out)[7] = 0;\
  (out)[8] = (inA)[0]*(inB)[8] + (inA)[4]*(inB)[9] + (inA)[8]*(inB)[10];\
  (out)[9] = (inA)[1]*(inB)[8] + (inA)[5]*(inB)[9] + (inA)[9]*(inB)[10];\
  (out)[10] = (inA)[2]*(inB)[8] + (inA)[6]*(inB)[9] + (inA)[10]*(inB)[10];\
  (out)[11] = 0;\
  (out)[12] = (inA)[0]*(inB)[12] + (inA)[4]*(inB)[13] + (inA)[8]*(inB)[14] + (inA)[12];\
  (out)[13] = (inA)[1]*(inB)[12] + (inA)[5]*(inB)[13] + (inA)[9]*(inB)[14] + (inA)[13];\
  (out)[14] = (inA)[2]*(inB)[12] + (inA)[6]*(inB)[13] + (inA)[10]*(inB)[14] + (inA)[14];\
  (out)[15] = 1;

#define Matrix_Inv(out,in)\
  (out)[0] = (in)[0];\
  (out)[1] = (in)[4];\
  (out)[2] = (in)[8];\
  (out)[3] = 0;\
  (out)[4] = (in)[1];\
  (out)[5] = (in)[5];\
  (out)[6] = (in)[9];\
  (out)[7] = 0;\
  (out)[8] = (in)[2];\
  (out)[9] = (in)[6];\
  (out)[10] = (in)[10];\
  (out)[11] = 0;\
  (out)[12] = -((in)[0]*(in)[12] + (in)[1]*(in)[13] + (in)[2]*(in)[14]);\
  (out)[13] = -((in)[4]*(in)[12] + (in)[5]*(in)[13] + (in)[6]*(in)[14]);\
  (out)[14] = -((in)[8]*(in)[12] + (in)[9]*(in)[13] + (in)[10]*(in)[14]);\
  (out)[15] = 1;

#define Matrix_Copy(out,in)\
  (out)[0]=(in)[0];\
  (out)[1]=(in)[1];\
  (out)[2]=(in)[2];\
  (out)[3]=(in)[3];\
  (out)[4]=(in)[4];\
  (out)[5]=(in)[5];\
  (out)[6]=(in)[6];\
  (out)[7]=(in)[7];\
  (out)[8]=(in)[8];\
  (out)[9]=(in)[9];\
  (out)[10]=(in)[10];\
  (out)[11]=(in)[11];\
  (out)[12]=(in)[12];\
  (out)[13]=(in)[13];\
  (out)[14]=(in)[14];\
  (out)[15]=(in)[15];

#define Matrix_Eye(inout)\
  (inout)[0] = 1;\
  (inout)[1] = 0;\
  (inout)[2] = 0;\
  (inout)[3] = 0;\
  (inout)[4] = 0;\
  (inout)[5] = 1;\
  (inout)[6] = 0;\
  (inout)[7] = 0;\
  (inout)[8] = 0;\
  (inout)[9] = 0;\
  (inout)[10] = 1;\
  (inout)[11] = 0;\
  (inout)[12] = 0;\
  (inout)[13] = 0;\
  (inout)[14] = 0;\
  (inout)[15] = 1;

#define Matrix_Multiply_Cumul(inout,inB){\
    Matrix4x4 out;\
    Matrix_Multiply(out,inout,inB);\
    Matrix_Copy(inout,out);}


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//DECLARATION OF VARIABLES
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/// DHM Table parameters
#define DHM_Alpha 0
#define DHM_A 1
#define DHM_Theta 2
#define DHM_D 3


/// Custom robot base (user frame)
Matrix4x4 Robot_BaseFrame = {1, 0, 0, 0 , 0, 1, 0, 0, 0, 0, 1, 0 , 0, 0, 0, 1};

/// Custom robot tool (tool frame, end of arm tool or TCP)
Matrix4x4 Robot_ToolFrame = {1, 0, 0, 0 , 0, 1, 0, 0, 0, 0, 1, 0 , 0, 0, 0, 1};

/// Robot parameters
/// All robot data is held in a large array
tRobot Robot_Data = {0};


// These global variable are also pointers, 
// allowing to put the variables inside the Robot_Data DHM table
float *Robot_Kin_DHM_Table = Robot_Data + 0 * Table_Size;

/// xyzwpr of the base
float *Robot_Kin_Base = Robot_Data + 6 * Table_Size;

/// xyzwpr of the tool
float *Robot_Kin_Tool = Robot_Data + 7 * Table_Size;

/// Robot lower limits
float *Robot_JointLimits_Upper = Robot_Data + 8 * Table_Size;

/// Robot upper limits
float *Robot_JointLimits_Lower = Robot_Data + 9 * Table_Size;

/// Robot axis senses
float *Robot_Senses = Robot_Data + 10 * Table_Size;

// A value mappings

float *Robot_Kin_DHM_L1 = Robot_Kin_DHM_Table + 0 * Table_Size;
float *Robot_Kin_DHM_L2 = Robot_Kin_DHM_Table + 1 * Table_Size;
float *Robot_Kin_DHM_L3 = Robot_Kin_DHM_Table + 2 * Table_Size;
float *Robot_Kin_DHM_L4 = Robot_Kin_DHM_Table + 3 * Table_Size;
float *Robot_Kin_DHM_L5 = Robot_Kin_DHM_Table + 4 * Table_Size;
float *Robot_Kin_DHM_L6 = Robot_Kin_DHM_Table + 5 * Table_Size;


float &Robot_Kin_DHM_A2(Robot_Kin_DHM_Table[1 * Table_Size + 1]);
float &Robot_Kin_DHM_A3(Robot_Kin_DHM_Table[2 * Table_Size + 1]);
float &Robot_Kin_DHM_A4(Robot_Kin_DHM_Table[3 * Table_Size + 1]);

// D value mappings
float &Robot_Kin_DHM_D1(Robot_Kin_DHM_Table[0 * Table_Size + 3]);
float &Robot_Kin_DHM_D2(Robot_Kin_DHM_Table[1 * Table_Size + 3]);
float &Robot_Kin_DHM_D4(Robot_Kin_DHM_Table[3 * Table_Size + 3]);
float &Robot_Kin_DHM_D6(Robot_Kin_DHM_Table[5 * Table_Size + 3]);

// Theta value mappings (mastering)
float &Robot_Kin_DHM_Theta1(Robot_Kin_DHM_Table[0 * Table_Size + 2]);
float &Robot_Kin_DHM_Theta2(Robot_Kin_DHM_Table[1 * Table_Size + 2]);
float &Robot_Kin_DHM_Theta3(Robot_Kin_DHM_Table[2 * Table_Size + 2]);
float &Robot_Kin_DHM_Theta4(Robot_Kin_DHM_Table[3 * Table_Size + 2]);
float &Robot_Kin_DHM_Theta5(Robot_Kin_DHM_Table[4 * Table_Size + 2]);
float &Robot_Kin_DHM_Theta6(Robot_Kin_DHM_Table[5 * Table_Size + 2]);





void robot_data_reset() {
  // Reset user base and tool frames
  Matrix_Eye(Robot_BaseFrame);
  Matrix_Eye(Robot_ToolFrame);

  // Reset internal base frame and tool frames
  for (int i = 0; i < 6; i++) {
    Robot_Kin_Base[i] = 0.0;
  }

  // Reset joint senses and joint limits
  for (int i = 0; i < ROBOT_nDOFs; i++) {
    Robot_Senses[i] = +1.0;

  }

}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

//This function set the variable inside Robot_Data to the DHparams
void robot_set_AR3() {
   robot_data_reset();

  // Alpha parameters
  Robot_Kin_DHM_L1[DHM_Alpha] = DHparams[0][1] * M_PI / 180;
  Robot_Kin_DHM_L2[DHM_Alpha] = DHparams[1][1] * M_PI / 180;
  Robot_Kin_DHM_L3[DHM_Alpha] = DHparams[2][1] * M_PI / 180;
  Robot_Kin_DHM_L4[DHM_Alpha] = DHparams[3][1] * M_PI / 180;
  Robot_Kin_DHM_L5[DHM_Alpha] = DHparams[4][1] * M_PI / 180;
  Robot_Kin_DHM_L6[DHM_Alpha] = DHparams[5][1] * M_PI / 180;

  // Theta parameters
  Robot_Kin_DHM_L1[DHM_Theta] = DHparams[0][0] * M_PI / 180;
  Robot_Kin_DHM_L2[DHM_Theta] = DHparams[1][0] * M_PI / 180;
  Robot_Kin_DHM_L3[DHM_Theta] = DHparams[2][0] * M_PI / 180;
  Robot_Kin_DHM_L4[DHM_Theta] = DHparams[3][0] * M_PI / 180;
  Robot_Kin_DHM_L5[DHM_Theta] = DHparams[4][0] * M_PI / 180;
  Robot_Kin_DHM_L6[DHM_Theta] = DHparams[5][0] * M_PI / 180;

  // A parameters
  Robot_Kin_DHM_L1[DHM_A] = DHparams[0][3];
  Robot_Kin_DHM_L2[DHM_A] = DHparams[1][3];
  Robot_Kin_DHM_L3[DHM_A] = DHparams[2][3];
  Robot_Kin_DHM_L4[DHM_A] = DHparams[3][3];
  Robot_Kin_DHM_L5[DHM_A] = DHparams[4][3];
  Robot_Kin_DHM_L6[DHM_A] = DHparams[5][3];

  // D parameters
  Robot_Kin_DHM_L1[DHM_D] = DHparams[0][2];
  Robot_Kin_DHM_L2[DHM_D] = DHparams[1][2];
  Robot_Kin_DHM_L3[DHM_D] = DHparams[2][2];
  Robot_Kin_DHM_L4[DHM_D] = DHparams[3][2];
  Robot_Kin_DHM_L5[DHM_D] = DHparams[4][2];
  Robot_Kin_DHM_L6[DHM_D] = DHparams[5][2];


  Robot_JointLimits_Lower[0] = J1axisLimNeg;
  Robot_JointLimits_Upper[0] = J1axisLimPos;
  Robot_JointLimits_Lower[1] = J2axisLimNeg;
  Robot_JointLimits_Upper[1] = J2axisLimPos;
  Robot_JointLimits_Lower[2] = J3axisLimNeg;
  Robot_JointLimits_Upper[2] = J3axisLimPos;
  Robot_JointLimits_Lower[3] = J4axisLimNeg;
  Robot_JointLimits_Upper[3] = J4axisLimPos;
  Robot_JointLimits_Lower[4] = J5axisLimNeg;
  Robot_JointLimits_Upper[4] = J5axisLimPos;
  Robot_JointLimits_Lower[5] = J6axisLimNeg;
  Robot_JointLimits_Upper[5] = J6axisLimPos;

}

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//MATRICE OPERATIONS
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

template <typename T>
bool robot_joints_valid(const T joints[ROBOT_nDOFs]) {

  for (int i = 0; i < ROBOT_nDOFs; i++) {
    if (joints[i] < -Robot_JointLimits_Lower[i] || joints[i] > Robot_JointLimits_Upper[i]) {
      return false;
    }
  }
  return true;
}


//This function return a 4x4 matrix as an argument (pose) following the modified DH rules for the inputs T rx, T tx, T rz and T tz source : https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters
template <typename T>
void DHM_2_pose(T rx, T tx, T rz, T tz, Matrix4x4 pose)
{
  T crx;
  T srx;
  T crz;
  T srz;
  crx = cos(rx);
  srx = sin(rx);
  crz = cos(rz);
  srz = sin(rz);
  pose[0] = crz;
  pose[4] = -srz;
  pose[8] = 0.0;
  pose[12] = tx;
  pose[1] = crx * srz;
  pose[5] = crx * crz;
  pose[9] = -srx;
  pose[13] = -tz * srx;
  pose[2] = srx * srz;
  pose[6] = crz * srx;
  pose[10] = crx;
  pose[14] = tz * crx;
  pose[3] = 0.0;
  pose[7] = 0.0;
  pose[11] = 0.0;
  pose[15] = 1.0;
}


//return and tranform a coordinate system xyzwpr into a 4x4 matrix 
template <typename T>
void xyzwpr_2_pose(const T xyzwpr[6], Matrix4x4 pose) {
  T srx;
  T crx;
  T sry;
  T cry;
  T srz;
  T crz;
  T H_tmp;
  srx = sin(xyzwpr[3]);
  crx = cos(xyzwpr[3]);
  sry = sin(xyzwpr[4]);
  cry = cos(xyzwpr[4]);
  srz = sin(xyzwpr[5]);
  crz = cos(xyzwpr[5]);
  pose[0] = cry * crz;
  pose[4] = -cry * srz;
  pose[8] = sry;
  pose[12] = xyzwpr[0];
  H_tmp = crz * srx;
  pose[1] = crx * srz + H_tmp * sry;
  crz *= crx;
  pose[5] = crz - srx * sry * srz;
  pose[9] = -cry * srx;
  pose[13] = xyzwpr[1];
  pose[2] = srx * srz - crz * sry;
  pose[6] = H_tmp + crx * sry * srz;
  pose[10] = crx * cry;
  pose[14] = xyzwpr[2];
  pose[3] = 0.0;
  pose[7] = 0.0;
  pose[11] = 0.0;
  pose[15] = 1.0;
}


/// Calculate the [x,y,z,u,v,w] position with rotation vector for a pose target
template <typename T>
void pose_2_xyzuvw(const Matrix4x4 pose, T out[6]) {
  T sin_angle;
  T angle;
  T vector[3];
  int iidx;
  int vector_tmp;
  signed char b_I[9];
  out[0] = pose[12];
  out[1] = pose[13];
  out[2] = pose[14];
  sin_angle = (((pose[0] + pose[5]) + pose[10]) - 1.0) * 0.5;
  if (sin_angle <= -1.0) {
    sin_angle = -1.0;
  }

  if (sin_angle >= 1.0) {
    sin_angle = 1.0;
  }

  angle = acos(sin_angle);
  if (angle < 1.0E-6) {
    vector[0] = 0.0;
    vector[1] = 0.0;
    vector[2] = 0.0;
  } else {
    sin_angle = sin(angle);
    if (abs(sin_angle) < 1.0E-6) { //IMPOTANT : cosinus of 90 give a really small number instead of 0, the result is forced back to what it should
      sin_angle = pose[0];
      iidx = 0;
      if (pose[0] < pose[5]) {
        sin_angle = pose[5];
        iidx = 1;
      }

      if (sin_angle < pose[10]) {
        sin_angle = pose[10];
        iidx = 2;
      }

      for (vector_tmp = 0; vector_tmp < 9; vector_tmp++) {
        b_I[vector_tmp] = 0;
      }

      b_I[0] = 1;
      b_I[4] = 1;
      b_I[8] = 1;
      sin_angle = 2.0 * (1.0 + sin_angle);
      if (sin_angle <= 0.0) {
        sin_angle = 0.0;
      } else {
        sin_angle = sqrt(sin_angle);
      }

      vector_tmp = iidx << 2;
      vector[0] = (pose[vector_tmp] + static_cast<T>(b_I[3 * iidx])) /
                  sin_angle;
      vector[1] = (pose[1 + vector_tmp] + static_cast<T>(b_I[1 + 3 * iidx]))
                  / sin_angle;
      vector[2] = (pose[2 + vector_tmp] + static_cast<T>(b_I[2 + 3 * iidx]))
                  / sin_angle;
      angle = M_PI;
    } else {
      sin_angle = 1.0 / (2.0 * sin_angle);
      vector[0] = (pose[6] - pose[9]) * sin_angle;
      vector[1] = (pose[8] - pose[2]) * sin_angle;
      vector[2] = (pose[1] - pose[4]) * sin_angle;
    }
  }

  sin_angle = angle * 180.0 / M_PI;
  out[3] = vector[0] * sin_angle * M_PI / 180.0;
  out[4] = vector[1] * sin_angle * M_PI / 180.0;
  out[5] = vector[2] * sin_angle * M_PI / 180.0;
}


//This function tranform a coordinate system xyzwpr into a 4x4 matrix using UR euler rules and return it as an argument.
template <typename T>
void xyzuvw_2_pose(const T xyzuvw[6], Matrix4x4 pose)
{
  T s;
  T angle;
  T axisunit[3];
  T ex;
  T c;
  T pose_tmp;
  T b_pose_tmp;
  s = sqrt((xyzuvw[3] * xyzuvw[3] + xyzuvw[4] * xyzuvw[4]) + xyzuvw[5] *
           xyzuvw[5]);
  angle = s * 180.0 / M_PI;
  if (abs(angle) < 1.0E-6) { //IMPOTANT : cosinus of 90 give a really small number instead of 0, the result is forced back to what it should
    memset(&pose[0], 0, sizeof(T) << 4);
    pose[0] = 1.0;
    pose[5] = 1.0;
    pose[10] = 1.0;
    pose[15] = 1.0;
  } else {
    axisunit[1] = abs(xyzuvw[4]);
    axisunit[2] = abs(xyzuvw[5]);
    ex = abs(xyzuvw[3]);
    if (abs(xyzuvw[3]) < axisunit[1]) {
      ex = axisunit[1];
    }

    if (ex < axisunit[2]) {
      ex = axisunit[2];
    }

    if (ex < 1.0E-6) { //IMPOTANT : cosinus of 90 give a really small number instead of 0, the result is forced back to what it should
      memset(&pose[0], 0, sizeof(T) << 4);
      pose[0] = 1.0;
      pose[5] = 1.0;
      pose[10] = 1.0;
      pose[15] = 1.0;
    } else {
      axisunit[0] = xyzuvw[3] / s;
      axisunit[1] = xyzuvw[4] / s;
      axisunit[2] = xyzuvw[5] / s;
      s = angle * 3.1415926535897931 / 180.0;
      c = cos(s);
      s = sin(s);
      angle = axisunit[0] * axisunit[0];
      pose[0] = angle + c * (1.0 - angle);
      angle = axisunit[0] * axisunit[1] * (1.0 - c);
      ex = axisunit[2] * s;
      pose[4] = angle - ex;
      pose_tmp = axisunit[0] * axisunit[2] * (1.0 - c);
      b_pose_tmp = axisunit[1] * s;
      pose[8] = pose_tmp + b_pose_tmp;
      pose[1] = angle + ex;
      angle = axisunit[1] * axisunit[1];
      pose[5] = angle + (1.0 - angle) * c;
      angle = axisunit[1] * axisunit[2] * (1.0 - c);
      ex = axisunit[0] * s;
      pose[9] = angle - ex;
      pose[2] = pose_tmp - b_pose_tmp;
      pose[6] = angle + ex;
      angle = axisunit[2] * axisunit[2];
      pose[10] = angle + (1.0 - angle) * c;
      pose[3] = 0.0;
      pose[7] = 0.0;
      pose[11] = 0.0;
      pose[15] = 1.0;
    }
  }

  pose[12] = xyzuvw[0];
  pose[13] = xyzuvw[1];
  pose[14] = xyzuvw[2];
}




template <typename T>
void forward_kinematics_arm(const T *joints, Matrix4x4 pose) {
  xyzwpr_2_pose(Robot_Kin_Base, pose);
  for (int i = 0; i < ROBOT_nDOFs; i++) {
    Matrix4x4 hi;
    float *dhm_i = Robot_Kin_DHM_Table + i * Table_Size;
    T ji_rad = joints[i] * Robot_Senses[i] * M_PI / 180.0;
    DHM_2_pose(dhm_i[0], dhm_i[1], dhm_i[2] + ji_rad, dhm_i[3], hi);
    Matrix_Multiply_Cumul(pose, hi);
  }
  Matrix4x4 tool_pose;
  xyzwpr_2_pose(Robot_Kin_Tool, tool_pose);
  Matrix_Multiply_Cumul(pose, tool_pose);
}


//Calculate de foward kinematic of the robot without the tool
template <typename T>
void forward_kinematics_robot(const T joints[ROBOT_nDOFs], Matrix4x4 target) {
  Matrix4x4 invBaseFrame;
  Matrix4x4 pose_arm;
  Matrix_Inv(invBaseFrame, Robot_BaseFrame); // invRobot_Tool could be precalculated, the tool does not change so often
  forward_kinematics_arm(joints, pose_arm);
  Matrix_Multiply(target, invBaseFrame, pose_arm);
  Matrix_Multiply_Cumul(target, Robot_ToolFrame);
}


template <typename T>
void forward_kinematics_robot_xyzuvw(const T joints[ROBOT_nDOFs], T target_xyzuvw[6]) {
  Matrix4x4 pose;
  forward_kinematics_robot(joints, pose);    //send the joints values and return the pose matrix as an argument
  pose_2_xyzuvw(pose, target_xyzuvw);        //send the pose matrix and return the xyzuvw values in an array as an argument
}



/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//FOWARD KINEMATIC
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*
 *This function input the JxangleIn into an array, 
 *send it to the foward kinematic solver and 
 *output the result into the position variables
 */
void SolveFowardKinematic() {

  robot_set_AR3();

  float target_xyzuvw[6];
  float joints[ROBOT_nDOFs];

  float JangleIn[6] = {0,0,0,0,0,0};
  for (int i = 0; i < ROBOT_nDOFs; i++) {
    joints[i] = JangleIn[i];
  }

  for (int i = 0; i < 6; i++) {
      std::cout << joints[i] << std::endl;  // Print each element of the array
  }


  forward_kinematics_robot_xyzuvw(joints, target_xyzuvw);

  xyzuvw_Out[0] = target_xyzuvw[0];
  xyzuvw_Out[1] = target_xyzuvw[1];
  xyzuvw_Out[2] = target_xyzuvw[2];
  xyzuvw_Out[3] = target_xyzuvw[3] / M_PI * 180;
  xyzuvw_Out[4] = target_xyzuvw[4] / M_PI * 180;
  xyzuvw_Out[5] = target_xyzuvw[5] / M_PI * 180;


  for (int i = 0; i < 6; i++) {
      std::cout << xyzuvw_Out[i] << std::endl;  // Print each element of the array
  }


}


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//REVERSE KINEMATIC
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void updatejoints() {

  for (int i = 0; i > ROBOT_nDOFs; i++) {
    JangleIn[i] = JangleOut[i];
  }

}

void JointEstimate() {

  for (int i = 0; i < ROBOT_nDOFs; i++) {
    joints_estimate[i] = JangleIn[i];
  }
}



template <typename T>
void inverse_kinematics_raw(const T pose[16], const tRobot DK, const T joints_approx_in[6], T joints[6], int *nsol)
{
  int i0;
  T base[16];
  T joints_approx[6];
  T tool[16];
  int i;
  T Hout[16];
  T b_Hout[9];
  T dv0[4];
  bool guard1 = false;
  T make_sqrt;
  T P04[4];
  T q1;
  int i1;
  T c_Hout[16];
  T k2;
  T k1;
  T ai;
  T B;
  T C;
  T s31;
  T c31;
  T q13_idx_2;
  T bb_div_cc;
  T q13_idx_0;
  for (i0 = 0; i0 < 6; i0++) {
    joints_approx[i0] = DK[60 + i0] * joints_approx_in[i0];
  }

  xyzwpr_2_pose(*(T (*)[6])&DK[36], base);
  xyzwpr_2_pose(*(T (*)[6])&DK[42], tool);
  for (i0 = 0; i0 < 4; i0++) {
    i = i0 << 2;
    Hout[i] = base[i0];
    Hout[1 + i] = base[i0 + 4];
    Hout[2 + i] = base[i0 + 8];
    Hout[3 + i] = base[i0 + 12];
  }

  for (i0 = 0; i0 < 3; i0++) {
    i = i0 << 2;
    Hout[3 + i] = 0.0;
    b_Hout[3 * i0] = -Hout[i];
    b_Hout[1 + 3 * i0] = -Hout[1 + i];
    b_Hout[2 + 3 * i0] = -Hout[2 + i];
  }

  for (i0 = 0; i0 < 3; i0++) {
    Hout[12 + i0] = (b_Hout[i0] * base[12] + b_Hout[i0 + 3] * base[13]) + b_Hout[i0 + 6] * base[14];
  }

  for (i0 = 0; i0 < 4; i0++) {
    i = i0 << 2;
    base[i] = tool[i0];
    base[1 + i] = tool[i0 + 4];
    base[2 + i] = tool[i0 + 8];
    base[3 + i] = tool[i0 + 12];
  }

  for (i0 = 0; i0 < 3; i0++) {
    i = i0 << 2;
    base[3 + i] = 0.0;
    b_Hout[3 * i0] = -base[i];
    b_Hout[1 + 3 * i0] = -base[1 + i];
    b_Hout[2 + 3 * i0] = -base[2 + i];
  }

  for (i0 = 0; i0 < 3; i0++) {
    base[12 + i0] = (b_Hout[i0] * tool[12] + b_Hout[i0 + 3] * tool[13]) + b_Hout[i0 + 6] * tool[14];
  }

  dv0[0] = 0.0;
  dv0[1] = 0.0;
  dv0[2] = -DK[33];
  dv0[3] = 1.0;
  for (i0 = 0; i0 < 4; i0++) {
    for (i = 0; i < 4; i++) {
      i1 = i << 2;
      c_Hout[i0 + i1] = ((Hout[i0] * pose[i1] + Hout[i0 + 4] * pose[1 + i1]) + Hout[i0 + 8] * pose[2 + i1]) + Hout[i0 + 12] * pose[3 + i1];
    }

    P04[i0] = 0.0;
    for (i = 0; i < 4; i++) {
      i1 = i << 2;
      make_sqrt = ((c_Hout[i0] * base[i1] + c_Hout[i0 + 4] * base[1 + i1]) + c_Hout[i0 + 8] * base[2 + i1]) + c_Hout[i0 + 12] * base[3 + i1];
      tool[i0 + i1] = make_sqrt;
      P04[i0] += make_sqrt * dv0[i];
    }
  }

  guard1 = false;
  if (DK[9] == 0.0) {
    q1 = atan2(P04[1], P04[0]);
    guard1 = true;
  } else {
    make_sqrt = (P04[0] * P04[0] + P04[1] * P04[1]) - DK[9] * DK[9];
    if (make_sqrt < 0.0) {
      for (i = 0; i < 6; i++) {
        joints[i] = 0.0;
      }

      *nsol = 0;
    } else {
      q1 = atan2(P04[1], P04[0]) - atan2(DK[9], sqrt(make_sqrt));
      guard1 = true;
    }
  }

  if (guard1) {
    k2 = P04[2] - DK[3];
    k1 = (cos(q1) * P04[0] + sin(q1) * P04[1]) - DK[7];
    ai = (((k1 * k1 + k2 * k2) - DK[13] * DK[13]) - DK[21] * DK[21]) - DK[19] * DK[19];
    B = 2.0 * DK[21] * DK[13];
    C = 2.0 * DK[19] * DK[13];
    s31 = 0.0;
    c31 = 0.0;
    if (C == 0.0) {
      s31 = -ai / B;
      make_sqrt = 1.0 - s31 * s31;
      if (make_sqrt >= 0.0) {
        c31 = sqrt(make_sqrt);
      }
    } else {
      q13_idx_2 = C * C;
      bb_div_cc = B * B / q13_idx_2;
      make_sqrt = 2.0 * ai * B / q13_idx_2;
      make_sqrt = make_sqrt * make_sqrt - 4.0 * ((1.0 + bb_div_cc) * (ai * ai / q13_idx_2 - 1.0));
      if (make_sqrt >= 0.0) {
        s31 = (-2.0 * ai * B / q13_idx_2 + sqrt(make_sqrt)) / (2.0 * (1.0 + bb_div_cc));
        c31 = (ai + B * s31) / C;
      }
    }

    if ((make_sqrt >= 0.0) && (abs(s31) <= 1.0)) {
      B = atan2(s31, c31);
      make_sqrt = cos(B);
      ai = sin(B);
      C = (DK[13] - DK[21] * ai) + DK[19] * make_sqrt;
      make_sqrt = DK[21] * make_sqrt + DK[19] * ai;
      q13_idx_0 = q1 + -DK[2];
      k2 = atan2(C * k1 - make_sqrt * k2, C * k2 + make_sqrt * k1) + (-DK[8] - M_PI / 2);
      q13_idx_2 = B + -DK[14];
      bb_div_cc = joints_approx[3] * M_PI / 180.0 - (-DK[20]);
      q1 = q13_idx_0 + DK[2];
      B = k2 + DK[8];
      C = q13_idx_2 + DK[14];
      make_sqrt = B + C;
      s31 = cos(make_sqrt);
      c31 = cos(q1);
      Hout[0] = s31 * c31;
      ai = sin(q1);
      Hout[4] = s31 * ai;
      make_sqrt = sin(make_sqrt);
      Hout[8] = -make_sqrt;
      Hout[12] = (DK[3] * make_sqrt - DK[7] * s31) - DK[13] * cos(C);
      Hout[1] = -sin(B + C) * c31;
      Hout[5] = -sin(B + C) * ai;
      Hout[9] = -s31;
      Hout[13] = (DK[3] * s31 + DK[7] * make_sqrt) + DK[13] * sin(C);
      Hout[2] = -ai;
      Hout[6] = c31;
      Hout[10] = 0.0;
      Hout[14] = 0.0;
      Hout[3] = 0.0;
      Hout[7] = 0.0;
      Hout[11] = 0.0;
      Hout[15] = 1.0;
      for (i0 = 0; i0 < 4; i0++) {
        for (i = 0; i < 4; i++) {
          i1 = i << 2;
          base[i0 + i1] = ((Hout[i0] * tool[i1] + Hout[i0 + 4] * tool[1 + i1]) + Hout[i0 + 8] * tool[2 + i1]) + Hout[i0 + 12] * tool[3 + i1];
        }
      }

      make_sqrt = 1.0 - base[9] * base[9];
      if (make_sqrt <= 0.0) {
        make_sqrt = 0.0;
      } else {
        make_sqrt = sqrt(make_sqrt);
      }

      if (make_sqrt < 1.0E-6) {
        C = atan2(make_sqrt, base[9]);
        make_sqrt = sin(bb_div_cc);
        ai = cos(bb_div_cc);
        make_sqrt = atan2(make_sqrt * base[0] + ai * base[2], make_sqrt * base[2] - ai * base[0]);
      } else if (joints_approx[4] >= 0.0) {
        bb_div_cc = atan2(base[10] / make_sqrt, -base[8] / make_sqrt);
        C = atan2(make_sqrt, base[9]);
        make_sqrt = sin(C);
        make_sqrt = atan2(base[5] / make_sqrt, -base[1] / make_sqrt);
      } else {
        bb_div_cc = atan2(-base[10] / make_sqrt, base[8] / make_sqrt);
        C = atan2(-make_sqrt, base[9]);
        make_sqrt = sin(C);
        make_sqrt = atan2(base[5] / make_sqrt, -base[1] / make_sqrt);
      }

      joints[0] = q13_idx_0;
      joints[3] = bb_div_cc + -DK[20];
      joints[1] = k2;
      joints[4] = C + -DK[26];
      joints[2] = q13_idx_2;
      joints[5] = make_sqrt + (-DK[32] + M_PI);
      make_sqrt = joints[5];
      if (joints[5] > 3.1415926535897931) {
        make_sqrt = joints[5] - M_PI * 2;
      } else {
        if (joints[5] <= -M_PI) {
          make_sqrt = joints[5] + M_PI * 2;
        }
      }

      joints[5] = make_sqrt;
      for (i0 = 0; i0 < 6; i0++) {
        joints[i0] = DK[60 + i0] * (joints[i0] * 180.0 / M_PI);
      }

      *nsol = 1.0;
    } else {
      for (i = 0; i < 6; i++) {
        joints[i] = 0.0;
      }

      *nsol = 0;
    }
  }
}




template <typename T>
int inverse_kinematics_robot(const Matrix4x4 target, T joints[ROBOT_nDOFs], const T *joints_estimate) {
  Matrix4x4 invToolFrame;
  Matrix4x4 pose_arm;
  int nsol;
  Matrix_Inv(invToolFrame, Robot_ToolFrame); // invRobot_Tool could be precalculated, the tool does not change so often
  Matrix_Multiply(pose_arm, Robot_BaseFrame, target);
  Matrix_Multiply_Cumul(pose_arm, invToolFrame);
  if (joints_estimate != nullptr) {
    inverse_kinematics_raw(pose_arm, Robot_Data, joints_estimate, joints, &nsol);
  } else {
    // Warning! This is dangerous if joints does not have a valid/reasonable result
    T joints_approx[6];
    memcpy(joints_approx, joints, ROBOT_nDOFs * sizeof(T));
    inverse_kinematics_raw(pose_arm, Robot_Data, joints_approx, joints, &nsol);
  }
  if (nsol == 0) {
    return 0;
  }

  return 1;
}



template <typename T>
int inverse_kinematics_robot_xyzuvw(const T target_xyzuvw1[6], T joints[ROBOT_nDOFs], const T *joints_estimate) {

  Matrix4x4 pose;
  xyzuvw_2_pose(target_xyzuvw1, pose);
  return inverse_kinematics_robot(pose, joints, joints_estimate);
}



void SolveInverseKinematic() {

  float joints[ROBOT_nDOFs];
  float target[6];

  float solbuffer[ROBOT_nDOFs] = {0};
  int NumberOfSol = 0;
  int solVal = 0;

  KinematicError = 0;

  JointEstimate();
  target[0] = xyzuvw_In[0];
  target[1] = xyzuvw_In[1];
  target[2] = xyzuvw_In[2];
  target[3] = xyzuvw_In[3] * M_PI / 180;
  target[4] = xyzuvw_In[4] * M_PI / 180;
  target[5] = xyzuvw_In[5] * M_PI / 180;

  // Serial.println("X : " + String(target[0]) + " Y : " + String(target[1]) + " Z : " + String(target[2]) + " rx : " + String(xyzuvw_In[3]) + " ry : " + String(xyzuvw_In[4]) + " rz : " + String(xyzuvw_In[5]));


  for (int i = -3; i <= 3; i++) {
    joints_estimate[4] = i * 30;
    int success = inverse_kinematics_robot_xyzuvw<float>(target, joints, joints_estimate);
    if (success) {
      if (solbuffer[4] != joints[4]) {
        if (robot_joints_valid(joints)) {
          for (int j = 0; j < ROBOT_nDOFs; j++) {
            solbuffer[j] = joints[j];
            SolutionMatrix[j][NumberOfSol] = solbuffer[j];
          }
          if (NumberOfSol <= 6) {
            NumberOfSol++;
          }
        }
      }
    } else {
      KinematicError = 1;
    }
  }

  joints_estimate[4] = JangleIn[4];


  solVal = 0;
  for (int i = 0; i < ROBOT_nDOFs; i++) {
    if ((abs(joints_estimate[i] - SolutionMatrix[i][0]) > 20) and NumberOfSol > 1) {
      solVal = 1;
    } else if ((abs(joints_estimate[i] - SolutionMatrix[i][1]) > 20) and NumberOfSol > 1) {
      solVal = 0;
    }


    // Serial.println(String(i) + "  Joint estimate : " + String(joints_estimate[i]) + " // Joint sol 1 : " + String(SolutionMatrix[i][0]) + " // Joint sol 2 : " + String(SolutionMatrix[i][1]));
  }

  if (NumberOfSol == 0) {
    KinematicError = 1;
  }


  // Serial.println("Sol : " + String(solVal) + " Nb sol : " + String(NumberOfSol));

  for (int i = 0; i < ROBOT_nDOFs; i++) {
    JangleOut[i] = SolutionMatrix[i][solVal];
  }

}









/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//CALCULATE POSITIONS
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



void updatePos() {

  JangleIn[0] = (J1StepM - J1zeroStep) / J1StepDeg;
  JangleIn[1] = (J2StepM - J2zeroStep) / J2StepDeg;
  JangleIn[2] = (J3StepM - J3zeroStep) / J3StepDeg;
  JangleIn[3] = (J4StepM - J4zeroStep) / J4StepDeg;
  JangleIn[4] = (J5StepM - J5zeroStep) / J5StepDeg;
  JangleIn[5] = (J6StepM - J6zeroStep) / J6StepDeg;

  J7_pos = (J7StepM - J7zeroStep) / J7StepDeg;
  J8_pos = (J8StepM - J8zeroStep) / J8StepDeg;
  J9_pos = (J9StepM - J9zeroStep) / J9StepDeg;

  SolveFowardKinematic();
}





/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//MAIN
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main() {
    
 SolveFowardKinematic();

}
