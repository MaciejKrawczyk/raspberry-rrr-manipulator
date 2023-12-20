from flask import Flask
from flask_socketio import SocketIO, emit
import RPi.GPIO as GPIO
import time
import threading
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

# Initialize PWM for pins 23 and 24
pwm_pin_23 = GPIO.PWM(23, 1000)  # 1000 Hz frequency
pwm_pin_24 = GPIO.PWM(24, 1000)  # 1000 Hz frequency

# Function to power pin with PWM duty cycle
def power_pin_pwm(pin, duty_cycle):
    pin.start(duty_cycle)

@socketio.on('message')
def handle_message(data):
    button_pressed = data.get('pressed', False)
    button_name = data.get('button', '')

    if button_pressed and button_name == 'plus':
        power_pin_pwm(pwm_pin_24, 100)  # 100% duty cycle (full power)
        emit('response', {'data': 'Plus Button Pressed'})
    elif button_pressed and button_name == 'minus':
        power_pin_pwm(pwm_pin_23, 100)  # 100% duty cycle (full power)
        emit('response', {'data': 'Minus Button Pressed'})
    elif not button_pressed:
        power_pin_pwm(pwm_pin_24, 0)  # 0% duty cycle (off)
        power_pin_pwm(pwm_pin_23, 0)  # 0% duty cycle (off)
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
        pwm_pin_23.start(0)  # Start PWM with 0% duty cycle (off)
        pwm_pin_24.start(0)  # Start PWM with 0% duty cycle (off)
        socketio.run(app, host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        pwm_pin_23.stop()
        pwm_pin_24.stop()
        GPIO.cleanup()
        loop_thread.join()
    except Exception as e:
        print("An error occurred:", e)
        pwm_pin_23.stop()
        pwm_pin_24.stop()
        GPIO.cleanup()
        loop_thread.join()
