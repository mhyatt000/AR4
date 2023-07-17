#pragma once

#include <Arduino.h>
#include "define.h"
#include "speed.h"
#include "driver.h"

class CTRL {
// robot controller

private:
    const int min_wait = 500;
    const int max_wait = 2000;
    int steps[MAXDOF] = {0};
    int state[MAXDOF] = {0};
    int stepcenter[MAXDOF];
    int stepmaster[MAXDOF];
    int alarm;

    int steppins[MAXDOF] = {0,2,4,6,8,10,12,32,34};
    int dirpins[MAXDOF] = {1,3,5,7,9,11,13,33,35};
    int switches[MAXDOF] = {26,27,28,29,30,31,36,37,38};
    int away[MAXDOF] = {1, 0, 1, 1, 0, 1, 0, 0, 0};

    float limneg[MAXDOF] = { 170, 42, 89, 165, 105, 155, 0, 0, 0};
    float limpos[MAXDOF] = { 170, 90, 52, 165, 105, 155, 3450, 3450, 3450};
    float limit[MAXDOF];
    float stepdeg[MAXDOF] = { 44.44444444, 55.55555556, 55.55555556, 42.72664356, 21.86024888, 22.22222222, 14.28571429, 14.28571429, 14.28571429};
    float steplim[MAXDOF];

    float tocalibrate[MAXDOF];
    float calBaseOff[MAXDOF] = { -1, 2, 4.1, -1.5, 3, -7, 0, 0, 0};
    float calOff[MAXDOF] = {0};

public:
    Driver driver;

    CTRL() {
        set_steplims();
        driver = Driver();
    }

    void set_steplims() {
        for (int i=0; i<MAXDOF; i++){ limit[i] = limpos[i] + limneg[i]; }
        for (int i=0; i<MAXDOF; i++){ steplim[i] = limit[i] * stepdeg[i]; }
    }

    void point_away() {
        for (int i=0; i<MAXDOF; i++){ digitalWrite(dirpins[i], away[i]); }
    }

    void point_toward() {
        for (int i=0; i<MAXDOF; i++){ digitalWrite(dirpins[i], !away[i]); }
    }


    void switch_read() {
            /*
            4 times, check each limit switch
            if they are HIGH wait a little (maybe cuz of noise?)
            if they are still HIGH, youve hit a switch
            */
            for (int n=0; n<4; n++) {
                for (int i=0; i<MAXDOF; i++) {
                    if (digitalRead(switches[i] == LOW)) {
                        state[i] = LOW;
                        break;
                    } else {
                        delayMicroseconds(10);
                    }
                }
            }
            for (int i=0; i<MAXDOF; i++) {
                state[i] = digitalRead(switches[i]);
            }
    } // switch read

    void switch_display() {
        switch_read();
        for (int i=0; i<MAXDOF; i++) {
            Serial.print("| " + String(state[i]) + " |");
        }
        Serial.println("");
    }

    void drive_limit(int steps[], float percent_speed) {
        int dones[MAXDOF] = {0};
        int completes[MAXDOF] = {0};

        int wait = ((max_wait - ((percent_speed / 100) * max_wait)) + min_wait + 300);

        point_toward();

        int ndone = 0;
        for (int i=0; i<MAXDOF; i++) {
            if (!steps[i]) {
                completes[i] = 1;
                ndone += 1;
            }
        }

        int ncal = 0;
        for (int i=0; i<MAXDOF; i++) { ncal += tocalibrate[i]; }
        
        while (ndone < MAXDOF) {

            switch_read();
            for (int i=0; i<MAXDOF; i++) {

                // TODO maybe just rely on limit?
                if (dones[i] < steps[i] && state[i] == LOW && !completes[i]) {
                  digitalWrite(steppins[i], LOW);
                  delayMicroseconds(50);
                  digitalWrite(steppins[i], HIGH);
                  dones[i]++;
                }
                else {
                  completes[i] = 1;
                }

            }

            ndone = 0;
            for (int i=0; i<MAXDOF; i++) { ndone += completes[i]; }

            delayMicroseconds(wait);
      }

    } // drive_limit



