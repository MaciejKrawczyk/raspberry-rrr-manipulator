import queue
from threading import Thread, Event

PULSES_PER_REVOLUTION = 1200


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

    def calculate_angle(self):
        # Example calculation, modify as per the actual mechanism
        self._angle = self.encoder.get_pulses() * 360 / PULSES_PER_REVOLUTION

    def get_angle(self):
        self.calculate_angle()
        return self._angle

    def set_angle(self, angle):
        # Assuming angle is directly proportional to pulses
        required_pulses = angle * PULSES_PER_REVOLUTION / 360
        current_pulses = self.get_angle() * PULSES_PER_REVOLUTION / 360
        # Adjusting the pulses based on the desired angle
        self.encoder._pulses = int(current_pulses + (required_pulses - current_pulses))

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

    def run(self, processed_command):
        type = processed_command[0]
        body = processed_command[1]
        if type == 'move_to_point':
            self.move_to_point(body['x'], body['y'], body['z'])
        elif type == 'move_to_angle':
            self.move_to_angle(body['alfa'], body['beta'], body['gamma'])
        elif type == 'sleep':
            self.sleep()
        elif type == 'run_program':
            self.run_program(body)
        elif type == 'set_speed':
            self.set_speed(body['speed'])
            # print(self.speed)
            return self.speed
        elif type == 'move_alfa':
            self.move_alfa(body['alfa'])
            # print(self.motor_alfa.get_angle())
            return self.motor_alfa.get_angle()
        elif type == 'move_beta':
            self.move_beta(body['beta'])
            # print(self.motor_beta.get_angle())
            return self.motor_beta.get_angle()
        elif type == 'move_gamma':
            self.move_gamma(body['gamma'])
            # print(self.motor_gamma.get_angle())
            return self.motor_gamma.get_angle()
        elif type == 'move_x':
            self.move_x(body['x'])
            # print(self.get_x())
            return self.get_x()
        elif type == 'move_y':
            self.move_y(body['y'])
            # print(self.get_y())
            return self.get_y()
        elif type == 'move_z':
            self.move_z(body['z'])
            # print(self.get_z())
            return self.get_z()

    def set_speed(self, speed):
        self.speed += speed
        self.motor_alfa.set_speed(self.speed)
        self.motor_beta.set_speed(self.speed)
        self.motor_gamma.set_speed(self.speed)

    # def move_end_effector(self, x, y, z):

    def move_to_point(self, x, y, z):
        print("moved to point")
        return "ok"

    def move_to_angle(self, alfa, beta, gamma):
        print("moved to angle")
        return "ok"

    def sleep(self, time=1):
        print("sleeping")
        return "sleeping"

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

    def move_alfa(self, value):
        self.motor_alfa.set_angle(self.motor_alfa.get_angle() + value)

    def move_beta(self, value):
        self.motor_beta.set_angle(self.motor_beta.get_angle() + value)

    def move_gamma(self, value):
        self.motor_gamma.set_angle(self.motor_gamma.get_angle() + value)

    def move_y(self, value):
        pass

    def move_x(self, value):
        pass

    def move_z(self, value):
        pass

    def run_program(self, value):
        pass


class RobotCommandProcessor:
    def __init__(self):
        pass

    def get_processed_command(self, command):
        type = command['type']
        body = command['body']
        processed_command = [type, body]
        return processed_command


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


class RobotSystemWorker:
    def __init__(self, robot_command_processor: RobotCommandProcessor):

        self.robot: Robot = init_robot()
        self.robot_command_processor = robot_command_processor

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
                # print(command)

                # ---- processing command

                processed_command = self.robot_command_processor.get_processed_command(command)
                feedback = self.robot.run(processed_command)

                # ----

                self.feedback_queue.put(feedback)
            except queue.Empty:
                continue

    def add_command(self, command):
        self.command_queue.put(command)

    def get_feedback(self):
        return self.feedback_queue.get()
