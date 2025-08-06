from flask import Blueprint, jsonify
from app.services.memory_service import get_memory, delete_memory

memory_bp = Blueprint("memory", __name__, url_prefix="/api/memory")

@memory_bp.route("/<user_id>", methods=["GET"])
def get_user_memory(user_id):
    memory = get_memory(user_id)
    if memory is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(memory)

@memory_bp.route("/<user_id>", methods=["DELETE"])
def delete_user_memory(user_id):
    try:
        success = delete_memory(user_id)
        if success:
            return jsonify({"message": "Memory cleared"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
