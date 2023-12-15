import RPi.GPIO as GPIO
from enum import Enum

class Pin(Enum):
    ALFA_MOTOR_PLUS = 17
    ALFA_MOTOR_MINUS = 27
    BETA_MOTOR_PLUS = 0
    BETA_MOTOR_MINUS = 0
    GAMMA_MOTOR_PLUS = 0
    GAMMA_MOTOR_MINUS = 0

class PowerPin(Enum):
    ALFA_MOTOR_PLUS_POWER = 23
    ALFA_MOTOR_MINUS_POWER = 24
    BETA_MOTOR_PLUS_POWER = 0
    BETA_MOTOR_MINUS_POWER = 0
    GAMMA_MOTOR_PLUS_POWER = 0
    GAMMA_MOTOR_MINUS_POWER = 0

# Pin = {
#     "ALFA_MOTOR_PLUS": 17,
#     "ALFA_MOTOR_MINUS": 27,
#     "BETA_MOTOR_PLUS": 0,
#     "BETA_MOTOR_MINUS": 0,
#     "GAMMA_MOTOR_PLUS": 0,
#     "GAMMA_MOTOR_MINUS": 0
# }

# PowerPin = {
#     "ALFA_MOTOR_PLUS_POWER": 23,
#     "ALFA_MOTOR_MINUS_POWER": 24,
#     "BETA_MOTOR_PLUS_POWER": 0,
#     "BETA_MOTOR_MINUS_POWER": 0,
#     "GAMMA_MOTOR_PLUS_POWER": 0,
#     "GAMMA_MOTOR_MINUS_POWER": 0
# }


def setup_pins():
    GPIO.setmode(GPIO.BCM)
    
    # Setup for the regular pins
    GPIO.setup(Pin.ALFA_MOTOR_MINUS.value, GPIO.OUT)
    GPIO.setup(Pin.ALFA_MOTOR_PLUS.value, GPIO.OUT)
    
    # Setup for the power pins
    GPIO.setup(PowerPin.ALFA_MOTOR_MINUS_POWER.value, GPIO.OUT)
    GPIO.setup(PowerPin.ALFA_MOTOR_PLUS_POWER.value, GPIO.OUT)

class PinsController:
    def __init__(self):
        setup_pins()
        
    def pin_HIGH_2(self, pin: PowerPin):
        GPIO.output(pin.value, GPIO.HIGH)

    def pin_LOW_2(self, pin: PowerPin):
        GPIO.output(pin.value, GPIO.LOW)
        
    def pin_HIGH(self, pin: int):
        GPIO.output(pin, GPIO.HIGH)

    def pin_LOW(self, pin: int):
        GPIO.output(pin, GPIO.LOW)

# Example of using the PinsController
# pins_controller = PinsController()
# pins_controller.pin_HIGH(PowerPin.ALFA_MOTOR_PLUS_POWER)
