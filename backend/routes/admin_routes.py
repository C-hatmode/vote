from flask import Blueprint, request, jsonify
from models.admin_model import AdminModel

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/register", methods=["POST"])
def register_admin():
    data = request.get_json(force=True)
    required_fields = ["name", "email", "password", "phone", "role"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    AdminModel.create_admin(data)
    return jsonify({"message": "Admin registered successfully"}), 201
