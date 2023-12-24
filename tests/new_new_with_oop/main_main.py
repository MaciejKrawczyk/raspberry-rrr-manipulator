# from tests.new_new_with_oop.Motor import MotorEncoderCombo
# from tests.new_new_with_oop.Robot import Robot
# from tests.new_new_with_oop.Vectors import Vector3Cartesian
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

# motor_theta1.run_motor('plus', 100)


try: 
    motor_theta1_controller.move_to(270)
    time.sleep(1)
    motor_theta1_controller.move_to(0)
    # motor_theta1_controller.move_to(90)
    # motor_theta1_controller.move_to(180)
    

except KeyboardInterrupt:
    print("Shutting down gracefully...")
    # PWM_THETA1_PLUS.stop()
    # PWM_THETA1_MINUS.stop()
    # motor_theta1.stop()
    GPIO.cleanup()
    quit()
    
except Exception as e:
    print("An error occurred:", e)
    # PWM_THETA1_PLUS.stop()
    # PWM_THETA1_MINUS.stop()
    GPIO.cleanup()
    quit()

# motor_theta1.stop() 

# while True:
#     try: 
#         # # 20% speed for 3 seconds
#         # PWM_THETA1_PLUS.start(20)
#         motor_theta1.run_motor('plus',100)
#         # print(motor_theta1.get_angle())
#         print(motor_theta1.measure_speed())
#         # time.sleep(3)

#         # # 50% speed for 3 seconds
#         # PWM_THETA1_PLUS.ChangeDutyCycle(50)
#         # motor_theta1.run_motor('minus', 50)
#         # print(motor_theta1.get_angle())
#         # time.sleep(3)

#         # # 75% speed for 3 seconds
#         # PWM_THETA1_PLUS.ChangeDutyCycle(75)
#         # motor_theta1.run_motor('plus', 75)
#         # print(motor_theta1.get_angle())
#         # time.sleep(3)

#         # # 100% (max) speed for 3 seconds
#         # PWM_THETA1_PLUS.ChangeDutyCycle(100)
#         # motor_theta1.run_motor('minus', 100)
#         # print(motor_theta1.get_angle())
#         # time.sleep(3)
        
#         # quit()
        
#         # motor_theta1.run_motor('plus', 75)
#         # print(motor_theta1.get_angle())
        
#     except KeyboardInterrupt:
#         print("Shutting down gracefully...")
#         # PWM_THETA1_PLUS.stop()
#         # PWM_THETA1_MINUS.stop()
#         motor_theta1.stop()
#         GPIO.cleanup()
#         quit()

#     except Exception as e:
#         print("An error occurred:", e)
#         # PWM_THETA1_PLUS.stop()
#         # PWM_THETA1_MINUS.stop()
#         motor_theta1.stop()
#         GPIO.cleanup()
#         quit()

# motor_theta1 = MotorEncoderCombo(MOTOR_THETA1_PLUS_INPUT_PIN, MOTOR_THETA1_MINUS_INPUT_PIN, MOTOR_THETA1_PLUS_OUTPUT_PIN, MOTOR_THETA1_MINUS_OUTPUT_PIN)
# motor_theta2 = MotorEncoderCombo(MOTOR_THETA2_PLUS_INPUT_PIN, MOTOR_THETA2_MINUS_INPUT_PIN, MOTOR_THETA2_PLUS_OUTPUT_PIN, MOTOR_THETA2_MINUS_OUTPUT_PIN)
# motor_theta3 = MotorEncoderCombo(MOTOR_THETA3_PLUS_INPUT_PIN, MOTOR_THETA3_MINUS_INPUT_PIN, MOTOR_THETA3_PLUS_OUTPUT_PIN, MOTOR_THETA3_MINUS_OUTPUT_PIN)

# robot = Robot(motor_theta1, motor_theta2, motor_theta3, 1, 1, 1)

# point_from = Vector3Cartesian(-0.5, 0, 1)
# point_to = Vector3Cartesian(0.5, 0, 0.2)

# path = robot.move3(point_from, point_to)

