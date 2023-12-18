# from RRRManipulator import RRRManipulator as RRR
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# def main():
#     rrr = RRR(1, 1, 1)
#     steps = 2  # Define the number of steps for each segment
#
#     # Define start, intermediate, and end points for movement
#     start_point = (x_start, y_start, z_start) = (-0.5, 0, 2.5)
#     mid_point = (x_mid, y_mid, z_mid) = (0.5, 0, 0.2)  # The new third point
#     end_point = (x_end, y_end, z_end) = (1, -1.5, 1.5)
#
#     # Function to calculate movement between two points
#     def calculate_movement(start, end, steps):
#         x_range = np.linspace(start[0], end[0], steps)
#         y_range = np.linspace(start[1], end[1], steps)
#         z_range = np.linspace(start[2], end[2], steps)
#         xs, ys, zs, alphas, betas, gammas = [], [], [], [], [], []
#
#         for x, y, z in zip(x_range, y_range, z_range):
#             angles = rrr.inverse_kinematics3(x, y, z)
#             point = rrr.forward_kinematics(angles['theta1'], angles['theta2'], angles['theta3'])
#
#             # Store the results
#             xs.append(point['x'])
#             ys.append(point['y'])
#             zs.append(point['z'])
#             alphas.append(angles['theta1'])
#             betas.append(angles['theta2'])
#             gammas.append(angles['theta3'])
#
#         return xs, ys, zs, alphas, betas, gammas
#
#     # Calculate movement for each segment
#     xs1, ys1, zs1, alphas1, betas1, gammas1 = calculate_movement(start_point, mid_point, steps)
#     xs2, ys2, zs2, alphas2, betas2, gammas2 = calculate_movement(mid_point, end_point, steps)
#
#     # Combine results for plotting
#     xs = xs1 + xs2
#     ys = ys1 + ys2
#     zs = zs1 + zs2
#     alphas = alphas1 + alphas2
#     betas = betas1 + betas2
#     gammas = gammas1 + gammas2
#
#     # Plotting
#     plt.figure(figsize=(12, 8))
#
#     # Plot x, y, z with colorblind-friendly colors
#     plt.subplot(2, 1, 1)
#     plt.plot(xs, label='x', color='blue')
#     plt.plot(ys, label='y', color='orange')
#     plt.plot(zs, label='z', color='green')
#     plt.title('Position over Steps')
#     plt.xlabel('Step')
#     plt.ylabel('Position')
#     plt.legend()
#
#     # Plot alphas, betas, gammas with colorblind-friendly colors
#     plt.subplot(2, 1, 2)
#     plt.plot(alphas, label='alpha', color='magenta')
#     plt.plot(betas, label='beta', color='green')
#     plt.plot(gammas, label='gamma', color='red')
#     plt.title('Angles over Steps')
#     plt.xlabel('Step')
#     plt.ylabel('Angle (Radians)')
#     plt.legend()
#
#     plt.tight_layout()
#     plt.show()
#
#
import asyncio

from RRRManipulator import Motor, RRRManipulator



async def mainik():
    motor = Motor(range_max=360, range_min=0)
    await motor.rotate(90)


if __name__ == "__main__":
    # main()
    motor_alfa = Motor(range_max=360, range_min=0)
    motor_beta = Motor(range_max=270, range_min=0)
    motor_gamma = Motor(range_max=270, range_min=0)
    rrr = RRRManipulator(l1=1, l2=1, l3=1, motor_alfa=motor_alfa, motor_beta=motor_beta, motor_gamma=motor_gamma)

    asyncio.run(mainik())
