from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from robot import Worker, Robot, Motor, Encoder, RobotController, Program
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

worker = Worker()
worker.start()

print("Initializing robot...")
print("Robot is successfully initialized")
print("Initializing robot controller...")
print("Robot controller is successfully initialized")


@socketio.on('send_command')
def handle_command(command):
    worker.add_command(command)
    feedback = worker.get_feedback()
    socketio.emit('feedback', feedback)


if __name__ == '__main__':
    socketio.run(app, debug=True)
