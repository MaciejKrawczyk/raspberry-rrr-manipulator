from matplotlib import pyplot as plt

from tests.new_new_with_oop.Motor import Motor, Encoder
from tests.new_new_with_oop.Robot import Robot

encoder_alfa = Encoder(1)
motor_alfa = Motor(2, encoder_alfa)

encoder_beta = Encoder(3)
motor_beta = Motor(4, encoder_beta)

encoder_gamma = Encoder(5)
motor_gamma = Motor(6, encoder_gamma)

robot = Robot(motor_alfa, motor_beta, motor_gamma, 1, 1, 1)

parameter_set_from = {'x': -0.5, 'y': 0, 'z': 1}
parameter_set_to = {'x': 0.5, 'y': 0, 'z': 0.2}
#
# trajectory = robot.move(parameter_set_from, parameter_set_to)
#
# robot.plot_trajectory(trajectory)
#
# # Create the trajectory
# trajectory = robot.move(parameter_set_from, parameter_set_to)

trajectory_angles = robot.move(parameter_set_from, parameter_set_to)

robot.plot_trajectory(trajectory_angles)

# Convert joint angles to x, y, z coordinates
trajectory_xyz = []
for angles in trajectory_angles:
    alfa, beta, gamma = angles['theta1'], angles['theta2'], angles['theta3']
    coordinates = robot.forward_kinematics(alfa, beta, gamma)
    print(coordinates)
    trajectory_xyz.append(coordinates)

# Extract x, y, z coordinates from trajectory
x_values = [point['x'] for point in trajectory_xyz]
y_values = [point['y'] for point in trajectory_xyz]
z_values = [point['z'] for point in trajectory_xyz]

# Creating the 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plotting the trajectory
ax.plot(x_values, y_values, z_values, label='Trajectory', color='b')

# Setting labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_title('3D Trajectory of Robot Movement')

# Show plot
plt.show()
