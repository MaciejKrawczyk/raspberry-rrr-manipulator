from tests.new_new_with_oop.Motor import Motor

PULSES_PER_REVOLUTION = 1200


class MotorController:
    def __init__(self, motor: Motor):
        self.motor = motor

    def set_angle_to(self, angle):
        pass

    def increment_angle_by(self, angle):
        pass

    def run(self):
        self.motor.run()
