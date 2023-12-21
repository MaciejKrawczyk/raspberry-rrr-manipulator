import math

import numpy as np

from tests.new_new_with_oop.Motor import Motor
from tests.new_new_with_oop.Vectors import Vector3Cartesian, Vector3Configuration
from utils import convert_to_degrees

import matplotlib.pyplot as plt

ALFA_LIMITS = (0, 360)
BETA_LIMITS = (-45, 90)
GAMMA_LIMITS = (-110, 0)
# in radians
# ALFA_LIMITS = (0, 2 * math.pi)
# BETA_LIMITS = (-math.pi / 4, math.pi / 2)
# GAMMA_LIMITS = (-math.pi * 110 / 180, 0)


def interpolate(start, end, steps):
    return np.linspace(start, end, steps)


class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0
        self.previous_error = 0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        self.previous_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative


class Robot:
    def __init__(self, motor_alfa: Motor, motor_beta: Motor, motor_gamma: Motor, l1: float, l2: float, l3: float):
        self.motor_alfa = motor_alfa
        self.motor_beta = motor_beta
        self.motor_gamma = motor_gamma
        self._x = 0
        self._y = 0
        self._z = 0
        self.speed = 0
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.pid_alfa = PIDController(Kp=1.0, Ki=0.1, Kd=0.05)
        self.pid_beta = PIDController(Kp=1.0, Ki=0.1, Kd=0.05)
        self.pid_gamma = PIDController(Kp=1.0, Ki=0.1, Kd=0.05)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def get_alfa(self):
        return self.motor_alfa.get_angle()

    def get_beta(self):
        return self.motor_beta.get_angle()

    def get_gamma(self):
        return self.motor_gamma.get_angle()

    def forward_kinematics(self, alfa: float, beta: float, gamma: float):
        """ wg mojej implementacji """
        a3 = self.l3
        a2 = self.l2
        h1 = self.l1
        print(alfa,beta,gamma)

        c23 = math.cos(beta + gamma)
        s23 = math.sin(beta + gamma)
        c2 = math.cos(beta)
        s2 = math.sin(beta)
        c1 = math.cos(alfa)
        s1 = math.sin(alfa)

        x = c1 * (a3 * c23 + a2 * c2)
        y = s1 * (a3 * c23 + a2 * c2)
        z = a3 * s23 + a2 * s2 + h1

        return {"x": x, "y": y, "z": z}

    def _check_workspace(self, alfa, beta, gamma):
        if not (ALFA_LIMITS[0] <= alfa <= ALFA_LIMITS[1]):
            raise ValueError(f"Alfa angle {alfa} is out of range {ALFA_LIMITS}")

        if not (BETA_LIMITS[0] <= beta <= BETA_LIMITS[1]):
            raise ValueError(f"Beta angle {beta} is out of range {BETA_LIMITS}")

        if not (GAMMA_LIMITS[0] <= gamma <= GAMMA_LIMITS[1]):
            raise ValueError(f"Gamma angle {gamma} is out of range {GAMMA_LIMITS}")

        return True

    def check_workspace_angles(self, alfa, beta, gamma):
        return self._check_workspace(alfa, beta, gamma)

    def check_workspace_point(self, x, y, z):
        angles = self.inverse_kinematics3(x, y, z)
        return self._check_workspace(angles['theta1'], angles['theta2'], angles['theta3'])

    def forward_kinematics2(self, alfa: float, beta: float, gamma: float):
        L2 = self.l3
        L1 = self.l2
        h = self.l1

        x = round((L1 * math.cos(beta) + L2 * math.cos(beta + gamma)) * math.cos(alfa), 2)
        y = round((L1 * math.cos(beta) + L2 * math.cos(beta + gamma)) * math.sin(alfa), 2)
        z = round(h + L1 * math.sin(beta) + L2 * math.sin(beta + gamma), 2)

        return {"x": x, "y": y, "z": z}

    def inverse_kinematics2(self, x, y, z, degrees=False):
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

        angles = {"theta1": theta1, "theta2": theta2, "theta3": theta3}
        return convert_to_degrees(angles) if degrees else angles

    def inverse_kinematics3(self, x, y, z, degrees=False):
        """
        elbow down???
        wg filmiku z yt https://www.youtube.com/watch?v=Jj5pqbQWKuE CORRECT!!!!!
        """
        h = self.l1
        L1 = self.l2
        L2 = self.l3

        theta1 = math.atan2(y, x)  # 1
        r2 = z - h  # 4
        r1 = math.sqrt(x ** 2 + y ** 2)  #
        r3 = math.sqrt(r1 ** 2 + r2 ** 2)  #
        fi1 = math.atan2(r2, r1)  # 3
        fi2 = math.acos((L2 ** 2 - L1 ** 2 - r3 ** 2) / (-2 * L1 * r3))  #
        theta2 = fi2 + fi1  # 2
        fi3 = math.acos((r3 ** 2 - L1 ** 2 - L2 ** 2) / (-2 * L1 * L2))  #
        theta3 = fi3 - math.pi  #

        angles = {"theta1": theta1, "theta2": theta2, "theta3": theta3}
        return convert_to_degrees(angles) if degrees else angles

    def calculate_steps(self, parameter_set_from, parameter_set_to, point_distance):
        distance = np.sqrt((parameter_set_to['x'] - parameter_set_from['x']) ** 2 +
                           (parameter_set_to['y'] - parameter_set_from['y']) ** 2 +
                           (parameter_set_to['z'] - parameter_set_from['z']) ** 2)
        return max(int(distance / point_distance), 1)

    def move(self, parameter_set_from, parameter_set_to, point_distance=0.01):
        """ TODO: THIS IS ALSO WRONG!!!!! IMPLEMENT YOURSELF!!!!11 """
        steps = self.calculate_steps(parameter_set_from, parameter_set_to, point_distance)

        xs = interpolate(parameter_set_from['x'], parameter_set_to['x'], steps)
        ys = interpolate(parameter_set_from['y'], parameter_set_to['y'], steps)
        zs = interpolate(parameter_set_from['z'], parameter_set_to['z'], steps)

        trajectory = []

        for i in range(steps):
            x_rounded = round(xs[i], 2)
            y_rounded = round(ys[i], 2)
            z_rounded = round(zs[i], 2)

            joint_angles = self.inverse_kinematics3(x_rounded, y_rounded, z_rounded)
            print(x_rounded, y_rounded, z_rounded)
            print(joint_angles)
            print("-----")
            trajectory.append(joint_angles)

        return trajectory

    def move2(self, parameter_set_from, parameter_set_to, point_distance=0.01):
        """ TODO => IT'S WRONG! IMPLEMENT INVERSE/FORWARD KINEMATICS!!!!1 FIRST CALCULATE THE INVERSE KINEMATICS ANGLES, THAN BASED ON ANGLES CALCULATE NEW POSITIONS"""
        xs, ys, zs = [], [], []
        current_x, current_y, current_z = parameter_set_from['x'], parameter_set_from['y'], parameter_set_from['z']
        target_x, target_y, target_z = parameter_set_to['x'], parameter_set_to['y'], parameter_set_to['z']

        while not (current_x == target_x and current_y == target_y and current_z == target_z):
            if current_x < target_x:
                current_x = min(current_x + point_distance, target_x)
            else:
                current_x = max(current_x - point_distance, target_x)

            if current_y < target_y:
                current_y = min(current_y + point_distance, target_y)
            else:
                current_y = max(current_y - point_distance, target_y)

            if current_z < target_z:
                current_z = min(current_z + point_distance, target_z)
            else:
                current_z = max(current_z - point_distance, target_z)

            xs.append(round(current_x, 2))
            ys.append(round(current_y, 2))
            zs.append(round(current_z, 2))

        trajectory = []
        for i in range(len(xs)):
            joint_angles = self.inverse_kinematics3(xs[i], ys[i], zs[i])
            trajectory.append(joint_angles)

        return trajectory

    def move3(self, parameter_set_from: Vector3Cartesian, parameter_set_to: Vector3Cartesian, point_distance=0.01):

        from_angles = self.inverse_kinematics3(parameter_set_from.x, parameter_set_from.y, parameter_set_from.z)
        to_angles = self.inverse_kinematics3(parameter_set_to.x, parameter_set_to.y, parameter_set_to.z)

        # if self.check_workspace_angles(from_angles['theta1'], from_angles['theta2'], from_angles['theta3']) and \
        #         self.check_workspace_angles(to_angles['theta1'], to_angles['theta2'], to_angles['theta3']):
        #     points are in the workspace, continue...

        # Calculate the number of steps
        num_steps_alfa = int(abs(to_angles['theta1'] - from_angles['theta1']) / point_distance)
        num_steps_beta = int(abs(to_angles['theta2'] - from_angles['theta2']) / point_distance)
        num_steps_gamma = int(abs(to_angles['theta3'] - from_angles['theta3']) / point_distance)

        # Generate a sequence of evenly spaced angles
        alfa_values = np.linspace(from_angles['theta1'], to_angles['theta1'], num_steps_alfa)
        beta_values = np.linspace(from_angles['theta2'], to_angles['theta2'], num_steps_beta)
        gamma_values = np.linspace(from_angles['theta3'], to_angles['theta3'], num_steps_gamma)

        # Create a trajectory list
        trajectory_configuration_space = []

        # For each step, create a Vector3Configuration object and add it to the trajectory list
        for alfa, beta, gamma in zip(alfa_values, beta_values, gamma_values):
            trajectory_configuration_space.append(Vector3Configuration(alfa, beta, gamma))

        # Create a trajectory list for cartesian space
        trajectory_cartesian_space = []

        # For each configuration in the trajectory
        for config in trajectory_configuration_space:
            # Calculate the forward kinematics
            position = self.forward_kinematics(config.alfa, config.beta, config.gamma)

            # Create a Vector3Cartesian object and add it to the trajectory list
            trajectory_cartesian_space.append(Vector3Cartesian(position['x'], position['y'], position['z']))

        return trajectory_cartesian_space

    def plot_trajectory(self, trajectory):
        theta1_values = [angles['theta1'] for angles in trajectory]
        theta2_values = [angles['theta2'] for angles in trajectory]
        theta3_values = [angles['theta3'] for angles in trajectory]
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
