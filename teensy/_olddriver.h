#ifndef DRIVER_H
#define DRIVER_H

#include "Buffer.h"
#include <tuple>
#include <Arduino.h>
#include <utility>
#include <string>

class Driver {
private:
    int steps[MAXDOF];
    int dir[MAXDOF];
    std::string speed_type;
    float speed;
    float acc;
    float dec;
    float ramp;
    float ACCspd, DCCspd, SpeedVal, high;
    float xyzuvw_In[3], xyzuvw_Out[3];
    float speedSP, lineDist, curDelay;
    float min_delay, max_delay, rndSpeed;
    bool rndTrue;
    std::string speedViolation;
    float ACCStep, NORStep, DCCStep, calcStepGap;
    int dirpin[MAXDOF];
    int stepPin[MAXDOF];
    int PE[MAXDOF], SE1[MAXDOF], SE2[MAXDOF], LO1[MAXDOF], LO2[MAXDOF];
    int cur[MAXDOF], stepM[MAXDOF];
    bool debug;
    int StepM[MAXDOF];
    int ACC_stepinc, DCC_stepinc, HighStep;

public:
    // constructor
    Driver();

    // add other member functions here
    int findMaxSteps(const int steps[]);
    void determineActiveMotors(const int steps[], int actives[]);
    void setDirection();
    bool isStepRemain(int cur[]);
    void set_delay(float& curDelay, int& highStepCur);
    void setup(int PE[], int LO1[], int SE1[], int LO2[], int SE2[]);
    void driveMotors(int cur[], int PE[], int SE1[], int SE2[], float distDelay, float& disDelayCur);
    void setStepDirection(int cur[], int StepM[]);
    void updateMotors(int cur[], int PE[], int SE1[], int SE2[]);
    void setRndSpeed(float curDelay);
    void drive_j(int steps[]);
};

#endif  // DRIVER_H