    void backoff() {

        point_away();

        for (int n=0; n<250; n++) {
            for (int i=0; i<MAXDOF; i++) {
                if (tocalibrate[i]) {
                    digitalWrite(steppins[i], LOW);
                    delayMicroseconds(5);
                    digitalWrite(steppins[i], HIGH);
                    delayMicroseconds(5);
                }
            }
            delayMicroseconds(4000);

        } // 250 times

    } // backoff


    void overdrive() {
        // MAKE SURE LIMIT SWITCH STAYS MADE

        point_toward();

        for (int i=0; i<55; i++) {
            for (int i=0; i<MAXDOF; i++) {
                if (tocalibrate[i]) {
                  digitalWrite(steppins[i], LOW);
                  delayMicroseconds(5);
                  digitalWrite(steppins[i], HIGH);
                  delayMicroseconds(5);
                }
            }
            delayMicroseconds(3000);
        }

    } // overdrive

    void calibrate(){

        // what to cal?
        for (int i = 0; i < MAXDOF; i++) { tocalibrate[i] = i<2 ? 1 : 0; }

        for (int i=0; i<MAXDOF; i++) { steps[i] = tocalibrate[i] ? steplim[i] : 0; }

        int percent_speed = 80;
        drive_limit(steps, percent_speed);
        delay(500);

        backoff();

        percent_speed = .02;
        drive_limit(steps, percent_speed);
        overdrive();
        delay(500);

        // SEE IF ANY SWITCHES NOT MADE
        alarm = 0;
        switch_read();
        for (int i=0; i<MAXDOF; i++) {
            if (tocalibrate[i] && !state[i]) { alarm = i+1; } 
        }

        switch_display();
        if (!alarm) {
            Serial.println("no alarm");
            for (int i=0; i<MAXDOF; i++) { 

                //set master steps and center step
                if (tocalibrate[i]) { 
                  int total_deg = limit[i] + calBaseOff[i] + calOff[i];
                  stepmaster[i] = total_deg * stepdeg[i];
                  int pos_deg = limpos[i] + calBaseOff[i] + calOff[i];
                  stepcenter[i] = pos_deg * stepdeg[i];
                }

            }

            Serial.println("ready to drive home");
            drive_joints(stepcenter, away);
            // driver.drive_joints(stepcenter, away);
            sendRobotPos();

        }
        else {
            delay(5);
            Serial.println(alarm);
            alarm = 0;
        }

    } // calibrate

    void drive_joints(int steps[], int dir[]){
        String SpeedType= "p";
        float SpeedVal=80;
        float ACCspd=10;
        float DCCspd=10;
        float ACCramp=50;
        driveMotorsJ(steps[0], steps[1], steps[2], steps[3], steps[4], 0, steps[6], steps[7], steps[8], dir[0], dir[1], dir[2], dir[3], dir[4], dir[5], dir[6], dir[7], dir[8], SpeedType, SpeedVal, ACCspd, DCCspd, ACCramp);
    }

