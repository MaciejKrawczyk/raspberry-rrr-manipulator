from tests.new_new_with_oop.Motor import MotorEncoderCombo
from tests.new_new_with_oop.Robot import Robot
from tests.new_new_with_oop.Vectors import Vector3Cartesian

MOTOR_THETA1_PLUS_INPUT_PIN = 17
MOTOR_THETA1_MINUS_INPUT_PIN = 18

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

# encoder_motor_theta1 = Encoder(1)
# encoder_motor_theta2 = Encoder(2)
# encoder_motor_theta3 = Encoder(3)

motor_theta1 = MotorEncoderCombo(MOTOR_THETA1_PLUS_INPUT_PIN, MOTOR_THETA1_MINUS_INPUT_PIN, MOTOR_THETA1_PLUS_OUTPUT_PIN, MOTOR_THETA1_MINUS_OUTPUT_PIN)
motor_theta2 = MotorEncoderCombo(MOTOR_THETA2_PLUS_INPUT_PIN, MOTOR_THETA2_MINUS_INPUT_PIN, MOTOR_THETA2_PLUS_OUTPUT_PIN, MOTOR_THETA2_MINUS_OUTPUT_PIN)
motor_theta3 = MotorEncoderCombo(MOTOR_THETA3_PLUS_INPUT_PIN, MOTOR_THETA3_MINUS_INPUT_PIN, MOTOR_THETA3_PLUS_OUTPUT_PIN, MOTOR_THETA3_MINUS_OUTPUT_PIN)

robot = Robot(motor_theta1, motor_theta2, motor_theta3, 1, 1, 1)

point_from = Vector3Cartesian(-0.5, 0, 1)
point_to = Vector3Cartesian(0.5, 0, 0.2)

path = robot.move3(point_from, point_to)
