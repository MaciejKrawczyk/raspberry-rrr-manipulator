import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def spherical_rrr_workspace(arm_lengths, joint_ranges, resolution=10):
    """
    Calculate the workspace of a spherical RRR manipulator.

    Parameters:
    arm_lengths (list): Lengths of the arms of the manipulator.
    joint_ranges (list): Range of motion for each joint in degrees (min, max).
    resolution (int): Number of points to calculate for each joint range.

    Returns:
    np.array: Array of points in the workspace.
    """
    l1, l2, l3 = arm_lengths
    points = []

    # Convert joint ranges from degrees to radians
    joint_ranges_rad = [(np.deg2rad(j[0]), np.deg2rad(j[1])) for j in joint_ranges]

    # Generate points in the workspace
    for theta1 in np.linspace(*joint_ranges_rad[0], resolution):
        for theta2 in np.linspace(*joint_ranges_rad[1], resolution):
            for theta3 in np.linspace(*joint_ranges_rad[2], resolution):
                # Calculate position of the end effector
                x = (l1 + l2 * np.cos(theta2) + l3 * np.cos(theta2 + theta3)) * np.sin(theta1)
                y = (l1 + l2 * np.cos(theta2) + l3 * np.cos(theta2 + theta3)) * np.cos(theta1)
                z = l2 * np.sin(theta2) + l3 * np.sin(theta2 + theta3)
                points.append([x, y, z])

    return np.array(points)


# Arm lengths and joint ranges for the manipulator
arm_lengths = [1, 1, 1]  # Example lengths for each arm
joint_ranges = [(0, 360), (-45, 90), (-110, 0)]  # Example ranges for each joint

# Calculate workspace
workspace_points = spherical_rrr_workspace(arm_lengths, joint_ranges, resolution=20)

# Plotting the workspace
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(workspace_points[:, 0], workspace_points[:, 1], workspace_points[:, 2], c='b', marker='o')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('Przestrzeń robocza manipulatora RRR')
plt.show()
