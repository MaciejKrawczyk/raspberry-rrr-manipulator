from flask import Flask
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import time
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Encoder pins and other initializations
ENCA = 17  # GPIO pin 17
ENCB = 27  # GPIO pin 27
posi = 0
steps_per_rotation = 1250

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENCA, GPIO.IN)
GPIO.setup(ENCB, GPIO.IN)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)

# Function to power pin
def power_pin(pin, state):
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)

@socketio.on('message')
def handle_message(data):
    button_pressed = data.get('pressed', False)
    button_name = data.get('button', '')

    if button_pressed and button_name == 'plus':
        power_pin(24, True)
        emit('response', {'data': 'Plus Button Pressed'})
    elif button_pressed and button_name == 'minus':
        power_pin(23, True)
        emit('response', {'data': 'Minus Button Pressed'})
    elif not button_pressed:
        power_pin(24, False)
        power_pin(23, False)
        emit('response', {'data': 'Button Released'})
    else:
        emit('response', {'data': 'Message received!'})

def readEncoder(channel):
    global posi
    b = GPIO.input(ENCB)
    posi += 1 if b > 0 else -1

def loop():
    global posi
    while True:
        pos = posi
        rotations = pos / steps_per_rotation
        angle = int(rotations * 360)
        # print("Angle:", angle)
        socketio.emit('angle_update', {'angle': angle})
        time.sleep(0.05)

if __name__ == "__main__":
    GPIO.add_event_detect(ENCA, GPIO.RISING, callback=readEncoder)
    loop_thread = threading.Thread(target=loop)
    loop_thread.start()
    try:
        socketio.run(app, host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        GPIO.cleanup()
        loop_thread.join()
    except Exception as e:
        print("An error occurred:", e)
        GPIO.cleanup()
        loop_thread.join()
