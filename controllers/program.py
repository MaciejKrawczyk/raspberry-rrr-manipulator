from flask import Blueprint, request, jsonify
from app import db
from models.Program import Program

bp = Blueprint('program', __name__)


@bp.route('/api/program', methods=['POST', 'DELETE', 'GET'])
def program():
    if request.method == 'POST':
        program_data = request.json
        if not program_data:
            return jsonify({"error": "Program data is required"}), 400

        new_program = Program(
            name=program_data.get('name'),
            description=program_data.get('description')
        )

        db.session.add(new_program)
        db.session.commit()

        return jsonify({
            "message": "Program added successfully",
            "program": new_program.to_dict()
        }), 201

    elif request.method == 'GET':
        all_programs = Program.query.all()
        all_programs = [program.to_dict() for program in all_programs]
        return jsonify(all_programs), 200

    elif request.method == 'DELETE':
        program_id = request.json.get('id')
        program = Program.query.get(program_id)
        if program:
            deleted_program = program.to_dict()
            db.session.delete(program)
            db.session.commit()
            return jsonify({"message": "Program deleted successfully", "deleted_program": deleted_program}), 200
        else:
            return jsonify({"error": "Program not found"}), 404

    return jsonify({"error": "Invalid request"}), 400
