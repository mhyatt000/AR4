# MATRIX OPERATION

# This allow to return a array as an argument instead of using global pointer

import numpy as np


def matrix_multiply(inA, inB):
    # Ensure input are numpy arrays
    inA = np.array(inA).reshape(4, 4)
    inB = np.array(inB).reshape(4, 4)
    # Perform matrix multiplication
    out = inA @ inB
    # Set the 4th column (zero-indexed) to be [0, 0, 0, 1]
    out[:, 3] = [0, 0, 0, 1]
    # Flatten the output matrix and return it as a list
    return out.flatten().tolist()


def matrix_inv(in_mat):
    # Ensure input is a numpy array
    in_mat = np.array(in_mat).reshape(4, 4)

    # Create output matrix
    out = np.zeros((4, 4))

    # Swap rows and columns
    out[:3, :3] = in_mat[:3, :3].T

    # Apply the transformations for the last row
    out[:3, 3] = -out[:3, :3] @ in_mat[:3, 3]
    out[3, 3] = 1

    # Flatten the output matrix and return it as a list
    return out.flatten().tolist()


def matrix_copy(in_mat):
    return np.array(in_mat).flatten().tolist()


def matrix_eye():
    return np.eye(4).flatten().tolist()


def matrix_multiply_cumul(inout, inB):
    # Ensure input is a numpy array
    inout = np.array(inout).reshape(4, 4)
    inB = np.array(inB).reshape(4, 4)

    # Perform multiplication
    out = inout @ inB

    # Flatten the output matrix and return it as a list
    return out.flatten().tolist()


M_PI = 3.14159265358979323846

DHM = {
    "Alpha": 0,
    "A": 1,
    "Theta": 2,
    "D": 3,
}
# Define the size of the table, replace with your desired size
Table_Size = 4  # Replace with your table size

# Custom robot base (user frame)
Robot_BaseFrame = np.eye(4).flatten().tolist()

# Custom robot tool (tool frame, end of arm tool or TCP)
Robot_ToolFrame = np.eye(4).flatten().tolist()

# Robot parameters
# All robot data is held in a large array
Robot_Data = np.zeros(Table_Size * 11)

# These global variable are pointers, allowing to put the variables inside the Robot_Data
# DHM table
Robot_Kin_DHM_Table = Robot_Data[0 * Table_Size : 1 * Table_Size]

# xyzwpr of the base
Robot_Kin_Base = Robot_Data[6 * Table_Size : 7 * Table_Size]

# xyzwpr of the tool
Robot_Kin_Tool = Robot_Data[7 * Table_Size : 8 * Table_Size]

# Robot lower limits
Robot_JointLimits_Upper = Robot_Data[8 * Table_Size : 9 * Table_Size]

# Robot upper limits
Robot_JointLimits_Lower = Robot_Data[9 * Table_Size : 10 * Table_Size]

# Robot axis senses
Robot_Senses = Robot_Data[10 * Table_Size : 11 * Table_Size]

# A value mappings
Robot_Kin_DHM_L1 = Robot_Kin_DHM_Table[0 * Table_Size : 1 * Table_Size]
Robot_Kin_DHM_L2 = Robot_Kin_DHM_Table[1 * Table_Size : 2 * Table_Size]
Robot_Kin_DHM_L3 = Robot_Kin_DHM_Table[2 * Table_Size : 3 * Table_Size]
Robot_Kin_DHM_L4 = Robot_Kin_DHM_Table[3 * Table_Size : 4 * Table_Size]
Robot_Kin_DHM_L5 = Robot_Kin_DHM_Table[4 * Table_Size : 5 * Table_Size]
Robot_Kin_DHM_L6 = Robot_Kin_DHM_Table[5 * Table_Size : 6 * Table_Size]


def robot_set_AR3():
    global Robot_Data

    # I'm assuming that 'robot_data_reset' function resets the Robot_Data to zeros.
    Robot_Data = np.zeros(Table_Size * 11)

    # I'm assuming that 'DHparams' is a 2D array with 6 rows and 4 columns.
    # Each row corresponds to the parameters of a robot link.
    # Replace it with the actual DHparams data.
    DHparams = np.zeros((6, 4))  # Replace with your actual DHparams data

    # Replace these with your actual limits data
    limits = None

    Robot_Kin = [
        Robot_Kin_DHM_L1,
        Robot_Kin_DHM_L2,
        Robot_Kin_DHM_L3,
        Robot_Kin_DHM_L4,
        Robot_Kin_DHM_L5,
        Robot_Kin_DHM_L6,
    ],

    for i, (DHparams_row, Robot_Kin_DHM_L) in enumerate( zip( DHparams,Robot_Kin)):

        # Alpha parameters
        Robot_Kin_DHM_L[DHM_Alpha] = DHparams_row[1] * M_PI / 180
        # Theta parameters
        Robot_Kin_DHM_L[DHM_Theta] = DHparams_row[0] * M_PI / 180
        # A parameters
        Robot_Kin_DHM_L[DHM_A] = DHparams_row[3]
        # D parameters
        Robot_Kin_DHM_L[DHM_D] = DHparams_row[2]

        # Joint Limits
        Robot_JointLimits_Lower[i] = globals()[f"J{i+1}axisLimNeg"]
        Robot_JointLimits_Upper[i] = globals()[f"J{i+1}axisLimPos"]


