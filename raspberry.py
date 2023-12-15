import RPi.GPIO as GPIO
import time

ENCA = 17  # GPIO pin 17
ENCB = 27  # GPIO pin 27

posi = 0
rotation_count = 0
steps_per_rotation = 1250


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ENCA, GPIO.IN)
    GPIO.setup(ENCB, GPIO.IN)
    GPIO.add_event_detect(ENCA, GPIO.RISING, callback=readEncoder)


def loop():
    while True:
        global posi, rotation_count
        # Read the position and calculate rotations
        pos = posi
        rotations = pos / steps_per_rotation
        angle = rotations * 360
        angle_to_print = angle

        print(angle_to_print)

        # print(angle)
        time.sleep(0.01)


def readEncoder(channel):
    b = GPIO.input(ENCB)
    global posi
    if b > 0:
        posi += 1
    else:
        posi -= 1


if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        GPIO.cleanup()
