from flask import Blueprint, request, jsonify
from app.services.user_service import create_or_update_user, get_user_by_id

user_bp = Blueprint("user", __name__, url_prefix="/api/users")

@user_bp.route("", methods=["POST"])
def create_user():
    data = request.get_json()
    user = create_or_update_user(data)
    
    if not user:
        return jsonify({"error": "Failed to create or update user."}), 400

    return jsonify({"message": "User created or updated successfully", "user_id": user['user_id']})


@user_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500