def robot_data_reset():
    """docstring"""
    Matrix_eye(Robot_BaseFrame)
    Matrix_eye(Robot_ToolFrame)

    # Reset internal base frame and tool frames
    for i in range(6):
        Robot_Kin_Base[i] = 0.0
    # Reset joint senses and joint limits
    for i in range(ROBOT_nDOFs):
        Robot_Senses[i] = +1.0



def robot_joints_valid(joints ,limits_lower, limits_upper): 

    for joint, lower, upper in zip(joints,limits_lower,limits_upper):
        if joint < -lower or joint > upper:
            return False
    return True


def DHM_2_pose(rx, tx, rz, tz):
    crx = np.cos(rx)
    srx = np.sin(rx)
    crz = np.cos(rz)
    srz = np.sin(rz)

    pose = np.array([
        [crz, -srz, 0.0, tx],
        [crx * srz, crx * crz, -srx, -tz * srx],
        [srx * srz, crz * srx, crx, tz * crx],
        [0.0, 0.0, 0.0, 1.0]
    ])

    return pose


def xyzwpr_2_pose(xyzwpr):

    srx = np.sin(xyzwpr[3])
    crx = np.cos(xyzwpr[3])
    sry = np.sin(xyzwpr[4])
    cry = np.cos(xyzwpr[4])
    srz = np.sin(xyzwpr[5])
    crz = np.cos(xyzwpr[5])

    pose = np.zeros((4, 4))

    pose[0, 0] = cry * crz
    pose[0, 1] = -cry * srz
    pose[0, 2] = sry
    pose[0, 3] = xyzwpr[0]

    H_tmp = crz * srx

    pose[1, 0] = crx * srz + H_tmp * sry
    pose[1, 1] = crz * crx - srx * sry * srz
    pose[1, 2] = -cry * srx
    pose[1, 3] = xyzwpr[1]

    pose[2, 0] = srx * srz - crz * sry
    pose[2, 1] = H_tmp + crx * sry * srz
    pose[2, 2] = crx * cry
    pose[2, 3] = xyzwpr[2]

    pose[3, 3] = 1.0

    return pose


def pose_2_xyzuvw(pose):
    sin_angle = (((pose[0, 0] + pose[1, 1]) + pose[2, 2]) - 1.0) * 0.5
    sin_angle = np.clip(sin_angle, -1, 1)

    angle = np.arccos(sin_angle)
    if angle < 1.0E-6:
        vector = np.zeros(3)
    else:
        sin_angle = np.sin(angle)
        if np.abs(sin_angle) < 1.0E-6: 
            max_index = np.argmax([pose[0, 0], pose[1, 1], pose[2, 2]])
            b_I = np.eye(3)
            sin_angle = 2.0 * (1.0 + pose[max_index, max_index])
            sin_angle = np.sqrt(np.maximum(0, sin_angle))

            vector = (pose[max_index, :] + b_I[:, max_index]) / sin_angle
            angle = np.pi
        else:
            sin_angle = 1.0 / (2.0 * sin_angle)
            vector = np.array([
                (pose[1, 2] - pose[2, 1]) * sin_angle,
                (pose[2, 0] - pose[0, 2]) * sin_angle,
                (pose[0, 1] - pose[1, 0]) * sin_angle
            ])

    sin_angle = angle * 180.0 / np.pi
    return np.concatenate([pose[0:3, 3], vector * sin_angle * np.pi / 180.0])

def xyzuvw_2_pose(xyzuvw):
    s = np.sqrt(np.sum(xyzuvw[3:] ** 2))
    angle = s * 180.0 / np.pi
    pose = np.zeros((4, 4))

    if np.abs(angle) < 1.0E-6: 
        pose[:3, :3] = np.eye(3)
    else:
        axisunit = np.abs(xyzuvw[3:6])
        ex = np.max(axisunit)
        if ex < 1.0E-6: 
            pose[:3, :3] = np.eye(3)
        else:
            axisunit = xyzuvw[3:6] / s
            s = angle * np.pi / 180.0
            c = np.cos(s)
            s = np.sin(s)

            pose[0, 0] = axisunit[0] ** 2 + c * (1 - axisunit[0] ** 2)
            pose[1, 1] = axisunit[1] ** 2 + c * (1 - axisunit[1] ** 2)
            pose[2, 2] = axisunit[2] ** 2 + c * (1 - axisunit[2] ** 2)

            pose[0, 1] = axisunit[0] * axisunit[1] * (1 - c) - axisunit[2] * s
            pose[0, 2] = axisunit[0] * axisunit[2] * (1 - c) + axisunit[1] * s
            pose[1, 0] = axisunit[0] * axisunit[1] * (1 - c) + axisunit[2] * s
            pose[1, 2] = axisunit[1] * axisunit[2] * (1 -
