from flask import Blueprint, request, jsonify
from app import db
from models.Command import Command

bp = Blueprint('command', __name__)


def create_command(program_id, command_type):
    new_command = Command(program_id=program_id, type=command_type, next_command_id=None)
    db.session.add(new_command)
    db.session.commit()
    db.session.flush()
    return new_command


def update_last_command(program_id, new_command_id):
    last_command = Command.query.filter_by(program_id=program_id, next_command_id=None).first()
    if last_command:
        last_command.next_command_id = new_command_id
        db.session.commit()
        db.session.flush()


@bp.route('/api/command', methods=['POST', 'DELETE', 'GET'])
def command():
    if request.method == 'POST':
        program_id = request.json.get('program_id')
        command_type = request.json.get('command_type')

        new_command = create_command(program_id, command_type)
        update_last_command(program_id, new_command.id)

        return jsonify({'message': 'Command created successfully', 'command_id': new_command.id}), 201

    elif request.method == 'GET':
        program_id = request.args.get('program_id')
        if program_id is not None:
            commands = Command.query.filter_by(program_id=program_id).all()
            commands_list = [command.to_dict() for command in commands]
            return jsonify(commands_list), 200
        else:
            return jsonify({'message': 'program_id parameter is missing'}), 400

    elif request.method == 'DELETE':
        # Implement your DELETE logic here
        return jsonify({'message': 'DELETE request received'}), 200
