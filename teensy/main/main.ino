#include <math.h>
#include <avr/pgmspace.h>
#include <Encoder.h>

#include <Arduino.h>
#include <tuple>
#include <iostream>
#include <string>
#include <vector>

#include "define.h"
#include "buffer.h"
#include "ctrl.h"

int steppins[DOF] = {0,2,4,6,8,10};
int dirpins[DOF] = {1,3,5,7,9,11};
int switches[MAXDOF] = {26,27,28,29,30,31,36,37,38};

// TODO what are these?
const int Input39 = 39;
const int Output40 = 40;
const int Output41 = 41;


Buffer buffer;
CTRL ctrl;

String command;
String recData;
String checkData;
String function;

String flag = "";
String moveSequence;
bool rndTrue;
bool use_spline ;
bool end_spline;

int kinematic_error = 0;

int * parseString(String str) {
  static int steps[9];
  int i = 0;
  
  int idx1 = 0;
  int idx2 = str.indexOf('#');
  
  while (idx2 != -1) {
    String substr = str.substring(idx1, idx2);
    // Serial.println(substr);  // Print the substring for debugging
    steps[i++] = substr.toInt();
    idx1 = idx2 + 1;
    idx2 = str.indexOf('#', idx1);
  }
  
  steps[i] = str.substring(idx1).toInt(); // for the last element
  
  return steps;
}

int * getDirections(int * steps) {
  static int directions[9];
  for(int i = 0; i < 9; i++) {
    directions[i] = steps[i] > 0 ? 1 : 0;
  }
  return directions;
}


void execute() {

    command = buffer.getcmd(0);
    auto [function, contents] = buffer.parse_cmd(command);

    if (command == "CMD") { 
        Serial.println("CMD recieved");
    }

    if (command == "CAL") { 
        Serial.println("CAL recieved");
        ctrl.calibrate();
    }

    if (command == "LIM") { 
        Serial.println("LIM recieved");
        ctrl.switch_display();
    }

    if (function == "MJ") { 
        Serial.println("MJ recieved");
        int *steps = {parseString(contents)};
        int *dirs = {getDirections(steps)};
        for (int i=0; i<9; i++) { if (!dirs[i]) { steps[i] = 0-steps[i]; } }
        ctrl.drive_joints(steps,dirs);
    }




} // execute


void setup() {

    Serial.begin(9600);

    for (int i=0; i<DOF; i++) { // cant be MAXDOF cuz only 6 steppins
        pinMode(steppins[i], OUTPUT);
        pinMode(dirpins[i], OUTPUT);
        pinMode(switches[i], INPUT);

        digitalWrite(steppins[i], HIGH);
    }

    // TODO what are these?
    pinMode(Input39, INPUT_PULLUP);
    pinMode(Output40, OUTPUT);
    pinMode(Output41, OUTPUT);

    //reset move command flag
    moveSequence = "";
    flag = "";
    rndTrue = false;
    use_spline  = false;
    end_spline = false;

} // setup

int loopidx=0;
void loop() {

      Serial.println("loop " + String(loopidx));
      loopidx++;
      delay(500);

      if (!end_spline) { 
          buffer.process_serial(); 
      } // read another spline command

      //dont start unless at least one command has been read in
      if (!buffer.isEmpty() && buffer.getcmd(0).length()) {

        kinematic_error = 0;
        execute();

        buffer.setcmd(0,"");
        buffer.shift_cmd("");

      }

} // loop