    void driveMotorsJ(int J1step, int J2step, int J3step, int J4step, int J5step, int J6step, int J7step, int J8step, int J9step, int J1dir, int J2dir, int J3dir, int J4dir, int J5dir, int J6dir, int J7dir, int J8dir, int J9dir, String SpeedType, float SpeedVal, float ACCspd, float DCCspd, float ACCramp) {

      int HighStep = J1step;
      if (J2step > HighStep) { HighStep = J2step; }
      if (J3step > HighStep) { HighStep = J3step; }
      if (J4step > HighStep) { HighStep = J4step; }
      if (J5step > HighStep) { HighStep = J5step; }
      if (J6step > HighStep) { HighStep = J6step; }
      if (J7step > HighStep) { HighStep = J7step; }
      if (J8step > HighStep) { HighStep = J8step; }
      if (J9step > HighStep) { HighStep = J9step; }

      int J1active = 0;
      int J2active = 0;
      int J3active = 0;
      int J4active = 0;
      int J5active = 0;
      int J6active = 0;
      int J7active = 0;
      int J8active = 0;
      int J9active = 0;
      int Jactive = 0;

      if (J1step >= 1) { J1active = 1; }
      if (J2step >= 1) { J2active = 1; }
      if (J3step >= 1) { J3active = 1; }
      if (J4step >= 1) { J4active = 1; }
      if (J5step >= 1) { J5active = 1; }
      if (J6step >= 1) { J6active = 1; }
      if (J7step >= 1) { J7active = 1; }
      if (J8step >= 1) { J8active = 1; }
      if (J9step >= 1) { J9active = 1; }
      Jactive = (J1active + J2active + J3active + J4active + J5active + J6active + J7active + J8active + J9active);

      int J1_PE = 0;
      int J2_PE = 0;
      int J3_PE = 0;
      int J4_PE = 0;
      int J5_PE = 0;
      int J6_PE = 0;
      int J7_PE = 0;
      int J8_PE = 0;
      int J9_PE = 0;

      int J1_SE_1 = 0;
      int J2_SE_1 = 0;
      int J3_SE_1 = 0;
      int J4_SE_1 = 0;
      int J5_SE_1 = 0;
      int J6_SE_1 = 0;
      int J7_SE_1 = 0;
      int J8_SE_1 = 0;
      int J9_SE_1 = 0;

      int J1_SE_2 = 0;
      int J2_SE_2 = 0;
      int J3_SE_2 = 0;
      int J4_SE_2 = 0;
      int J5_SE_2 = 0;
      int J6_SE_2 = 0;
      int J7_SE_2 = 0;
      int J8_SE_2 = 0;
      int J9_SE_2 = 0;

      int J1_LO_1 = 0;
      int J2_LO_1 = 0;
      int J3_LO_1 = 0;
      int J4_LO_1 = 0;
      int J5_LO_1 = 0;
      int J6_LO_1 = 0;
      int J7_LO_1 = 0;
      int J8_LO_1 = 0;
      int J9_LO_1 = 0;

      int J1_LO_2 = 0;
      int J2_LO_2 = 0;
      int J3_LO_2 = 0;
      int J4_LO_2 = 0;
      int J5_LO_2 = 0;
      int J6_LO_2 = 0;
      int J7_LO_2 = 0;
      int J8_LO_2 = 0;
      int J9_LO_2 = 0;

      //reset
      int J1cur = 0;
      int J2cur = 0;
      int J3cur = 0;
      int J4cur = 0;
      int J5cur = 0;
      int J6cur = 0;
      int J7cur = 0;
      int J8cur = 0;
      int J9cur = 0;

      int J1_PEcur = 0;
      int J2_PEcur = 0;
      int J3_PEcur = 0;
      int J4_PEcur = 0;
      int J5_PEcur = 0;
      int J6_PEcur = 0;
      int J7_PEcur = 0;
      int J8_PEcur = 0;
      int J9_PEcur = 0;

      int J1_SE_1cur = 0;
      int J2_SE_1cur = 0;
      int J3_SE_1cur = 0;
      int J4_SE_1cur = 0;
      int J5_SE_1cur = 0;
      int J6_SE_1cur = 0;
      int J7_SE_1cur = 0;
      int J8_SE_1cur = 0;
      int J9_SE_1cur = 0;

      int J1_SE_2cur = 0;
      int J2_SE_2cur = 0;
      int J3_SE_2cur = 0;
      int J4_SE_2cur = 0;
      int J5_SE_2cur = 0;
      int J6_SE_2cur = 0;
      int J7_SE_2cur = 0;
      int J8_SE_2cur = 0;
      int J9_SE_2cur = 0;

      int highStepCur = 0;
      float curDelay = 0;

      float speedSP;
      float moveDist;

      int J1StepM = 0;
      int J2StepM = 0;
      int J3StepM = 0;
      int J4StepM = 0;
      int J5StepM = 0;
      int J6StepM = 0;
      int J7StepM = 0;
      int J8StepM = 0;
      int J9StepM = 0;

      if (J1dir) { digitalWrite(dirpins[0], HIGH); }
      else { digitalWrite(dirpins[0], LOW); }
      if (J2dir) { digitalWrite(dirpins[1], LOW); }
      else { digitalWrite(dirpins[1], HIGH); }
      if (J3dir) { digitalWrite(dirpins[2], LOW); }
      else { digitalWrite(dirpins[2], HIGH); }
      if (J4dir) { digitalWrite(dirpins[3], HIGH); }
      else { digitalWrite(dirpins[3], LOW); }
      if (J5dir) { digitalWrite(dirpins[4], LOW); }
      else { digitalWrite(dirpins[4], HIGH); }
      if (J6dir) { digitalWrite(dirpins[5], LOW); }
      else { digitalWrite(dirpins[5], HIGH); }
      if (J7dir) { digitalWrite(dirpins[6], HIGH); }
      else { digitalWrite(dirpins[6], LOW); }
      if (J8dir) { digitalWrite(dirpins[7], HIGH); }
      else { digitalWrite(dirpins[7], LOW); }
      if (J9dir) { digitalWrite(dirpins[8], HIGH); }
      else { digitalWrite(dirpins[8], LOW); }

      float calcStepGap;

      float ACCStep = HighStep * (ACCspd / 100);
      float NORStep = HighStep * ((100 - ACCspd - DCCspd) / 100);
      float DCCStep = HighStep * (DCCspd / 100);

      if (SpeedType == "s") {
        speedSP = (SpeedVal * 1000000) * .8;
      }
      else if (SpeedType == "m") {
        // lineDist = pow((pow((xyzuvw_In[0] - xyzuvw_Out[0]), 2) + pow((xyzuvw_In[1] - xyzuvw_Out[1]), 2) + pow((xyzuvw_In[2] - xyzuvw_Out[2]), 2)), .5);
        // speedSP = ((lineDist / SpeedVal) * 1000000) * .8;
      }

      String speedViolation;
      int maxSpeedDelay=3500;
      int minSpeedDelay=30;
      if (SpeedType == "s" or SpeedType == "m" ) {
        float zeroStepGap = speedSP / HighStep;
        float zeroACCstepInc = (zeroStepGap * (100 / ACCramp)) / ACCStep;
        float zeroACCtime = ((ACCStep) * zeroStepGap) + ((ACCStep - 9) * (((ACCStep) * (zeroACCstepInc / 2))));
        float zeroNORtime = NORStep * zeroStepGap;
        float zeroDCCstepInc = (zeroStepGap * (100 / ACCramp)) / DCCStep;
        float zeroDCCtime = ((DCCStep) * zeroStepGap) + ((DCCStep - 9) * (((DCCStep) * (zeroDCCstepInc / 2))));
        float zeroTOTtime = zeroACCtime + zeroNORtime + zeroDCCtime;
        float overclockPerc = speedSP / zeroTOTtime;
        calcStepGap = zeroStepGap * overclockPerc;
        if (calcStepGap <= minSpeedDelay) {
          calcStepGap = minSpeedDelay;
          speedViolation = "1";
        }
      }

      else if (SpeedType == "p") {
        calcStepGap = (maxSpeedDelay - ((SpeedVal / 100) * maxSpeedDelay));
        if (calcStepGap < minSpeedDelay) {
          calcStepGap = minSpeedDelay;
        }
      }

      float calcACCstepInc = (calcStepGap * (100 / ACCramp)) / ACCStep;
      float calcDCCstepInc = (calcStepGap * (100 / ACCramp)) / DCCStep;
      float calcACCstartDel = (calcACCstepInc * ACCStep) * 2;

      bool rndTrue = false;
      int rndSpeed = 0;
      if (rndTrue == true) {
        curDelay = rndSpeed;
        rndTrue = false;
      }
      else {
        curDelay = calcACCstartDel;
      }

      while (J1cur < J1step || J2cur < J2step || J3cur < J3step || J4cur < J4step || J5cur < J5step || J6cur < J6step || J7cur < J7step || J8cur < J8step || J9cur < J9step) {

        if (highStepCur <= ACCStep) {
          curDelay = curDelay - (calcACCstepInc);
        }
        else if (highStepCur >= (HighStep - DCCStep)) {
          curDelay = curDelay + (calcDCCstepInc);
        }
        else {
          curDelay = calcStepGap;
        }

        float distDelay = 60;
        int debugg = 0;
        if (debugg == 1) {
          distDelay = 0;
        }
        float disDelayCur = 0;


        if (J1cur < J1step)
        {
          J1_PE = (HighStep / J1step);
          ///find left over 1
          J1_LO_1 = (HighStep - (J1step * J1_PE));
          ///find skip 1
          if (J1_LO_1 > 0)
          {
            J1_SE_1 = (HighStep / J1_LO_1);
          }
          else
          {
            J1_SE_1 = 0;
          }
          ///find left over 2
          if (J1_SE_1 > 0)
          {
            J1_LO_2 = HighStep - ((J1step * J1_PE) + ((J1step * J1_PE) / J1_SE_1));
          }
          else
          {
            J1_LO_2 = 0;
          }
          ///find skip 2
          if (J1_LO_2 > 0)
          {
            J1_SE_2 = (HighStep / J1_LO_2);
          }
          else
          {
            J1_SE_2 = 0;
          }
          /////////  J1  ///////////////
          if (J1_SE_2 == 0)
          {
            J1_SE_2cur = (J1_SE_2 + 1);
          }
          if (J1_SE_2cur != J1_SE_2)
          {
            J1_SE_2cur = ++J1_SE_2cur;
            if (J1_SE_1 == 0)
            {
              J1_SE_1cur = (J1_SE_1 + 1);
            }
            if (J1_SE_1cur != J1_SE_1)
            {
              J1_SE_1cur = ++J1_SE_1cur;
              J1_PEcur = ++J1_PEcur;
              if (J1_PEcur == J1_PE)
              {
                J1cur = ++J1cur;
                J1_PEcur = 0;
                digitalWrite(steppins[0], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J1dir == 0) {
                  J1StepM == --J1StepM;
                }
                else {
                  J1StepM == ++J1StepM;
                }
              }
            }
            else
            {
              J1_SE_1cur = 0;
            }
          }
          else
          {
            J1_SE_2cur = 0;
          }
        }


        /////// J2 ////////////////////////////////
        ///find pulse every
        if (J2cur < J2step)
        {
          J2_PE = (HighStep / J2step);
          ///find left over 1
          J2_LO_1 = (HighStep - (J2step * J2_PE));
          ///find skip 1
          if (J2_LO_1 > 0)
          {
            J2_SE_1 = (HighStep / J2_LO_1);
          }
          else
          {
            J2_SE_1 = 0;
          }
          ///find left over 2
          if (J2_SE_1 > 0)
          {
            J2_LO_2 = HighStep - ((J2step * J2_PE) + ((J2step * J2_PE) / J2_SE_1));
          }
          else
          {
            J2_LO_2 = 0;
          }
          ///find skip 2
          if (J2_LO_2 > 0)
          {
            J2_SE_2 = (HighStep / J2_LO_2);
          }
          else
          {
            J2_SE_2 = 0;
          }
          /////////  J2  ///////////////
          if (J2_SE_2 == 0)
          {
            J2_SE_2cur = (J2_SE_2 + 1);
          }
          if (J2_SE_2cur != J2_SE_2)
          {
            J2_SE_2cur = ++J2_SE_2cur;
            if (J2_SE_1 == 0)
            {
              J2_SE_1cur = (J2_SE_1 + 1);
            }
            if (J2_SE_1cur != J2_SE_1)
            {
              J2_SE_1cur = ++J2_SE_1cur;
              J2_PEcur = ++J2_PEcur;
              if (J2_PEcur == J2_PE)
              {
                J2cur = ++J2cur;
                J2_PEcur = 0;
                digitalWrite(steppins[1], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J2dir == 0) {
                  J2StepM == --J2StepM;
                }
                else {
                  J2StepM == ++J2StepM;
                }
              }
            }
            else
            {
              J2_SE_1cur = 0;
            }
          }
          else
          {
            J2_SE_2cur = 0;
          }
        }

        /////// J3 ////////////////////////////////
        ///find pulse every
        if (J3cur < J3step)
        {
          J3_PE = (HighStep / J3step);
          ///find left over 1
          J3_LO_1 = (HighStep - (J3step * J3_PE));
          ///find skip 1
          if (J3_LO_1 > 0)
          {
            J3_SE_1 = (HighStep / J3_LO_1);
          }
          else
          {
            J3_SE_1 = 0;
          }
          ///find left over 2
          if (J3_SE_1 > 0)
          {
            J3_LO_2 = HighStep - ((J3step * J3_PE) + ((J3step * J3_PE) / J3_SE_1));
          }
          else
          {
            J3_LO_2 = 0;
          }
          ///find skip 2
          if (J3_LO_2 > 0)
          {
            J3_SE_2 = (HighStep / J3_LO_2);
          }
          else
          {
            J3_SE_2 = 0;
          }
          /////////  J3  ///////////////
          if (J3_SE_2 == 0)
          {
            J3_SE_2cur = (J3_SE_2 + 1);
          }
          if (J3_SE_2cur != J3_SE_2)
          {
            J3_SE_2cur = ++J3_SE_2cur;
            if (J3_SE_1 == 0)
            {
              J3_SE_1cur = (J3_SE_1 + 1);
            }
            if (J3_SE_1cur != J3_SE_1)
            {
              J3_SE_1cur = ++J3_SE_1cur;
              J3_PEcur = ++J3_PEcur;
              if (J3_PEcur == J3_PE)
              {
                J3cur = ++J3cur;
                J3_PEcur = 0;
                digitalWrite(steppins[2], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J3dir == 0) {
                  J3StepM == --J3StepM;
                }
                else {
                  J3StepM == ++J3StepM;
                }
              }
            }
            else
            {
              J3_SE_1cur = 0;
            }
          }
          else
          {
            J3_SE_2cur = 0;
          }
        }


        /////// J4 ////////////////////////////////
        ///find pulse every
        if (J4cur < J4step)
        {
          J4_PE = (HighStep / J4step);
          ///find left over 1
          J4_LO_1 = (HighStep - (J4step * J4_PE));
          ///find skip 1
          if (J4_LO_1 > 0)
          {
            J4_SE_1 = (HighStep / J4_LO_1);
          }
          else
          {
            J4_SE_1 = 0;
          }
          ///find left over 2
          if (J4_SE_1 > 0)
          {
            J4_LO_2 = HighStep - ((J4step * J4_PE) + ((J4step * J4_PE) / J4_SE_1));
          }
          else
          {
            J4_LO_2 = 0;
          }
          ///find skip 2
          if (J4_LO_2 > 0)
          {
            J4_SE_2 = (HighStep / J4_LO_2);
          }
          else
          {
            J4_SE_2 = 0;
          }
          /////////  J4  ///////////////
          if (J4_SE_2 == 0)
          {
            J4_SE_2cur = (J4_SE_2 + 1);
          }
          if (J4_SE_2cur != J4_SE_2)
          {
            J4_SE_2cur = ++J4_SE_2cur;
            if (J4_SE_1 == 0)
            {
              J4_SE_1cur = (J4_SE_1 + 1);
            }
            if (J4_SE_1cur != J4_SE_1)
            {
              J4_SE_1cur = ++J4_SE_1cur;
              J4_PEcur = ++J4_PEcur;
              if (J4_PEcur == J4_PE)
              {
                J4cur = ++J4cur;
                J4_PEcur = 0;
                digitalWrite(steppins[3], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J4dir == 0) {
                  J4StepM == --J4StepM;
                }
                else {
                  J4StepM == ++J4StepM;
                }
              }
            }
            else
            {
              J4_SE_1cur = 0;
            }
          }
          else
          {
            J4_SE_2cur = 0;
          }
        }


        /////// J5 ////////////////////////////////
        ///find pulse every
        if (J5cur < J5step)
        {
          J5_PE = (HighStep / J5step);
          ///find left over 1
          J5_LO_1 = (HighStep - (J5step * J5_PE));
          ///find skip 1
          if (J5_LO_1 > 0)
          {
            J5_SE_1 = (HighStep / J5_LO_1);
          }
          else
          {
            J5_SE_1 = 0;
          }
          ///find left over 2
          if (J5_SE_1 > 0)
          {
            J5_LO_2 = HighStep - ((J5step * J5_PE) + ((J5step * J5_PE) / J5_SE_1));
          }
          else
          {
            J5_LO_2 = 0;
          }
          ///find skip 2
          if (J5_LO_2 > 0)
          {
            J5_SE_2 = (HighStep / J5_LO_2);
          }
          else
          {
            J5_SE_2 = 0;
          }
          /////////  J5  ///////////////
          if (J5_SE_2 == 0)
          {
            J5_SE_2cur = (J5_SE_2 + 1);
          }
          if (J5_SE_2cur != J5_SE_2)
          {
            J5_SE_2cur = ++J5_SE_2cur;
            if (J5_SE_1 == 0)
            {
              J5_SE_1cur = (J5_SE_1 + 1);
            }
            if (J5_SE_1cur != J5_SE_1)
            {
              J5_SE_1cur = ++J5_SE_1cur;
              J5_PEcur = ++J5_PEcur;
              if (J5_PEcur == J5_PE)
              {
                J5cur = ++J5cur;
                J5_PEcur = 0;
                digitalWrite(steppins[4], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J5dir == 0) {
                  J5StepM == --J5StepM;
                }
                else {
                  J5StepM == ++J5StepM;
                }
              }
            }
            else
            {
              J5_SE_1cur = 0;
            }
          }
          else
          {
            J5_SE_2cur = 0;
          }
        }


        /////// J6 ////////////////////////////////
        ///find pulse every
        if (J6cur < J6step)
        {
          J6_PE = (HighStep / J6step);
          ///find left over 1
          J6_LO_1 = (HighStep - (J6step * J6_PE));
          ///find skip 1
          if (J6_LO_1 > 0)
          {
            J6_SE_1 = (HighStep / J6_LO_1);
          }
          else
          {
            J6_SE_1 = 0;
          }
          ///find left over 2
          if (J6_SE_1 > 0)
          {
            J6_LO_2 = HighStep - ((J6step * J6_PE) + ((J6step * J6_PE) / J6_SE_1));
          }
          else
          {
            J6_LO_2 = 0;
          }
          ///find skip 2
          if (J6_LO_2 > 0)
          {
            J6_SE_2 = (HighStep / J6_LO_2);
          }
          else
          {
            J6_SE_2 = 0;
          }
          /////////  J6  ///////////////
          if (J6_SE_2 == 0)
          {
            J6_SE_2cur = (J6_SE_2 + 1);
          }
          if (J6_SE_2cur != J6_SE_2)
          {
            J6_SE_2cur = ++J6_SE_2cur;
            if (J6_SE_1 == 0)
            {
              J6_SE_1cur = (J6_SE_1 + 1);
            }
            if (J6_SE_1cur != J6_SE_1)
            {
              J6_SE_1cur = ++J6_SE_1cur;
              J6_PEcur = ++J6_PEcur;
              if (J6_PEcur == J6_PE)
              {
                J6cur = ++J6cur;
                J6_PEcur = 0;
                digitalWrite(steppins[5], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J6dir == 0) {
                  J6StepM == --J6StepM;
                }
                else {
                  J6StepM == ++J6StepM;
                }
              }
            }
            else
            {
              J6_SE_1cur = 0;
            }
          }
          else
          {
            J6_SE_2cur = 0;
          }
        }


        /////// J7 ////////////////////////////////
        ///find pulse every
        if (J7cur < J7step)
        {
          J7_PE = (HighStep / J7step);
          ///find left over 1
          J7_LO_1 = (HighStep - (J7step * J7_PE));
          ///find skip 1
          if (J7_LO_1 > 0)
          {
            J7_SE_1 = (HighStep / J7_LO_1);
          }
          else
          {
            J7_SE_1 = 0;
          }
          ///find left over 2
          if (J7_SE_1 > 0)
          {
            J7_LO_2 = HighStep - ((J7step * J7_PE) + ((J7step * J7_PE) / J7_SE_1));
          }
          else
          {
            J7_LO_2 = 0;
          }
          ///find skip 2
          if (J7_LO_2 > 0)
          {
            J7_SE_2 = (HighStep / J7_LO_2);
          }
          else
          {
            J7_SE_2 = 0;
          }
          /////////  J7  ///////////////
          if (J7_SE_2 == 0)
          {
            J7_SE_2cur = (J7_SE_2 + 1);
          }
          if (J7_SE_2cur != J7_SE_2)
          {
            J7_SE_2cur = ++J7_SE_2cur;
            if (J7_SE_1 == 0)
            {
              J7_SE_1cur = (J7_SE_1 + 1);
            }
            if (J7_SE_1cur != J7_SE_1)
            {
              J7_SE_1cur = ++J7_SE_1cur;
              J7_PEcur = ++J7_PEcur;
              if (J7_PEcur == J7_PE)
              {
                J7cur = ++J7cur;
                J7_PEcur = 0;
                digitalWrite(steppins[6], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J7dir == 0) {
                  J7StepM == --J7StepM;
                }
                else {
                  J7StepM == ++J7StepM;
                }
              }
            }
            else
            {
              J7_SE_1cur = 0;
            }
          }
          else
          {
            J7_SE_2cur = 0;
          }
        }




        /////// J8 ////////////////////////////////
        ///find pulse every
        if (J8cur < J8step)
        {
          J8_PE = (HighStep / J8step);
          ///find left over 1
          J8_LO_1 = (HighStep - (J8step * J8_PE));
          ///find skip 1
          if (J8_LO_1 > 0)
          {
            J8_SE_1 = (HighStep / J8_LO_1);
          }
          else
          {
            J8_SE_1 = 0;
          }
          ///find left over 2
          if (J8_SE_1 > 0)
          {
            J8_LO_2 = HighStep - ((J8step * J8_PE) + ((J8step * J8_PE) / J8_SE_1));
          }
          else
          {
            J8_LO_2 = 0;
          }
          ///find skip 2
          if (J8_LO_2 > 0)
          {
            J8_SE_2 = (HighStep / J8_LO_2);
          }
          else
          {
            J8_SE_2 = 0;
          }
          /////////  J8  ///////////////
          if (J8_SE_2 == 0)
          {
            J8_SE_2cur = (J8_SE_2 + 1);
          }
          if (J8_SE_2cur != J8_SE_2)
          {
            J8_SE_2cur = ++J8_SE_2cur;
            if (J8_SE_1 == 0)
            {
              J8_SE_1cur = (J8_SE_1 + 1);
            }
            if (J8_SE_1cur != J8_SE_1)
            {
              J8_SE_1cur = ++J8_SE_1cur;
              J8_PEcur = ++J8_PEcur;
              if (J8_PEcur == J8_PE)
              {
                J8cur = ++J8cur;
                J8_PEcur = 0;
                digitalWrite(steppins[7], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J8dir == 0) {
                  J8StepM == --J8StepM;
                }
                else {
                  J8StepM == ++J8StepM;
                }
              }
            }
            else
            {
              J8_SE_1cur = 0;
            }
          }
          else
          {
            J8_SE_2cur = 0;
          }
        }


        /////// J9 ////////////////////////////////
        ///find pulse every
        if (J9cur < J9step)
        {
          J9_PE = (HighStep / J9step);
          ///find left over 1
          J9_LO_1 = (HighStep - (J9step * J9_PE));
          ///find skip 1
          if (J9_LO_1 > 0)
          {
            J9_SE_1 = (HighStep / J9_LO_1);
          }
          else
          {
            J9_SE_1 = 0;
          }
          ///find left over 2
          if (J9_SE_1 > 0)
          {
            J9_LO_2 = HighStep - ((J9step * J9_PE) + ((J9step * J9_PE) / J9_SE_1));
          }
          else
          {
            J9_LO_2 = 0;
          }
          ///find skip 2
          if (J9_LO_2 > 0)
          {
            J9_SE_2 = (HighStep / J9_LO_2);
          }
          else
          {
            J9_SE_2 = 0;
          }
          /////////  J9  ///////////////
          if (J9_SE_2 == 0)
          {
            J9_SE_2cur = (J9_SE_2 + 1);
          }
          if (J9_SE_2cur != J9_SE_2)
          {
            J9_SE_2cur = ++J9_SE_2cur;
            if (J9_SE_1 == 0)
            {
              J9_SE_1cur = (J9_SE_1 + 1);
            }
            if (J9_SE_1cur != J9_SE_1)
            {
              J9_SE_1cur = ++J9_SE_1cur;
              J9_PEcur = ++J9_PEcur;
              if (J9_PEcur == J9_PE)
              {
                J9cur = ++J9cur;
                J9_PEcur = 0;
                digitalWrite(steppins[8], LOW);
                delayMicroseconds(distDelay);
                disDelayCur = disDelayCur + distDelay;
                if (J9dir == 0) {
                  J9StepM == --J9StepM;
                }
                else {
                  J9StepM == ++J9StepM;
                }
              }
            }
            else
            {
              J9_SE_1cur = 0;
            }
          }
          else
          {
            J9_SE_2cur = 0;
          }
        }


        // inc cur step
        highStepCur = ++highStepCur;
        for (int i=0; i<MAXDOF; i++) {
            digitalWrite(steppins[i], HIGH);
        }
        if (debugg == 0) {
          delayMicroseconds(curDelay - disDelayCur);
        }

      }
      //set rounding speed to last move speed
      rndSpeed = curDelay;
    }


    void sendRobotPos() {
      // Implementation of the sendRobotPos function...
    }
};
