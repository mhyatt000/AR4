
#include <Arduino.h>
#include <TeensyStep.h>

const int DOF = 6;

StepControl controller; 

Stepper* motors[] = {
    new Stepper(1, 1),
    new Stepper(2, 3),
    new Stepper(4, 5),
    new Stepper(6, 7),
    new Stepper(8, 9),
    new Stepper(10,11),
};

for (int i=0; i<DOF; i++) {
    if (!away[i]) { motors[i]->setInverseRotation(true); }
    motors[i](100)->setAcceleration(50);
    motors[i]->setTargetRel(stepcenter[i]);
}

controller.move(motors);

