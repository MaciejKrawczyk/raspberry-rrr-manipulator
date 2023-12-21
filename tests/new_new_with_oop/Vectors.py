class Vector3Configuration:
    def __init__(self, theta1: float, theta2: float, theta3: float):
        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

    def __str__(self):
        return f"Vector3({self.theta1}, {self.theta2}, {self.theta3})"


class Vector3Cartesian:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
