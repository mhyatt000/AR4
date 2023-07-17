#include "buffer.h"
#include <tuple>
#include <Arduino.h>
#include <utility>

Buffer::Buffer() {
    for(int i = 0; i < 3; i++) {
        cmds.push_back("");
    }
}

String Buffer::getcmd(int idx) {
    if (idx >= 0 && idx < cmds.size()) {
        auto it = cmds.begin();
        std::advance(it, idx);
        return *it;
    } else {
        // Handle invalid index (out of range)
        return "INVALID";
    }
}

std::tuple<String, String> Buffer::parse_cmd(const String& cmd) {
    String function = cmd.substring(0, 2);
    String contents = cmd.substring(2);

    return std::make_tuple(function, contents);
}


void Buffer::setcmd(int idx, const String& value) {
    if (idx >= 0 && idx < cmds.size()) {
        auto it = cmds.begin();
        std::advance(it, idx);
        *it = value;
    } else {
        // Handle invalid index (out of range)
        std::cout << "Invalid index" << std::endl;
    }
}


void Buffer::shift_cmd(const String& command) {
    if(cmds.size() >= 3 && !getcmd(0).length()) { cmds.pop_front();  }
    cmds.push_back(command);  // Add the new command.
}

void Buffer::display() {
    for(const auto& cmd : cmds) { Serial.println("display: " + cmd); }
}

bool Buffer::isEmpty() { 
    return (!getcmd(0).length() && !getcmd(1).length() && !getcmd(2).length());
}

String Buffer::read_serial() {
    String data = "";
    while (Serial.available() > 0) {
        char received = Serial.read();
        data += received ;

        if (received == '\n') {
            return data.trim();
        } 
    }
    return data.trim();
} 

void Buffer::process_serial() {

    if (Serial.available() > 0 && !getcmd(2).length()) {
         String command = read_serial();
        setcmd(2,command);

        auto [function, contents] = parse_cmd(command);
        
        if (function == "SS") { // stop spline?
            use_spline = false;
            splineEndReceived = true;
        }
    }
    
    if (use_spline) {
        if (!moveSequence.length()) { moveSequence = "firstMoveActive"; }
        if (Alarm == "0") { pos.send_spline(); } 
        else {
            Serial.println(Alarm);
            Alarm = "0";
        }
    }

    shift_cmd("");

    if (function == "ML" && moveSequence == "firstMoveActive" && !getcmd(1).length() && !getcmd(0).length() && use_spline) {
        processSecondMove();
    }
}

void Buffer::processSecondMove() {
    moveSequence = "secondMoveProcessed";

    if (Serial.available() > 0 && !getcmd(1).length()) {
        String command = read_serial();
        setcmd(1,command);

        auto [function, contents] = parse_cmd(command);

        if (function == "ML") {
            delay(5);
            if (Alarm == "0") { pos.send_spline(); } 
            else {
                Serial.println(Alarm);
                Alarm = "0";
            }
        }

    }

} 
