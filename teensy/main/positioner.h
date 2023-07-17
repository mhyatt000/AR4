#ifndef POSITIONER_H
#define POSITIONER_H

#include "define.h"

class Positioner {
public:
    Positioner();
    void send_pos();
    void send_spline();
    void update_pos();
    void correct_pos();
    void solve_fwd_kin();

private:
    int angles[MAXDOF];
    int stepm[MAXDOF];
    int stepzero[MAXDOF];
    int stepdeg[MAXDOF];
    int speed_violation;
    int cartesians[DOF];
    String debug;
    String flag;
};

#endif // POSITIONER_H
