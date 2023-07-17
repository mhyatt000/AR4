import numpy as np
import matplotlib.pyplot as plt

RAD = np.pi / 180


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


def get_transformation_matrix(theta, d, a, alpha):
    """
    Given the DH parameters, compute the transformation matrix.
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


def forward_kinematics(joints, params):
    """ Given a list of joint angles and DH parameters, compute the forward kinematics.  """

    T = np.eye(4)
    for i in range(len(joints)):
        Ti = get_transformation_matrix(THETA[i], D[i], A[i], ALPHA[i])
        T = np.dot(T, Ti)

    return T


def rotationMatrixToEulerAngles(R):
    """
    Calculates rotation angles from a rotation matrix. Assumes 'rx-ry-rz' order.

    This is also known as the intrinsic rotation or Tait-Bryan angles,
    where each rotation is performed with respect to the local coordinate frame.
    """

    # Ensure the matrix is in the right form
    assert isRotationMatrix(R)

    sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def isRotationMatrix(R):
    """Checks if a matrix is a valid rotation matrix"""
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


def joint2pose(joints):
    """docstring"""

    result = forward_kinematics(joints, params)
    # print(result)
    x, y, z = result[:-1, -1]

    # print(x, y, z)

    R = result[:3, :3]
    rx, ry, rz = rotationMatrixToEulerAngles(R)
    # print("End effector orientation:", rx, ry, rz)

    return x,y,z,rx,ry,rz

def plot3d(X,Y,Z, name='3D Plot'):
    """docstring"""

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

    # Plot the data points
    ax.scatter(X, Y, Z)

    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(name)

    # Show the plot
    plt.show()
    plt.close()  

def main():
    """docstring"""

    for idx in range(6):

        X,Y,Z = [],[],[]
        for i in range(10):
            joints = np.array([0, 0, 0, 0, 0, 0])  # replace with your joint angles
            # # joints = np.array([0,0,0])  # replace with your joint angles
            joints[idx] += i
            x,y,z,*_ = joint2pose(joints)

            X.append(x)
            Y.append(y)
            Z.append(z)

        plot3d(X,Y,Z, name=f'Joint {idx+1}')
            
    


if __name__ == '__main__': 
    main()
