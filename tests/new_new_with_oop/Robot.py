import math

import numpy as np
from sympy import Symbol, lambdify

from tests.new_new_with_oop.Motor import Motor, MotorEncoderCombo
from tests.new_new_with_oop.Vectors import Vector3Cartesian, Vector3Configuration

from utils import rad_to_degrees, degrees_to_rad

import matplotlib.pyplot as plt

THETA1_LIMITS = (degrees_to_rad(0), degrees_to_rad(360))
THETA2_LIMITS = (degrees_to_rad(-45), degrees_to_rad(90))
THETA3_LIMITS = (degrees_to_rad(-110), degrees_to_rad(0))


class Robot:
    def __init__(self, motor_theta1: MotorEncoderCombo, motor_theta2: MotorEncoderCombo,
                 motor_theta3: MotorEncoderCombo, l1: float, l2: float, l3: float):
        self.motor_theta1 = motor_theta1
        self.motor_theta2 = motor_theta2
        self.motor_theta3 = motor_theta3
        self._x = 0
        self._y = 0
        self._z = 0
        self.speed = 0
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def get_theta1(self):
        return self.motor_theta1.get_angle()

    def get_theta2(self):
        return self.motor_theta2.get_angle()

    def get_theta3(self):
        return self.motor_theta3.get_angle()

    def forward_kinematics(self, theta1: float, theta2: float, theta3: float):
        """ wg mojej implementacji """
        a3 = self.l3
        a2 = self.l2
        h1 = self.l1

        c23 = math.cos(theta2 + theta3)
        s23 = math.sin(theta2 + theta3)
        c2 = math.cos(theta2)
        s2 = math.sin(theta2)
        c1 = math.cos(theta1)
        s1 = math.sin(theta1)

        x = round(c1 * (a3 * c23 + a2 * c2), 2)
        y = round(s1 * (a3 * c23 + a2 * c2), 2)
        z = round((a3 * s23 + a2 * s2 + h1), 2)

        point = Vector3Cartesian(x, y, z)
        return point

    def _check_workspace(self, angles: Vector3Configuration):
        if not (THETA1_LIMITS[0] <= angles.theta1 <= THETA1_LIMITS[1]):
            raise ValueError(f"Alfa angle {angles.theta1} is out of range {THETA2_LIMITS}")

        if not (THETA2_LIMITS[0] <= angles.theta2 <= THETA2_LIMITS[1]):
            raise ValueError(f"Beta angle {angles.theta2} is out of range {THETA2_LIMITS}")

        if not (THETA3_LIMITS[0] <= angles.theta3 <= THETA3_LIMITS[1]):
            raise ValueError(f"Gamma angle {angles.theta3} is out of range {THETA3_LIMITS}")

        return True

    def check_workspace_angles(self, angles: Vector3Configuration):
        return self._check_workspace(angles)

    def check_workspace_point(self, point: Vector3Cartesian):
        angles = self.inverse_kinematics3(point)
        return self._check_workspace(angles)

    def inverse_kinematics2(self, x, y, z):
        """
        wg filmiku z yt https://www.youtube.com/watch?v=D93iQVoSScQ
        elbow up ????
        """

        h = self.l1
        L1 = self.l2
        L2 = self.l3

        theta1 = math.atan2(y, x)  # 1
        r2 = z - h  # 4
        r1 = math.sqrt(x ** 2 + y ** 2)  #
        r3 = math.sqrt(r1 ** 2 + r2 ** 2)  #
        fi2 = math.atan2(r2, r1)  # 3
        fi1 = math.acos((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3))  #
        theta2 = fi2 - fi1  # 2
        fi3 = math.acos((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2))  #
        theta3 = math.pi - fi3  #

        angles = Vector3Configuration(theta1, theta2, theta3)
        return angles

    def inverse_kinematics3(self, point: Vector3Cartesian):
        """
        elbow down???
        wg filmiku z yt https://www.youtube.com/watch?v=Jj5pqbQWKuE CORRECT!!!!!
        """
        h = self.l1
        L1 = self.l2
        L2 = self.l3

        theta1 = math.atan2(point.y, point.x)  # 1
        r2 = point.z - h  # 4
        r1 = math.sqrt(point.x ** 2 + point.y ** 2)  #
        r3 = math.sqrt(r1 ** 2 + r2 ** 2)  #
        fi1 = math.atan2(r2, r1)  # 3
        fi2 = math.acos((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3))  #
        theta2 = fi2 + fi1  # 2
        fi3 = math.acos((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2))  #
        theta3 = fi3 - math.pi  #

        angles = Vector3Configuration(theta1, theta2, theta3)
        return angles

    def move3(self, point_from: Vector3Cartesian, point_to: Vector3Cartesian, point_distance=0.01):
        from_angles = self.inverse_kinematics3(point_from)
        to_angles = self.inverse_kinematics3(point_to)
        print(from_angles)
        print(to_angles)


        alfa_values = []
        beta_values = []
        gamma_values = []
        alfa_prime_values = []
        beta_prime_values = []
        gamma_prime_values = []

        max_velocity = 0
        for t in np.linspace(0, 1, 50):
            time = Symbol('time')
            f_alfa = from_angles.theta1 + time * (to_angles.theta1 - from_angles.theta1)
            f_alfa_prime = f_alfa.diff(time)
            f_alfa = lambdify(time, f_alfa)
            f_alfa_prime = lambdify(time, f_alfa_prime)
            f_beta = from_angles.theta2 + time * (to_angles.theta2 - from_angles.theta2)
            f_beta_prime = f_beta.diff(time)
            f_beta = lambdify(time, f_beta)
            f_beta_prime = lambdify(time, f_beta_prime)
            f_gamma = from_angles.theta3 + time * (to_angles.theta3 - from_angles.theta3)
            f_gamma_prime = f_gamma.diff(time)
            f_gamma = lambdify(time, f_gamma)
            f_gamma_prime = lambdify(time, f_gamma_prime)

            alfa = f_alfa(t)
            beta = f_beta(t)
            gamma = f_gamma(t)

            alfa_prime = abs(f_alfa_prime(t))
            beta_prime = abs(f_beta_prime(t))
            gamma_prime = abs(f_gamma_prime(t))

            alfa_values.append(alfa)
            beta_values.append(beta)
            gamma_values.append(gamma)
            alfa_prime_values.append(alfa_prime)
            beta_prime_values.append(beta_prime)
            gamma_prime_values.append(gamma_prime)

            # Update max_velocity if the current velocities are higher
            max_velocity = max(max_velocity, alfa_prime, beta_prime, gamma_prime)

        # Normalize the velocities to be between 0 and 1
        if max_velocity != 0:
            alfa_prime_values = [value / max_velocity for value in alfa_prime_values]
            beta_prime_values = [value / max_velocity for value in beta_prime_values]
            gamma_prime_values = [value / max_velocity for value in gamma_prime_values]

        # Create trajectory lists
        trajectory_configuration_space = []
        trajectory_velocities = []

        # Populate the trajectory lists
        for alfa, beta, gamma, alfa_prime, beta_prime, gamma_prime in zip(
                alfa_values, beta_values, gamma_values,
                alfa_prime_values, beta_prime_values, gamma_prime_values):
            trajectory_configuration_space.append(Vector3Configuration(alfa, beta, gamma))
            trajectory_velocities.append(Vector3Configuration(alfa_prime, beta_prime, gamma_prime))

        # Create a trajectory list for cartesian space
        trajectory_cartesian_space = []

        # For each configuration in the trajectory, calculate the forward kinematics
        for config in trajectory_configuration_space:
            position = self.forward_kinematics(config.theta1, config.theta2, config.theta3)
            trajectory_cartesian_space.append(Vector3Cartesian(position.x, position.y, position.z))

        return trajectory_cartesian_space, trajectory_velocities

    def plot_trajectory(self, trajectory):
        theta1_values = [angles.theta1 for angles in trajectory]
        theta2_values = [angles.theta2 for angles in trajectory]
        theta3_values = [angles.theta3 for angles in trajectory]
        steps = list(range(len(trajectory)))

        plt.figure(figsize=(12, 8))

        plt.subplot(3, 1, 1)
        plt.plot(steps, theta1_values, 'r-')
        plt.title('Theta1 over Time')
        plt.ylabel('Theta1 (rad)')

        plt.subplot(3, 1, 2)
        plt.plot(steps, theta2_values, 'g-')
        plt.title('Theta2 over Time')
        plt.ylabel('Theta2 (rad)')

        plt.subplot(3, 1, 3)
        plt.plot(steps, theta3_values, 'b-')
        plt.title('Theta3 over Time')
        plt.ylabel('Theta3 (rad)')
        plt.xlabel('Step')

        plt.tight_layout()
        plt.show()

    def plot_trajectory_velocities(self, trajectory_velocities):
        # Extracting the velocity values for each joint
        theta1_velocities = [vel.theta1 for vel in trajectory_velocities]
        theta2_velocities = [vel.theta2 for vel in trajectory_velocities]
        theta3_velocities = [vel.theta3 for vel in trajectory_velocities]
        steps = list(range(len(trajectory_velocities)))

        # Setting up the plot
        plt.figure(figsize=(12, 8))

        # Plotting Theta1 velocities
        plt.subplot(3, 1, 1)
        plt.plot(steps, theta1_velocities, 'r-')
        plt.title('Theta1 Velocity over Time')
        plt.ylabel('Theta1 Velocity (rad/s)')

        # Plotting Theta2 velocities
        plt.subplot(3, 1, 2)
        plt.plot(steps, theta2_velocities, 'g-')
        plt.title('Theta2 Velocity over Time')
        plt.ylabel('Theta2 Velocity (rad/s)')

        # Plotting Theta3 velocities
        plt.subplot(3, 1, 3)
        plt.plot(steps, theta3_velocities, 'b-')
        plt.title('Theta3 Velocity over Time')
        plt.ylabel('Theta3 Velocity (rad/s)')
        plt.xlabel('Step')

        # Display the plot
        plt.tight_layout()
        plt.show()
