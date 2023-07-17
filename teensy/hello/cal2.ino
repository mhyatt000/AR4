#include <AccelStepper.h>

#define DOF 6
#define MAXDOF 9


AccelStepper motor1(1, 0, 1);
AccelStepper motor2(1, 2, 3);
AccelStepper motor3(1, 4, 5);
AccelStepper motor4(1, 6, 7);
AccelStepper motor5(1, 8, 9);
AccelStepper motor6(1, 10, 11);

AccelStepper motors[DOF] = {motor1,motor2,motor3,motor4,motor5,motor6};


// long positions[DOF] = {500, 500, 500};


// limit switches
int switches[] = { 26, 27, 28, 29, 30, 31, 36, 37, 38};
// is clockwise away from limit
int away[] = { 1, -1, 1, 1, -1, 1, 2, 2, 2};
int calibrated[9] = {0};

void pass() { 
    for (int i = 0; i < DOF; i++) {
        int state = digitalRead(switches[i]);
        Serial.print(" state: " + String(state));
    }
    Serial.println("");
}

void bounce() {
    for (int i = 0; i < DOF; i++) {
        int limit = digitalRead(switches[i]);
        if (limit) {
            calibrated[i] = 1;
            motors[i].setMaxSpeed(1000);
            motors[i].move(1000*away[i]) ;
            motors[i].setCurrentPosition(1000); 
            motors[i].setMaxSpeed(1000);
            motors[i].runToPosition();
        } 
    }
    Serial.println("bounce");
    delay(5); 

}


int alldist(){
    int dist = 0;
    for (int i = 0; i < DOF; i++) {
        dist += motors[i].distanceToGo();
    }
    return dist;
}

void allgo(){
    while(alldist()) {
        for (int i=0; i<DOF; i++){
            motors[i].run();
        }
    }
}


void home() {

    for (int i=0; i<DOF; i++){
        motors[i].moveTo(1000 * away[i]);
    }
    allgo();
        
} // home
    

void backoff(){
    Serial.println("started backoff");

    for (int i=0; i<DOF; i++){
        motors[i].setMaxSpeed(750);
        motors[i].setAcceleration(100);
        motors[i].setMinPulseWidth(20);
        motors[i].move(-10000 * away[i]);
    }
    allgo();
    Serial.println("end backoff");


} // calibrate

bool alllimit() {
    bool lim = true;
    for (int i=0; i<DOF; i++){ lim = lim && digitalRead(switches[i]); }
    return lim;
}

void calibrate(int speed){

    for (int i=0; i<DOF; i++){
        motors[i].setMaxSpeed(speed);
        motors[i].setAcceleration(100);
        motors[i].setMinPulseWidth(20);
        motors[i].move(-10000 * away[i]);
    }
    while (!alllimit()) {
        pass();
        for (int i=0; i<5; i++){
            if (!digitalRead(switches[i])) { motors[i].run(); }
            else { motors[i].stop(); }
        }
    }
    delay(5);
    
} // calibrate

void setup() {

    Serial.begin(9600);

    // for (int i=0; i<MAXDOF; i++) {
        // attachInterrupt(digitalPinToInterrupt(switches[i]), bounce, HIGH);
    // }

    calibrate(500);
    Serial.println("cal1");
    backoff();
    Serial.println("backoff");
    calibrate(50);
    Serial.println("cal2");

    Serial.println("done");
}

void temp() {

    for (int i=0; i<DOF; i++){
        motors[i] = AccelStepper(1,2*i, 2*i+1);
        motors[i].setMaxSpeed(2000);
        motors[i].setAcceleration(500);
        motors[i].setMinPulseWidth(20);
    }

    home();

    for (int i=0; i<DOF; i++){
        motors[i].move(away[i] ? 100 : -100);
    }

    Serial.println("Setup completed. Motors are set to move to initial positions.");
    delay(5);
} // setup

void loop() {

    // for (int i=0; i<DOF; i++){
        // motors[i].run();
        // if (!motors[i].distanceToGo()){
            // motors[i].moveTo(-motors[i].currentPosition());
            // motors[i].move(away[i] ? 100 : -100);
        // }

    // }

} // loop
