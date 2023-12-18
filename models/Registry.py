from sqlalchemy.orm import relationship

from . import db


class Registry(db.Model):
    __tablename__ = 'registry'

    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))

    # Define the relationship to the Position model
    position = relationship('Position', backref='registries')

    def to_dict(self):
        return {
            'id': self.id,
            'position_id': self.position_id,
            'Position': self.position.to_dict() if self.position else None
        }
