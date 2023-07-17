import numpy as np

def compute_dh_transform(theta, alpha, d, a):
    """
    Compute the transformation matrix using the Denavit-Hartenberg parameters.
    """
    T = np.array(
        [
            [
                np.cos(theta),
                -np.sin(theta) * np.cos(alpha),
                np.sin(theta) * np.sin(alpha),
                a * np.cos(theta),
            ],
            [
                np.sin(theta),
                np.cos(theta) * np.cos(alpha),
                -np.cos(theta) * np.sin(alpha),
                a * np.sin(theta),
            ],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1],
        ]
    )
    return T


def forward_kinematics(params):
    """
    Compute the forward kinematics of a 6 axis robot arm using the DH method.
    """
    RAD = np.pi / 180  # Convert degrees to radians.

    THETA = params[0] * RAD
    ALPHA = params[1] * RAD
    D = params[2]
    A = params[3]

    T = np.eye(4)  # Identity matrix.
    for i in range(6):
        T_i = compute_dh_transform(THETA[i], ALPHA[i], D[i], A[i])
        T = T @ T_i  # Multiply the matrices together.

    return T


def test_forward_kinematics():
    params = np.array(
        [
            [0, -90, 0, 0, 0, 180],
            [0, -90, 0, -90, 90, -90],
            [169.77, 0, 0, 222.63, 0, 36.25],
            [0, 64.2, 305, 0, 0, 0],
        ]
    )
    T = forward_kinematics(params)
    print(T)

    # Extract the position and orientation from the transformation matrix.
    position = T[:3, 3]
    orientation = (
        np.array(
            [
                np.arctan2(T[2, 1], T[2, 2]),
                np.arctan2(-T[2, 0], np.sqrt(T[0, 0] ** 2 + T[1, 0] ** 2)),
                np.arctan2(T[1, 0], T[0, 0]),
            ]
        )
        * 180
        / np.pi
    )
    # Compare with the expected values.
    np.testing.assert_almost_equal(position, [323.08, 2.01597e-06, 474.77], decimal=5)
    np.testing.assert_almost_equal(orientation, [3.93402e-06, 90, 1.59872e-13], decimal=5)

test_forward_kinematics()
