from flask import Blueprint, request, jsonify
from app.services.chat_service import create_or_respond, get_history
chat_bp = Blueprint("chats", __name__, url_prefix="/api/chats")

@chat_bp.route("", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        print("📥 Received data:", data)
       
        conv_id = data.get("conversation_id")
        user_id = data.get("user_id")
        user_input = data.get("user_input")
        tone_feedback = data.get("tone_feedback")

        print(f"🧾 Inputs → user_id: {user_id}, user_input: {user_input}, tone_feedback: {tone_feedback}")

        # ✅ Fix this line
        response_data = create_or_respond(conv_id, user_id, user_input, tone_feedback)

        print("✅ Response from create_or_respond:", response_data)
        return jsonify(response_data)

    except Exception as e:
        print("❌ Exception in /api/chats:", e)
        return jsonify({"error": str(e)}), 500


@chat_bp.route("/<conv_id>", methods=["GET"])
def history(conv_id):
    hist = get_history(conv_id)
    if hist is None: return jsonify({"error":"Not found"}), 404
    return jsonify({"conversation_id": conv_id, "messages": hist})

from app.services.chat_service import get_all_conversations  # Make sure this exists

@chat_bp.route("", methods=["GET"])
def list_conversations():
    try:
        conversations = get_all_conversations()
        return jsonify({"conversations": conversations})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
