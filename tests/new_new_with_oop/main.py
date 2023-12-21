import matplotlib as mpl
from matplotlib import pyplot as plt

from tests.new_new_with_oop.Motor import Motor, Encoder
from tests.new_new_with_oop.Robot import Robot
from tests.new_new_with_oop.Vectors import Vector3Cartesian

# mpl.use('Qt5Agg')

encoder_alfa = Encoder(1)
motor_alfa = Motor(2, encoder_alfa)

encoder_beta = Encoder(3)
motor_beta = Motor(4, encoder_beta)

encoder_gamma = Encoder(5)
motor_gamma = Motor(6, encoder_gamma)

robot = Robot(motor_alfa, motor_beta, motor_gamma, 1, 1, 1)

# parameter_set_from = {'x': -0.5, 'y': 0, 'z': 1}
# parameter_set_to = {'x': 0.5, 'y': 0, 'z': 0.2}
# parameter_set_to2 = {'x': 1, "y": -1, "z": 1}

parameter_set_from = Vector3Cartesian(-0.5, 0, 1)
parameter_set_to = Vector3Cartesian(0.5, 0, 0.2)
parameter_set_to2 = Vector3Cartesian(1, -1, 1)

# inverse kinematics point 1 + 2

# angles = robot.inverse_kinematics3(parameter_set_from['x'], parameter_set_from['y'], parameter_set_from['z'], True)
# angles2 = robot.inverse_kinematics3(parameter_set_to['x'], parameter_set_to['y'], parameter_set_to['z'], True)
#
# position = robot.forward_kinematics(0, 0, 0)
#
# print(position)
# print(angles)
# print(angles2)

# trajectory + plot

trajectory_points = robot.move3(parameter_set_from, parameter_set_to)

trajectory_angles = []

for point in trajectory_points:
    # cartesian to angles
    trajectory_angles.append(robot.inverse_kinematics3(point))

robot.plot_trajectory(trajectory_angles)

# Convert joint angles to x, y, z coordinates
# trajectory_xyz = []
# for angles in trajectory_angles:
    # alfa, beta, gamma = angles['theta1'], angles['theta2'], angles['theta3']
    # coordinates = robot.forward_kinematics2(alfa, beta, gamma)
    # print(coordinates)
    # trajectory_xyz.append(coordinates)

# Extract x, y, z coordinates from trajectory
x_values = [point.x for point in trajectory_points]
y_values = [point.y for point in trajectory_points]
z_values = [point.z for point in trajectory_points]

print(x_values)
print(y_values)
print(z_values)

max_x = max(abs(val) for val in x_values)
max_y = max(abs(val) for val in y_values)

ax = plt.axes(projection='3d')

ax.set_xlim(-max_x, max_x)
ax.set_ylim(-max_y, max_y)

ax.scatter(x_values, y_values, z_values, c='b', marker='o')

# Setting labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('3D Trajectory of Robot Movement')

# Rotate the plot
elevation_angle = 90  # Adjust as needed
azimuthal_angle = 0  # Adjust as needed
ax.view_init(elev=elevation_angle, azim=azimuthal_angle)

# Show plot
plt.show()
