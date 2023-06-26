


void resetEncoders() {

  J1collisionTrue = 0;
  J2collisionTrue = 0;
  J3collisionTrue = 0;
  J4collisionTrue = 0;
  J5collisionTrue = 0;
  J6collisionTrue = 0;

  //set encoders to current position
  J1encPos.write(J1StepM * J1encMult);
  J2encPos.write(J2StepM * J2encMult);
  J3encPos.write(J3StepM * J3encMult);
  J4encPos.write(J4StepM * J4encMult);
  J5encPos.write(J5StepM * J5encMult);
  J6encPos.write(J6StepM * J6encMult);
  //delayMicroseconds(5);

}

void checkEncoders() {
  //read encoders
  J1EncSteps = J1encPos.read() / J1encMult;
  J2EncSteps = J2encPos.read() / J2encMult;
  J3EncSteps = J3encPos.read() / J3encMult;
  J4EncSteps = J4encPos.read() / J4encMult;
  J5EncSteps = J5encPos.read() / J5encMult;
  J6EncSteps = J6encPos.read() / J6encMult;

  if (abs((J1EncSteps - J1StepM)) >= 15) {
    if (J1LoopMode == 0) {
      J1collisionTrue = 1;
      J1StepM = J1encPos.read() / J1encMult;
    }
  }
  if (abs((J2EncSteps - J2StepM)) >= 15) {
    if (J2LoopMode == 0) {
      J2collisionTrue = 1;
      J2StepM = J2encPos.read() / J2encMult;
    }
  }
  if (abs((J3EncSteps - J3StepM)) >= 15) {
    if (J3LoopMode == 0) {
      J3collisionTrue = 1;
      J3StepM = J3encPos.read() / J3encMult;
    }
  }
  if (abs((J4EncSteps - J4StepM)) >= 15) {
    if (J4LoopMode == 0) {
      J4collisionTrue = 1;
      J4StepM = J4encPos.read() / J4encMult;
    }
  }
  if (abs((J5EncSteps - J5StepM)) >= 15) {
    if (J5LoopMode == 0) {
      J5collisionTrue = 1;
      J5StepM = J5encPos.read() / J5encMult;
    }
  }
  if (abs((J6EncSteps - J6StepM)) >= 15) {
    if (J6LoopMode == 0) {
      J6collisionTrue = 1;
      J6StepM = J6encPos.read() / J6encMult;
    }
  }

  TotalCollision = J1collisionTrue + J2collisionTrue + J3collisionTrue + J4collisionTrue + J5collisionTrue + J6collisionTrue;
  if (TotalCollision > 0) {
    flag = "EC" + String(J1collisionTrue) + String(J2collisionTrue) + String(J3collisionTrue) + String(J4collisionTrue) + String(J5collisionTrue) + String(J6collisionTrue);
  }
}







