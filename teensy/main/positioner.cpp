#include <Arduino.h>
#include <utility>
#include "positioner.h"
#include <cstring>

Positioner::Positioner() {
    memset(angles, 0, sizeof(angles));
}

void Positioner::send_pos() {
    Serial.println("send_pos");
    // Implementation of send_pos function
}

void Positioner::send_spline() {

    // update_pos();

    // String sendPos = "A" + String(angles[0], 3) + "B" + String(angles[1], 3) + "C" + String(angles[2], 3) + "D" + String(angles[3], 3) + "E" + String(angles[4], 3) + "F" + String(angles[5], 3) + "G" + String(xyzuvw_Out[0], 3) + "H" + String(xyzuvw_Out[1], 3) + "I" + String(xyzuvw_Out[2], 3) + "J" + String(xyzuvw_Out[3], 3) + "K" + String(xyzuvw_Out[4], 3) + "L" + String(xyzuvw_Out[5], 3) + "M" + speedViolation + "N" + debug + "O" + flag + "P" + angles[6] + "Q" + angles[7] + "R" + angles[8];
    // delay(5);
    // Serial.println(sendPos);
    // speedViolation = "0";

}

void Positioner::update_pos() {

    // for (int i=0; i<MAXDOF; i++) {
        // angles[i] = (stepm[i] - stepzero[i]) / stepdeg[i];
    // } 

    // solve_fwd_kin();
}

void Positioner::correct_pos() {
    Serial.println("correct_pos");
    // Implementation of correct_pos function

    /* 
    robot_set_AR3();

    float target_xyzuvw[6];
    float joints[ROBOT_nDOFs];

    for (int i = 0; i < DOF; i++) {
        joints[i] = JangleIn[i];
    }


    forward_kinematics_robot_xyzuvw(joints, target_xyzuvw);

    xyzuvw_Out[0] = target_xyzuvw[0];
    xyzuvw_Out[1] = target_xyzuvw[1];
    xyzuvw_Out[2] = target_xyzuvw[2];
    xyzuvw_Out[3] = target_xyzuvw[3] / M_PI * 180;
    xyzuvw_Out[4] = target_xyzuvw[4] / M_PI * 180;
    xyzuvw_Out[5] = target_xyzuvw[5] / M_PI * 180;
    */
}

void solve_fwd_kin() {
    // forward kinematic

}
