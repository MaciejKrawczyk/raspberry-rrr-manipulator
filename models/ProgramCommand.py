from . import db


class ProgramCommand(db.Model):
    __tablename__ = 'program_command'

    id = db.Column(db.Integer, primary_key=True)
    programId = db.Column(db.Integer, db.ForeignKey('program.id'))
    commandId = db.Column(db.Integer, db.ForeignKey('command.id'))
    nextCommandId = db.Column(db.Integer, db.ForeignKey('command.id'), nullable=True)
