from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from robot import Worker
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
cors = CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

worker = Worker()
worker.start()


@socketio.on('send_command')
def handle_command(command):
    worker.add_command(command)
    feedback = worker.get_feedback()
    socketio.emit('feedback', feedback)


if __name__ == '__main__':
    socketio.run(app, debug=True)
