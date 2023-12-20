from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from robot import RobotSystemWorker, Robot, Motor, Encoder, RobotController, Program, RobotCommandProcessor
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

robot_command_processor = RobotCommandProcessor()


worker = RobotSystemWorker(robot_command_processor)
worker.start()

print("Initializing robot...")
print("Robot is successfully initialized")
print("Initializing robot controller...")
print("Robot controller is successfully initialized")


@socketio.on('send_command')
def handle_command(command):
    """
     types of commands:
      - move_to_point x y z(x: x coordinate, y: y coordinate, z: z coordinate)
      - move_to_angle alfa beta gamma(alfa: alfa angle, beta: beta angle, gamma: gamma angle)
      - sleep
      - run_program program_name
      - set_speed speed(increment value)
      - move_alfa angle(increment value)
      - move_beta angle(increment value)
      - move_gamma angle(increment value)
      - move_x x(increment value)
      - move_y y(increment value)
      - move_z z(increment value)
    """
    # command = command.split()
    worker.add_command(command)
    feedback = worker.get_feedback()
    socketio.emit('feedback', feedback)


if __name__ == '__main__':
    socketio.run(app, debug=True)
