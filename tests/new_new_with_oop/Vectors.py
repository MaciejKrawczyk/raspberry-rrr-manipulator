class Vector3Configuration:
    def __init__(self, alfa=0, beta=0, gamma=0):
        self.alfa = alfa
        self.beta = beta
        self.gamma = gamma

    def __str__(self):
        return f"Vector3({self.alfa}, {self.beta}, {self.gamma})"


class Vector3Cartesian:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
