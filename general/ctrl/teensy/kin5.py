import math
import matplotlib.pyplot as plt
from functools import reduce

import numpy as np


def extract_position_and_rotation(T):
    # Extract the position from the 4th column of the transformation matrix
    position = T[:3, 3]

    # Extract 3x3 rotation matrix
    R = T[:3, :3]

    # Calculate Euler angles (rotation around x, y and z, respectively) from rotation matrix
    rotation = np.zeros(3)
    rotation[0] = np.arctan2(R[2, 1], R[2, 2])  # rotation around x-axis (U)
    rotation[1] = np.arctan2(
        -R[2, 0], np.sqrt((R[2, 1] ** 2) + (R[2, 2] ** 2))
    )  # rotation around y-axis (V)
    rotation[2] = np.arctan2(R[1, 0], R[0, 0])  # rotation around z-axis (W)

    return position, rotation


def dh_transform_matrix(theta, d, r, alpha):
    """
    Compute a Denavit-Hartenberg transformation matrix

    Parameters:
    theta : float : Joint angle (rotation around z-axis)
    d     : float : Joint offset (translation along z-axis)
    r     : float : Link length (translation along x-axis)
    alpha : float : Link twist (rotation around x-axis)

    Returns:
    4x4 np.array : The resulting transformation matrix
    """

    # Rotation around z-axis by theta
    R_z = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0, 0],
            [np.sin(theta), np.cos(theta), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    # Translation along z-axis by d
    T_z = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, d], [0, 0, 0, 1]])

    # Translation along x-axis by r
    T_x = np.array([[1, 0, 0, r], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    # Rotation around x-axis by alpha
    R_x = np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(alpha), -np.sin(alpha), 0],
            [0, np.sin(alpha), np.cos(alpha), 0],
            [0, 0, 0, 1],
        ]
    )

    # Combine transformations
    return np.dot(np.dot(np.dot(R_z, T_z), T_x), R_x)

class DH:
    params = np.array(
        [
            [0, 0, 169.77, 0],
            [-90, -90, 0, 64.2],
            [0, 0, 0, 305],
            [0, -90, 222.63, 0],
            [0, 90, 0, 0],
            [180, -90, 36.25, 0],
        ]
    )

    def __init__(self):
        self.alpha = self.params[:, 1] * np.pi / 180
        self.theta = self.params[:, 0] * np.pi / 180
        self.r = self.params[:, 3]
        self.d = self.params[:, 2]


def mk_sphere(ax):
    """docstring"""

    center = (0, 0, 0)

    # Radius of the sphere
    r = 480

    # Create a meshgrid of points in the sphere's volume
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 50)
    x = center[0] + r * np.outer(np.cos(u), np.sin(v))
    y = center[1] + r * np.outer(np.sin(u), np.sin(v))
    z = center[2] + r * np.outer(np.ones(np.size(u)), np.cos(v))

    # Plot the surface of the sphere
    ax.plot_surface(x, y, z, color='grey', alpha=0.3)  # Translucent grey
    ax.plot([-r,r], [0,0], [0,0], color='grey')  
    ax.plot([0,0], [-r,r], [0,0], color='grey')  
    ax.plot([0,0], [0,0], [-r,r], color='grey')  

    # Set plot limits
    ax.set_xlim([-r, r])
    ax.set_ylim([-r, r])
    ax.set_zlim([-r, r])


def plot3d(X,Y,Z, name='3D Plot'):
    """docstring"""

    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    mk_sphere(ax)

    # Plot the data points
    ax.plot(X, Y, Z)
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

    dh = DH()

    print('init')
    print(extract_position_and_rotation(np.eye(4)))

    T = np.eye(4)
    Ts = []
    X,Y,Z = [0],[0],[0]
    for i in range(len(dh.alpha)):
        alpha, theta, r, d = dh.alpha[i], dh.theta[i], dh.r[i], dh.d[i]

        theta += (170* np.pi / 180) if i == 1 else 0

        _T = dh_transform_matrix(theta, d, r, alpha)
        T = np.matmul(T,_T)
        # Ts.append(_T)

        (x,y,z),(u,v,w) = extract_position_and_rotation(T)
        X.append(x)
        Y.append(y)
        Z.append(z)
        print(int(x),int(y),int(z))

    # T = reduce(np.matmul, Ts, np.eye(4))
    # print(T)

    plot3d(X,Y,Z)
    # plot3d([0,x],[0,y],[0,z])
    # plot3d([0,X[0],x],[0,Y[0],y],[0,Z[0],z])

if __name__ == '__main__': 
    main()
