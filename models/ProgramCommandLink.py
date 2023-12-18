from . import db


class ProgramCommandLink(db.Model):
    __tablename__ = 'program_command_link'

    linkId = db.Column(db.Integer, primary_key=True)
    programId = db.Column(db.Integer, db.ForeignKey('program.id'))
    commandId = db.Column(db.Integer, db.ForeignKey('command.id'))
    nextCommandId = db.Column(db.Integer, db.ForeignKey('command.id'))
