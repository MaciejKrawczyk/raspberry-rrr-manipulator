from tests.new_new_with_oop.MotorController import MotorController
from tests.new_new_with_oop.Robot import Robot

STEP = 0.1


class RobotController:
    def __init__(self, robot: Robot):
        self.motor_alfa_controller = MotorController(robot.motor_theta1)
        self.motor_beta_controller = MotorController(robot.motor_theta2)
        self.motor_gamma_controller = MotorController(robot.motor_theta3)

    def move(self, parameter_set_from, parameter_set_to):
        """ | calculated by inverse kinematics """




    # ----------------------------
    # just for changing values
    def set_alfa_to(self, alfa):
        pass

    def increment_alfa_by(self, alfa):
        pass

    # ----------------------------

    def set_beta_to(self, beta):
        pass

    def increment_beta_by(self, beta):
        pass

    # ----------------------------

    def set_gamma_to(self, gamma):
        pass

    def increment_gamma_by(self, gamma):
        pass

    # ----------------------------

    def set_x_to(self, x):
        pass

    def increment_x_by(self, x):
        pass

    # ----------------------------

    def set_y_to(self, y):
        pass

    def increment_y_by(self, y):
        pass

    # ----------------------------

    def set_z_to(self, z):
        pass

    def increment_z_by(self, z):
        pass
