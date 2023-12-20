import queue
from threading import Thread, Event


class Encoder:
    def __init__(self, input_pin):
        self.input_pin = input_pin
        self._pulses: int = 0

    def get_pulses(self):
        return self._pulses


class Motor:
    def __init__(self, output_pin, encoder: Encoder):
        self.output_pin = output_pin
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

    # def move_end_effector(self, x, y, z):

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


class Program:
    def __init__(self):
        self.commands = []


class RobotController:
    def __init__(self, robot: Robot):
        self.robot = robot

    def command_move_to_point(self, x: float, y: float, z: float):
        self.robot.move_to_point(x, y, z)

    def command_move_to_angle(self, alfa: float, beta: float, gamma: float):
        self.robot.move_to_angle(alfa, beta, gamma)

    def command_sleep(self):
        self.robot.sleep()

    def run_program(self, program: Program):
        pass

    def set_speed(self, speed: int):
        self.robot.set_speed = speed


# ------------------

def init_robot():
    encoder_alfa = Encoder(1)
    encoder_beta = Encoder(2)
    encoder_gamma = Encoder(3)

    motor_alfa = Motor(1, encoder_alfa)
    motor_beta = Motor(2, encoder_beta)
    motor_gamma = Motor(3, encoder_gamma)

    robot = Robot(motor_alfa, motor_beta, motor_gamma, 1, 1, 1)
    return robot


class Worker:
    def __init__(self):

        self.robot: Robot = init_robot()

        self.command_queue = queue.Queue()
        self.feedback_queue = queue.Queue()
        self.stop_event = Event()
        self.thread = Thread(target=self._run, daemon=True)

    def start(self):
        self.stop_event.clear()
        self.thread.start()

    def _run(self):
        """ robot loop """
        while not self.stop_event.is_set():
            try:
                command = self.command_queue.get(timeout=1)
                feedback = f"Processed: {command}"
                self.feedback_queue.put(feedback)
            except queue.Empty:
                continue

    def add_command(self, command):
        self.command_queue.put(command)

    def get_feedback(self):
        return self.feedback_queue.get()
