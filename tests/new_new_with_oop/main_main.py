import RPi.GPIO as GPIO
import time

from Motor import MotorEncoderCombo
from MotorController import MotorController
    
    
GPIO.setmode(GPIO.BCM)

MOTOR_THETA1_PLUS_INPUT_PIN = 17
MOTOR_THETA1_MINUS_INPUT_PIN = 27

MOTOR_THETA1_PLUS_OUTPUT_PIN = 23
MOTOR_THETA1_MINUS_OUTPUT_PIN = 24

MOTOR_THETA2_PLUS_INPUT_PIN = 0
MOTOR_THETA2_MINUS_INPUT_PIN = 0

MOTOR_THETA2_PLUS_OUTPUT_PIN = 0
MOTOR_THETA2_MINUS_OUTPUT_PIN = 0

MOTOR_THETA3_PLUS_INPUT_PIN = 0
MOTOR_THETA3_MINUS_INPUT_PIN = 0

MOTOR_THETA3_PLUS_OUTPUT_PIN = 0
MOTOR_THETA3_MINUS_OUTPUT_PIN = 0

# ------------

motor_theta1 = MotorEncoderCombo(MOTOR_THETA1_PLUS_INPUT_PIN, MOTOR_THETA1_MINUS_INPUT_PIN, MOTOR_THETA1_PLUS_OUTPUT_PIN, MOTOR_THETA1_MINUS_OUTPUT_PIN)
motor_theta1_controller = MotorController(motor_theta1)


try: 
    motor_theta1_controller.move_to(270)
    time.sleep(1)
    motor_theta1_controller.move_to(0)
    # motor_theta1_controller.move_to(90)
    # motor_theta1_controller.move_to(180)
    

except KeyboardInterrupt:
    print("Shutting down gracefully...")
    GPIO.cleanup()
    quit()
    
except Exception as e:
    print("An error occurred:", e)
    GPIO.cleanup()
    quit()
