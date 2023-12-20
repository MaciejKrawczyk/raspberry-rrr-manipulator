from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from threading import Thread, Event
import queue
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
cors = CORS(app)  # Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow CORS for SocketIO

# Queues for command and feedback
command_queue = queue.Queue()
feedback_queue = queue.Queue()

# Event to control the worker thread
stop_event = Event()


# Worker Thread Function
def worker():
    while not stop_event.is_set():
        try:
            command = command_queue.get(timeout=1)  # Timeout to check for stop_event
            if command == "STOP":
                feedback_queue.put("Worker is stopped")
                stop_event.set()
                time.sleep(2)  # Wait for 2 seconds
                restart_worker()  # Restart worker
                feedback_queue.put("Worker is restarted")
                break
            # Process command...
            feedback = "Processed: " + command
            feedback_queue.put(feedback)
        except queue.Empty:
            continue


# Function to start or restart worker thread
def restart_worker():
    global worker_thread
    stop_event.clear()
    worker_thread = Thread(target=worker, daemon=True)
    worker_thread.start()


# Start Worker Thread
worker_thread = Thread(target=worker, daemon=True)
worker_thread.start()


# SocketIO Events
@socketio.on('send_command')
def handle_command(command):
    command_queue.put(command)
    feedback = feedback_queue.get()
    socketio.emit('feedback', feedback)


if __name__ == '__main__':
    socketio.run(app, debug=True)
