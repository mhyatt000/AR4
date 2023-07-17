#include "driver.h"
#include <tuple>
#include <Arduino.h>
#include <utility>
#include <string>
#include "speed.h"


Driver::Driver(){}

void display(float arr[]) {
    for (int i=0; i<MAXDOF; i++) {
        Serial.print("| " + String(arr[i]) + " |");
    }
    Serial.println("");
}

void display(int arr[]) {
    for (int i=0; i<MAXDOF; i++) {
        Serial.print("| " + String(arr[i]) + " |");
    }
    Serial.println("");
}

void Driver::get_most(int steps[]) {
    //FIND HIGHEST STEP

    most = 0;
    for (int i=0; i<MAXDOF; i++) {
        Serial.println(steps[i]);
        most = steps[i] > most ? steps[i] : most ;
    }
}

void Driver::reset() {
    for (int i = 0; i < MAXDOF; i++) {
        PE[i] = 0;
        SE1[i] = 0;
        SE2[i] = 0;
        LO1[i] = 0;
        LO2[i] = 0;
        cur[i] = 0;
        PEcur[i] = 0;
        SE1cur[i] = 0;
        SE2cur[i] = 0;
        active[i] = {0};
    }

    nactive = 0;
    highStepCur = 0;

} // reset


void Driver::drive_joints(int _steps[], int _directions[]) {
    /* drive motors by the number of joint steps */

    for (int i=0; i<MAXDOF; i++) {
        steps[i] = _steps[i];
        directions[i] = _directions[i];
    }

    reset();
    get_most(steps);

    for (int i=0; i<MAXDOF; i++) {
        active[i] = steps[i] ? 1 : 0;
        nactive += active[i];
    }

    // float moveDist;

    for (int i=0; i<MAXDOF; i++) { digitalWrite(dirpins[i], directions[i]); }

    spd.set_speed_steps(most);
    spd.apply_speed_type();
    spd.set_increments();

    //set starting delay
    // hardcoded for now... use rounding?
    if (round == true) {
        // TODO what is round speed
        // spd.delay = rndSpeed;
        round = false;
    } else { spd.delay = spd.accstartDel; }

    _drive_motors();
}

bool Driver::is_done() {
    /* return true if all cur < steps */

    bool done = true;
    for (int i=0; i<MAXDOF; i++) {
        done = done && cur[i] >= steps[i];
    }
    return done;
}



void Driver::_drive_motors() {

    Serial.println(String(spd.accstep));
    Serial.println(String(spd.norstep));
    Serial.println(String(spd.dccstep));
    Serial.println();
    Serial.println(String(spd.gap));
    spd.set_delay(highStepCur);
    Serial.println(String(spd.delay));

    display(steps);
    Serial.println(most);

    while (!is_done()) {
        // Serial.println("not done");

        spd.set_delay(highStepCur);

        float distDelay = 60;
        int debug = 1;
        if (debug == 1) {
          distDelay = 0;
        }
        float disDelayCur = 0;

        for (int i=0; i<MAXDOF; i++) {
            // Serial.println(String(spd.delay));
            // Serial.println(String(distDelay));
            // Serial.println();

            if (cur[i] < steps[i]) {
              PE[i] = (most / steps[i]);
              display(PE);

              LO1[i] = (most - (steps[i] * PE[i]));

              if (LO1[i] > 0) { SE1[i] = (most / LO1[i]); }
              else { SE1[i] = 0; }

              if (SE1[i] > 0) {
                LO2[i] = (most - ((steps[i] * PE[i]) + ((steps[i] * PE[i]) / SE1[i])));
              } else { LO2[i] = 0; }

              if (LO2[i] > 0) { SE2[i] = (most / LO2[i]); }
              else { SE2[i] = 0; }

              if (SE2[i] == 0) { SE2cur[i] = (SE2[i] + 1); }

              if (SE2cur[i] != SE2[i]) {
                SE2cur[i]++;
                if (SE1[i] == 0) { SE1cur[i] = (SE1[i] + 1); }

                if (SE1cur[i] != SE1[i]) {
                    SE1cur[i]++;
                    PEcur[i]++;
                    if (PEcur[i] == PE[i]) {
                        cur[i]++;
                        PEcur[i] = 0;
                        digitalWrite(stepPin[i], LOW);
                        delayMicroseconds(distDelay);
                        disDelayCur = disDelayCur + distDelay;
                        if (directions[i] == 0) { StepM[i]--; }
                        else { StepM[i]++; }
                  }
                } else { SE1cur[i] = 0; }
              } else { SE2cur[i] = 0; }
            }

        } // for

        // inc cur step
        highStepCur++;

        for (int i=0; i<MAXDOF; i++) {
            digitalWrite(stepPin[i], HIGH);
        }
        if (debug == 0) { delayMicroseconds(spd.delay - disDelayCur); }

    } // while
 
    //set rounding speed to last move speed
    // rndSpeed = spd.delay;

}

