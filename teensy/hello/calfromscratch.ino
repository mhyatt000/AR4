
int reverseSwitch = 2;  // Push button for reverse
int driverPUL = 0;    // PUL- pin
int driverDIR = 1;    // DIR- pin
int spd = A0;     // Potentiometer

// Variables

int pd = 500;       // Pulse Delay period
boolean setdir = LOW; // Set Direction
int i = 0;

// Interrupt Handler

void reverse (){ setdir = !setdir; }


void setup() {

  pinMode (driverPUL, OUTPUT);
  pinMode (driverDIR, OUTPUT);
  // if you want you can change direction with button press
  // attachInterrupt(digitalPinToInterrupt(reverseSwitch), revmotor, FALLING);
  
}


void loop() {
  
    // if you want you can toggle speed with potentiometer
    // pd = map((analogRead(spd)),0,1023,2000,50);
    digitalWrite(driverDIR,setdir);
    digitalWrite(driverPUL,HIGH);
    delayMicroseconds(pd);
    digitalWrite(driverPUL,LOW);
    delayMicroseconds(pd);
 
    if (i > 1000 || i < -1000) {
        reverse();
    }
    if (setdir) {
        i++ ;
    }
    else {
        i-- ;
    }
}




void drive_limit(int[] steps, float percent_speed) {

    // RESET COUNTERS
    // TODO whats the difference
    // NOTE maybe dones is the nsteps done and completes is status
    int dones[MAXDOF] = {0};
    int completes[MAXDOF] = {0};

    int wait = ((max_wait - ((percent_speed / 100) * max_wait)) + min_wait + 300);

    // SET CAL DIRECTION
    // move towards limit
    for (int i=0; i<DOF; i++){ digitalWrite(dirpins[i], !away[i]); }

    // DRIVE MOTORS FOR CALIBRATION
    int[] states;

    int nodone = 0;
    for (int i=0; i<DOF; i++) {
        if (!steps[i]) {
            completes[i] = 1;
            nodone += 1
        }
    }

  while (nodone) {

    /*
    4 times, check each limit switch
    if they are HIGH wait a little (maybe cuz of noise?)
    if they are still HIGH, youve hit a switch
    */
    for (int n=0; n<4; n++) {
        for (int i=0; i<DOF; i++) {
            if digitalRead(switches[i] == LOW) {
                states[i] == LOW;
                break;
            } else {
                delayMicroseconds(10);
                break;
            }
        }
        for (int i=0; i<DOF; i++) {
            states[i] = digitalRead(switches[i]);
        }
    }

    for (int i=0; i<DOF; i++) {

        // TODO maybe just rely on limit?
        if (dones[i] < steps[i] && states[i] == LOW && !completes[i]) {
          digitalWrite(steppins[i], LOW);
          delayMicroseconds(50);
          digitalWrite(steppins[i], HIGH);
          dones[i]++;
        }
        else {
          completes[i] = 1;
        }

    }

    nodone = 0;
    for (int i=0; i<DOF; i++) { nodone += completes[i] }

    delayMicroseconds(wait);
  }

} // drive_limit

void backoff(int[] tocalibrate) {

    for (int i=0; i<DOF; i++) {
        digitalWrite(dirpins[i], away[i]);
    }

    for (int i=0; i<250; i++) {

        for (int i=0; i<DOF; i++) {
            if (tocalibrate[i]) {
                digitalWrite(steppins[i], LOW);
                delayMicroseconds(5);
                digitalWrite(steppins[i], HIGH);
                delayMicroseconds(5);
            }
        }

    } // 250 times

} // backoff

