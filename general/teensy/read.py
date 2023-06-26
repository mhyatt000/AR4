
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//READ DATA
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


void processSerial() {
  if (Serial.available() > 0 and cmdBuffer3 == "") {
    char recieved = Serial.read();
    recData += recieved;
    // Process message when new line character is recieved
    if (recieved == '\n') {
      //place data in last position
      cmdBuffer3 = recData;
      //determine if move command
      recData.trim();
      String procCMDtype = recData.substring(0, 2);
      if (procCMDtype == "SS") {
        splineTrue = false;
        splineEndReceived = true;
      }
      if (splineTrue == true) {
        if (moveSequence == "") {
          moveSequence = "firsMoveActive";
        }
        //close serial so next command can be read in
        if (Alarm == "0") {
          sendRobotPosSpline();
        }
        else {
          Serial.println(Alarm);
          Alarm = "0";
        }
      }

      recData = ""; // Clear recieved buffer

      shiftCMDarray();


      //if second position is empty and first move command read in process second move ahead of time
      if (procCMDtype == "ML" and moveSequence == "firsMoveActive" and cmdBuffer2 == "" and cmdBuffer1 != "" and splineTrue == true) {
        moveSequence = "secondMoveProcessed";
        while (cmdBuffer2 == "") {
          if (Serial.available() > 0) {
            char recieved = Serial.read();
            recData += recieved;
            if (recieved == '\n') {
              cmdBuffer2 = recData;
              recData.trim();
              procCMDtype = recData.substring(0, 2);
              if (procCMDtype == "ML") {
                //close serial so next command can be read in
                delay(5);
                if (Alarm == "0") {
                  sendRobotPosSpline();
                }
                else {
                  Serial.println(Alarm);
                  Alarm = "0";
                }
              }
              recData = ""; // Clear recieved buffer
            }
          }
        }
      }
    }
  }
}


void shiftCMDarray() {
  if (cmdBuffer1 == "") {
    //shift 2 to 1
    cmdBuffer1 = cmdBuffer2;
    cmdBuffer2 = "";
  }
  if (cmdBuffer2 == "") {
    //shift 3 to 2
    cmdBuffer2 = cmdBuffer3;
    cmdBuffer3 = "";
  }
  if (cmdBuffer1 == "") {
    //shift 2 to 1
    cmdBuffer1 = cmdBuffer2;
    cmdBuffer2 = "";
  }
}

