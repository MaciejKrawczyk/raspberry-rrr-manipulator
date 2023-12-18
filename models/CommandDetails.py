from . import db


class CommandDetails(db.Model):
    __tablename__ = 'command_details'

    id = db.Column(db.Integer, primary_key=True)
    commandId = db.Column(db.Integer, db.ForeignKey('command.id'))
    time = db.Column(db.Integer)
    positionId = db.Column(db.Integer, db.ForeignKey('position.id'))
    regId = db.Column(db.Integer)
