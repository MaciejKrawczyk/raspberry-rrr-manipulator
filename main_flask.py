from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import RPi.GPIO as GPIO
import threading
import time

# Assuming RRRManipulator and setup_pins are modules you have that are relevant to your project
from setup_pins import PinsController, setup_pins

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
pins_controller = PinsController()

# Function to power pin
def power_pin(pin, state):
    if state:
        GPIO.output(pin, GPIO.HIGH)
    else:
        GPIO.output(pin, GPIO.LOW)

@socketio.on('message')
def handle_message(data):
    button_pressed = data.get('pressed', False)
    button_name = data.get('button', '')

    if button_pressed and button_name == 'plus':
        print('Plus Button Pressed')
        power_pin(24, True)  # Adjust the pin number as needed for the 'plus' button
        emit('response', {'data': 'Plus Button Pressed'})
    elif button_pressed and button_name == 'minus':
        print('Minus Button Pressed')
        power_pin(23, True)  # Adjust the pin number as needed for the 'minus' button
        emit('response', {'data': 'Minus Button Pressed'})
    elif not button_pressed:
        # Assuming that releasing any button turns off both for simplicity
        print('Button Released')
        power_pin(24, False)
        power_pin(23, False)
        emit('response', {'data': 'Button Released'})
    else:
        print('received message: ' + str(data))
        emit('response', {'data': 'Message received!'})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
