from flask import Blueprint, request, jsonify
from models.vote_model import VoteModel

vote_bp = Blueprint("vote", __name__)

@vote_bp.route("/cast", methods=["POST"])
def cast_vote():
    data = request.get_json(force=True)
    required_fields = ["voter_id", "candidate_id", "blockchain_ref"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    VoteModel.cast_vote(data)
    return jsonify({"message": "Vote cast successfully"}), 201
