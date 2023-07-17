#ifndef Buffer_h
#define Buffer_h

#include <Arduino.h>
#include <list>
#include <iostream>
#include "positioner.h"


class Buffer {
public:
    Buffer();
    void shift_cmd(const String& command);
    void display();
    bool isEmpty();
    String read_serial();
    void process_serial();
    void processSecondMove();
    String getcmd(int idx);
    void setcmd(int idx, const String& value);
    Positioner pos; // maybe call posMGR
    std::tuple<String, String> parse_cmd(const String& cmd);

private:
    std::list<String> cmds;
    String moveSequence;
    String Alarm;
    String function;
    bool use_spline;
    bool splineEndReceived;
};

#endif
