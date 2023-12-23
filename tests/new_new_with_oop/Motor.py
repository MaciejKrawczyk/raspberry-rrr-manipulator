import time
import RPi.GPIO as GPIO

# Assuming PULSES_PER_REVOLUTION is defined globally
PULSES_PER_REVOLUTION = 1250  # or set to your specific number of pulses per motor revolution

class MotorEncoderCombo:
    def __init__(self, input_plus_pin, input_minus_pin, output_plus_pin, output_minus_pin,
                 pulses_per_revolution=PULSES_PER_REVOLUTION):
        self.output_plus_pin = output_plus_pin
        self.output_minus_pin = output_minus_pin
        self.input_plus_pin = input_plus_pin
        self.input_minus_pin = input_minus_pin
        self.pulses_per_revolution = pulses_per_revolution
        self._pulses = 0
        
        # GPIO setup for the encoder input pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.input_plus_pin, GPIO.IN)
        GPIO.setup(self.input_minus_pin, GPIO.IN)

        # GPIO setup for the motor output pins
        GPIO.setup(self.output_plus_pin, GPIO.OUT)
        GPIO.setup(self.output_minus_pin, GPIO.OUT)

        # Initialize PWM for output pins
        self.pwm_output_plus = GPIO.PWM(self.output_plus_pin, 100)
        self.pwm_output_minus = GPIO.PWM(self.output_minus_pin, 100)
        
        GPIO.add_event_detect(self.input_plus_pin, GPIO.RISING, callback=self._read_encoder)

    def _read_encoder(self, channel):
        b = GPIO.input(self.input_minus_pin)
        self._pulses += 1 if b > 0 else -1
        
    def get_pulses(self):
        return self._pulses

    def get_angle(self):
        return (self._pulses * 360) / self.pulses_per_revolution

    def set_angle(self, angle):
        # This method can be expanded to include logic for moving the motor to the desired angle
        pass

    def run_motor(self, direction, percent_of_power):
        if direction == "plus":
            self.pwm_output_minus.stop()
            self.pwm_output_plus.start(percent_of_power)
        elif direction == "minus":
            self.pwm_output_plus.stop()
            self.pwm_output_minus.start(percent_of_power)
        else:
            self.stop()
                
    def stop(self):
        """Stop the motor by setting both PWM outputs to 0% duty cycle."""
        self.pwm_output_plus.ChangeDutyCycle(0)
        self.pwm_output_minus.ChangeDutyCycle(0)
        self.pwm_output_plus.stop()
        self.pwm_output_minus.stop()