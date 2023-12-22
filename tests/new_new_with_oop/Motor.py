PULSES_PER_REVOLUTION = 1200


class Encoder:
    def __init__(self, input_pin):
        self.input_pin = input_pin
        self._pulses: int = 0

    def update_pulses(self):
        pass

    def get_pulses(self):
        return self._pulses


class Motor:
    def __init__(self, output_pin, encoder: Encoder):
        self.output_pin = output_pin
        self.encoder = encoder
        self._angle = 0

    def get_angle(self):
        self._angle = self.encoder.get_pulses() * 360 / PULSES_PER_REVOLUTION
        return self._angle

    def set_angle(self, angle):
        self._angle = angle

    def run(self):
        pass


class MotorEncoderCombo:
    def __init__(self, output_plus_pin, output_minus_pin, input_plus_pin, input_minus_pin,
                 pulses_per_revolution=PULSES_PER_REVOLUTION):
        self.output_plus_pin = output_plus_pin
        self.output_minus_pin = output_minus_pin
        self.input_plus_pin = input_plus_pin
        self.input_minus_pin = input_minus_pin
        self._angle = 0
        self._pulses: int = 0

    def update_pulses(self):
        pass

    def get_pulses(self):
        return self._pulses

    def get_angle(self):
        self._angle = self.get_pulses() * 360 / PULSES_PER_REVOLUTION
        return self._angle

    def set_angle(self, angle):
        self._angle = angle

    def run(self):
        pass
