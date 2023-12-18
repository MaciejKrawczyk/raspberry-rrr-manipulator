from flask import Blueprint, request, jsonify
from app import db
from models.Registry import Registry
from models.Position import Position

bp = Blueprint('registry', __name__)  # Define a blueprint


@bp.route('/api/registry', methods=['POST', 'DELETE', 'GET'])
def registry():
    if request.method == 'POST':
        # Extract position data from request
        position_data = request.json
        if not position_data:
            return jsonify({"error": "Position data is required"}), 400

        # Create a new Position object
        new_position = Position(
            x=position_data.get('x'),
            y=position_data.get('y'),
            z=position_data.get('z'),
            alfa=position_data.get('alfa'),
            beta=position_data.get('beta'),
            gamma=position_data.get('gamma')
        )

        # Add the new Position to the database session
        db.session.add(new_position)
        db.session.flush()  # Flush to get the new position's ID before committing

        # Create a new Registry object with the new position's ID
        new_registry = Registry(position_id=new_position.id)

        # Add the new Registry to the database session and commit
        db.session.add(new_registry)
        db.session.commit()

        # Return the data of the newly added objects
        return jsonify({
            "message": "Registry and Position added successfully",
            "registry": new_registry.to_dict(),
            "position": new_position.to_dict()
        }), 201

    elif request.method == 'GET':
        # Query all registry entries
        all_registry_entries = Registry.query.all()

        # Convert the result to a list of dictionaries
        all_registry_entries = [entry.to_dict() for entry in all_registry_entries]

        # Return the result as a JSON response
        return jsonify(all_registry_entries), 200

    elif request.method == 'DELETE':
        # Extract ID from request
        registry_id = request.json.get('id')

        # Find the registry entry and delete it
        registry_entry = Registry.query.get(registry_id)
        if registry_entry:
            deleted_registry = registry_entry.to_dict()
            db.session.delete(registry_entry)
            db.session.commit()
            return jsonify({"message": "Registry deleted successfully", "deleted_registry": deleted_registry}), 200
        else:
            return jsonify({"error": "Registry not found"}), 404

    return jsonify({"error": "Invalid request"}), 400
