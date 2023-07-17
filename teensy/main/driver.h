#ifndef DRIVER_H
#define DRIVER_H

#include "Buffer.h"
#include <tuple>
#include <Arduino.h>
#include <utility>
#include <string>
#include "speed.h"

class Driver {
private:
    int steps[MAXDOF];
    int directions[MAXDOF];
    float xyzuvw_In[3], xyzuvw_Out[3];

    // TODO abstract this 
    int steppins[MAXDOF] = {0,2,4,6,8,10,12,32,34};
    int dirpins[MAXDOF] = {1,3,5,7,9,11,13,33,35};
    int switches[MAXDOF] = {26,27,28,29,30,31,36,37,38};
    int away[MAXDOF] = {1, 0, 1, 1, 0, 1, 0, 0, 0};

    bool round=false;
    int dirpin[MAXDOF];
    int stepPin[MAXDOF];
    float PE[MAXDOF], SE1[MAXDOF], SE2[MAXDOF], LO1[MAXDOF], LO2[MAXDOF];
    float PEcur[MAXDOF], SE1cur[MAXDOF], SE2cur[MAXDOF]; 
    int active[MAXDOF]; 
    int nactive;
    int cur[MAXDOF];
    bool debug;
    int StepM[MAXDOF];

    int highStepCur;
    int most;
    
    SpeedMGR spd;

public:
    Driver();
    void get_most(int steps[]);
    void reset(); 
    void drive_joints(int steps[], int directions[]); 
    bool is_done();
    void _drive_motors();


};

#endif  // DRIVER_H
