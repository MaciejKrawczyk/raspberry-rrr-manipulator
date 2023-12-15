import RPi.GPIO as GPIO
import time
import threading

# Assuming RRRManipulator and setup_pins are modules you have that are relevant to your project
from RRRManipulator import Motor
from setup_pins import PinsController, setup_pins

# Encoder pins
ENCA = 17  # GPIO pin 17
ENCB = 27  # GPIO pin 27

# Global variables
posi = 0
rotation_count = 0
steps_per_rotation = 1250

# Pins controller initialization
pins_controller = PinsController()

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENCA, GPIO.IN)
    GPIO.setup(ENCB, GPIO.IN)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(23, GPIO.OUT)
    GPIO.add_event_detect(ENCA, GPIO.RISING, callback=readEncoder)

def pins():
    pins_controller.pin_LOW(23)
    pins_controller.pin_HIGH(24)
    time.sleep(3)
    pins_controller.pin_LOW(24)
    pins_controller.pin_HIGH(23)
    time.sleep(3)  # Adjust as needed to prevent excessive CPU usage
    pins_controller.pin_LOW(24)
    pins_controller.pin_LOW(23)
    # while True:


def loop():
    global posi
    while True:
        # Read the position and calculate rotations
        pos = posi
        rotations = pos / steps_per_rotation
        angle = rotations * 360
        angle_to_print = angle
        
        print(angle_to_print)
        time.sleep(0.05)

def readEncoder(channel):
    b = GPIO.input(ENCB)
    global posi
    if b > 0:
        posi += 1
    else:
        posi -= 1

if __name__ == "__main__":
    setup()
    pins_thread = threading.Thread(target=pins)
    pins_thread.start()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
        pins_thread.join()  # Ensure the pins thread is properly closed
