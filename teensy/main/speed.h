#ifndef SPEED_H
#define SPEED_H

#include <Arduino.h>


class SpeedMGR {
public:
    float val;
    String type;
    float acc, dcc, ramp;

    float accstep, dccstep, norstep;
    int most;
    float gap; // used to be calcStepGap

    float speedSP, lineDist, curDelay;
    float min_delay, max_delay, rndSpeed;
    String violation;
    float ACCStep, NORStep, DCCStep, calcStepGap;
    int ACC_stepinc, DCC_stepinc, HighStep;

    float accstepInc;
    float dccstepInc;
    float accstartDel;

    int delay;

    SpeedMGR() {
        val = 80;
        type = "p";
        acc = 10;
        dcc = 10;
        ramp = 50;
        delay = 0;
        max_delay = 3000;
        min_delay = 350;
    }

    void set_speed_steps(int _most) {
        /* sets steps for acceleration and decceleration 
         * based on largest joint step
         */

        most = _most;
        Serial.println("most: " + String(most));
        Serial.println("acc: " + String(acc));
        accstep = most * (acc / 100);
        dccstep = most * (dcc / 100);
        norstep = most - (accstep + dccstep);
        
    }

    void apply_speed_type() {

        float speedSP;

        //set speed 
        if (type== "s") {
            speedSP = (val * 1000000) * .8;
            Serial.println("not supported");
            return; 
        }

        if (type== "m") {
            // a2 + b2 = c2
            // lineDist = pow((pow((xyzuvw_In[0] - xyzuvw_Out[0]), 2) + pow((xyzuvw_In[1] - xyzuvw_Out[1]), 2) + pow((xyzuvw_In[2] - xyzuvw_Out[2]), 2)), .5);
            speedSP = ((lineDist / val) * 1000000) * .8;
            Serial.println("not supported");
            return; 
        }

        // case: seconds or mm per sec
        if (type== "s" || type== "m" ) {

            float zeroStepGap = speedSP / most;
            float zeroACCstepInc = (zeroStepGap * (100 / ramp)) / accstep;
            float zeroACCtime = ((accstep) * zeroStepGap) + ((accstep - 9) * (((accstep) * (zeroACCstepInc / 2))));
            float zeroNORtime = norstep * zeroStepGap;
            float zeroDCCstepInc = (zeroStepGap * (100 / ramp)) / dccstep;
            float zeroDCCtime = ((dccstep) * zeroStepGap) + ((dccstep - 9) * (((dccstep) * (zeroDCCstepInc / 2))));
            float zeroTOTtime = zeroACCtime + zeroNORtime + zeroDCCtime;
            float overclockPerc = speedSP / zeroTOTtime;

            gap = zeroStepGap * overclockPerc;
            if (gap <= min_delay) {
                gap = min_delay;
                violation= "1";
            }
        }

        // case: percentage
        if (type== "p") {
            gap = (max_delay - ((val / 100) * max_delay)); // TODO call it delay?
            if (gap < min_delay) { gap = min_delay; }
        }

    } // apply

    void set_increments() {
        // calculate final step increments

        accstepInc = (gap * (100 / ramp)) / accstep;
        dccstepInc = (gap * (100 / ramp)) / dccstep;
        accstartDel = (gap * accstep) * 2;

        Serial.println("increments");
        Serial.println(String(accstepInc) + " | " + String(accstep));
        Serial.println(String(dccstepInc) + " | " + String(dccstep));
        Serial.println(String(accstartDel) + " | " );

    }

    void set_delay(int highStepCur) {
        if (highStepCur <= accstep) { delay -= (accstepInc); }
        else if (highStepCur >= (most - dccstep)) { delay += (dccstepInc); }
        else { delay = calcStepGap; }
    }



};

#endif
