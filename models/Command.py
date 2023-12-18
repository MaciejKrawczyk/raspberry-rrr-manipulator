from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Command(db.Model):
    __tablename__ = 'command'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    program_id = db.Column(db.Integer, ForeignKey('program.id'))
    next_command_id = db.Column(db.Integer, ForeignKey('command.id'), nullable=True)

    next_command = relationship("Command", remote_side=[id])

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'program_id': self.program_id,
            'next_command_id': self.next_command_id
        }
