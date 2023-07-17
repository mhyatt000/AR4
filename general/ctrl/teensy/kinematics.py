import math

import numpy as np

""" correct xyzuvw for joints = 0
323.08, 2.01597e-06, 474.77, 3.93402e-06, 90, 1.59872e-13, 
"""


"""
LINKS:
- Affine Transformation (Wikipedia): https://en.wikipedia.org/wiki/Affine_transformation
- 3D Transformation (Wikipedia): https://en.wikipedia.org/wiki/3D_transformation
- Rotation Matrix (Wikipedia): https://en.wikipedia.org/wiki/Rotation_matrix
- Inverse of a Matrix (Wikipedia): https://en.wikipedia.org/wiki/Invertible_matrix
- Homogeneous Coordinates (Wikipedia): https://en.wikipedia.org/wiki/Homogeneous_coordinates
- OpenGL Tutorial: Understanding the View Matrix: https://www.3dgep.com/understanding-the-view-matrix/
- Interactive 3D Graphics Course by Autodesk (free on Udacity): https://www.udacity.com/course/interactive-3d-graphics--cs291

KEYWORDS:
- Affine transformation
- 3D transformation
- Rotation matrix
- Inverse matrix
- Homogeneous coordinates
- View matrix
- Model matrix
- World space
- Local space
- Computer Graphics
- OpenGL
- DirectX
"""


PI = np.pi
RAD = PI / 180
DOF = 6


class DHM:
    """Denavit-Hartenberg Method
    defines the kinematic structure and geometry of the robot arm
    essential for forward and inverse kinematics calculations

    - ALPHA:
        twist angle between two consecutive coordinate frames along the z-axis
    - A:
        link length between two consecutive coordinate frames along the x-axis
    - THETA:
        rotation angle around the z-axis between two consecutive coordinate frames
    - D:
        offset or distance between two consecutive coordinate frames along the z-axis

    """

    params = np.array(
        [
            [0, -90, 0, 0, 0, 180],
            [0, -90, 0, -90, 90, -90],
            [169.77, 0, 0, 222.63, 0, 36.25],
            [0, 64.2, 305, 0, 0, 0],
        ]
    )

    THETA = params[0] * RAD
    ALPHA = params[1] * RAD
    D = params[2]
    A = params[3]

    def __init__(self):
        pass


def matx_inv(x):
    """docstring"""

    y = np.zeros((4, 4))
    y[:3, :3] = np.transpose(x[:3, :3])
    y[:, 3] = [0, 0, 0, 1]
    y[3, :3] = -np.dot(x[:3, :3], x[:3, 3])

    return y


def matx_multiply(A, B):

    out = np.zeros((4, 4))
    out[:3, :3] = np.matmul(A[:3, :3], B[:3, :3])

    out[:, 3] = [0, 0, 0, 1]
    out[3, :3] = np.dot(A[3, :3], B[:3, 3]) + A[3, :3]

    return out



