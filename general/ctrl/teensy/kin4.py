import numpy as np

# Constants
M_PI = 3.14159265358979323846
ROBOT_nDOFs = 6
DHparams = np.array(
    [
        [0, 0, 169.77, 0],
        [-90, -90, 0, 64.2],
        [0, 0, 0, 305],
        [0, -90, 222.63, 0],
        [0, 90, 0, 0],
        [180, -90, 36.25, 0],
    ],
    dtype=float,
)

# Conversion functions
def deg_to_rad(deg):
    return deg * M_PI / 180.0


def rad_to_deg(rad):
    return rad * 180.0 / M_PI


def dh_to_pose(dhm):
    rx, tx, rz, tz = dhm
    crx, srx, crz, srz = np.cos(rx), np.sin(rx), np.cos(rz), np.sin(rz)
    return np.array(
        [
            [crz, -crx * srz, srx * srz, tx],
            [srz, crx * crz, -srx * crz, -tz * srx],
            [0, srx, crx, tz * crx],
            [0, 0, 0, 1],
        ]
    )


def xyzwpr_to_pose(xyzwpr):
    x, y, z, w, p, r = xyzwpr
    sw, sp, sr = np.sin([w, p, r])
    cw, cp, cr = np.cos([w, p, r])
    return np.array(
        [
            [cp * cr, cp * sr, -sp, x],
            [sw * sp * cr - cw * sr, sw * sp * sr + cw * cr, sw * cp, y],
            [cw * sp * cr + sw * sr, cw * sp * sr - sw * cr, cw * cp, z],
            [0, 0, 0, 1],
        ]
    )


def forward_kinematics(joints):
    dhm_table = np.zeros((ROBOT_nDOFs, 4))
    dhm_table[:, 0] = deg_to_rad(DHparams[:, 1])
    dhm_table[:, 1] = DHparams[:, 3]
    dhm_table[:, 2] = deg_to_rad(DHparams[:, 0] + joints)
    dhm_table[:, 3] = DHparams[:, 2]

    pose = np.eye(4)
    for dhm in dhm_table:
        hi = dh_to_pose(dhm)
        pose = pose @ hi  # Matrix multiplication in Python

    return pose


joints = np.zeros(6)
pose = forward_kinematics(joints)
print(pose)


