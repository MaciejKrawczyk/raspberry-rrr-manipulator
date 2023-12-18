from . import db


class Command(db.Model):
    __tablename__ = 'command'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
