void driveMotorsJ(int[] steps, int[] dirs, String SpeedType, float SpeedVal, float ACCspd, float DCCspd, float ACCramp) {

  //FIND HIGHEST STEP
  int highest = steps[0];
  for (int i = 0; i < 9; i++) {
    highest = steps[i] > highest ? steps[i] : highest;
  }

  //FIND ACTIVE JOINTS
  int actives[9] = {0};
  for (int i = 0; i < 9; i++) {
      actives[i] = steps[i] >= 1 ? 1 : 0;
  }

  int total_active = 0; 
  for (int i = 0; i < 9; i++) {
      total_active += actives[i];
  }

  int PE[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  int SE_1[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  int SE_2[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  int LO_1[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  int LO_2[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};

  //reset
  int cur[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  int PEcur[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  int SE_1cur[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};
  int SE_2cur[9] = {0, 0, 0, 0, 0, 0, 0, 0, 0};

  int highStepCur = 0;
  float curDelay = 0;

  float speedSP;
  float moveDist;

  //SET DIRECTIONS
  for (int i=0; i < 9; i++ ) {
    if (dirs[i]) { digitalWrite(dirpins[i], HIGH); }
    else { digitalWrite(dirpins[i], HIGH); }
  }

  /////CALC SPEEDS//////
  float calcStepGap;

  //determine steps
  float ACCStep = highest * (ACCspd / 100);
  float NORStep = highest * ((100 - ACCspd - DCCspd) / 100);
  float DCCStep = highest * (DCCspd / 100);

  //set speed for seconds or mm per sec
  if (SpeedType == "s") { 
    speedSP = (SpeedVal * 1000000) * 0.8; 
  }
  else if (SpeedType == "m") {
    lineDist = pow((pow((xyzuvw_In[0] - xyzuvw_Out[0]), 2) + pow((xyzuvw_In[1] - xyzuvw_Out[1]), 2) + pow((xyzuvw_In[2] - xyzuvw_Out[2]), 2)), .5);
    speedSP = ((lineDist / SpeedVal) * 1000000) * 0.8;
  }

  //calc step gap for seconds or mm per sec
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

  //calc step gap for percentage
  else if (SpeedType == "p") {
    calcStepGap = (maxSpeedDelay - ((SpeedVal / 100) * maxSpeedDelay));
    if (calcStepGap < minSpeedDelay) {
      calcStepGap = minSpeedDelay;
    }
  }

  //calculate final step increments
  float calcACCstepInc = (calcStepGap * (100 / ACCramp)) / ACCStep;
  float calcDCCstepInc = (calcStepGap * (100 / ACCramp)) / DCCStep;
  float calcACCstartDel = (calcACCstepInc * ACCStep) * 2;

  //set starting delay
  if (rndTrue == true) {
    curDelay = rndSpeed;
    rndTrue = false;
  }
  else {
    curDelay = calcACCstartDel;
  }

  ///// DRIVE MOTORS /////
  while (J1cur < J1step || J2cur < J2step || J3cur < J3step || J4cur < J4step || J5cur < J5step || J6cur < J6step || J7cur < J7step || J8cur < J8step || J9cur < J9step)
  {

    ////DELAY CALC/////
    if (highStepCur <= ACCStep) {
      curDelay = curDelay - (calcACCstepInc);
    }
    else if (highStepCur >= (HighStep - DCCStep)) {
      curDelay = curDelay + (calcDCCstepInc);
    }
    else {
      curDelay = calcStepGap;
    }

    float distDelay = debugg == 1 ? 0 : 60;
    float disDelayCur = 0;

    /////// J1 ////////////////////////////////
    ///find pulse every
    if (J1cur < J1step)
    {
      J1_PE = (HighStep / J1step);
      ///find left over 1
      J1_LO_1 = (HighStep - (J1step * J1_PE));
      ///find skip 1
      if (J1_LO_1 > 0) { J1_SE_1 = (HighStep / J1_LO_1); }
      else { J1_SE_1 = 0; }
      ///find left over 2
      if (J1_SE_1 > 0) {
        J1_LO_2 = HighStep - ((J1step * J1_PE) + ((J1step * J1_PE) / J1_SE_1));
      }
      else { J1_LO_2 = 0; }
      ///find skip 2
      if (J1_LO_2 > 0) {
        J1_SE_2 = (HighStep / J1_LO_2);
      }
      else { J1_SE_2 = 0; }

      /////////  J1  ///////////////
      if (J1_SE_2 == 0) { J1_SE_2cur = (J1_SE_2 + 1); }
      if (J1_SE_2cur != J1_SE_2) {
        J1_SE_2cur = ++J1_SE_2cur;
        if (J1_SE_1 == 0) {
          J1_SE_1cur = (J1_SE_1 + 1);
        }
        if (J1_SE_1cur != J1_SE_1) {
          J1_SE_1cur = ++J1_SE_1cur;
          J1_PEcur = ++J1_PEcur;
          if (J1_PEcur == J1_PE) {
            J1cur = ++J1cur;
            J1_PEcur = 0;
            digitalWrite(J1stepPin, LOW);
            delayMicroseconds(distDelay);
            disDelayCur = disDelayCur + distDelay;
            if (J1dir == 0) {
              J1StepM == --J1StepM;
            }
            else { J1StepM == ++J1StepM; }
          }
        }
        else { J1_SE_1cur = 0; }
      }
      else { J1_SE_2cur = 0; }
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
            digitalWrite(J2stepPin, LOW);
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
            digitalWrite(J3stepPin, LOW);
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
            digitalWrite(J4stepPin, LOW);
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
            digitalWrite(J5stepPin, LOW);
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
            digitalWrite(J6stepPin, LOW);
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
            digitalWrite(J7stepPin, LOW);
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
            digitalWrite(J8stepPin, LOW);
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
            digitalWrite(J9stepPin, LOW);
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

    digitalWrite(J1stepPin, HIGH);
    digitalWrite(J2stepPin, HIGH);
    digitalWrite(J3stepPin, HIGH);
    digitalWrite(J4stepPin, HIGH);
    digitalWrite(J5stepPin, HIGH);
    digitalWrite(J6stepPin, HIGH);
    digitalWrite(J7stepPin, HIGH);
    digitalWrite(J8stepPin, HIGH);
    digitalWrite(J9stepPin, HIGH);
    if (debugg == 0) {
      delayMicroseconds(curDelay - disDelayCur);
    }

  }
  //set rounding speed to last move speed
  rndSpeed = curDelay;
}


void rj(){

    if (function == "RJ") {

      int[9] dirpins;
      int[9] faults;
      int total_fault;

      int J1stepStart = inData.indexOf("A");
      int J2stepStart = inData.indexOf("B");
      int J3stepStart = inData.indexOf("C");
      int J4stepStart = inData.indexOf("D");
      int J5stepStart = inData.indexOf("E");
      int J6stepStart = inData.indexOf("F");

      int J7Start = inData.indexOf("J7");
      int J8Start = inData.indexOf("J8");
      int J9Start = inData.indexOf("J9");
      int SPstart = inData.indexOf("S");
      int AcStart = inData.indexOf("Ac");
      int DcStart = inData.indexOf("Dc");
      int RmStart = inData.indexOf("Rm");

      int WristConStart = inData.indexOf("W");
      int LoopModeStart = inData.indexOf("Lm");

      float[6] angles;

      J1Angle = inData.substring(J1stepStart + 1, J2stepStart).toFloat();
      J2Angle = inData.substring(J2stepStart + 1, J3stepStart).toFloat();
      J3Angle = inData.substring(J3stepStart + 1, J4stepStart).toFloat();
      J4Angle = inData.substring(J4stepStart + 1, J5stepStart).toFloat();
      J5Angle = inData.substring(J5stepStart + 1, J6stepStart).toFloat();
      J6Angle = inData.substring(J6stepStart + 1, J7Start).toFloat();

      J7_In = inData.substring(J7Start + 2, J8Start).toFloat();
      J8_In = inData.substring(J8Start + 2, J9Start).toFloat();
      J9_In = inData.substring(J9Start + 2, SPstart).toFloat();

      String SpeedType = inData.substring(SPstart + 1, SPstart + 2);
      float SpeedVal = inData.substring(SPstart + 2, AcStart).toFloat();
      float ACCspd = inData.substring(AcStart + 2, DcStart).toFloat();
      float DCCspd = inData.substring(DcStart + 2, RmStart).toFloat();
      float ACCramp = inData.substring(RmStart + 2, WristConStart).toFloat();

      String WristCon = inData.substring(WristConStart + 1, LoopModeStart);
      String LoopMode = inData.substring(LoopModeStart + 2);

      LoopMode.trim();

      J1LoopMode = LoopMode.substring(0, 1).toInt();
      J2LoopMode = LoopMode.substring(1, 2).toInt();
      J3LoopMode = LoopMode.substring(2, 3).toInt();
      J4LoopMode = LoopMode.substring(3, 4).toInt();
      J5LoopMode = LoopMode.substring(4, 5).toInt();
      J6LoopMode = LoopMode.substring(5).toInt();

      int J1futStepM = (J1Angle + J1axisLimNeg) * J1StepDeg;
      int J2futStepM = (J2Angle + J2axisLimNeg) * J2StepDeg;
      int J3futStepM = (J3Angle + J3axisLimNeg) * J3StepDeg;
      int J4futStepM = (J4Angle + J4axisLimNeg) * J4StepDeg;
      int J5futStepM = (J5Angle + J5axisLimNeg) * J5StepDeg;
      int J6futStepM = (J6Angle + J6axisLimNeg) * J6StepDeg;
      int J7futStepM = (J7_In + J7axisLimNeg) * J7StepDeg;
      int J8futStepM = (J8_In + J8axisLimNeg) * J8StepDeg;
      int J9futStepM = (J9_In + J9axisLimNeg) * J9StepDeg;

      //calc delta from current to destination
      int J1stepDif = J1StepM - J1futStepM;
      int J2stepDif = J2StepM - J2futStepM;
      int J3stepDif = J3StepM - J3futStepM;
      int J4stepDif = J4StepM - J4futStepM;
      int J5stepDif = J5StepM - J5futStepM;
      int J6stepDif = J6StepM - J6futStepM;
      int J7stepDif = J7StepM - J7futStepM;
      int J8stepDif = J8StepM - J8futStepM;
      int J9stepDif = J9StepM - J9futStepM;


      //determine motor directions
      if (J1stepDif <= 0) { J1dir = 1; }
      else { J1dir = 0; }

      if (J2stepDif <= 0) { J2dir = 1; }
      else { J2dir = 0; }

      if (J3stepDif <= 0) { J3dir = 1; }
      else { J3dir = 0; }

      if (J4stepDif <= 0) { J4dir = 1; }
      else { J4dir = 0; }

      if (J5stepDif <= 0) { J5dir = 1; }
      else { J5dir = 0; }

      if (J6stepDif <= 0) { J6dir = 1; }
      else { J6dir = 0; }

      if (J7stepDif <= 0) { J7dir = 1; }
      else { J7dir = 0; }

      if (J8stepDif <= 0) { J8dir = 1; }
      else { J8dir = 0; }

      if (J9stepDif <= 0) { J9dir = 1; }
      else { J9dir = 0; }


      //determine if requested position is within axis limits
      if ((J1dir == 1 and (J1StepM + J1stepDif > J1StepLim)) or (J1dir == 0 and (J1StepM - J1stepDif < 0))) {
        J1axisFault = 1;
      }
      if ((J2dir == 1 and (J2StepM + J2stepDif > J2StepLim)) or (J2dir == 0 and (J2StepM - J2stepDif < 0))) {
        J2axisFault = 1;
      }
      if ((J3dir == 1 and (J3StepM + J3stepDif > J3StepLim)) or (J3dir == 0 and (J3StepM - J3stepDif < 0))) {
        J3axisFault = 1;
      }
      if ((J4dir == 1 and (J4StepM + J4stepDif > J4StepLim)) or (J4dir == 0 and (J4StepM - J4stepDif < 0))) {
        J4axisFault = 1;
      }
      if ((J5dir == 1 and (J5StepM + J5stepDif > J5StepLim)) or (J5dir == 0 and (J5StepM - J5stepDif < 0))) {
        J5axisFault = 1;
      }
      if ((J6dir == 1 and (J6StepM + J6stepDif > J6StepLim)) or (J6dir == 0 and (J6StepM - J6stepDif < 0))) {
        J6axisFault = 1;
      }
      if ((J7dir == 1 and (J7StepM + J7stepDif > J7StepLim)) or (J7dir == 0 and (J7StepM - J7stepDif < 0))) {
        J7axisFault = 1;
      }
      if ((J8dir == 1 and (J8StepM + J8stepDif > J8StepLim)) or (J8dir == 0 and (J8StepM - J8stepDif < 0))) {
        J8axisFault = 1;
      }
      if ((J9dir == 1 and (J9StepM + J9stepDif > J9StepLim)) or (J9dir == 0 and (J9StepM - J9stepDif < 0))) {
        J9axisFault = 1;
      }
      TotalAxisFault = J1axisFault + J2axisFault + J3axisFault + J4axisFault + J5axisFault + J6axisFault + J7axisFault + J8axisFault + J9axisFault;

      //send move command if no axis limit error
      if (TotalAxisFault == 0 && KinematicError == 0) {
        resetEncoders();
        driveMotorsJ(abs(J1stepDif), abs(J2stepDif), abs(J3stepDif), abs(J4stepDif), abs(J5stepDif), abs(J6stepDif), abs(J7stepDif), abs(J8stepDif), abs(J9stepDif), J1dir, J2dir, J3dir, J4dir, J5dir, J6dir, J7dir, J8dir, J9dir, SpeedType, SpeedVal, ACCspd, DCCspd, ACCramp);
        checkEncoders();
        sendRobotPos();
      }

      else if (KinematicError == 1) {
        Alarm = "ER";
        delay(5);
        Serial.println(Alarm);
      }

      else {
        Alarm = "EL" + String(J1axisFault) + String(J2axisFault) + String(J3axisFault) + String(J4axisFault) + String(J5axisFault) + String(J6axisFault) + String(J7axisFault) + String(J8axisFault) + String(J9axisFault);
        delay(5);
        Serial.println(Alarm);
      }


      inData = ""; // Clear recieved buffer
      ////////MOVE COMPLETE///////////

    }
}
