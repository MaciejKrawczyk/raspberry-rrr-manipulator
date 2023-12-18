from . import db


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    z = db.Column(db.Float)
    alfa = db.Column(db.Float)
    beta = db.Column(db.Float)
    gamma = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'alfa': self.alfa,
            'beta': self.beta,
            'gamma': self.gamma
        }