from . import db


class Registry(db.Model):
    __tablename__ = 'registry'

    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'position_id': self.position_id
        }
