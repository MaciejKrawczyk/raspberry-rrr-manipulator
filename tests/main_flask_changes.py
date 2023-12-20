from flask import Flask
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import time
import threading
from flask_sqlalchemy import SQLAlchemy

# Constants
ENCA = 17  # GPIO pin 17
ENCB = 27  # GPIO pin 27
PIN_PLUS = 24
PIN_MINUS = 23
STEPS_PER_ROTATION = 1250

# Initialize Flask and SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([ENCA, ENCB, PIN_PLUS, PIN_MINUS], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Encoder handler
class EncoderHandler:
    def __init__(self):
        self.position = 0
        GPIO.add_event_detect(ENCA, GPIO.RISING, callback=self.read_encoder)

    def read_encoder(self, channel):
        b = GPIO.input(ENCB)
        self.position += 1 if b > 0 else -1

    def get_angle(self):
        rotations = self.position / STEPS_PER_ROTATION
        return int(rotations * 360)


encoder = EncoderHandler()


# Functions
def power_pin(pin, state):
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)


@socketio.on('message')
def handle_message(data):
    button_pressed = data.get('pressed', False)
    button_name = data.get('button', '')

    if button_pressed:
        if button_name == 'plus':
            power_pin(PIN_PLUS, True)
            emit('response', {'data': 'Plus Button Pressed'})
        elif button_name == 'minus':
            power_pin(PIN_MINUS, True)
            emit('response', {'data': 'Minus Button Pressed'})
    else:
        power_pin(PIN_PLUS, False)
        power_pin(PIN_MINUS, False)
        emit('response', {'data': 'Button Released'})


def loop():
    while True:
        angle = encoder.get_angle()
        socketio.emit('angle_update', {'angle': angle})
        time.sleep(0.05)


if __name__ == "__main__":
    try:
        loop_thread = threading.Thread(target=loop)
        loop_thread.start()
        socketio.run(app, host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        GPIO.cleanup()
        loop_thread.join()
    except Exception as e:
        print("An error occurred:", e)
        GPIO.cleanup()
        loop_thread.join()
