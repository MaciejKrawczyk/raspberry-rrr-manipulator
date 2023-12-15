import RPi.GPIO as GPIO
import time

# Set the mode of numbering the pins
GPIO.setmode(GPIO.BCM)

# GPIO 23 and 24 set up as outputs
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

try:
    # Power pin 23 for 5 seconds
    GPIO.output(23, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(23, GPIO.LOW)

    # Then power pin 24 for 5 seconds
    GPIO.output(24, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(24, GPIO.LOW)

finally:
    # Clean up the GPIO to reset the port status
    GPIO.cleanup()
