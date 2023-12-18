from flask import Flask
from flask_cors import CORS
from models import db
from models.Command import Command
from models.Position import Position
from models.Program import Program
from models.Registry import Registry


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    CORS(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()

    # Import the controllers here to avoid circular imports
    from controllers import registry, command, program

    # Register the controller's routes
    app.register_blueprint(registry.bp)
    app.register_blueprint(program.bp)
    app.register_blueprint(command.bp)

    app.run(debug=True)
