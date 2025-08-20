import os
from flask import Blueprint, request, jsonify
from models.candidate_model import CandidateModel
from utils.validators import allowed_file
from config import UPLOAD_FOLDER

candidate_bp = Blueprint("candidate", __name__)

@candidate_bp.route("/register", methods=["POST"])
def register_candidate():
    if request.is_json:  # If request is JSON
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        party = data.get("party")
        region = data.get("region")
        phone = data.get("phone")
        symbol = data.get("symbol")  # Just store filename or URL

        if not all([name, email, party, region, phone, symbol]):
            return jsonify({"error": "Missing required fields"}), 400

        data = {
            "name": name,
            "email": email,
            "party": party,
            "symbol": symbol,
            "region": region,
            "phone": phone,
            "status": "pending"
        }

        CandidateModel.register_candidate(data)
        return jsonify({"message": "Candidate registered successfully"}), 201

    else:  # Handle multipart/form-data with file upload
        name = request.form.get("name")
        email = request.form.get("email")
        party = request.form.get("party")
        region = request.form.get("region")
        phone = request.form.get("phone")
        file = request.files.get("symbol")

        if not all([name, email, party, region, phone, file]):
            return jsonify({"error": "Missing required fields"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file format"}), 400

        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        data = {
            "name": name,
            "email": email,
            "party": party,
            "symbol": filepath,
            "region": region,
            "phone": phone,
            "status": "pending"
        }

        CandidateModel.register_candidate(data)
        return jsonify({"message": "Candidate registered successfully"}), 201

@candidate_bp.route("/list", methods=["GET"])
def list_candidates():
    candidates = CandidateModel.get_all()
    return jsonify({"candidates": candidates}), 200