class KinematicSolver:
    """docstring"""

    def __init__(self):

        self.cart = np.zeros(6)  # cartesian coordinates of end effector

    def reset(self):
        """docstring"""

        self.baseframe = np.eye(4)
        self.toolframe = np.eye(4)

        self.kin_base = np.zeros(6)
        self.senses = np.zeros(9)

    def prepare(self):
        """originally robot_set_ar3()"""
        """ why would you need to reset every time? """

        self.reset()

    def forward(self, joints):
        """docstring"""

        self.prepare()

        self.cartesian = np.zeros(6)
        # self.angles = np.array([J.angle for J in JointCTRL])

        inv_baseframe = matx_inv(self.baseframe)

        self.pose = self.xyzwpr2pose(self.kin_base)

        print(self.pose)
        # quit()

        for i in range(DOF):

            dhm = DHM.params[:, i]
            print('dhm',dhm)
            theta, alpha, d, a = dhm

            radians = joints[i] * RAD
            print('rad',radians)
            _pose = self.DHM2pose(theta, alpha, d + radians, a)
            print(_pose)
            print(self.pose)
            self.pose = matx_multiply(self.pose, _pose)
            print(" ".join([f'{round(x,2):5.2f}' for x in self.pose2xyzuvw(self.pose).tolist()]))
            print()

        tool_pose = np.zeros(6)  # the offset of the tool from J6 end effector
        tool_pose = self.xyzwpr2pose(tool_pose)
        self.pose = matx_multiply(self.pose, tool_pose)

        self.pose = matx_multiply(inv_baseframe, self.pose)
        self.pose = matx_multiply(self.pose, self.toolframe)

        self.cart = self.pose2xyzuvw(self.pose)

        self.cart[3:] /= RAD
        print('xyzuvw',self.cart)

    def DHM2pose(self, rx, tx, rz, tz):
        """
        following the modified DH rules for the inputs return 4x4 matrix pose
        source : https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters
        """

        crx = math.cos(rx)
        srx = math.sin(rx)
        crz = math.cos(rz)
        srz = math.sin(rz)

        pose = np.array(
            [
                [crz, crx * srz, srx * srz, 0.0],
                [-srz, crx * crz, crz * srx, 0.0],
                [0.0, -srx, crx, 0.0],
                [tx, -tz * srx, tz * crx, 1.0],
            ]
        )

        return pose

    def xyzwpr2pose(self, xyzwpr):
        """tranform a coordinate system xyzwpr into a 4x4 matrix"""
        print(xyzwpr)
        pose = [0 for _ in range(16)]  # TODO use self.pose ?

        srx = math.sin(xyzwpr[3])
        crx = math.cos(xyzwpr[3])
        sry = math.sin(xyzwpr[4])
        cry = math.cos(xyzwpr[4])
        srz = math.sin(xyzwpr[5])
        crz = math.cos(xyzwpr[5])

        pose[0] = cry * crz
        pose[4] = -cry * srz
        pose[8] = sry
        pose[12] = xyzwpr[0]

        H_tmp = crz * srx
        pose[1] = crx * srz + H_tmp * sry
        crz *= crx

        pose[5] = crz - srx * sry * srz
        pose[9] = -cry * srx
        pose[13] = xyzwpr[1]
        pose[2] = srx * srz - crz * sry
        pose[6] = H_tmp + crx * sry * srz
        pose[10] = crx * cry
        pose[14] = xyzwpr[2]
        pose[3] = 0.0
        pose[7] = 0.0
        pose[11] = 0.0
        pose[15] = 1.0

        return np.array(pose).reshape(4, 4)

    def pose2xyzuvw(self, _pose):
        """docstring"""

        pose = _pose.flatten()
        vector = [0] * 3
        out = [0] * 6

        out[0:2] = pose[12:14]

        sin_angle = (pose[0] + pose[5] + pose[10] - 1.0) * 0.5
        sin_angle = np.clip(sin_angle, -1, 1)

        angle = math.acos(sin_angle)
        if angle < 1.0e-6:
            vector[0:2] = [0, 0, 0]

        else:
            sin_angle = math.sin(angle)

            # IMPOTANT : cosinus of 90 give a really small number instead of 0,
            # the result is forced back to what it should
            if abs(sin_angle) < 1.0e-6:
                sin_angle = pose[0]
                iidx = 0

                if pose[0] < pose[5]:
                    sin_angle = pose[5]
                    iidx = 1
                if sin_angle < pose[10]:
                    sin_angle = pose[10]
                    iidx = 2

                b_I = [0 for i in range(9)]
                b_I[0], b_I[4], b_I[8] = [1, 1, 1]

                sin_angle = 2.0 * (1.0 + sin_angle)
                sin_angle = 0.0 if sin_angle <= 0.0 else sqrt(sin_angle)

                vector_tmp = iidx * 4
                vector[0] = (pose[vector_tmp] + b_I[3 * iidx]) / sin_angle
                vector[1] = (pose[1 + vector_tmp] + b_I[1 + 3 * iidx]) / sin_angle
                vector[2] = (pose[2 + vector_tmp] + b_I[2 + 3 * iidx]) / sin_angle
                angle = M_PI
            else:
                sin_angle = 1.0 / (2.0 * sin_angle)
                vector[0] = (pose[6] - pose[9]) * sin_angle
                vector[1] = (pose[8] - pose[2]) * sin_angle
                vector[2] = (pose[1] - pose[4]) * sin_angle

        sin_angle = angle * (1 / RAD)
        out[3] = vector[0] * sin_angle * RAD
        out[4] = vector[1] * sin_angle * RAD
        out[5] = vector[2] * sin_angle * RAD

        return np.array(out)

    def solve_inv():
        """docstring"""

    def joint_update():
        """TODO"""

        global JangleIn, JangleOut
        for i in range(ROBOT_nDOFs):
            JangleIn[i] = JangleOut[i]

    def joint_estimate():
        """TODO"""

        global joints_estimate, JangleIn
        for i in range(ROBOT_nDOFs):
            joints_estimate[i] = JangleIn[i]


def main():
    """docstring"""

    KIN = KinematicSolver()

    joints = [0, 20, 200, 0, 0, 0]
    KIN.forward(joints)


if __name__ == "__main__":
    main()
