import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

pwm = GPIO.PWM(23, 1000)
pwm.start(100)

while True:
     
    try:
        # GPIO.cleanup()
        ...
        
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
        # PWM_THETA1_PLUS.stop()
        # PWM_THETA1_MINUS.stop()
        # motor_theta1.stop()
        GPIO.cleanup()
        quit()
        
    except Exception as e:
        print("An error occurred:", e)
        # PWM_THETA1_PLUS.stop()
        # PWM_THETA1_MINUS.stop()
        GPIO.cleanup()
        quit()
