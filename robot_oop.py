# ---------------------
class Encoder:
    def __init__(self, pin):
        self.pin = pin
        self._pulses: int = 0

    def get_pulses(self):
        return self._pulses


class Motor:
    def __init__(self, in_pin, out_pin, encoder: Encoder):
        self.in_pin = in_pin
        self.out_pin = out_pin
        self.encoder = encoder
        self._angle = 0
        self._speed = 0
        # speed is based on PWM

    def calculate_angle(self):
        # calculate the angle based on encoder pulses
        pass

    def get_angle(self):
        self.calculate_angle()
        return self._angle

    def set_angle(self, angle):
        pass

    def set_speed(self, speed):
        self._speed = speed


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

    def set_speed(self, speed):
        self.speed = speed
        self.motor_alfa.set_speed(self.speed)
        self.motor_beta.set_speed(self.speed)
        self.motor_gamma.set_speed(self.speed)

    def move_to_point(self, x, y, z):
        pass

    def move_to_angle(self, alfa, beta, gamma):
        pass

    def sleep(self, time=1):
        pass

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


class RobotController:
    def __init__(self, robot: Robot):
        self.robot = robot

    def command_move_to_point(self, x: float, y: float, z: float):
        self.robot.move_to_point(x, y, z)

    def command_move_to_angle(self, alfa: float, beta: float, gamma: float):
        self.robot.move_to_angle(alfa, beta, gamma)

    def command_sleep(self):
        self.robot.sleep()

    def set_speed(self, speed: int):
        self.robot.set_speed = speed