void overdrive(int[] tocalibrate) {
    // MAKE SURE LIMIT SWITCH STAYS MADE

    for (int i=0; i<DOF; i++) {
        digitalWrite(dirpins[i], !away[i]);
    }

    for (int i=0; i<50; i++) {
        for (int i=0; i<DOF; i++) {
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

    // TODO get offsets if needed

    int[MAXDOF] tocalibrate = {1,1,1,1,1,1,0,0,0};

    int[MAXDOF] steps = {0};
    int[MAXDOF] stepcen = {0};
    
    Alarm = "0";

    for (int i=0; i<DOF; i++) { steps[i] = tocalibrate[i] ? steplimits[i] : 0; }

    percent_speed = 80;
    driveLimit(steps, percent_speed);
    delay(500);

    backoff();

    percent_speed = .02;
    driveLimit(steps, percent_speed);

    overdrive(tocalibrate);

    // SEE IF ANY SWITCHES NOT MADE
    delay(500);

    if (J1req == 1) { if (digitalRead(J1calPin) == LOW) { Alarm = "1"; } }
    if (J2req == 1) { if (digitalRead(J2calPin) == LOW) { Alarm = "2"; } }
    if (J3req == 1) { if (digitalRead(J3calPin) == LOW) { Alarm = "3"; } }
    if (J4req == 1) { if (digitalRead(J4calPin) == LOW) { Alarm = "4"; } }
    if (J5req == 1) { if (digitalRead(J5calPin) == LOW) { Alarm = "5"; } }
    if (J6req == 1) { if (digitalRead(J6calPin) == LOW) { Alarm = "6"; } }
    if (J7req == 1) { if (digitalRead(J7calPin) == LOW) { Alarm = "7"; } }
    if (J8req == 1) { if (digitalRead(J8calPin) == LOW) { Alarm = "8"; } }
    if (J9req == 1) { if (digitalRead(J9calPin) == LOW) { Alarm = "9"; } }

    if (Alarm == "0") {

        //set master steps and center step
        if (J1req == 1) {
          J1StepM = ((J1axisLim) + J1calBaseOff + J1calOff) * J1StepDeg;
          J1stepCen = ((J1axisLimPos) + J1calBaseOff + J1calOff) * J1StepDeg;
        }
        if (J2req == 1) {
          J2StepM = (0 + J2calBaseOff + J2calOff) * J2StepDeg;
          J2stepCen = ((J2axisLimNeg) - J2calBaseOff - J2calOff) * J2StepDeg;
        }
        if (J3req == 1) {
          J3StepM = ((J3axisLim) + J3calBaseOff + J3calOff) * J3StepDeg;
          J3stepCen = ((J3axisLimPos) + J3calBaseOff + J3calOff) * J3StepDeg;
        }
        if (J4req == 1) {
          J4StepM = (0 + J4calBaseOff + J4calOff) * J4StepDeg;
          J4stepCen = ((J4axisLimNeg) - J4calBaseOff - J4calOff) * J4StepDeg;
        }
        if (J5req == 1) {
          J5StepM = (0 + J5calBaseOff + J5calOff) * J5StepDeg;
          J5stepCen = ((J5axisLimNeg) - J5calBaseOff - J5calOff) * J5StepDeg;
        }
        if (J6req == 1) {
          J6StepM = ((J6axisLim) + J6calBaseOff + J6calOff) * J6StepDeg;
          J6stepCen = ((J6axisLimNeg) + J6calBaseOff + J6calOff) * J6StepDeg;
        }
        if (J7req == 1) {
          J7StepM = (0 + J7calBaseOff + J7calOff) * J7StepDeg;
          J7stepCen = 0;
        }
        if (J8req == 1) {
          J8StepM = (0 + J8calBaseOff + J8calOff) * J8StepDeg;
          J8stepCen = 0;
        }
        if (J9req == 1) {
          J9StepM = (0 + J9calBaseOff + J9calOff) * J9StepDeg;
          J9stepCen = 0;
        }

        //move to center
        int[] directions = away
        int J1dir = 0;
        int J2dir = 1;
        int J3dir = 0;
        int J4dir = 1;
        int J5dir = 1;
        int J6dir = 0;
        int J7dir = 1;
        int J8dir = 1;
        int J9dir = 1;

        float ACCspd = 10;
        float DCCspd = 10;
        String SpeedType = "p";
        float SpeedVal = 80;
        float ACCramp = 50;

        driveMotorsJ(J1stepCen, J2stepCen, J3stepCen, J4stepCen, J5stepCen, J6stepCen, J7stepCen, J8stepCen, J9stepCen, J1dir, J2dir, J3dir, J4dir, J5dir, J6dir, J7dir, J8dir, J9dir, SpeedType, SpeedVal, ACCspd, DCCspd, ACCramp);
        sendRobotPos();

    }
    else {
        delay(5);
        Serial.println(Alarm);
        Alarm = "0";
    }

    inData = ""; // Clear recieved buffer

} // calibrate
