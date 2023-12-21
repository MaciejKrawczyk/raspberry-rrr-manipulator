import math

import numpy as np

from tests.new_new_with_oop.Motor import Motor
from utils import convert_to_degrees

import matplotlib.pyplot as plt


def interpolate(start, end, steps):
    return np.linspace(start, end, steps)


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
        """ wg mojej implementacji, correct """
        a3 = self.l3
        a2 = self.l2
        h1 = self.l1

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

    def inverse_kinematics_final(self, x, y, z, degrees=False):
        """ based on outputs uses the correct inverse kinematics function """

        inv1 = self.inverse_kinematics2(x, y, z)
        if inv1['theta2'] < -math.pi / 2 or inv1['theta2'] > 3 * math.pi / 2:
            result = self.inverse_kinematics2(x, y, z)
        else:
            result = inv1

        return convert_to_degrees(result) if degrees else result

    def inverse_kinematics2(self, x, y, z, degrees=False):
        """
        wg filmiku z yt https://www.youtube.com/watch?v=D93iQVoSScQ
        elbow up
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
        elbow down
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
        steps = self.calculate_steps(parameter_set_from, parameter_set_to, point_distance)

        xs = interpolate(parameter_set_from['x'], parameter_set_to['x'], steps)
        ys = interpolate(parameter_set_from['y'], parameter_set_to['y'], steps)
        zs = interpolate(parameter_set_from['z'], parameter_set_to['z'], steps)

        trajectory = []

        for i in range(steps):
            joint_angles = self.inverse_kinematics3(xs[i], ys[i], zs[i])
            # joint_angles = self.inverse_kinematics2(xs[i], ys[i], zs[i])
            print(xs[i], ys[i], zs[i])
            print(joint_angles)
            print("-----")
            trajectory.append(joint_angles)

        return trajectory

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
