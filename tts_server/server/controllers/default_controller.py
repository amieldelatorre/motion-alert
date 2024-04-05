from flask import Blueprint, jsonify, request, abort
from server.services import tts_service


default_blueprint = Blueprint("default_bp", __name__)


@default_blueprint.route("/", methods=['GET'])
def home():
    res = {
        "response": "Hello World"
    }
    return jsonify(res)


@default_blueprint.route("/message", methods=['POST'])
def message():
    if not request.is_json:
        abort(400)

    request_data = request.json
    if "message" not in request_data:
        return jsonify({"error": "Missing 'message' from data received"}), 400

    msg = request_data["message"]
    tts_service.play_message(msg)

    return '', 200


