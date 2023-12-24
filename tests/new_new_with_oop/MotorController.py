from Motor import MotorEncoderCombo
import time
import matplotlib.pyplot as plt

PULSES_PER_REVOLUTION = 1200


class MotorController:
    def __init__(self, motor: MotorEncoderCombo):
        self.motor = motor

    def set_angle_to(self, angle):
        pass

    def increment_angle_by(self, angle):
        pass

    def run(self):
        self.motor.run()

    def move_to(self, angle):
        current_angle = self.motor.get_angle()

        # PID constants
        Kp = 0.1
        Ki = 0.1
        Kd = 0.11
        # Kd = 0

        angle_data = []
        time_data = []
        start_time = time.time()
        
        # Soft start parameters
        ramp_duration = 0  # Duration of the ramp-up period in seconds
        initial_power = 20   # Initial power level
        ramp_end_time = time.time() + ramp_duration

        integral = 0.0
        previous_error = 0.0

        while True:
            current_angle = self.motor.get_angle()
            error = angle - current_angle

            # PID calculations
            P = abs(error)
            integral += abs(error * 0.01)
            I = integral
            derivative = abs((error - previous_error) / 0.01)
            D = derivative
            pid_power = Kp * P + Ki * I + Kd * D

            # Soft start logic
            if time.time() < ramp_end_time:
                # Gradually increase power during the ramp-up period
                power_percent = initial_power + (pid_power - initial_power) * ((time.time() - (ramp_end_time - ramp_duration)) / ramp_duration)
            else:
                power_percent = pid_power

            # Clamp the power_percent between 15 and 100
            power_percent = max(20, min(100, power_percent))

            print(f"current_angle={current_angle}, angle={angle}, error={error}, power_percent={power_percent}")

            if error > 0:
                self.motor.run_motor('minus', power_percent)
            elif error < 0:
                self.motor.run_motor('plus', power_percent)

            time.sleep(0.01)

            angle_data.append(current_angle)
            time_data.append(time.time() - start_time)

            if abs(error) < 0.2:
                self.motor.stop()
                break

            previous_error = error
            
        # Plotting the angle data
        plt.plot(time_data, angle_data)
        plt.xlabel('Time (s)')
        plt.ylabel('Angle (degrees)')
        plt.title('Angle Change Over Time')

        plt.grid(True)  

        # Save the plot as an image file
        plt.savefig(f'angle_plot_{time.time()}.png')

        # Close the plot
        plt.close()