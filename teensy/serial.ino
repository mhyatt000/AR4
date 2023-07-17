

#include <algorithm> 
#include <cctype>


void shift_cmd(std::vector<std::string>& cmds) {
    if (cmds[0].empty()) {
        cmds[0] = cmds[1];
        cmds[1].clear();
    }
    if (cmds[1].empty()) {
        cmds[1] = cmds[2];
        cmds[2].clear();
    }
    if (cmds[0].empty()) {
        cmds[0] = cmds[1];
        cmds[1].clear();
    }
}



String read_serial() {
    String data = "";
    if (Serial.available() > 0) {
        char received = Serial.read();
        data += received;

        if (received == '\n') {
            return data;
        } 
    }
} // read_serial

void process_serial(std::vector<std::string>& cmds) {

    if (cmds[2].empty()) {
        String data = read_serial()
        cmds[2] = data;

        data.trim();
        String cmdtype = data.substring(0, 2);
        
        if (cmdtype == "SS") { // stop spline?
            use_spline = false;
            splineEndReceived = true;
        }
    }

    if (use_spline) {
        if (moveSequence.empty()) { moveSequence = "firstMoveActive"; }
        if (Alarm == "0") { sendRobotPosSpline(); } 
        else {
            Serial.println(Alarm);
            Alarm = "0";
        }
    }

    shift_cmd();

    if (cmdtype == "ML" && moveSequence == "firstMoveActive" && cmdBuffer2.empty() && !cmdBuffer1.empty() && use_spline) {
        processSecondMove();
    }

} // process command

void processSecondMove() {
    moveSequence = "secondMoveProcessed";

    if (cmdBuffer2.empty()) {
        String data = read_serial()
        cmdBuffer2 = data;

        String cmdtype = data.substring(0, 2);

        if (cmdtype == "ML") {
            delay(5);
            if (Alarm == "0") { sendRobotPosSpline(); } 
            else {
                Serial.println(Alarm);
                Alarm = "0";
            }
        }

    }

} // process second
