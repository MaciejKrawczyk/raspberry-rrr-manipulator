# app.py

from flask import Flask
from flask_cors import CORS
from models import db
from models.Command import Command
from models.CommandDetails import CommandDetails
from models.ProgramCommandLink import ProgramCommandLink
from models.Position import Position
from models.Program import Program
from models.Registry import Registry
from controllers import registry  # Import the controller

app = Flask(__name__)
app.config.from_object('config')
CORS(app)

db.init_app(app)

with app.app_context():
    db.create_all()

# Register the controller's routes
app.register_blueprint(registry.bp)

if __name__ == '__main__':
    app.run(debug=True)
