




/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//DRIVE MOTORS L
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

void driveMotorsL(int J1step, int J2step, int J3step, int J4step, int J5step, int J6step, int J7step, int J8step, int J9step, int J1dir, int J2dir, int J3dir, int J4dir, int J5dir, int J6dir, int J7dir, int J8dir, int J9dir, float curDelay) {

  //FIND HIGHEST STEP
  int HighStep = J1step;
  if (J2step > HighStep)
  {
    HighStep = J2step;
  }
  if (J3step > HighStep)
  {
    HighStep = J3step;
  }
  if (J4step > HighStep)
  {
    HighStep = J4step;
  }
  if (J5step > HighStep)
  {
    HighStep = J5step;
  }
  if (J6step > HighStep)
  {
    HighStep = J6step;
  }
  if (J7step > HighStep)
  {
    HighStep = J7step;
  }
  if (J8step > HighStep)
  {
    HighStep = J8step;
  }
  if (J9step > HighStep)
  {
    HighStep = J9step;
  }

  //FIND ACTIVE JOINTS
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

  if (J1step >= 1)
  {
    J1active = 1;
  }
  if (J2step >= 1)
  {
    J2active = 1;
  }
  if (J3step >= 1)
  {
    J3active = 1;
  }
  if (J4step >= 1)
  {
    J4active = 1;
  }
  if (J5step >= 1)
  {
    J5active = 1;
  }
  if (J6step >= 1)
  {
    J6active = 1;
  }
  if (J7step >= 1)
  {
    J7active = 1;
  }
  if (J8step >= 1)
  {
    J8active = 1;
  }
  if (J9step >= 1)
  {
    J9active = 1;
  }
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

  float speedSP;
  float moveDist;

  //process lookahead
  if (splineTrue == true) {
    processSerial();
  }

  //SET DIRECTIONS

  /// J1 ///
  if (J1dir) {
    digitalWrite(J1dirPin, HIGH);
  }
  else {
    digitalWrite(J1dirPin, LOW);
  }
  /// J2 ///
  if (J2dir) {
    digitalWrite(J2dirPin, LOW);
  }
  else {
    digitalWrite(J2dirPin, HIGH);
  }
  /// J3 ///
  if (J3dir) {
    digitalWrite(J3dirPin, LOW);
  }
  else {
    digitalWrite(J3dirPin, HIGH);
  }
  /// J4 ///
  if (J4dir) {
    digitalWrite(J4dirPin, HIGH);
  }
  else {
    digitalWrite(J4dirPin, LOW);
  }
  /// J5 ///
  if (J5dir) {
    digitalWrite(J5dirPin, LOW);
  }
  else {
    digitalWrite(J5dirPin, HIGH);
  }
  /// J6 ///
  if (J6dir) {
    digitalWrite(J6dirPin, LOW);
  }
  else {
    digitalWrite(J6dirPin, HIGH);
  }

  /// J7 ///
  if (J7dir) {
    digitalWrite(J7dirPin, HIGH);
  }
  else {
    digitalWrite(J7dirPin, LOW);
  }

  /// J8 ///
  if (J8dir) {
    digitalWrite(J8dirPin, HIGH);
  }
  else {
    digitalWrite(J8dirPin, LOW);
  }

  /// J9 ///
  if (J9dir) {
    digitalWrite(J9dirPin, HIGH);
  }
  else {
    digitalWrite(J9dirPin, LOW);
  }


  J1collisionTrue = 0;
  J2collisionTrue = 0;
  J3collisionTrue = 0;
  J4collisionTrue = 0;
  J5collisionTrue = 0;
  J6collisionTrue = 0;

  ///// DRIVE MOTORS /////
  while (J1cur < J1step || J2cur < J2step || J3cur < J3step || J4cur < J4step || J5cur < J5step || J6cur < J6step || J7cur < J7step || J8cur < J8step || J9cur < J9step)
  {

    float distDelay = 60;
    float disDelayCur = 0;

    //process lookahead
    if (splineTrue == true) {
      processSerial();
    }

    /////// J1 ////////////////////////////////
    ///find pulse every
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
            digitalWrite(J1stepPin, LOW);
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
    delayMicroseconds(curDelay - disDelayCur);

  }
}



