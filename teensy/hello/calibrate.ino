#include <AccelStepper.h>

#define DOF 6
#define MAXDOF 9

AccelStepper motor1(1, 0, 1);
AccelStepper motor2(1, 2, 3);
AccelStepper motor3(1, 4, 5);
AccelStepper motor4(1, 6, 7);
AccelStepper motor5(1, 8, 9);
AccelStepper motor6(1, 10, 11);

// long positions[DOF] = {500, 500, 500};


// limit switches
int switches[] = { 26, 27, 28, 29, 30, 31, 36, 37, 38};
int clockwise[] = { 1, 1, 1, 1, 1, 1, 1, 1, 1};

// int size(arr) {,
    // return sizeof(arr) / sizeof(arr[0]);
// }

void pass() { 
    for (int i = 0; i < DOF; i++) {
        int state = digitalRead(switches[i]);
        Serial.print(" state: " + String(state));
    }
    Serial.println("");
    delay(1); 
}

void home() {}

void setup() {

    Serial.begin(9600);
    
    // speed 1000 acc 500

    motor1.setMaxSpeed(2000); 
    motor2.setMaxSpeed(2000); 
    motor3.setMaxSpeed(2000); 
    motor4.setMaxSpeed(2000); 
    motor5.setMaxSpeed(2000); 
    motor6.setMaxSpeed(2000); 

    motor1.setAcceleration(500); 
    motor2.setAcceleration(500); 
    motor3.setAcceleration(500); 
    motor4.setAcceleration(500); 
    motor5.setAcceleration(500); 
    motor6.setAcceleration(500); 

    motor1.setMinPulseWidth(20);
    motor2.setMinPulseWidth(20);
    motor3.setMinPulseWidth(20);
    motor4.setMinPulseWidth(20);
    motor5.setMinPulseWidth(20);
    motor6.setMinPulseWidth(20);

    motor1.moveTo(100);
    motor2.moveTo(100);
    motor3.moveTo(100);
    motor4.moveTo(100);
    motor5.moveTo(100);
    motor6.moveTo(100);

    for (int i=0; i<9; i++) {
        attachInterrupt(digitalPinToInterrupt(switches[i]), pass, HIGH);
    }

    Serial.println("Setup completed. Motors are set to move to initial positions.");
    delay(5);
}

void loop() {

    motor1.run();
    motor2.run();
    motor3.run();
    motor4.run();
    motor5.run();
    motor6.run();

    if (0 == motor1.distanceToGo() + motor2.distanceToGo() + motor3.distanceToGo() + motor4.distanceToGo() + motor5.distanceToGo() + motor6.distanceToGo()) {
        
        motor1.moveTo(-motor1.currentPosition());
        motor2.moveTo(-motor2.currentPosition());
        motor3.moveTo(-motor3.currentPosition());
        motor4.moveTo(-motor4.currentPosition());
        motor5.moveTo(-motor5.currentPosition());
        motor6.moveTo(-motor6.currentPosition());
    }

        // for (int i=0; i<DOF; i++){
            // positions[i] = 
        // }


}


