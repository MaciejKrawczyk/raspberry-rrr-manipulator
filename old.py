# def forward_kinematics(self, alfa: float, beta: float, gamma: float):
#     """
#     calculate the position of the end effector
#     :param alfa: angle of the first joint
#     :param beta: angle of the second joint
#     :param gamma: angle of the third joint
#     :return: the position of the end effector
#     """
#
#     a3 = self.l3
#     a2 = self.l2
#     h1 = self.l1
#
#     c23 = math.cos(beta + gamma)
#     s23 = math.sin(beta + gamma)
#     c2 = math.cos(beta)
#     s2 = math.sin(beta)
#     c1 = math.cos(alfa)
#     s1 = math.sin(alfa)
#
#     x = c1 * (a3 * c23 + a2 * c2)
#     y = s1 * (a3 * s1 * c23 + a2 * s1 * c2)
#     z = a3 * s23 + a2 * s2 + h1
#
#     return {"x": x, "y": y, "z": z}
#
#
# def inverse_kinematics(self, x: float, y: float, z: float):
#     # calculations
#     angle1 = math.atan(y03 / x03)
#     r1 = math.sqrt(x03 ** 2 + y03 ** 2)
#     r2 = z03 - a1
#     angle12 = math.atan(r2 / r1)
#     r3 = math.sqrt(r1 ** 2 + r2 ** 2)
#     angle11 = math.acos((a23 ** 2 - a22 ** 2 - r23 ** 2) / (-2 * a2 * r3))
#     angle2 = angle12 - angle11
#     angle13 = math.acos((r23 ** 2 - a22 ** 2 - a23 ** 2) / (-2 * a2 * a3))
#     # angle3 = math.pi - angle13
#     angle3 = 180 - angle13
#
#     return {"angle1": angle1, "angle2": angle2, "angle3": angle3}
#     # pass
