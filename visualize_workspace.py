import numpy as np
import matplotlib.pyplot as plt
from RRRManipulator import RRRManipulator as RRR, RRRManipulator


def plot_workspace(rrr: RRRManipulator, num_points=50):
    """
    Plot the workspace of the RRR robotic arm.
    """
    # Generate a range of joint angles
    theta1_range = np.linspace(0, 360, num_points)
    theta2_range = np.linspace(-30, 270, num_points)
    theta3_range = np.linspace(-30, 180, num_points)

    # Initialize arrays for the end effector positions
    x_points = []
    y_points = []
    z_points = []

    # Calculate the position of the end effector for each combination of joint angles
    for theta1 in theta1_range:
        for theta2 in theta2_range:
            for theta3 in theta3_range:
                point = rrr.forward_kinematics(theta1, theta2, theta3)
                x_points.append(point['x'])
                y_points.append(point['y'])
                z_points.append(point['z'])

    # Plotting the workspace
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_points, y_points, z_points, c='b', marker='o')
    ax.set_xlabel('oś x')
    ax.set_ylabel('oś y')
    ax.set_zlabel('oś z')
    ax.set_title('Przestrzeń robocza manipulatora RRR')
    plt.show()


rrr = RRR(1, 1, 1)
# Visualize the workspace
plot_workspace(rrr)
