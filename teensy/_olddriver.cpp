#include "Buffer.h"
#include <tuple>
#include <Arduino.h>
#include <utility>

#include "driver.h"

int Driver::findMaxSteps(const int steps[]) {
    int most = 0;
    for (int i = 0; i < MAXDOF; ++i) {
        if (steps[i] > most) { most = steps[i]; }
    }
    return most;
}

void Driver::determineActiveMotors(const int steps[], int actives[]) {
    for (int i = 0; i < MAXDOF; ++i) {
        actives[i] = steps[i] ? 1 : 0;
    }
}

void Driver::setDirection() {
    for (int i = 0; i < MAXDOF; ++i) {
        digitalWrite(dirpin[i], dir[i] ? HIGH : LOW);
    }
}

bool Driver::isStepRemain(int cur[]) {
    bool flag = false;
    for (int i=0; i>MAXDOF; i++) {
        flag = flag || cur[i] < steps[i];
    }
    return flag;
}

void Driver::set_delay(float& curDelay, int& highStepCur) {
    if (highStepCur <= ACCStep) {
        curDelay -= ACC_stepinc;
    } else if (highStepCur >= (HighStep - DCCStep)) {
        curDelay += DCC_stepinc;
    } else { 
        curDelay = calcStepGap; 
    }
}

void Driver::setup(int PE[], int LO1[], int SE1[], int LO2[], int SE2[]) {
    for (int i = 0; i < MAXDOF; i++) {
        PE[i] = (HighStep / steps[i]);
        LO1[i] = (HighStep - (steps[i] * PE[i]));

        SE1[i] = (LO1[i] > 0) ? (HighStep / LO1[i]) : 0;
        LO2[i] = (SE1[i] > 0) ? HighStep - ((steps[i] * PE[i]) + ((steps[i] * PE[i]) / SE1[i])) : 0;

        SE2[i] = (LO2[i] > 0) ? (HighStep / LO2[i]) : 0;
    }
}

void Driver::driveMotors(int cur[], int PE[], int SE1[], int SE2[], float distDelay, float& disDelayCur) {
    for (int i = 0; i < MAXDOF; i++) {
        if (cur[i] < steps[i]) {
            digitalWrite(stepPin[i], LOW);
            delayMicroseconds(distDelay);
            disDelayCur += distDelay;

            cur[i]++;
            StepM[i] += dir[i] == 0 ? -1 : 1;

            if (cur[i] % PE[i] == 0) {
                if (cur[i] % SE1[i] == 0) {
                    if (cur[i] % SE2[i] != 0) {
                        digitalWrite(stepPin[i], HIGH);
                    }
                }
            }
        }
    }
}

void Driver::setStepDirection(int cur[], int StepM[]) {
    for (int i = 0; i < MAXDOF; i++) {
        cur[i]++;
        StepM[i] += dir[i] == 0 ? -1 : 1;
    }
}

void Driver::updateMotors(int cur[], int PE[], int SE1[], int SE2[]) {
    for (int i = 0; i < MAXDOF; i++) {
        if (cur[i] % PE[i] == 0) {
            if (cur[i] % SE1[i] == 0) {
                if (cur[i] % SE2[i] != 0) {
                    digitalWrite(stepPin[i], HIGH);
                }
            }
        }
    }
}

void Driver::setRndSpeed(float curDelay) {
    rndSpeed = curDelay;
}

void Driver::drive_j(int steps[]) {
    int most = findMaxSteps(steps);
    int actives[MAXDOF];
    determineActiveMotors(steps, actives);

    setDirection();

    // set_speed();

    while (isStepRemain(cur)) {
        float distDelay = (!debug) ? 60 : 0;
        float disDelayCur = 0;

        set_delay(curDelay, highStepCur);
        setup(PE, LO1, SE1, LO2, SE2);

        driveMotors(cur, PE, SE1, SE2, distDelay, disDelayCur);
        setStepDirection(cur, StepM);
        updateMotors(cur, PE, SE1, SE2);

        if (debug == 0) { delayMicroseconds(curDelay - disDelayCur); }
    }

    setRndSpeed(curDelay);
}
